"""
validate_xml.py

Validate XML files for well-formedness.
Accepts optional file paths (for pre-commit) or scans a root directory.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List

EXCLUDED_DIRS = {
    ".git",
    ".tmp",
    ".archive",
    ".reports",
    ".venv",
    "venv",
    "__pycache__",
    "duxaUI",
    "Infiniti-Blue",
    "QQ",
    "QQQuarm",
    "vert",
    "vert-blue",
    "zeal",
    "Nillipuss",
    "Nemesis",
    "LunaQuarmified",
}

try:
    from lxml import etree as xml_parser  # type: ignore

    PARSER_NAME = "lxml"

    def parse_xml(path: Path) -> None:
        xml_parser.parse(str(path))


except ImportError:  # pragma: no cover - fallback if lxml unavailable
    import xml.etree.ElementTree as xml_parser

    PARSER_NAME = "xml.etree"

    def parse_xml(path: Path) -> None:
        xml_parser.parse(path)


@dataclass
class XmlFinding:
    file: Path
    error: str


def iter_xml_files(root: Path) -> Iterable[Path]:
    for path in root.rglob("*.xml"):
        if any(part in EXCLUDED_DIRS for part in path.parts):
            continue
        if path.is_file():
            yield path


def normalize_files(files: List[str]) -> List[Path]:
    resolved: List[Path] = []
    for file in files:
        path = Path(file)
        if path.exists() and path.is_file():
            resolved.append(path)
    return resolved


def validate_paths(paths: Iterable[Path]) -> List[XmlFinding]:
    findings: List[XmlFinding] = []
    for path in paths:
        try:
            parse_xml(path)
        except Exception as exc:  # pragma: no cover - runtime parse errors
            findings.append(XmlFinding(file=path, error=str(exc)))
    return findings


def write_report(output_path: Path, findings: List[XmlFinding], summary: dict) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    report = {
        "summary": summary,
        "parser": PARSER_NAME,
        "errors": [
            {
                "file": str(finding.file),
                "error": finding.error,
            }
            for finding in findings
        ],
    }
    output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate XML well-formedness.")
    parser.add_argument(
        "files",
        nargs="*",
        help="Specific XML files to validate (defaults to scanning --root).",
    )
    parser.add_argument(
        "--root",
        default=".",
        help="Root directory to scan when no files are provided.",
    )
    parser.add_argument(
        "--report",
        default=".tmp/xml_wellformed.json",
        help="Output JSON report path (default: .tmp/xml_wellformed.json).",
    )

    args = parser.parse_args()
    output_path = Path(args.report)

    if args.files:
        paths = normalize_files(args.files)
    else:
        root = Path(args.root).resolve()
        paths = list(iter_xml_files(root))

    findings = validate_paths(paths)
    summary = {
        "files_checked": len(paths),
        "errors": len(findings),
    }

    write_report(output_path, findings, summary)

    print("XML Well-Formedness Check")
    print(f"Parser: {PARSER_NAME}")
    print(f"Files checked: {len(paths)}")
    print(f"Errors: {len(findings)}")
    print(f"Report: {output_path}")

    if findings:
        print("\nErrors:")
        for finding in findings:
            print(f"- {finding.file}: {finding.error}")

    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
