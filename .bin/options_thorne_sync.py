#!/usr/bin/env python3
"""
Sync Window to Thorne - Backup current working window files to Thorne/ and update metadata.

Copies the main working file from thorne_drak/ to Options/[Window]/Thorne/ and updates
the .sync-status.json metadata with current timestamp and git commit information.

Usage:
    python options_thorne_sync.py --window TARGET
    python options_thorne_sync.py --window Player --verbose
    python options_thorne_sync.py --all              # Sync all 16 windows
    python options_thorne_sync.py --all --force      # Force copy all windows
    python options_thorne_sync.py --all --dry-run    # Preview changes
    
Options:
    --window NAME       Sync specific window (e.g., Target, Player, Group, Spellbook)
    --all              Sync all 16 configured windows
    --force            Force copy even if destination file is identical
    --dry-run          Show what would be synced without making changes
    --verbose          Show detailed file operations
"""

import sys
import json
import shutil
import subprocess
from pathlib import Path
from datetime import datetime

# Window configuration - maps window name to one or more EQUI_*.xml files
WINDOW_MAPPING = {
    "Actions": "EQUI_ActionsWindow.xml",
    "AltAdvance": "EQUI_AAWindow.xml",
    "Animations": "EQUI_Animations.xml",
    "Bank": "EQUI_BankWnd.xml",
    "Bazaar": ["EQUI_BazaarWnd.xml", "EQUI_BazaarSearchWnd.xml"],
    "Breath": "EQUI_BreathWindow.xml",
    "Buff": "EQUI_BuffWindow.xml",
    "Cast": "EQUI_CastSpellWnd.xml",
    "Container": "EQUI_Container.xml",
    "Group": "EQUI_GroupWindow.xml",
    "Hotbutton": "EQUI_HotbuttonWnd.xml",
    "Inspect": "EQUI_InspectWnd.xml",
    "Inventory": "EQUI_Inventory.xml",
    "Loot": "EQUI_LootWnd.xml",
    "Merchant": "EQUI_MerchantWnd.xml",
    "Pet": "EQUI_PetInfoWindow.xml",
    "Player": "EQUI_PlayerWindow.xml",
    "Selector": "EQUI_SelectorWnd.xml",
    "ShortBuffs": "EQUI_ShortDurationBuffWindow.xml",
    "Skin": "EQUI_LoadskinWnd.xml",
    "Spellbook": "EQUI_SpellBookWnd.xml",
    "Stats": "EQUI_MusicPlayerWnd.xml",
    "Target": "EQUI_TargetWindow.xml",
}

class WindowSyncer:
    def __init__(self, workspace_root, dry_run=False, verbose=False, force=False):
        self.workspace_root = Path(workspace_root)
        self.thorne_drak = self.workspace_root / "thorne_drak"
        self.options_root = self.thorne_drak / "Options"
        self.dry_run = dry_run
        self.verbose = verbose
        self.force = force
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "git_commit": self._get_git_commit(),
            "synced": [],
            "skipped": [],
            "errors": [],
            "total_synced": 0,
        }
    
    def _get_git_commit(self):
        """Get current git commit hash."""
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--short", "HEAD"],
                cwd=str(self.workspace_root),
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except Exception:
            pass
        return "unknown"
    
    def _sync_window(self, window_name, xml_files):
        """Sync one or more files for a window."""
        if isinstance(xml_files, str):
            xml_files = [xml_files]

        dest_dir = self.options_root / window_name / "Thorne"
        sync_status_file = self.options_root / window_name / ".sync-status.json"
        synced_files = []
        skipped_files = []
        
        if not dest_dir.exists():
            msg = f"Destination directory not found: {dest_dir}"
            self.results["errors"].append({"window": window_name, "error": msg})
            if self.verbose:
                print(f"    [ERROR] {msg}")
            return False

        for xml_file in xml_files:
            source = self.thorne_drak / xml_file
            dest_file = dest_dir / xml_file

            # Validate source path
            if not source.exists():
                msg = f"Source file not found: {source}"
                self.results["errors"].append({"window": window_name, "error": msg})
                if self.verbose:
                    print(f"    [ERROR] {msg}")
                continue

            # Check if file is identical (unless forcing)
            if dest_file.exists() and not self.force:
                source_hash = self._file_hash(source)
                dest_hash = self._file_hash(dest_file)
                if source_hash == dest_hash:
                    skipped_files.append(xml_file)
                    if self.verbose:
                        print(f"    [SKIP] {xml_file} already identical")
                    continue

            # Copy file
            if not self.dry_run:
                try:
                    shutil.copy2(source, dest_file)
                except Exception as e:
                    msg = f"Failed to copy {xml_file}: {str(e)}"
                    self.results["errors"].append({"window": window_name, "error": msg})
                    if self.verbose:
                        print(f"    [ERROR] {msg}")
                    continue

            synced_files.append(xml_file)

            if self.verbose:
                status = "[FORCE]" if self.force and dest_file.exists() else "[SYNC]"
                print(f"    {status} {xml_file}")
                print(f"         -> {dest_file.relative_to(self.workspace_root)}")

        if not synced_files and not self.force:
            # Files identical, but still update parent README for navigation
            if not self.dry_run:
                try:
                    with open(sync_status_file, 'r') as f:
                        metadata = json.load(f)
                    self._generate_parent_readme(window_name, xml_files, metadata)
                except Exception:
                    pass  # If metadata read fails, skip README update

            self.results["skipped"].append({
                "window": window_name,
                "reason": "Files already identical",
                "files": skipped_files
            })
            if self.verbose:
                print("    [SKIP] All files already identical")
                print("    [README] Parent README updated")
            return False
        
        # Update metadata
        metadata = {
            "window": window_name,
            "filenames": xml_files,
            "description": f"{window_name} window Thorne configuration ({len(xml_files)} file(s))",
            "last_sync_date": datetime.now().isoformat(),
            "last_sync_commit": self.results["git_commit"],
            "in_sync": True
        }
        
        if not self.dry_run:
            try:
                with open(sync_status_file, 'w') as f:
                    json.dump(metadata, f, indent=2)
            except Exception as e:
                msg = f"Failed to update metadata: {str(e)}"
                self.results["errors"].append({"window": window_name, "error": msg})
                if self.verbose:
                    print(f"    [ERROR] {msg}")
                return False
        
        # Generate parent README for navigation
        if not self.dry_run:
            self._generate_parent_readme(window_name, xml_files, metadata)
        
        self.results["synced"].append({
            "window": window_name,
            "files": synced_files,
            "commit": self.results["git_commit"]
        })
        self.results["total_synced"] += 1
        
        return True
    
    def _generate_parent_readme(self, window_name, xml_files, metadata):
        """Generate parent README.md for window directory navigation."""
        if isinstance(xml_files, str):
            xml_files = [xml_files]

        window_dir = self.options_root / window_name
        readme_path = window_dir / "README.md"
        xml_display = ", ".join(xml_files)
        
        # Get list of variants
        variants = []
        if window_dir.exists():
            for item in sorted(window_dir.iterdir()):
                if item.is_dir() and not item.name.startswith('.'):
                    # Check if variant has XML file
                    # NOTE: Use a different variable to avoid shadowing
                    # the xml_files parameter (which we need later)
                    variant_xmls = list(item.glob("EQUI*.xml"))
                    if variant_xmls:
                        variants.append({
                            "name": item.name,
                            "has_readme": (item / "README.md").exists(),
                            "xml_file": variant_xmls[0].name
                        })
        
        # Generate README content
        content = f"""# {window_name} Window Options

## Overview

This directory contains variants for the {window_name} window ({xml_display}).

**Last Synced:** {metadata['last_sync_date'][:10]}  
**Git Commit:** {metadata['last_sync_commit']}

---

## Available Variants

"""
        
        # Add variant list
        if variants:
            for variant in variants:
                readme_indicator = "📄" if variant['has_readme'] else "  "
                content += f"- **[{variant['name']}/]({variant['name']}/)**  {readme_indicator}\n"
                content += f"  `{variant['xml_file']}`\n\n"
        else:
            content += "*No variants found*\n\n"
        
        # Use filename-only (relative) references — never absolute paths
        xml_names = [name if isinstance(name, str) else name.name for name in xml_files]
        
        content += f"""---

## Thorne Configuration

The `Thorne/` directory contains the current synchronized backup of the main working file(s) from `thorne_drak/`:

{chr(10).join([f"- `{name}`" for name in xml_names])}

## Metadata

See [.sync-status.json](.sync-status.json) for detailed sync metadata including:
- Last sync date and commit
- Sync status (in_sync: true/false)
- Window description

---

**Part of:** [Thorne UI Options System](../../.docs/options-sync/)
"""
        
        # Write README only if content actually changed
        try:
            if readme_path.exists():
                existing = readme_path.read_text(encoding='utf-8')
                if existing == content:
                    if self.verbose:
                        print("    [README] No changes, skipped")
                    return
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(content)
            if self.verbose:
                print("    [README] Updated parent README.md")
        except Exception as e:
            if self.verbose:
                print(f"    [WARN] Failed to update parent README: {str(e)}")
    
    def _file_hash(self, file_path):
        """Quick file hash for comparison."""
        import hashlib
        md5 = hashlib.md5()
        try:
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b''):
                    md5.update(chunk)
            return md5.hexdigest()
        except Exception:
            return None
    
    def sync_window(self, window_name):
        """Sync a specific window."""
        window_name = window_name.strip()
        
        # Find matching window
        for key, xml_files in WINDOW_MAPPING.items():
            if key.lower() == window_name.lower():
                if self.verbose:
                    print(f"Syncing: {key}")
                self._sync_window(key, xml_files)
                return True
        
        msg = f"Window not found: {window_name}. Available: {', '.join(WINDOW_MAPPING.keys())}"
        self.results["errors"].append({"error": msg})
        print(f"[ERROR] {msg}")
        return False
    
    def sync_all(self):
        """Sync all configured windows."""
        if self.verbose:
            print(f"Syncing all {len(WINDOW_MAPPING)} windows...\n")
        
        for window_name, xml_files in WINDOW_MAPPING.items():
            if self.verbose:
                print(f"  {window_name}:")
            self._sync_window(window_name, xml_files)
    
    def print_report(self):
        """Print sync report."""
        print("\n" + "="*70)
        print("WINDOW SYNC REPORT")
        print("="*70)
        print(f"Timestamp: {self.results['timestamp']}")
        print(f"Git Commit: {self.results['git_commit']}")
        
        if self.dry_run:
            print("\n[DRY-RUN MODE] - No files were actually modified\n")
        
        if self.results['synced']:
            print(f"\n[SYNCED] {len(self.results['synced'])} window(s)")
            for item in self.results['synced']:
                print(f"  {item['window']}")
                for file_name in item.get('files', []):
                    source = self.thorne_drak / file_name
                    dest = self.options_root / item['window'] / 'Thorne' / file_name
                    print(f"    {source.relative_to(self.workspace_root)} -> {dest.relative_to(self.workspace_root)}")
        
        if self.results['skipped']:
            print(f"\n[SKIPPED] {len(self.results['skipped'])} window(s)")
            for item in self.results['skipped']:
                print(f"  {item['window']} - {item['reason']}")
        
        if self.results['errors']:
            print(f"\n[ERRORS] {len(self.results['errors'])} issue(s)")
            for item in self.results['errors']:
                if 'window' in item:
                    print(f"  {item['window']}: {item['error']}")
                else:
                    print(f"  {item['error']}")
        
        print("\n" + "="*70)
        print(f"Total Synced: {self.results['total_synced']}")
        print("="*70 + "\n")
    
    def save_report(self, output_file):
        """Save report to JSON."""
        with open(output_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"Report saved to: {output_file}")


def main():
    import argparse
    import textwrap

    window_count = len(WINDOW_MAPPING)
    available_windows = ", ".join(WINDOW_MAPPING.keys())
    available_windows_wrapped = textwrap.fill(
        available_windows,
        width=72,
        initial_indent="    ",
        subsequent_indent="    ",
    )
    
    parser = argparse.ArgumentParser(
        prog="options_thorne_sync.py",
        description=f"""
    Sync Window to Thorne - Backup working window files to Thorne/ directory

    Copies the main working file from thorne_drak/ to Options/[Window]/Thorne/ 
and updates sync metadata with current timestamp and git commit information.

FEATURES:
    ✓ Single window or bulk sync of all {window_count} configured windows
  ✓ Dry-run mode to preview changes before applying
  ✓ Automatic parent README generation for navigation
  ✓ Metadata tracking with git commit information
  ✓ Duplicate detection (skips if already identical)
    ✓ Force mode to re-copy files and refresh metadata/readme

CAUTION: This is a DESTRUCTIVE OPERATOR. Use --dry-run first to preview.
""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
EXAMPLES:

  # Sync single window (with preview)
    python .bin/options_thorne_sync.py --window Player --dry-run
    python .bin/options_thorne_sync.py --window Player

    # Sync all {window_count} windows with verbose output
    python .bin/options_thorne_sync.py --all --verbose

    # Force re-copy and metadata refresh for all windows
        python .bin/options_thorne_sync.py --all --force

  # Preview what would be synced
    python .bin/options_thorne_sync.py --all --dry-run

AVAILABLE WINDOWS:
{available_windows_wrapped}

OUTPUT:
  - Console: Sync report with counts and filenames
  - .reports/sync_report.json: Detailed metadata and results
  - <Window>/README.md: Auto-generated navigation file
  - <Window>/.sync-status.json: Metadata with timestamp and git commit
"""
    )
    
    # Make window and all mutually exclusive
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--window", "-w",
        metavar="NAME",
        help="Sync specific window (e.g., Player, Target, Inventory)"
    )
    group.add_argument(
        "--all", "-a",
        action="store_true",
        help=f"Sync all {window_count} configured windows"
    )
    
    parser.add_argument(
        "--dry-run", "-d",
        action="store_true",
        help="Preview changes without modifying files"
    )
    parser.add_argument(
        "--force", "-f",
        action="store_true",
        help="Force copy even when source and destination are identical"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show detailed file operations and results"
    )
    
    args = parser.parse_args()
    
    # Determine workspace root
    script_dir = Path(__file__).parent
    workspace_root = script_dir.parent
    
    # Validate workspace
    if not (workspace_root / "thorne_drak").exists():
        print(f"ERROR: thorne_drak directory not found at {workspace_root / 'thorne_drak'}")
        sys.exit(1)
    
    # Create syncer
    syncer = WindowSyncer(
        workspace_root,
        dry_run=args.dry_run,
        verbose=args.verbose,
        force=args.force,
    )
    
    # Execute sync
    if args.all:
        syncer.sync_all()
    else:
        syncer.sync_window(args.window)
    
    # Print report
    syncer.print_report()
    
    # Save report
    report_file = workspace_root / ".reports" / "sync_report.json"
    report_file.parent.mkdir(parents=True, exist_ok=True)
    syncer.save_report(report_file)


if __name__ == "__main__":
    main()
