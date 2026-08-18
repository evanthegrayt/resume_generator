from dataclasses import replace
from pathlib import Path

from resume_generator.models import Resume

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - exercised on Python < 3.11
    import tomli as tomllib


CONTACT_FIELDS = {"name", "location", "phone", "email", "linkedin", "github"}
REQUIRED_DOCUMENT_FIELDS = {"phone", "email"}


def load_contact_overrides(path):
    path = Path(path)
    data = tomllib.loads(path.read_text(encoding="utf-8"))
    contact = data.get("contact", {})
    if not isinstance(contact, dict):
        raise ValueError("[contact] must be a table")

    unknown_fields = set(contact) - CONTACT_FIELDS
    if unknown_fields:
        unknown = ", ".join(sorted(unknown_fields))
        raise ValueError(f"unknown contact field(s): {unknown}")

    return {key: str(value) for key, value in contact.items() if value is not None}


def load_document_contact(path):
    overrides = load_contact_overrides(path)
    missing_fields = sorted(field for field in REQUIRED_DOCUMENT_FIELDS if not overrides.get(field))
    if missing_fields:
        missing = ", ".join(missing_fields)
        raise ValueError(f"document contact file must define: {missing}")
    return overrides


def apply_contact_overrides(resume: Resume, overrides):
    if not overrides:
        return resume
    return replace(resume, contact=replace(resume.contact, **overrides))
