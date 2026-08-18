"""HTML rendering adapter for the public GitHub Pages resume."""

from html import escape
from pathlib import Path
from typing import Union

from resume_generator.models import Resume

__all__ = (
    "build_html",
    "render_education",
    "render_experience",
    "render_html",
    "render_open_source",
    "render_skills",
    "render_summary",
    "section",
)


def section(title: str, body: str, left_class: str = "") -> str:
    """Render a legacy two-column resume section."""

    left_classes = "left-margin"
    if left_class:
        left_classes = f"{left_classes} {left_class}"
    return f"""      <div class="section">
        <div class="{left_classes}">
          <h2 class="header-left">{escape(title)}</h2>
        </div>

        <div class="right-margin">
{body}
        </div>

        <div class="after-floats"></div>
      </div>"""


def render_summary(resume: Resume) -> str:
    """Render the summary paragraph and public profile links."""

    return f"""          <p class="intro">
            {escape(resume.variant.summary)}
            <br>
            <br>
            For more information, including my entire work history, please see
            my
            <a
              href="https://www.{escape(resume.contact.linkedin)}"
              class="link"
            >
              LinkedIn
            </a>
            profile, or view my
            <a href="https://www.{escape(resume.contact.github)}" class="link">
              Github
            </a>
            page to see some of my personal projects.
          </p>"""


def render_skills(resume: Resume) -> str:
    """Render the technical skills list."""

    rows = "\n".join(f"            <li>{escape(skill.label)}: {escape(skill.value)}</li>" for skill in resume.skills)
    return f"""          <h3 class="list-header">Technical Skills</h3>

          <ul class="list skills">
{rows}
          </ul>"""


def render_experience(resume: Resume) -> str:
    """Render all companies, roles, and impact bullets."""

    blocks = []
    for company in resume.experience:
        role_blocks = []
        for role in company.roles:
            bullets = "\n\n".join(
                f"""            <li>
              {escape(bullet)}
            </li>"""
                for bullet in role.bullets
            )
            role_blocks.append(
                f"""          <div>
            <h4 class="position-held">{escape(role.title)}</h4>
            <h4 class="date">{escape(role.dates)}</h4>
          </div>

          <div class="after-floats"></div>

          <ul class="list duties">
{bullets}
          </ul>"""
            )
        blocks.append(
            f"""          <h3 class="employer">{escape(company.name)} | {escape(company.location)}</h3>

{chr(10).join(role_blocks)}"""
        )
    return "\n".join(blocks)


def render_open_source(resume: Resume) -> str:
    """Render open-source contribution bullets."""

    rows = "\n\n".join(
        f"""            <li>
              {escape(bullet)}
            </li>"""
        for bullet in resume.open_source
    )
    return f"""          <ul class="list duties">
{rows}
          </ul>"""


def render_education(resume: Resume) -> str:
    """Render the education section."""

    return f"""          <h3 class="employer">{escape(resume.education.school)} | {escape(resume.education.location)}</h3>

          <h4 class="position-held">{escape(resume.education.details)}</h4>

          <div class="after-floats"></div>"""


def render_html(resume: Resume) -> str:
    """Render the complete public resume HTML document."""

    return f"""<!DOCTYPE html>
<!-- If you're interested, you can view this online at
  https://evanthegrayt.github.io/resume_generator/ -->
<html>
  <head>
    <title>Evan Gray's (Responsive!) Resume</title>
    <meta name="viewport" content="width=device-width" />
    <meta charset="UTF-8" />
    <link rel="stylesheet" type="text/css" href="style.css">
    <link
      href="https://fonts.googleapis.com/css?family=Noto+Sans+KR:400,700&amp;display=swap"
      rel="stylesheet"
    >
  </head>

  <body>
    <div class="base-outline">
      <h1 class="main-heading">{escape(resume.contact.name)}</h1>

{section("Summary", render_summary(resume))}

      <div class="after-floats"></div>

{section("Experience", render_experience(resume))}

      <div class="after-floats"></div>

{section("Open Source", render_open_source(resume))}

      <div class="after-floats"></div>

{section("Education", render_education(resume), left_class="education")}

      <div class="after-floats"></div>

{section("Skills", render_skills(resume))}
    </div>
  </body>
</html>
"""


def build_html(resume: Resume, out_path: Union[str, Path]) -> Path:
    """Write the rendered HTML resume to ``out_path`` and return the path."""

    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(render_html(resume), encoding="utf-8")
    return out_path
