"""Command-line entry point for building resume outputs."""

import argparse
from collections.abc import Iterable
from pathlib import Path
from typing import Optional

from resume_generator.adapters.html import build_html
from resume_generator.content import available_variants, build_resume_data
from resume_generator.private_contact import apply_contact_overrides, load_document_contact

__all__ = (
    "CONTACT_FILE",
    "DOCS_DIR",
    "DOWNLOADS_DIR",
    "HTML_PATH",
    "build_docx_outputs",
    "build_html_output",
    "html_variant",
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


def selected_variants(name: str, variant_names: Iterable[str]) -> Iterable[str]:
    """Return the concrete variant names requested by the CLI."""

    return variant_names if name == "all" else [name]


def html_variant(name: str, variant_names: Iterable[str]) -> str:
    """Return the single variant to use for HTML output."""

    if name != "all":
        return name

    names = tuple(variant_names)
    if "general" in names:
        return "general"
    return names[0]


def parse_args() -> argparse.Namespace:
    """Parse command-line options for output format, variant, and contact file."""

    parser = argparse.ArgumentParser(description="Build resume outputs.")
    parser.add_argument(
        "--variant",
        default="all",
        help="Which resume variant to build. Use 'all' for every DOCX/PDF variant. Defaults to all.",
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
    parser.add_argument(
        "--input",
        type=Path,
        default=None,
        help="Path to a resume TOML file. Defaults to the packaged Evan Gray resume.",
    )
    return parser.parse_args()


def build_docx_outputs(
    variant_name: str,
    no_pdf: bool,
    contact_overrides: dict[str, str],
    input_path: Optional[Path] = None,
) -> None:
    """Build DOCX and optionally PDF output for one resume variant."""

    from resume_generator.adapters.docx import build_docx, export_pdf

    resume = apply_contact_overrides(build_resume_data(variant_name, input_path), contact_overrides)
    docx_path = build_docx(resume, DOWNLOADS_DIR)
    print(f"wrote {docx_path}")
    if not no_pdf:
        pdf_path = export_pdf(docx_path)
        print(f"wrote {pdf_path}")


def build_html_output(input_path: Optional[Path] = None, variant_name: str = "general") -> None:
    """Build the public GitHub Pages HTML resume."""

    resume = build_resume_data(variant_name, input_path)
    html_path = build_html(resume, HTML_PATH)
    print(f"wrote {html_path}")


def main() -> None:
    """Run the resume generator from the command line."""

    args = parse_args()

    try:
        variant_names = available_variants(args.input)
        if args.variant != "all" and args.variant not in variant_names:
            names = ", ".join(variant_names)
            raise ValueError(f"unknown resume variant {args.variant!r}; expected one of: {names}")
    except (OSError, ValueError) as error:
        raise SystemExit(f"error: {error}") from error

    if args.format in ("all", "docx"):
        try:
            contact_overrides = load_document_contact(args.contact_file)
        except (OSError, ValueError) as error:
            raise SystemExit(f"error: {error}") from error

        for variant in selected_variants(args.variant, variant_names):
            build_docx_outputs(variant, args.no_pdf, contact_overrides, args.input)

    if args.format in ("all", "html"):
        build_html_output(args.input, html_variant(args.variant, variant_names))
