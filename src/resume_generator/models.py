from collections.abc import Sequence
from dataclasses import dataclass
from typing import Union


@dataclass(frozen=True)
class Contact:
    name: str
    location: str
    phone: str
    email: str
    linkedin: str
    github: str

    def display_items(self):
        return [item for item in (self.location, self.phone, self.email, self.linkedin, self.github) if item]


@dataclass(frozen=True)
class Variant:
    name: str
    stem: str
    headline: str
    summary: str


@dataclass(frozen=True)
class VariantText:
    general: str
    rails: str

    def resolve(self, variant: str) -> str:
        return self.rails if variant == "rails" else self.general


ResumeText = Union[str, VariantText]


@dataclass(frozen=True)
class SkillRow:
    label: str
    value: str


@dataclass(frozen=True)
class Role:
    title: str
    dates: str
    bullets: Sequence[ResumeText]

    def resolve(self, variant: str) -> "ResolvedRole":
        return ResolvedRole(
            title=self.title,
            dates=self.dates,
            bullets=[resolve_text(bullet, variant) for bullet in self.bullets],
        )


@dataclass(frozen=True)
class Company:
    name: str
    location: str
    roles: Sequence[Role]

    def resolve(self, variant: str) -> "ResolvedCompany":
        return ResolvedCompany(
            name=self.name,
            location=self.location,
            roles=[role.resolve(variant) for role in self.roles],
        )


@dataclass(frozen=True)
class Education:
    school: str
    location: str
    details: str


@dataclass(frozen=True)
class ResolvedRole:
    title: str
    dates: str
    bullets: list[str]


@dataclass(frozen=True)
class ResolvedCompany:
    name: str
    location: str
    roles: list[ResolvedRole]


@dataclass(frozen=True)
class Resume:
    contact: Contact
    variant: Variant
    skills: list[SkillRow]
    experience: list[ResolvedCompany]
    open_source: list[str]
    education: Education


def resolve_text(text: ResumeText, variant: str) -> str:
    if isinstance(text, VariantText):
        return text.resolve(variant)
    return text
