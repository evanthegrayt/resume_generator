from resume_generator.content import build_resume_data
from resume_generator.private_contact import apply_contact_overrides, load_document_contact


def test_private_contact_overrides_local_contact_fields(tmp_path):
    private_contact = tmp_path / "resume.private.toml"
    private_contact.write_text(
        """[contact]
email = "evan@example.test"
phone = "555.123.4567"
""",
        encoding="utf-8",
    )

    overrides = load_document_contact(private_contact)
    resume = apply_contact_overrides(build_resume_data("general"), overrides)

    assert resume.contact.email == "evan@example.test"
    assert resume.contact.phone == "555.123.4567"
    assert resume.contact.display_items() == [
        "Edmond, OK",
        "555.123.4567",
        "evan@example.test",
        "linkedin.com/in/evanthegrayt",
        "github.com/evanthegrayt",
    ]

def test_document_contact_requires_phone_and_email(tmp_path):
    private_contact = tmp_path / "resume.private.toml"
    private_contact.write_text(
        """[contact]
email = "evan@example.test"
""",
        encoding="utf-8",
    )

    try:
        load_document_contact(private_contact)
    except ValueError as error:
        assert "phone" in str(error)
    else:
        raise AssertionError("missing phone should fail document contact loading")
