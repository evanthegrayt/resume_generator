from resume_fixtures import write_custom_resume

from resume_generator.content import available_variants, build_resume_data


def test_html_resume_uses_general_variant_content():
    resume = build_resume_data("general")

    assert resume.variant.name == "general"
    assert resume.variant.stem == "evan-gray-resume-general"
    assert resume.contact.email == ""
    assert resume.contact.phone == ""
    assert "Backend Systems" in resume.variant.headline
    assert "Rails APIs, data-heavy workflows" not in resume.variant.summary


def test_contact_display_items_skip_empty_private_fields():
    resume = build_resume_data("general")

    assert resume.contact.display_items() == [
        "Edmond, OK",
        "linkedin.com/in/evanthegrayt",
        "github.com/evanthegrayt",
    ]


def test_variant_specific_role_text_is_resolved():
    general = build_resume_data("general")
    rails = build_resume_data("rails")

    general_public_strategies = general.experience[3].roles[1].bullets
    rails_public_strategies = rails.experience[3].roles[1].bullets

    assert "finished the API/database work" in general_public_strategies[0]
    assert "finished the Rails API/database work" in rails_public_strategies[0]


def test_custom_resume_toml_can_define_its_own_variants(tmp_path):
    resume_path = write_custom_resume(tmp_path)

    default = build_resume_data("default", resume_path)
    research = build_resume_data("research", resume_path)

    assert available_variants(resume_path) == ("default", "research")
    assert default.contact.name == "Ada Example"
    assert default.variant.stem == "ada-example-resume"
    assert [skill.label for skill in default.skills] == ["Languages"]
    assert [skill.label for skill in research.skills] == ["Languages", "Research"]
    assert default.experience[0].roles[0].bullets[1] == "Documented a general algorithm."
    assert research.experience[0].roles[0].bullets[1] == "Documented the first published general algorithm."
