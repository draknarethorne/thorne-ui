#!/usr/bin/env python3
"""
Copy labels from thorne-ui-alpha to thorne-ui.
"""

import os
import sys
import requests

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

def get_labels(token, owner, repo):
    """Get all labels from a repository."""
    url = f"https://api.github.com/repos/{owner}/{repo}/labels"
    headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}
    
    labels = []
    page = 1
    per_page = 30
    
    while True:
        params = {"page": page, "per_page": per_page}
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code != 200:
            return []
        
        batch = response.json()
        if not batch:
            break
        
        labels.extend(batch)
        page += 1
    
    return labels

def create_label(token, owner, repo, name, color, description=""):
    """Create a label in a repository."""
    url = f"https://api.github.com/repos/{owner}/{repo}/labels"
    headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}
    
    payload = {
        "name": name,
        "color": color,
        "description": description
    }
    
    response = requests.post(url, headers=headers, json=payload)
    return response.status_code in [201, 422]  # 422 = already exists

def main():
    """Main function."""
    print(f"Copying labels from {SOURCE_OWNER}/{SOURCE_REPO} to {TARGET_OWNER}/{TARGET_REPO}...\n")
    token = get_github_token()
    
    # Get source labels
    source_labels = get_labels(token, SOURCE_OWNER, SOURCE_REPO)
    
    if not source_labels:
        print("No labels found in source repo.")
        return
    
    print(f"Found {len(source_labels)} label(s) to copy:\n")
    
    created = 0
    
    for label in source_labels:
        name = label['name']
        color = label['color']
        description = label.get('description', '')
        
        if create_label(token, TARGET_OWNER, TARGET_REPO, name, color, description):
            print(f"✓ {name}")
            created += 1
        else:
            print(f"✗ {name} (failed)")
    
    print(f"\nResults: {created} created/skipped")

if __name__ == "__main__":
    main()
