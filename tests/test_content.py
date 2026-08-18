from resume_generator.content import build_resume_data


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
