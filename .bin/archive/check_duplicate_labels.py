#!/usr/bin/env python3
"""
Check for and remove duplicate labels in thorne-ui repository.
"""

import os
import sys
import requests
from collections import defaultdict

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
            print(f"Error fetching labels: {response.status_code}")
            return []
        
        batch = response.json()
        if not batch:
            break
        
        labels.extend(batch)
        page += 1
    
    return labels

def delete_label(token, owner, repo, name):
    """Delete a label from a repository."""
    url = f"https://api.github.com/repos/{owner}/{repo}/labels/{name}"
    headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}
    
    response = requests.delete(url, headers=headers)
    return response.status_code == 204

def main():
    """Main function."""
    print(f"Checking for duplicate labels in {TARGET_OWNER}/{TARGET_REPO}...\n")
    token = get_github_token()
    
    # Get all labels
    labels = get_labels(token, TARGET_OWNER, TARGET_REPO)
    
    if not labels:
        print("No labels found.")
        return
    
    # Group by name
    label_groups = defaultdict(list)
    for label in labels:
        label_groups[label['name']].append(label)
    
    # Find duplicates
    duplicates = {name: group for name, group in label_groups.items() if len(group) > 1}
    
    if not duplicates:
        print(f"✓ No duplicate labels found. Total labels: {len(labels)}")
        return
    
    print(f"Found {len(duplicates)} duplicate label(s):\n")
    
    for name, group in duplicates.items():
        print(f"  {name}: {len(group)} copies")
        for i, label in enumerate(group, 1):
            print(f"    [{i}] Color: #{label['color']}, Description: {label.get('description', 'N/A')}")
    
    # Ask user if they want to remove duplicates
    print(f"\nRemoving duplicate labels (keeping first, deleting others)...\n")
    
    deleted = 0
    failed = 0
    
    for name, group in duplicates.items():
        # Keep the first one, delete the rest
        for label in group[1:]:
            if delete_label(token, TARGET_OWNER, TARGET_REPO, name):
                print(f"✓ Deleted duplicate: {name}")
                deleted += 1
            else:
                print(f"✗ Failed to delete: {name}")
                failed += 1
    
    print(f"\nResults: {deleted} deleted, {failed} failed")

if __name__ == "__main__":
    main()
