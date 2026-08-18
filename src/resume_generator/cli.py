import argparse
from pathlib import Path

from resume_generator.adapters.html import build_html
from resume_generator.content import VARIANTS, build_resume_data
from resume_generator.private_contact import apply_contact_overrides, load_document_contact

DOCS_DIR = Path("docs")
DOWNLOADS_DIR = DOCS_DIR / "downloads"
HTML_PATH = DOCS_DIR / "index.html"
CONTACT_FILE = Path("resume.private.toml")


def selected_variants(name):
    return VARIANTS.keys() if name == "all" else [name]


def parse_args():
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


def build_docx_outputs(variant_name, no_pdf, contact_overrides):
    from resume_generator.adapters.docx import build_docx, export_pdf

    resume = apply_contact_overrides(build_resume_data(variant_name), contact_overrides)
    docx_path = build_docx(resume, DOWNLOADS_DIR)
    print(f"wrote {docx_path}")
    if not no_pdf:
        pdf_path = export_pdf(docx_path)
        print(f"wrote {pdf_path}")


def build_html_output():
    resume = build_resume_data("general")
    html_path = build_html(resume, HTML_PATH)
    print(f"wrote {html_path}")


def main():
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
