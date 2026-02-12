#!/usr/bin/env python3
"""
Sync Window to Default - Backup current working window files to Default/ and update metadata.

Copies the main working file from thorne_drak/ to Options/[Window]/Default/ and updates
the .sync-status.json metadata with current timestamp and git commit information.

Usage:
    python sync_window_to_default.py --window TARGET
    python sync_window_to_default.py --window Player --verbose
    python sync_window_to_default.py --all              # Sync all 13 windows
    python sync_window_to_default.py --all --dry-run    # Preview changes
    
Options:
    --window NAME       Sync specific window (e.g., Target, Player, Group, Spellbook)
    --all              Sync all 13 configured windows
    --dry-run          Show what would be synced without making changes
    --verbose          Show detailed file operations
"""

import os
import sys
import json
import shutil
import subprocess
from pathlib import Path
from datetime import datetime

# Window configuration - maps window name to EQUI_*.xml file
WINDOW_MAPPING = {
    "Actions": "EQUI_ActionsWindow.xml",
    "Animations": "EQUI_Animations.xml",
    "Group": "EQUI_GroupWindow.xml",
    "Hotbutton": "EQUI_HotbuttonWnd.xml",
    "Inventory": "EQUI_Inventory.xml",
    "Loot": "EQUI_LootWnd.xml",
    "Merchant": "EQUI_MerchantWnd.xml",
    "Pet": "EQUI_PetInfoWindow.xml",
    "Player": "EQUI_PlayerWindow.xml",
    "Selector": "EQUI_SelectorWnd.xml",
    "Skin": "EQUI_LoadskinWnd.xml",
    "Spellbook": "EQUI_SpellbookWnd.xml",
    "Target": "EQUI_TargetWindow.xml",
}

class WindowSyncer:
    def __init__(self, workspace_root, dry_run=False, verbose=False):
        self.workspace_root = Path(workspace_root)
        self.thorne_drak = self.workspace_root / "thorne_drak"
        self.options_root = self.thorne_drak / "Options"
        self.dry_run = dry_run
        self.verbose = verbose
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
        except:
            pass
        return "unknown"
    
    def _sync_window(self, window_name, xml_file):
        """Sync a single window file."""
        source = self.thorne_drak / xml_file
        dest_dir = self.options_root / window_name / "Default"
        dest_file = dest_dir / xml_file
        sync_status_file = self.options_root / window_name / ".sync-status.json"
        
        # Validate paths
        if not source.exists():
            msg = f"Source file not found: {source}"
            self.results["errors"].append({"window": window_name, "error": msg})
            if self.verbose:
                print(f"    [ERROR] {msg}")
            return False
        
        if not dest_dir.exists():
            msg = f"Destination directory not found: {dest_dir}"
            self.results["errors"].append({"window": window_name, "error": msg})
            if self.verbose:
                print(f"    [ERROR] {msg}")
            return False
        
        # Check if files are identical
        if dest_file.exists():
            source_hash = self._file_hash(source)
            dest_hash = self._file_hash(dest_file)
            if source_hash == dest_hash:
                # Files identical, but still update parent README for navigation
                if not self.dry_run:
                    # Read existing metadata for README generation
                    try:
                        with open(sync_status_file, 'r') as f:
                            metadata = json.load(f)
                        self._generate_parent_readme(window_name, xml_file, metadata)
                    except:
                        pass  # If metadata read fails, skip README update
                
                self.results["skipped"].append({
                    "window": window_name,
                    "reason": "Files already identical"
                })
                if self.verbose:
                    print(f"    [SKIP] Files already identical")
                    print(f"    [README] Parent README updated")
                return False
        
        # Copy file
        if not self.dry_run:
            try:
                shutil.copy2(source, dest_file)
            except Exception as e:
                msg = f"Failed to copy file: {str(e)}"
                self.results["errors"].append({"window": window_name, "error": msg})
                if self.verbose:
                    print(f"    [ERROR] {msg}")
                return False
        
        # Update metadata
        metadata = {
            "window": window_name,
            "filename": xml_file,
            "description": f"{window_name} window default configuration",
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
            self._generate_parent_readme(window_name, xml_file, metadata)
        
        self.results["synced"].append({
            "window": window_name,
            "source": str(source.relative_to(self.workspace_root)),
            "dest": str(dest_file.relative_to(self.workspace_root)),
            "commit": self.results["git_commit"]
        })
        self.results["total_synced"] += 1
        
        if self.verbose:
            print(f"    [SYNC] {xml_file}")
            print(f"         -> {dest_file.relative_to(self.workspace_root)}")
        
        return True
    
    def _generate_parent_readme(self, window_name, xml_file, metadata):
        """Generate parent README.md for window directory navigation."""
        window_dir = self.options_root / window_name
        readme_path = window_dir / "README.md"
        
        # Get list of variants
        variants = []
        if window_dir.exists():
            for item in sorted(window_dir.iterdir()):
                if item.is_dir() and not item.name.startswith('.'):
                    # Check if variant has XML file
                    xml_files = list(item.glob("EQUI*.xml"))
                    if xml_files:
                        variants.append({
                            "name": item.name,
                            "has_readme": (item / "README.md").exists(),
                            "xml_file": xml_files[0].name
                        })
        
        # Generate README content
        content = f"""# {window_name} Window Options

## Overview

This directory contains variants for the {window_name} window ({xml_file}).

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
        
        content += f"""---

## Default Configuration

The `Default/` directory contains the current synchronized backup of the main working file from `thorne_drak/{xml_file}`.

## Metadata

See [.sync-status.json](.sync-status.json) for detailed sync metadata including:
- Last sync date and commit
- Sync status (in_sync: true/false)
- Window description

---

**Part of:** [Thorne UI Options System](../../.docs/options-sync/)
"""
        
        # Write README
        try:
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(content)
            if self.verbose:
                print(f"    [README] Updated parent README.md")
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
        except:
            return None
    
    def sync_window(self, window_name):
        """Sync a specific window."""
        window_name = window_name.strip()
        
        # Find matching window
        for key, xml_file in WINDOW_MAPPING.items():
            if key.lower() == window_name.lower():
                if self.verbose:
                    print(f"Syncing: {key}")
                self._sync_window(key, xml_file)
                return True
        
        msg = f"Window not found: {window_name}. Available: {', '.join(WINDOW_MAPPING.keys())}"
        self.results["errors"].append({"error": msg})
        print(f"[ERROR] {msg}")
        return False
    
    def sync_all(self):
        """Sync all configured windows."""
        if self.verbose:
            print(f"Syncing all {len(WINDOW_MAPPING)} windows...\n")
        
        for window_name, xml_file in WINDOW_MAPPING.items():
            if self.verbose:
                print(f"  {window_name}:")
            self._sync_window(window_name, xml_file)
    
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
                print(f"    {item['source']} -> {item['dest']}")
        
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
    # Parse arguments
    window_name = None
    sync_all = "--all" in sys.argv
    dry_run = "--dry-run" in sys.argv
    verbose = "--verbose" in sys.argv
    
    # Find --window argument
    if "--window" in sys.argv:
        idx = sys.argv.index("--window")
        if idx + 1 < len(sys.argv):
            window_name = sys.argv[idx + 1]
    
    # Determine workspace root
    script_dir = Path(__file__).parent
    workspace_root = script_dir.parent
    
    # Validate workspace
    if not (workspace_root / "thorne_drak").exists():
        print(f"ERROR: thorne_drak directory not found at {workspace_root / 'thorne_drak'}")
        sys.exit(1)
    
    # Create syncer
    syncer = WindowSyncer(workspace_root, dry_run=dry_run, verbose=verbose)
    
    # Execute sync
    if sync_all:
        syncer.sync_all()
    elif window_name:
        syncer.sync_window(window_name)
    else:
        print("Usage:")
        print("  python sync_window_to_default.py --window TARGET")
        print("  python sync_window_to_default.py --all [--dry-run] [--verbose]")
        print()
        print("Available windows:")
        for name in sorted(WINDOW_MAPPING.keys()):
            print(f"  - {name}")
        sys.exit(1)
    
    # Print report
    syncer.print_report()
    
    # Save report
    report_file = workspace_root / ".reports" / "sync_report.json"
    report_file.parent.mkdir(parents=True, exist_ok=True)
    syncer.save_report(report_file)


if __name__ == "__main__":
    main()
