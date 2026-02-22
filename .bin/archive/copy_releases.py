#!/usr/bin/env python3
"""
Copy releases from thorne-ui-alpha to thorne-ui for historical purposes.
Requires GitHub Personal Access Token with 'repo' scope.
"""

import os
import sys
import requests
from pathlib import Path

# Configuration
SOURCE_OWNER = "draknarethorne"
SOURCE_REPO = "thorne-ui-alpha"
TARGET_OWNER = "draknarethorne"
TARGET_REPO = "thorne-ui"

def get_github_token():
    """Get GitHub token from environment or user input."""
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        token = input("Enter your GitHub Personal Access Token: ").strip()
    if not token:
        print("Error: GitHub token is required.")
        sys.exit(1)
    return token

def list_releases(token, owner, repo):
    """List all releases from a repository."""
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

def download_asset(token, asset_url, target_path):
    """Download a release asset."""
    headers = {"Authorization": f"token {token}", "Accept": "application/octet-stream"}
    response = requests.get(asset_url, headers=headers)
    
    if response.status_code != 200:
        print(f"Error downloading asset: {response.status_code}")
        return False
    
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    with open(target_path, "wb") as f:
        f.write(response.content)
    
    print(f"  Downloaded: {os.path.basename(target_path)}")
    return True

def create_release_with_assets(token, owner, repo, release_data, asset_files):
    """Create a release in target repository with assets."""
    url = f"https://api.github.com/repos/{owner}/{repo}/releases"
    headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}
    
    # Prepare release payload
    payload = {
        "tag_name": release_data["tag_name"],
        "target_commitish": release_data.get("target_commitish", "main"),
        "name": release_data.get("name", release_data["tag_name"]),
        "body": release_data.get("body", ""),
        "draft": release_data.get("draft", False),
        "prerelease": release_data.get("prerelease", False),
    }
    
    # Create release
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code not in [201, 409]:  # 409 = tag already exists
        print(f"Error creating release {payload['tag_name']}: {response.status_code}")
        print(response.text)
        return False
    
    if response.status_code == 409:
        print(f"Release {payload['tag_name']} already exists, skipping.")
        return False
    
    release = response.json()
    print(f"Created release: {payload['tag_name']}")
    
    # Upload assets
    upload_url_template = release["upload_url"].replace("{?name,label}", "")
    
    for asset_file in asset_files:
        if not os.path.exists(asset_file):
            print(f"  Warning: Asset file not found: {asset_file}")
            continue
        
        filename = os.path.basename(asset_file)
        with open(asset_file, "rb") as f:
            upload_response = requests.post(
                f"{upload_url_template}?name={filename}",
                headers={"Authorization": f"token {token}", "Content-Type": "application/octet-stream"},
                data=f.read()
            )
        
        if upload_response.status_code in [201, 422]:  # 422 = asset already exists
            print(f"  Uploaded: {filename}")
        elif upload_response.status_code == 400:
            print(f"  Skipped (likely already exists): {filename}")
        else:
            print(f"  Error uploading {filename}: {upload_response.status_code}")
            if upload_response.text:
                print(f"    Response: {upload_response.text[:200]}")
    
    return True

def main():
    """Main function to copy releases."""
    print(f"Copying releases from {SOURCE_OWNER}/{SOURCE_REPO} to {TARGET_OWNER}/{TARGET_REPO}")
    print()
    
    token = get_github_token()
    
    # List source releases
    print(f"Fetching releases from {SOURCE_REPO}...")
    source_releases = list_releases(token, SOURCE_OWNER, SOURCE_REPO)
    print(f"Found {len(source_releases)} release(s)\n")
    
    if not source_releases:
        print("No releases found.")
        return
    
    # Create temp directory for assets
    temp_dir = Path(".release_assets")
    
    try:
        for release in source_releases:
            tag = release["tag_name"]
            print(f"Processing {tag}...")
            
            # Download assets
            asset_files = []
            if release["assets"]:
                assets_dir = temp_dir / tag
                os.makedirs(assets_dir, exist_ok=True)
                
                for asset in release["assets"]:
                    asset_path = assets_dir / asset["name"]
                    download_asset(token, asset["url"], str(asset_path))
                    asset_files.append(str(asset_path))
            
            # Create release in target repo
            create_release_with_assets(token, TARGET_OWNER, TARGET_REPO, release, asset_files)
            print()
    
    finally:
        # Cleanup temp directory
        if temp_dir.exists():
            import shutil
            shutil.rmtree(temp_dir)
            print("Cleaned up temporary files.")

if __name__ == "__main__":
    main()
