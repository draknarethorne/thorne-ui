"""
scan_links.py  —  Thorne UI Markdown Link Scanner

Scan markdown files for local links and report broken references.
Supports categorized output, false-positive filtering, and auto-fix.

Usage:
    python .bin/scan_links.py                  # Scan and report
    python .bin/scan_links.py --fix            # Apply safe auto-fixes
    python .bin/scan_links.py --verbose        # Show all categories expanded
    python .bin/scan_links.py --fix --verbose  # Fix + detailed output
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional, Tuple
from urllib.parse import unquote

# ---------------------------------------------------------------------------
# Regex patterns
# ---------------------------------------------------------------------------

# Matches both [text](url) and ![alt](url), capturing the URL portion
INLINE_LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")

# Matches reference-style link definitions: [label]: url
REFERENCE_LINK_RE = re.compile(r"^\s*\[[^\]]+\]:\s*(\S+)")

# Detect non-URL content inside parens (false positives from data tables)
# e.g. [WRIST](40x40, X=280, Y=120, EQType: 10) or [Size](45×45, X=169)
FALSE_POSITIVE_RE = re.compile(
    r"^\d+x\d+|"           # starts with dimensions like 40x40
    r"^\d+×\d+|"           # unicode × variant
    r"^Size\s|"            # starts with "Size "
    r"^X=|^Y=|"            # coordinate data
    r"^EQType|"            # EQ type data
    r",\s*X=|,\s*Y=",     # embedded coordinates
    re.IGNORECASE,
)

# Detect Windows absolute paths in backtick references and inline text
# Matches C:\path, c:\path, C:/path patterns
ABSOLUTE_PATH_RE = re.compile(
    r"`([A-Za-z]:\\[^`]+)`"   # backtick-wrapped: `C:\Thorne-UI\...`
)

# Absolute path prefixes that should be flagged
ABSOLUTE_PATH_PREFIXES = (
    r"C:\Thorne-UI",
    r"c:\Thorne-UI",
    r"c:\thorne-ui",
    r"C:/Thorne-UI",
    r"c:/Thorne-UI",
    r"C:\TAKP",
    r"c:\TAKP",
    r"C:/TAKP",
    r"c:/TAKP",
)

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

# ---------------------------------------------------------------------------
# Categories for broken link classification
# ---------------------------------------------------------------------------

CATEGORY_ORDER = [
    "auto-fixable",
    "absolute-path",
    "real-broken",
    "template-placeholder",
    "false-positive",
]

CATEGORY_LABELS = {
    "auto-fixable": "Auto-Fixable (suggestion found)",
    "absolute-path": "Absolute Paths (should be relative)",
    "real-broken": "Broken Links (no suggestion)",
    "template-placeholder": "Template / Example Placeholders",
    "false-positive": "False Positives (filtered)",
}

# Patterns that indicate a link is a template/example placeholder, not real
TEMPLATE_PLACEHOLDER_PATTERNS = [
    "script_name",
    "EQUI_WindowName",
    "EQUI_Name.xml",
    "./Name.xml",
    "./FileName",
    "./file.xml",
    "WindowName.xml",
]


def load_link_scan_config(root: Path) -> tuple[set[str], list[str]]:
    """Load exclusion configuration from .scan_linksrc.json.
    Returns (excluded_dirs, excluded_paths).
    """
    config_path = root / ".scan_linksrc.json"

    if not config_path.exists():
        return DEFAULT_EXCLUDED_DIRS.copy(), []

    try:
        config = json.loads(config_path.read_text(encoding="utf-8"))
        excluded = DEFAULT_EXCLUDED_DIRS.copy()

        if "exclude_dirs" in config:
            for item in config["exclude_dirs"]:
                clean_item = item.replace("**", "").replace("/*", "").strip("/")
                if clean_item:
                    excluded.add(clean_item)

        # exclude_paths: relative path prefixes (e.g. ".github/agents")
        excluded_paths = []
        if "exclude_paths" in config:
            for p in config["exclude_paths"]:
                excluded_paths.append(p.replace("\\", "/").strip("/"))

        return excluded, excluded_paths
    except (json.JSONDecodeError, IOError):
        return DEFAULT_EXCLUDED_DIRS.copy(), []


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------


@dataclass
class LinkFinding:
    file: Path
    line_number: int
    raw_url: str
    resolved_path: Optional[Path]
    reason: str
    category: str = "real-broken"
    suggestion: Optional[str] = None
    applied_fix: bool = False
    context_line: str = ""


# ---------------------------------------------------------------------------
# Filesystem helpers
# ---------------------------------------------------------------------------


def iter_markdown_files(root: Path, excluded_dirs: set[str],
                       excluded_paths: list[str] | None = None) -> Iterable[Path]:
    for path in root.rglob("*.md"):
        if any(part in excluded_dirs for part in path.parts):
            continue
        # Check path-prefix exclusions (e.g. ".github/agents")
        if excluded_paths:
            rel = path.relative_to(root).as_posix()
            if any(rel.startswith(ep + "/") or rel == ep for ep in excluded_paths):
                continue
        yield path


def normalize_url(raw_url: str) -> str:
    url = raw_url.strip()
    if url.startswith("<") and url.endswith(">"):
        url = url[1:-1].strip()
    # Strip markdown title syntax: (url "title")
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


def resolve_target(md_file: Path, root: Path, link_path: str) -> Path:
    # Decode percent-encoded characters (e.g. %20 -> space)
    decoded = unquote(link_path)
    if decoded.startswith("/"):
        return (root / decoded.lstrip("/")).resolve()
    return (md_file.parent / decoded).resolve()


def build_basename_index(root: Path, excluded_dirs: set[str]) -> dict[str, List[Path]]:
    index: dict[str, List[Path]] = {}
    for path in root.rglob("*"):
        if any(part in excluded_dirs for part in path.parts):
            continue
        if path.is_file():
            index.setdefault(path.name.lower(), []).append(path)
    # Also index directories (for dir-link targets)
    for path in root.rglob("*"):
        if any(part in excluded_dirs for part in path.parts):
            continue
        if path.is_dir():
            index.setdefault(path.name.lower() + "/", []).append(path)
    return index


def relpath_for(md_file: Path, target: Path) -> str:
    """Compute a relative posix path from md_file's directory to target."""
    try:
        rel = os.path.relpath(target.resolve(), md_file.parent.resolve())
        return Path(rel).as_posix()
    except ValueError:
        return str(target)


# ---------------------------------------------------------------------------
# Suggestion engine
# ---------------------------------------------------------------------------


def pick_suggestion(
    md_file: Path,
    root: Path,
    link_path: str,
    basename_index: dict[str, List[Path]],
) -> Optional[str]:
    """Try to find the correct target for a broken link."""
    link_path = link_path.rstrip()
    decoded = unquote(link_path)

    # Strategy 1: Directory link with trailing slash — try without slash
    if decoded.endswith("/"):
        trimmed = decoded.rstrip("/")
        target = resolve_target(md_file, root, trimmed)
        if target.exists():
            return trimmed

    # Strategy 2: Missing extension — try adding .md
    if Path(decoded).suffix == "":
        with_md = f"{decoded}.md"
        target = resolve_target(md_file, root, with_md)
        if target.exists():
            return with_md

    # Strategy 3: Hyphen vs underscore substitution (common rename pattern)
    # e.g. ui-analysis/ -> ui_analysis/, initial-phases/ -> initial_phases/
    underscore_variant = decoded.replace("-", "_")
    if underscore_variant != decoded:
        target = resolve_target(md_file, root, underscore_variant)
        if target.exists():
            return underscore_variant
        # Also try with trailing slash stripped
        target = resolve_target(md_file, root, underscore_variant.rstrip("/"))
        if target.exists():
            return underscore_variant.rstrip("/")

    # Strategy 4: Case-insensitive basename search for unique match
    basename = Path(decoded).name.lower()
    if not basename:
        basename = Path(decoded.rstrip("/")).name.lower()
    matches = basename_index.get(basename, [])
    if len(matches) == 1:
        suggestion = relpath_for(md_file, matches[0])
        # Verify the suggestion actually resolves
        check = resolve_target(md_file, root, suggestion)
        if check.exists():
            return suggestion

    # Strategy 5: Walk ../  depth corrections
    # If the link has ../ segments, try adding/removing one level
    if "../" in decoded:
        parts = decoded.split("/")
        # Try adding one more ../
        deeper = "../" + decoded
        target = resolve_target(md_file, root, deeper)
        if target.exists():
            return deeper
        # Try removing one ../
        if parts[0] == "..":
            shallower = "/".join(parts[1:])
            target = resolve_target(md_file, root, shallower)
            if target.exists():
                return shallower

    # Strategy 6: For paths referencing old directory names, try common renames
    # development/ -> .development/, docs/ -> .docs/
    rename_map = {
        "development/": ".development/",
        "docs/": ".docs/",
    }
    for old, new in rename_map.items():
        if old in decoded:
            renamed = decoded.replace(old, new, 1)
            target = resolve_target(md_file, root, renamed)
            if target.exists():
                return renamed
            # Also try with underscore substitution
            renamed_us = renamed.replace("-", "_")
            target = resolve_target(md_file, root, renamed_us)
            if target.exists():
                return renamed_us

    # Strategy 7: Basename search in directory index
    if decoded.endswith("/"):
        dir_name = Path(decoded.rstrip("/")).name.lower() + "/"
        dir_matches = basename_index.get(dir_name, [])
        if len(dir_matches) == 1:
            suggestion = relpath_for(md_file, dir_matches[0])
            return suggestion + "/"

    return None


# ---------------------------------------------------------------------------
# Link extraction and filtering
# ---------------------------------------------------------------------------


def extract_urls(line: str) -> List[str]:
    """Extract markdown link URLs from a line of text."""
    urls = [m.group(1) for m in INLINE_LINK_RE.finditer(line)]
    ref = REFERENCE_LINK_RE.match(line)
    if ref:
        urls.append(ref.group(1))
    return urls


def is_false_positive(url: str) -> bool:
    """Detect URLs that are actually data in parentheses, not real links."""
    if FALSE_POSITIVE_RE.search(url):
        return True
    # Comma-separated data is not a URL
    if "," in url and not url.startswith("./") and "/" not in url:
        return True
    return False


def is_template_placeholder(url: str, source_file: Path) -> bool:
    """Detect links that are template examples, not intended to resolve."""
    # Check if the source file is a template file
    source_str = str(source_file)
    if "templates" in source_str.lower():
        return True
    # Check URL against known placeholder patterns
    for pattern in TEMPLATE_PLACEHOLDER_PATTERNS:
        if pattern in url:
            return True
    return False


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


# ---------------------------------------------------------------------------
# Main scanner
# ---------------------------------------------------------------------------


def classify_finding(
    finding: LinkFinding,
    source_file: Path,
) -> str:
    """Assign a category to a broken link finding."""
    url = finding.raw_url

    if is_false_positive(url):
        return "false-positive"

    if is_template_placeholder(url, source_file):
        return "template-placeholder"

    if finding.suggestion:
        return "auto-fixable"

    return "real-broken"


# --- Absolute path helpers ---------------------------------------------------

# Map of known absolute prefixes to their repo-relative equivalents.
# This handles paths like C:\Thorne-UI\thorne_drak\foo -> thorne_drak/foo
ABSOLUTE_PREFIX_MAP = {
    r"C:\Thorne-UI\\": "",           # repo root
    r"C:\TAKP\uifiles\\": "",        # maps into the TAKP workspace root
    r"c:\TAKP\uifiles\\": "",
}


def _suggest_relative_for_absolute(
    abs_path: str, source_file: Path, root: Path
) -> str | None:
    """Given an absolute Windows path found in a markdown file, try to
    compute the relative equivalent from the source file's location."""
    # Normalize separators
    normalized = abs_path.replace("\\", "/")

    # Try to strip a known prefix and get a repo-relative path
    repo_rel = None
    for prefix_pattern in ("C:/Thorne-UI/", "c:/Thorne-UI/", "C:/TAKP/uifiles/", "c:/TAKP/uifiles/"):
        low_norm = normalized.lower()
        low_prefix = prefix_pattern.lower()
        if low_norm.startswith(low_prefix):
            repo_rel = normalized[len(prefix_pattern):]
            break

    if repo_rel is None:
        return None

    # Compute relative path from source file to the repo-relative target
    source_dir = source_file.parent.relative_to(root)
    try:
        rel = os.path.relpath(repo_rel.replace("/", os.sep), str(source_dir))
        # Normalize to forward slashes for markdown
        return rel.replace("\\", "/")
    except ValueError:
        return repo_rel


def scan_links(
    root: Path,
    fix: bool,
    excluded_dirs: set[str],
    excluded_paths: list[str] | None = None,
) -> Tuple[List[LinkFinding], int, int, int]:
    broken: List[LinkFinding] = []
    total_files = 0
    total_links = 0
    fixes_applied = 0

    basename_index = build_basename_index(root, excluded_dirs)

    for md_file in sorted(iter_markdown_files(root, excluded_dirs, excluded_paths)):
        total_files += 1
        try:
            lines = md_file.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            lines = md_file.read_text(encoding="latin-1").splitlines()

        updated = False
        in_code_block = False

        for i, line in enumerate(lines, start=1):
            # Track fenced code blocks — skip both passes inside them
            stripped = line.strip()
            if stripped.startswith("```"):
                in_code_block = not in_code_block
                continue
            if in_code_block:
                continue

            # --- Pass 1: Scan markdown links for broken targets ---
            urls = extract_urls(line)
            if urls:
                for raw_url in urls:
                    total_links += 1
                    url = normalize_url(raw_url)
                    if should_skip(url):
                        continue

                    # Skip false positives early
                    if is_false_positive(url):
                        continue

                    path_part, _frag = split_url(url)
                    path_part = strip_query(path_part)
                    if not path_part:
                        continue

                    target = resolve_target(md_file, root, path_part)
                    if target.exists():
                        continue

                    suggestion = pick_suggestion(md_file, root, path_part, basename_index)

                    finding = LinkFinding(
                        file=md_file,
                        line_number=i,
                        raw_url=raw_url,
                        resolved_path=target,
                        reason="target_not_found",
                        suggestion=suggestion,
                        context_line=line.strip()[:120],
                    )
                    finding.category = classify_finding(finding, md_file)

                    if fix and suggestion and finding.category == "auto-fixable":
                        # Replace the raw URL with the suggestion in the line
                        new_url = suggestion
                        # Preserve fragment if present
                        _, frag = split_url(url)
                        if frag:
                            new_url = f"{suggestion}#{frag}"
                        # Target the link target specifically: ](old_url) -> ](new_url)
                        # This avoids replacing a matching substring in the
                        # display text when the filename appears in both.
                        old_target = f"]({raw_url})"
                        new_target = f"]({new_url})"
                        if old_target in line:
                            line = line.replace(old_target, new_target, 1)
                        else:
                            line = line.replace(raw_url, new_url, 1)
                        lines[i - 1] = line
                        updated = True
                        fixes_applied += 1
                        finding.applied_fix = True

                    broken.append(finding)

            # --- Pass 2: Detect absolute paths in backtick references ---
            for m in ABSOLUTE_PATH_RE.finditer(line):
                abs_path = m.group(1)
                # Only flag paths that match our known prefixes
                if not any(abs_path.startswith(p) or abs_path.lower().startswith(p.lower())
                           for p in ABSOLUTE_PATH_PREFIXES):
                    continue

                # Try to compute a relative suggestion
                abs_suggestion = _suggest_relative_for_absolute(
                    abs_path, md_file, root
                )

                finding = LinkFinding(
                    file=md_file,
                    line_number=i,
                    raw_url=abs_path,
                    resolved_path=None,
                    reason="absolute_path",
                    category="absolute-path",
                    suggestion=abs_suggestion,
                    context_line=line.strip()[:120],
                )

                if fix and abs_suggestion:
                    line = line.replace(abs_path, abs_suggestion, 1)
                    lines[i - 1] = line
                    updated = True
                    fixes_applied += 1
                    finding.applied_fix = True

                broken.append(finding)

        if fix and updated:
            md_file.write_text("\n".join(lines) + "\n", encoding="utf-8")

    return broken, total_files, total_links, fixes_applied


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------


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
                "category": f.category,
                "suggestion": f.suggestion,
                "applied_fix": f.applied_fix,
                "context": f.context_line,
            }
            for f in findings
        ],
    }

    output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")


def print_findings(
    findings: List[LinkFinding],
    root: Path,
    verbose: bool = False,
) -> None:
    """Print categorized findings with context."""
    # Group by category
    by_category: dict[str, list[LinkFinding]] = defaultdict(list)
    for f in findings:
        by_category[f.category].append(f)

    for cat in CATEGORY_ORDER:
        items = by_category.get(cat, [])
        if not items:
            continue

        label = CATEGORY_LABELS.get(cat, cat)

        # Skip false positives and templates in non-verbose mode
        if cat in ("false-positive", "template-placeholder") and not verbose:
            print(f"\n  {label}: {len(items)} (use --verbose to show)")
            continue

        print(f"\n  {label} ({len(items)}):")
        print(f"  {'-' * 60}")

        # Group by source file for readability
        by_file: dict[str, list[LinkFinding]] = defaultdict(list)
        for item in items:
            try:
                rel = os.path.relpath(item.file, root)
            except ValueError:
                rel = str(item.file)
            by_file[rel].append(item)

        for src_file, file_items in sorted(by_file.items()):
            print(f"  {src_file}")
            for item in sorted(file_items, key=lambda x: x.line_number):
                fix_marker = " [FIXED]" if item.applied_fix else ""
                if item.suggestion:
                    print(f"    L{item.line_number}: {item.raw_url}")
                    print(f"       -> {item.suggestion}{fix_marker}")
                else:
                    print(f"    L{item.line_number}: {item.raw_url}")
                if verbose and item.context_line:
                    ctx = item.context_line
                    if len(ctx) > 100:
                        ctx = ctx[:100] + "..."
                    print(f"       | {ctx}")


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Thorne UI — Markdown Link Scanner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Examples:\n"
        "  python .bin/scan_links.py              # Scan and report\n"
        "  python .bin/scan_links.py --fix        # Auto-fix safe suggestions\n"
        "  python .bin/scan_links.py --verbose    # Show all categories\n",
    )
    parser.add_argument(
        "--root",
        default=".",
        help="Repository root to scan (default: cwd).",
    )
    parser.add_argument(
        "--output",
        default=".tmp/scan_links.json",
        help="Output JSON report path (default: .tmp/scan_links.json).",
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Apply safe auto-fixes where a unique suggestion is found.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show false positives and template placeholders in output.",
    )

    args = parser.parse_args()
    root = Path(args.root).resolve()
    output_path = Path(args.output)

    # Load exclusion configuration
    excluded_dirs, excluded_paths = load_link_scan_config(root)

    findings, total_files, total_links, fixes_applied = scan_links(
        root, args.fix, excluded_dirs, excluded_paths
    )

    # Count by category (exclude false positives from broken count)
    real_broken = sum(
        1 for f in findings if f.category not in ("false-positive", "template-placeholder")
    )
    fixable = sum(1 for f in findings if f.category == "auto-fixable" and not f.applied_fix)
    fixed = sum(1 for f in findings if f.applied_fix)

    summary = {
        "root": str(root),
        "markdown_files": total_files,
        "links_scanned": total_links,
        "broken_links": real_broken,
        "auto_fixable": fixable,
        "fixes_applied": fixed,
        "false_positives": sum(1 for f in findings if f.category == "false-positive"),
        "template_placeholders": sum(
            1 for f in findings if f.category == "template-placeholder"
        ),
    }

    write_report(output_path, findings, summary)

    # Console output
    print("=" * 50)
    print("  Thorne UI -- Markdown Link Scanner")
    print("=" * 50)
    print(f"  Root:           {root}")
    print(f"  Files scanned:  {total_files}")
    print(f"  Links scanned:  {total_links}")
    print(f"  Broken links:   {real_broken}")
    if fixable > 0:
        print(f"  Auto-fixable:   {fixable}  (run with --fix to apply)")
    if fixed > 0:
        print(f"  Fixes applied:  {fixed}")
    print(f"  Report:         {output_path}")

    if findings:
        print_findings(findings, root, verbose=args.verbose)

    print()
    if real_broken == 0:
        print("  OK - No broken links found.")
    elif args.fix and fixed > 0:
        remaining = real_broken - fixed
        print(f"  Applied {fixed} fixes. {remaining} broken links remain.")
    else:
        fixable_msg = f" ({fixable} auto-fixable with --fix)" if fixable > 0 else ""
        print(f"  Found {real_broken} broken links{fixable_msg}.")

    return 1 if (real_broken - fixed) > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
