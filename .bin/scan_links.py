"""
scan_links.py

Scan markdown files for local links and report broken references.
Optionally apply safe fixes when a unique replacement is found.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional, Tuple

INLINE_LINK_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
REFERENCE_LINK_RE = re.compile(r"^\s*\[[^\]]+\]:\s*(\S+)")

SKIP_SCHEMES = (
    "http://",
    "https://",
    "mailto:",
    "ftp://",
    "tel:",
)

# Default exclusions (used if config file not found)
DEFAULT_EXCLUDED_DIRS = {
    ".git",
    ".tmp",
    ".archive",
    ".reports",
    ".venv",
    "venv",
    "__pycache__",
}


def load_link_scan_config(root: Path) -> set[str]:
    """Load exclusion configuration from .scan_linksrc.json"""
    config_path = root / ".scan_linksrc.json"
    
    if not config_path.exists():
        return DEFAULT_EXCLUDED_DIRS.copy()
    
    try:
        config = json.loads(config_path.read_text(encoding="utf-8"))
        excluded = DEFAULT_EXCLUDED_DIRS.copy()
        
        # Add configured exclusions
        if "exclude_dirs" in config:
            for item in config["exclude_dirs"]:
                # Remove glob patterns and wildcards for simple dir matching
                clean_item = item.replace("**", "").replace("/*", "").strip("/")
                if clean_item:
                    excluded.add(clean_item)
        
        return excluded
    except (json.JSONDecodeError, IOError):
        return DEFAULT_EXCLUDED_DIRS.copy()


@dataclass
class LinkFinding:
    file: Path
    line_number: int
    raw_url: str
    resolved_path: Optional[Path]
    reason: str
    suggestion: Optional[str] = None
    applied_fix: bool = False


def iter_markdown_files(root: Path, excluded_dirs: set[str]) -> Iterable[Path]:
    for path in root.rglob("*.md"):
        if any(part in excluded_dirs for part in path.parts):
            continue
        yield path


def normalize_url(raw_url: str) -> str:
    url = raw_url.strip()
    if url.startswith("<") and url.endswith(">"):
        url = url[1:-1].strip()
    if " " in url:
        url = url.split(" ", 1)[0].strip()
    return url


def split_url(url: str) -> Tuple[str, Optional[str]]:
    if "#" in url:
        path, frag = url.split("#", 1)
        return path, frag
    return url, None


def strip_query(path: str) -> str:
    return path.split("?", 1)[0]


def to_posix(path: Path) -> str:
    return path.as_posix()


def resolve_target(md_file: Path, root: Path, link_path: str) -> Path:
    if link_path.startswith("/"):
        return (root / link_path.lstrip("/")).resolve()
    return (md_file.parent / link_path).resolve()


def build_basename_index(root: Path, excluded_dirs: set[str]) -> dict[str, List[Path]]:
    index: dict[str, List[Path]] = {}
    for path in root.rglob("*"):
        if any(part in excluded_dirs for part in path.parts):
            continue
        if path.is_file():
            index.setdefault(path.name.lower(), []).append(path)
    return index


def relpath_for(md_file: Path, target: Path) -> str:
    rel = target.resolve().relative_to(md_file.parent.resolve())
    return rel.as_posix()


def pick_suggestion(
    md_file: Path,
    root: Path,
    link_path: str,
    basename_index: dict[str, List[Path]],
) -> Optional[str]:
    link_path = link_path.rstrip()

    if link_path.endswith("/"):
        trimmed = link_path.rstrip("/")
        target = resolve_target(md_file, root, trimmed)
        if target.exists():
            return trimmed

    candidate = link_path
    if Path(candidate).suffix == "":
        with_md = f"{candidate}.md"
        target = resolve_target(md_file, root, with_md)
        if target.exists():
            return with_md

    basename = Path(link_path).name.lower()
    matches = basename_index.get(basename, [])
    if len(matches) == 1:
        return relpath_for(md_file, matches[0])

    return None


def extract_urls(line: str) -> List[str]:
    urls = [m.group(1) for m in INLINE_LINK_RE.finditer(line)]
    ref = REFERENCE_LINK_RE.match(line)
    if ref:
        urls.append(ref.group(1))
    return urls


def should_skip(url: str) -> bool:
    if not url:
        return True
    if url.startswith(SKIP_SCHEMES):
        return True
    if url.startswith("#"):
        return True
    if url.startswith("{"):
        return True
    return False


def scan_links(root: Path, fix: bool, excluded_dirs: set[str]) -> Tuple[List[LinkFinding], int, int, int]:
    broken: List[LinkFinding] = []
    total_files = 0
    total_links = 0
    fixes_applied = 0

    basename_index = build_basename_index(root, excluded_dirs)

    for md_file in iter_markdown_files(root, excluded_dirs):
        total_files += 1
        try:
            lines = md_file.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            lines = md_file.read_text(encoding="latin-1").splitlines()

        updated = False

        for i, line in enumerate(lines, start=1):
            urls = extract_urls(line)
            if not urls:
                continue

            for raw_url in urls:
                total_links += 1
                url = normalize_url(raw_url)
                if should_skip(url):
                    continue

                path_part, _frag = split_url(url)
                path_part = strip_query(path_part)
                if not path_part:
                    continue

                target = resolve_target(md_file, root, path_part)
                if target.exists():
                    continue

                suggestion = pick_suggestion(md_file, root, path_part, basename_index)
                applied = False

                if fix and suggestion:
                    line = line.replace(raw_url, suggestion, 1)
                    lines[i - 1] = line
                    updated = True
                    applied = True
                    fixes_applied += 1

                broken.append(
                    LinkFinding(
                        file=md_file,
                        line_number=i,
                        raw_url=raw_url,
                        resolved_path=target,
                        reason="target_not_found",
                        suggestion=suggestion,
                        applied_fix=applied,
                    )
                )

        if fix and updated:
            md_file.write_text("\n".join(lines) + "\n", encoding="utf-8")

    return broken, total_files, total_links, fixes_applied


def write_report(output_path: Path, findings: List[LinkFinding], summary: dict) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    report = {
        "summary": summary,
        "broken_links": [
            {
                "file": str(f.file),
                "line": f.line_number,
                "link": f.raw_url,
                "resolved_path": str(f.resolved_path) if f.resolved_path else None,
                "reason": f.reason,
                "suggestion": f.suggestion,
                "applied_fix": f.applied_fix,
            }
            for f in findings
        ],
    }

    output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan markdown links for broken paths.")
    parser.add_argument(
        "--root",
        default=".",
        help="Repository root to scan (default: current directory).",
    )
    parser.add_argument(
        "--output",
        default=".tmp/scan_links.json",
        help="Output JSON report path (default: .tmp/scan_links.json).",
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Apply safe fixes when a unique replacement is found.",
    )

    args = parser.parse_args()
    root = Path(args.root).resolve()
    output_path = Path(args.output)
    
    # Load exclusion configuration
    excluded_dirs = load_link_scan_config(root)

    findings, total_files, total_links, fixes_applied = scan_links(root, args.fix, excluded_dirs)

    summary = {
        "root": str(root),
        "markdown_files": total_files,
        "links_scanned": total_links,
        "broken_links": len(findings),
        "fixes_applied": fixes_applied,
    }

    write_report(output_path, findings, summary)

    print("Markdown Link Scan")
    print(f"Root: {root}")
    print(f"Files scanned: {total_files}")
    print(f"Links scanned: {total_links}")
    print(f"Broken links: {len(findings)}")
    print(f"Fixes applied: {fixes_applied}")
    print(f"Report: {output_path}")

    if findings:
        print("\nBroken links:")
        for finding in findings:
            suggestion = f" -> {finding.suggestion}" if finding.suggestion else ""
            print(
                f"- {finding.file}:{finding.line_number} :: {finding.raw_url}{suggestion}"
            )

    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
