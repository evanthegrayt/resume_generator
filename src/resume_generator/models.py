"""Typed data objects used by the resume builders.

The project keeps resume content in plain Python data structures, then resolves
that content into a concrete resume variant before handing it to an output
adapter.
"""

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Union

__all__ = (
    "Company",
    "Contact",
    "Education",
    "ResolvedCompany",
    "ResolvedRole",
    "Resume",
    "ResumeText",
    "Role",
    "SkillRow",
    "Variant",
    "VariantText",
    "resolve_text",
)


@dataclass(frozen=True)
class Contact:
    """Public or private contact details shown on resume outputs.

    Attributes:
        name: Person's display name.
        location: Public geographic location.
        phone: Phone number for private document outputs, or an empty string for public HTML.
        email: Email address for private document outputs, or an empty string for public HTML.
        linkedin: LinkedIn profile host/path without a URL scheme.
        github: GitHub profile host/path without a URL scheme.
    """

    name: str
    location: str
    phone: str
    email: str
    linkedin: str
    github: str

    def display_items(self) -> list[str]:
        """Return non-empty contact values in the order they should be rendered."""

        return [item for item in (self.location, self.phone, self.email, self.linkedin, self.github) if item]


@dataclass(frozen=True)
class Variant:
    """Configuration for one resume positioning variant.

    Attributes:
        name: Stable variant key used by the CLI.
        stem: File-name stem for generated document outputs.
        headline: Short headline placed under the candidate name.
        summary: Variant-specific professional summary.
    """

    name: str
    stem: str
    headline: str
    summary: str


@dataclass(frozen=True)
class VariantText:
    """Text that changes between resume variants.

    Attributes:
        default: Copy to use when no variant-specific override exists.
        variants: Copy keyed by variant name.
    """

    default: str
    variants: Mapping[str, str]

    def resolve(self, variant: str) -> str:
        """Return the text for ``variant``, falling back to default copy."""

        return self.variants.get(variant, self.default)


ResumeText = Union[str, VariantText]
"""Resume copy that is either shared text or text requiring variant resolution."""


@dataclass(frozen=True)
class SkillRow:
    """A labeled row in the technical skills section.

    Attributes:
        label: Skill category label.
        value: Comma-separated skills or technologies in that category.
    """

    label: str
    value: str


@dataclass(frozen=True)
class Role:
    """One job title held at a company.

    Attributes:
        title: Role title and work arrangement.
        dates: Human-readable employment date range.
        bullets: Impact bullets, optionally containing variant-specific text.
    """

    title: str
    dates: str
    bullets: Sequence[ResumeText]

    def resolve(self, variant: str) -> "ResolvedRole":
        """Return a role whose bullets are plain strings for ``variant``."""

        return ResolvedRole(
            title=self.title,
            dates=self.dates,
            bullets=[resolve_text(bullet, variant) for bullet in self.bullets],
        )


@dataclass(frozen=True)
class Company:
    """A company entry containing one or more roles.

    Attributes:
        name: Employer name.
        location: Employer location.
        roles: Roles held at the employer, newest first.
    """

    name: str
    location: str
    roles: Sequence[Role]

    def resolve(self, variant: str) -> "ResolvedCompany":
        """Return a company whose roles are resolved for ``variant``."""

        return ResolvedCompany(
            name=self.name,
            location=self.location,
            roles=[role.resolve(variant) for role in self.roles],
        )


@dataclass(frozen=True)
class Education:
    """Education section content.

    Attributes:
        school: Institution name.
        location: Institution location.
        details: Degree, study area, or other short education note.
    """

    school: str
    location: str
    details: str


@dataclass(frozen=True)
class ResolvedRole:
    """A role ready for rendering with variant-specific text already selected.

    Attributes:
        title: Role title and work arrangement.
        dates: Human-readable employment date range.
        bullets: Render-ready impact bullets.
    """

    title: str
    dates: str
    bullets: list[str]


@dataclass(frozen=True)
class ResolvedCompany:
    """A company entry ready for rendering.

    Attributes:
        name: Employer name.
        location: Employer location.
        roles: Render-ready roles held at the employer.
    """

    name: str
    location: str
    roles: list[ResolvedRole]


@dataclass(frozen=True)
class Resume:
    """A complete, render-ready resume.

    Attributes:
        contact: Contact details appropriate to the output being generated.
        variant: Variant configuration used for the output.
        skills: Technical skills rows.
        experience: Render-ready experience entries.
        open_source: Open-source contribution bullets.
        education: Education section content.
    """

    contact: Contact
    variant: Variant
    skills: list[SkillRow]
    experience: list[ResolvedCompany]
    open_source: list[str]
    education: Education


def resolve_text(text: ResumeText, variant: str) -> str:
    """Resolve shared or variant-specific resume copy into a plain string."""

    if isinstance(text, VariantText):
        return text.resolve(variant)
    return text
