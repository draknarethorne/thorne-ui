#!/usr/bin/env python3
"""
Update release descriptions in thorne-ui with the original detailed descriptions from thorne-ui-alpha.
"""

import os
import sys
import requests

# Configuration
SOURCE_OWNER = "draknarethorne"
SOURCE_REPO = "thorne-ui-alpha"
TARGET_OWNER = "draknarethorne"
TARGET_REPO = "thorne-ui"

def get_github_token():
    """Get GitHub token from environment."""
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("Error: GITHUB_TOKEN environment variable not set")
        sys.exit(1)
    return token

def get_releases(token, owner, repo):
    """Get all releases from a repository with full details."""
    url = f"https://api.github.com/repos/{owner}/{repo}/releases"
    headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}
    
    releases = []
    page = 1
    per_page = 30
    
    while True:
        params = {"page": page, "per_page": per_page}
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code != 200:
            print(f"Error fetching releases: {response.status_code}")
            print(response.text)
            sys.exit(1)
        
        batch = response.json()
        if not batch:
            break
        
        releases.extend(batch)
        page += 1
    
    return releases

def update_release(token, owner, repo, release_id, body):
    """Update a release's body/description."""
    url = f"https://api.github.com/repos/{owner}/{repo}/releases/{release_id}"
    headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}
    
    payload = {"body": body}
    response = requests.patch(url, headers=headers, json=payload)
    
    return response.status_code == 200

def main():
    """Main function."""
    print(f"Fetching releases from {SOURCE_OWNER}/{SOURCE_REPO}...")
    token = get_github_token()
    
    source_releases = get_releases(token, SOURCE_OWNER, SOURCE_REPO)
    target_releases = get_releases(token, TARGET_OWNER, TARGET_REPO)
    
    # Create a map of target releases by tag
    target_by_tag = {r["tag_name"]: r for r in target_releases}
    
    print(f"Found {len(source_releases)} source releases")
    print(f"Found {len(target_releases)} target releases\n")
    
    updated = 0
    skipped = 0
    
    for source in source_releases:
        tag = source["tag_name"]
        
        if tag not in target_by_tag:
            print(f"⊘ {tag}: Not found in target repo, skipping")
            skipped += 1
            continue
        
        target = target_by_tag[tag]
        source_body = source.get("body", "")
        target_body = target.get("body", "")
        
        # Check if bodies are different
        if source_body == target_body:
            print(f"✓ {tag}: Descriptions already match")
            continue
        
        # Update the release
        if update_release(token, TARGET_OWNER, TARGET_REPO, target["id"], source_body):
            print(f"✓ {tag}: Updated description")
            updated += 1
        else:
            print(f"✗ {tag}: Failed to update description")
    
    print(f"\nResults: {updated} updated, {skipped} skipped")

if __name__ == "__main__":
    main()
