#!/bin/bash

set -ex

# Check if branch name is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <PR-number>"
    exit 1
fi

PR_NUMBER=$1

# Fetch all open pull requests (NOTE THE NAME OF THE BRANCH)
prs=$(gh pr list --state open --label "automated pr" --json number,headRefName -q ".[] | select(.headRefName | test(\"update-your-readme-$PR_NUMBER\")).number")

# Loop through each PR and close it
for pr in $prs; do
    echo "Closing PR #$pr"
    gh pr close $pr --comment "Closing this PR because the parent PR has been closed."
done