"""Resume TOML loading and variant assembly.

The renderers work with dataclasses from :mod:`resume_generator.models`. This
module owns the translation from editable TOML resume data into those internal
objects.
"""

from collections.abc import Mapping
from functools import lru_cache
from importlib.resources import files
from pathlib import Path
from typing import Any, Optional, Union

from resume_generator.models import (
    Company,
    Contact,
    Education,
    Resume,
    Role,
    SkillRow,
    Variant,
    VariantText,
)

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - exercised on Python < 3.11
    import tomli as tomllib

__all__ = (
    "CONTACT",
    "DEFAULT_RESUME_RESOURCE",
    "EDUCATION",
    "EXPERIENCE",
    "OPEN_SOURCE",
    "VARIANTS",
    "available_variants",
    "build_resume_data",
    "load_resume_source",
    "skill_rows",
)

# Packaged TOML resume used when the CLI does not receive ``--input``.
DEFAULT_RESUME_RESOURCE = "default_resume.toml"


def load_resume_source(path: Optional[Union[str, Path]] = None) -> dict[str, Any]:
    """Load resume source data from ``path`` or the packaged default TOML file."""

    if path is None:
        data = files("resume_generator.data").joinpath(DEFAULT_RESUME_RESOURCE).read_text(encoding="utf-8")
    else:
        data = Path(path).read_text(encoding="utf-8")
    return tomllib.loads(data)


@lru_cache(maxsize=1)
def _default_source() -> dict[str, Any]:
    """Return cached source data for the packaged default resume."""

    return load_resume_source()


def required_table(data: Mapping[str, Any], key: str) -> Mapping[str, Any]:
    """Return a required TOML table from ``data``."""

    value = data.get(key)
    if not isinstance(value, Mapping):
        raise ValueError(f"{key} must be a table")
    return value


def optional_table(data: Mapping[str, Any], key: str) -> Mapping[str, Any]:
    """Return an optional TOML table from ``data``."""

    value = data.get(key, {})
    if not isinstance(value, Mapping):
        raise ValueError(f"{key} must be a table")
    return value


def string_field(data: Mapping[str, Any], key: str) -> str:
    """Return a required string value from a TOML table."""

    value = data.get(key)
    if not isinstance(value, str):
        raise ValueError(f"{key} must be a string")
    return value


def optional_string_field(data: Mapping[str, Any], key: str) -> str:
    """Return an optional string value from a TOML table, defaulting to blank."""

    value = data.get(key, "")
    if not isinstance(value, str):
        raise ValueError(f"{key} must be a string")
    return value


def string_list(data: Mapping[str, Any], key: str) -> list[str]:
    """Return a required list of strings from a TOML table."""

    value = data.get(key)
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise ValueError(f"{key} must be a list of strings")
    return value


def parse_open_source(data: Mapping[str, Any]) -> list[str]:
    """Build open-source section bullets from resume source data."""

    return string_list(required_table(data, "open_source"), "bullets")


def parse_contact(data: Mapping[str, Any]) -> Contact:
    """Build contact details from resume source data."""

    contact = required_table(data, "contact")
    return Contact(
        name=string_field(contact, "name"),
        location=string_field(contact, "location"),
        phone=optional_string_field(contact, "phone"),
        email=optional_string_field(contact, "email"),
        linkedin=optional_string_field(contact, "linkedin"),
        github=optional_string_field(contact, "github"),
    )


def parse_variants(data: Mapping[str, Any]) -> dict[str, Variant]:
    """Build available resume variants from resume source data."""

    variants = required_table(data, "variants")
    parsed = {}
    for name, variant_data in variants.items():
        if not isinstance(variant_data, Mapping):
            raise ValueError(f"variants.{name} must be a table")
        parsed[name] = Variant(
            name=name,
            stem=string_field(variant_data, "stem"),
            headline=string_field(variant_data, "headline"),
            summary=string_field(variant_data, "summary"),
        )
    if not parsed:
        raise ValueError("variants must define at least one variant")
    return parsed


def parse_skill_rows(data: Mapping[str, Any], variant: str) -> list[SkillRow]:
    """Build skill rows that apply to ``variant``."""

    rows = data.get("skills", [])
    if not isinstance(rows, list):
        raise ValueError("skills must be a list of tables")

    parsed = []
    for row in rows:
        if not isinstance(row, Mapping):
            raise ValueError("each skill must be a table")
        variant_filter = row.get("variants", [])
        if not isinstance(variant_filter, list) or not all(isinstance(item, str) for item in variant_filter):
            raise ValueError("skills.variants must be a list of strings")
        if variant_filter and variant not in variant_filter:
            continue
        parsed.append(SkillRow(label=string_field(row, "label"), value=string_field(row, "value")))
    return parsed


def parse_bullet(data: Mapping[str, Any]) -> Union[str, VariantText]:
    """Build shared or variant-specific bullet text from a TOML bullet table."""

    if not isinstance(data, Mapping):
        raise ValueError("each bullet must be a table")

    default = string_field(data, "text")
    variants = optional_table(data, "variants")
    if variants:
        if not all(isinstance(name, str) and isinstance(value, str) for name, value in variants.items()):
            raise ValueError("bullet variants must map variant names to strings")
        return VariantText(default=default, variants=dict(variants))
    return default


def parse_experience(data: Mapping[str, Any]) -> list[Company]:
    """Build unresolved company and role entries from resume source data."""

    companies = data.get("experience", [])
    if not isinstance(companies, list):
        raise ValueError("experience must be a list of tables")

    parsed_companies = []
    for company in companies:
        if not isinstance(company, Mapping):
            raise ValueError("each experience entry must be a table")
        roles = company.get("roles", [])
        if not isinstance(roles, list):
            raise ValueError("experience.roles must be a list of tables")

        parsed_roles = []
        for role in roles:
            if not isinstance(role, Mapping):
                raise ValueError("each role must be a table")
            bullets = role.get("bullets", [])
            if not isinstance(bullets, list):
                raise ValueError("experience.roles.bullets must be a list of tables")
            parsed_roles.append(
                Role(
                    title=string_field(role, "title"),
                    dates=string_field(role, "dates"),
                    bullets=[parse_bullet(bullet) for bullet in bullets],
                )
            )

        parsed_companies.append(
            Company(
                name=string_field(company, "name"),
                location=string_field(company, "location"),
                roles=parsed_roles,
            )
        )
    return parsed_companies


def parse_education(data: Mapping[str, Any]) -> Education:
    """Build education section data from resume source data."""

    education = required_table(data, "education")
    return Education(
        school=string_field(education, "school"),
        location=string_field(education, "location"),
        details=string_field(education, "details"),
    )


def available_variants(path: Optional[Union[str, Path]] = None) -> tuple[str, ...]:
    """Return variant names available in a resume TOML source."""

    return tuple(parse_variants(load_resume_source(path)).keys())


def skill_rows(variant: str, path: Optional[Union[str, Path]] = None) -> list[SkillRow]:
    """Return technical skill rows tailored to ``variant``."""

    return parse_skill_rows(load_resume_source(path), variant)


def build_resume_data(variant: str, path: Optional[Union[str, Path]] = None) -> Resume:
    """Build a complete, render-ready resume for ``variant`` from TOML source data."""

    data = load_resume_source(path)
    variants = parse_variants(data)
    if variant not in variants:
        names = ", ".join(variants)
        raise ValueError(f"unknown resume variant {variant!r}; expected one of: {names}")
    return Resume(
        contact=parse_contact(data),
        variant=variants[variant],
        skills=parse_skill_rows(data, variant),
        experience=[company.resolve(variant) for company in parse_experience(data)],
        open_source=parse_open_source(data),
        education=parse_education(data),
    )


# Default resume objects kept for callers that import the content module directly.
CONTACT = parse_contact(_default_source())
VARIANTS = parse_variants(_default_source())
EXPERIENCE = parse_experience(_default_source())
OPEN_SOURCE = parse_open_source(_default_source())
EDUCATION = parse_education(_default_source())
