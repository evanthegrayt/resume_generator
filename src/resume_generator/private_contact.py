"""Local private contact loading for document-only resume outputs."""

from dataclasses import replace
from pathlib import Path
from typing import Union

from resume_generator.models import Resume

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - exercised on Python < 3.11
    import tomli as tomllib


__all__ = (
    "CONTACT_FIELDS",
    "REQUIRED_DOCUMENT_FIELDS",
    "apply_contact_overrides",
    "load_contact_overrides",
    "load_document_contact",
)

# Contact fields that may be overridden by the local TOML file.
CONTACT_FIELDS = {"name", "location", "phone", "email", "linkedin", "github"}

# Private document outputs must include direct contact details.
REQUIRED_DOCUMENT_FIELDS = {"phone", "email"}


def load_contact_overrides(path: Union[str, Path]) -> dict[str, str]:
    """Read and validate contact overrides from a TOML file."""

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


def load_document_contact(path: Union[str, Path]) -> dict[str, str]:
    """Load contact overrides required for private DOCX/PDF outputs."""

    overrides = load_contact_overrides(path)
    missing_fields = sorted(field for field in REQUIRED_DOCUMENT_FIELDS if not overrides.get(field))
    if missing_fields:
        missing = ", ".join(missing_fields)
        raise ValueError(f"document contact file must define: {missing}")
    return overrides


def apply_contact_overrides(resume: Resume, overrides: dict[str, str]) -> Resume:
    """Return ``resume`` with contact values replaced by local overrides."""

    if not overrides:
        return resume
    return replace(resume, contact=replace(resume.contact, **overrides))
