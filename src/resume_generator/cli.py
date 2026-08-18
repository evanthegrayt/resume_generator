"""Command-line entry point for building resume outputs."""

import argparse
from collections.abc import Iterable
from pathlib import Path

from resume_generator.adapters.html import build_html
from resume_generator.content import VARIANTS, build_resume_data
from resume_generator.private_contact import apply_contact_overrides, load_document_contact

__all__ = (
    "CONTACT_FILE",
    "DOCS_DIR",
    "DOWNLOADS_DIR",
    "HTML_PATH",
    "build_docx_outputs",
    "build_html_output",
    "main",
    "parse_args",
    "selected_variants",
)

# Generated GitHub Pages assets live in this tracked directory.
DOCS_DIR = Path("docs")

# Local document outputs are intentionally ignored because they contain private contact data.
DOWNLOADS_DIR = DOCS_DIR / "downloads"

# Public resume page written by the HTML adapter.
HTML_PATH = DOCS_DIR / "index.html"

# Default gitignored TOML file used for DOCX/PDF contact details.
CONTACT_FILE = Path("resume.private.toml")


def selected_variants(name: str) -> Iterable[str]:
    """Return the concrete variant names requested by the CLI."""

    return VARIANTS.keys() if name == "all" else [name]


def parse_args() -> argparse.Namespace:
    """Parse command-line options for output format, variant, and contact file."""

    parser = argparse.ArgumentParser(description="Build Evan Gray resume outputs.")
    parser.add_argument(
        "--variant",
        choices=["all", *VARIANTS.keys()],
        default="all",
        help="Which DOCX/PDF resume variant to build. Defaults to all.",
    )
    parser.add_argument(
        "--format",
        choices=["all", "docx", "html"],
        default="all",
        help="Which output format to build. Defaults to all.",
    )
    parser.add_argument("--no-pdf", action="store_true", help="Build DOCX files only; skip LibreOffice PDF export.")
    parser.add_argument(
        "--contact-file",
        type=Path,
        default=CONTACT_FILE,
        help="Path to a gitignored TOML file with phone/email for DOCX/PDF builds.",
    )
    return parser.parse_args()


def build_docx_outputs(variant_name: str, no_pdf: bool, contact_overrides: dict[str, str]) -> None:
    """Build DOCX and optionally PDF output for one resume variant."""

    from resume_generator.adapters.docx import build_docx, export_pdf

    resume = apply_contact_overrides(build_resume_data(variant_name), contact_overrides)
    docx_path = build_docx(resume, DOWNLOADS_DIR)
    print(f"wrote {docx_path}")
    if not no_pdf:
        pdf_path = export_pdf(docx_path)
        print(f"wrote {pdf_path}")


def build_html_output() -> None:
    """Build the public GitHub Pages HTML resume."""

    resume = build_resume_data("general")
    html_path = build_html(resume, HTML_PATH)
    print(f"wrote {html_path}")


def main() -> None:
    """Run the resume generator from the command line."""

    args = parse_args()

    if args.format in ("all", "docx"):
        try:
            contact_overrides = load_document_contact(args.contact_file)
        except (OSError, ValueError) as error:
            raise SystemExit(f"error: {error}") from error

        for variant in selected_variants(args.variant):
            build_docx_outputs(variant, args.no_pdf, contact_overrides)

    if args.format in ("all", "html"):
        build_html_output()
