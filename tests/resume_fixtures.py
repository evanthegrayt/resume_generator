"""Shared test fixtures for resume TOML inputs."""


def write_custom_resume(tmp_path):
    """Write a minimal custom resume TOML file and return its path."""

    resume_path = tmp_path / "resume.toml"
    resume_path.write_text(
        """[contact]
name = "Ada Example"
location = "London, UK"
phone = ""
email = ""
linkedin = "linkedin.com/in/ada-example"
github = "github.com/ada-example"

[variants.default]
stem = "ada-example-resume"
headline = "Principal Analytical Engine Programmer"
summary = "Builds reliable computing notes."

[variants.research]
stem = "ada-example-research"
headline = "Research Programmer"
summary = "Builds research-heavy computing notes."

[[skills]]
label = "Languages"
value = "Python, Ruby"

[[skills]]
label = "Research"
value = "Mathematics, documentation"
variants = ["research"]

[open_source]
bullets = ["Published reusable notes."]

[education]
school = "University of Examples"
location = "London, UK"
details = "Studied computation"

[[experience]]
name = "Analytical Engines"
location = "London, UK"

[[experience.roles]]
title = "Programmer"
dates = "1842 - 1843"

[[experience.roles.bullets]]
text = "Translated technical notes."

[[experience.roles.bullets]]
text = "Documented a general algorithm."

[experience.roles.bullets.variants]
research = "Documented the first published general algorithm."
""",
        encoding="utf-8",
    )
    return resume_path
