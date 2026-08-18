from dataclasses import replace

from resume_generator.adapters.html import render_html
from resume_generator.content import build_resume_data


def test_html_renderer_preserves_legacy_layout_classes():
    html = render_html(build_resume_data("general"))

    assert '<div class="base-outline">' in html
    assert '<h1 class="main-heading">Evan Gray</h1>' in html
    assert '<h2 class="header-left">Experience</h2>' in html
    assert '<ul class="list duties">' in html
    assert 'class="resume-page"' not in html
    assert 'class="resume-section"' not in html


def test_html_renderer_includes_new_sections_and_general_resume():
    html = render_html(build_resume_data("general"))

    assert '<h2 class="header-left">Summary</h2>' in html
    assert '<h2 class="header-left">Open Source Projects</h2>' in html
    assert "For more information, including my entire work history" in html
    assert 'href="https://www.linkedin.com/in/evanthegrayt"' in html
    assert 'href="https://www.github.com/evanthegrayt"' in html
    assert "Senior Software Engineer focused on backend systems" in html
    assert "finished the API/database work" in html
    assert "finished the Rails API/database work" not in html


def test_html_renderer_omits_empty_open_source_section():
    resume = build_resume_data("general")
    html = render_html(replace(resume, open_source=[]))

    assert '<h2 class="header-left">Open Source Projects</h2>' not in html


def test_html_renderer_omits_empty_optional_sections():
    resume = build_resume_data("general")
    html = render_html(replace(resume, skills=[], experience=[], open_source=[], education=None))

    assert '<h2 class="header-left">Experience</h2>' not in html
    assert '<h2 class="header-left">Open Source Projects</h2>' not in html
    assert '<h2 class="header-left">Education</h2>' not in html
    assert '<h2 class="header-left">Skills</h2>' not in html
