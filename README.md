# Resume Generator

An installable Python project that keeps my resume content in one source of
truth and renders it into multiple formats:

- a GitHub Pages HTML resume in `docs/index.html`
- local DOCX/PDF resume variants in `docs/downloads/`
- separate general software engineering and Ruby/Rails-focused document outputs

The project is intentionally small, but it is structured like a normal Python
package: `src/` layout, console script, tests, linting, and generated site
artifacts.

## Why This Exists

I maintain both a hosted resume and application-ready document resumes. This
generator keeps the content model, output adapters, and publishing files in one
place so the HTML and DOCX/PDF versions do not drift apart.

Private contact information is not stored in source control. The public HTML
resume uses public-safe contact details, while local document generation requires
a gitignored `resume.private.toml` file containing phone/email.

## Project Layout

```text
src/resume_generator/
  adapters/
    docx.py          # DOCX/PDF rendering support
    html.py          # GitHub Pages HTML renderer
  cli.py             # console command orchestration
  content.py         # resume content and variants
  models.py          # typed resume data objects
  private_contact.py # local-only contact override loading

docs/
  index.html         # tracked GitHub Pages resume
  style.css          # tracked legacy resume stylesheet
  downloads/         # ignored local DOCX/PDF output

tests/
  test_content.py
  test_html_adapter.py
  test_private_contact.py

Makefile              # one-command local setup, build, test, and lint tasks
```

## Setup

Most day-to-day commands go through `make`, so you do not need to activate the
virtual environment manually:

```sh
make setup
```

This creates `.venv/` and installs the package in editable mode. The
`resume-generator` console command exists inside `.venv/bin/`, and the Makefile
calls it from there.

To see the available commands:

```sh
make help
```

## Build The Public HTML Resume

```sh
make html
```

This writes:

```text
docs/index.html
```

`docs/style.css` is tracked alongside the generated HTML so GitHub Pages can
serve the resume directly from the `docs/` directory.

## Build Local DOCX/PDF Resumes

Document generation requires a local private contact file:

```sh
cp resume.private.example.toml resume.private.toml
```

Edit `resume.private.toml` with real contact details:

```toml
[contact]
email = "you@example.com"
phone = "555.555.5555"
```

Then build both DOCX/PDF variants:

```sh
make docx
```

Build a single variant:

```sh
.venv/bin/resume-generator --format docx --variant general
.venv/bin/resume-generator --format docx --variant rails
```

Skip PDF export:

```sh
make docx-no-pdf
```

Use a different private contact file:

```sh
.venv/bin/resume-generator --format docx --contact-file path/to/contact.toml
```

Document outputs are written to ignored local files:

```text
docs/downloads/evan-gray-resume-general.docx
docs/downloads/evan-gray-resume-general.pdf
docs/downloads/evan-gray-resume-rails.docx
docs/downloads/evan-gray-resume-rails.pdf
```

If the contact file is missing, or if it does not define both `phone` and
`email`, DOCX/PDF generation fails.

## Build Everything

```sh
make build
```

This builds the public HTML resume and the local document resumes. Because it
includes DOCX/PDF generation, it requires `resume.private.toml`.

The underlying Python entry points work too:

```sh
.venv/bin/resume-generator --format html
.venv/bin/python -m resume_generator --format html
```

## Development

Run tests:

```sh
make test
```

Run linting:

```sh
make lint
```

Run both:

```sh
make check
```

Run both before committing generated HTML or source changes.

## Privacy Model

Tracked files are safe to publish publicly. The repository intentionally omits
private phone/email from committed source and generated HTML.

Ignored local files:

- `resume.private.toml`
- `docs/downloads/`
- `.venv/`
- Python cache/build metadata

This keeps the public project useful as a portfolio piece while still supporting
application-ready resumes with private contact details.

## GitHub Pages

Configure GitHub Pages to publish from the `docs/` directory on the default
branch. The hosted resume is `docs/index.html`.
