"""Generate static API documentation with the standard-library pydoc module."""

import os
import pydoc
import sys
import types
from html import escape
from importlib import import_module
from pathlib import Path

# Repository root used to convert generated source links into publishable paths.
ROOT_DIR = Path(__file__).resolve().parents[1]

# Source directory inserted so docs can be generated without installing the package first.
SRC_DIR = ROOT_DIR / "src"

# Destination directory served alongside the GitHub Pages resume.
DOCS_DIR = ROOT_DIR / "docs/api"

# Public package modules that should appear in the generated API docs.
MODULES = [
    "resume_generator",
    "resume_generator.__main__",
    "resume_generator.adapters",
    "resume_generator.adapters.docx",
    "resume_generator.adapters.html",
    "resume_generator.cli",
    "resume_generator.content",
    "resume_generator.models",
    "resume_generator.private_contact",
]


def module_doc_filename(module: str) -> str:
    """Return the file name pydoc writes for ``module``."""

    return f"{module}.html"


def relative_source_path(source_path: Path) -> str:
    """Return a repository-relative source path for generated docs."""

    try:
        return str(source_path.relative_to(ROOT_DIR))
    except ValueError:
        return source_path.name


class PydocStub:
    """Small placeholder for optional runtime dependencies during doc generation."""

    def __init__(self, name: str = "optional dependency"):
        """Store a readable name for generated documentation output."""

        self.name = name

    def __call__(self, *args, **kwargs):
        """Return another placeholder when pydoc imports callable dependency objects."""

        arguments = ", ".join(str(argument) for argument in args)
        return PydocStub(f"{self.name}({arguments})")

    def __getattr__(self, name: str):
        """Return another placeholder for nested dependency attributes."""

        return PydocStub(f"{self.name}.{name}")

    def __repr__(self) -> str:
        """Return a stable representation for generated pydoc HTML."""

        return f"<{self.name}>"


def install_module_stub(name: str, **attributes) -> None:
    """Register a minimal module in ``sys.modules`` when an optional import is missing."""

    module = types.ModuleType(name)
    for attribute, value in attributes.items():
        setattr(module, attribute, value)
    sys.modules[name] = module


def install_optional_dependency_stubs() -> None:
    """Provide import-only stubs for dependencies that pydoc does not execute."""

    try:
        import tomli  # noqa: F401
    except ModuleNotFoundError:
        install_module_stub("tomli", loads=PydocStub("tomli.loads"))

    try:
        import docx  # noqa: F401
    except ModuleNotFoundError:
        install_module_stub("docx", Document=PydocStub("docx.Document"))
        install_module_stub("docx.enum")
        install_module_stub("docx.enum.text", WD_ALIGN_PARAGRAPH=PydocStub("docx.enum.text.WD_ALIGN_PARAGRAPH"))
        install_module_stub("docx.oxml", OxmlElement=PydocStub("docx.oxml.OxmlElement"))
        install_module_stub("docx.oxml.ns", qn=PydocStub("docx.oxml.ns.qn"))
        install_module_stub(
            "docx.shared",
            Inches=PydocStub("docx.shared.Inches"),
            Pt=PydocStub("docx.shared.Pt"),
            RGBColor=PydocStub("docx.shared.RGBColor"),
        )


def main() -> None:
    """Write pydoc HTML files for every configured module."""

    sys.path.insert(0, str(SRC_DIR))
    install_optional_dependency_stubs()
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    os.chdir(DOCS_DIR)
    for module in MODULES:
        documented_module = import_module(module)
        pydoc.writedoc(module)
        sanitize_source_path(documented_module, module_doc_filename(module))
    write_index()


def sanitize_source_path(module, doc_filename: str) -> None:
    """Replace pydoc's absolute local file link with a repository-relative path."""

    source = getattr(module, "__file__", None)
    if source is None:
        return

    source_path = Path(source).resolve()
    local_source = str(source_path)
    public_source = escape(relative_source_path(source_path))
    doc_path = Path(doc_filename)
    html = doc_path.read_text(encoding="utf-8")
    html = html.replace(f'<a href="file:{local_source}">{local_source}</a>', f"<span>{public_source}</span>")
    doc_path.write_text(html, encoding="utf-8")


def write_index() -> None:
    """Write a small landing page that links to the generated pydoc pages."""

    links = "\n".join(
        f'      <li><a href="{escape(module_doc_filename(module))}">{escape(module)}</a></li>' for module in MODULES
    )
    Path("index.html").write_text(
        f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Resume Generator API Documentation</title>
  </head>
  <body>
    <h1>Resume Generator API Documentation</h1>
    <ul>
{links}
    </ul>
  </body>
</html>
""",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
