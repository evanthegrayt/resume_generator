import pytest
from resume_fixtures import write_custom_resume

from resume_generator import cli


def test_docx_build_requires_contact_file(monkeypatch):
    monkeypatch.setattr(
        "sys.argv",
        ["resume-generator", "--format", "docx", "--no-pdf", "--contact-file", "/private/tmp/missing-contact.toml"],
    )

    with pytest.raises(SystemExit) as error:
        cli.main()

    assert "missing-contact.toml" in str(error.value)


def test_custom_input_variant_names_are_validated(monkeypatch, tmp_path):
    resume_path = write_custom_resume(tmp_path)
    monkeypatch.setattr(
        "sys.argv",
        ["resume-generator", "--format", "html", "--input", str(resume_path), "--variant", "missing"],
    )

    with pytest.raises(SystemExit) as error:
        cli.main()

    assert "expected one of: default, research" in str(error.value)
