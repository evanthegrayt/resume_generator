import pytest

from resume_generator import cli


def test_docx_build_requires_contact_file(monkeypatch):
    monkeypatch.setattr(
        "sys.argv",
        ["resume-generator", "--format", "docx", "--no-pdf", "--contact-file", "/private/tmp/missing-contact.toml"],
    )

    with pytest.raises(SystemExit) as error:
        cli.main()

    assert "missing-contact.toml" in str(error.value)
