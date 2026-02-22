#!/usr/bin/env python3
"""
Fetch labels and milestones from thorne-ui-alpha for review.
"""

import os
import sys
import requests

SOURCE_OWNER = "draknarethorne"
SOURCE_REPO = "thorne-ui-alpha"

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

def get_milestones(token, owner, repo):
    """Get all milestones from a repository."""
    url = f"https://api.github.com/repos/{owner}/{repo}/milestones"
    headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}
    
    milestones = []
    page = 1
    per_page = 30
    
    while True:
        params = {"page": page, "per_page": per_page, "state": "all"}
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code != 200:
            print(f"Error fetching milestones: {response.status_code}")
            return []
        
        batch = response.json()
        if not batch:
            break
        
        milestones.extend(batch)
        page += 1
    
    return milestones

def main():
    """Main function."""
    print(f"Fetching Labels and Milestones from {SOURCE_OWNER}/{SOURCE_REPO}...\n")
    token = get_github_token()
    
    # Get labels
    print("=" * 60)
    print("LABELS")
    print("=" * 60)
    labels = get_labels(token, SOURCE_OWNER, SOURCE_REPO)
    
    if labels:
        print(f"Found {len(labels)} label(s):\n")
        for label in labels:
            print(f"  • {label['name']}")
            if label.get('description'):
                print(f"    Description: {label['description']}")
            print(f"    Color: #{label['color']}")
            print()
    else:
        print("No labels found.\n")
    
    # Get milestones
    print("=" * 60)
    print("MILESTONES")
    print("=" * 60)
    milestones = get_milestones(token, SOURCE_OWNER, SOURCE_REPO)
    
    if milestones:
        print(f"Found {len(milestones)} milestone(s):\n")
        for ms in milestones:
            print(f"  • {ms['title']}")
            if ms.get('description'):
                print(f"    Description: {ms['description']}")
            print(f"    State: {ms['state']}")
            if ms.get('due_on'):
                print(f"    Due: {ms['due_on']}")
            print()
    else:
        print("No milestones found.\n")

if __name__ == "__main__":
    main()
