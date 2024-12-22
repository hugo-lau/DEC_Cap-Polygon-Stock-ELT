#!/usr/bin/env bash
set -eu

main() {
    export TOP_DIR=$(git rev-parse --show-toplevel)

    # Format Python files using black
    black "Integration-elt"  # Target only the Integration-elt folder

    # Optional: Lint any SQL files if needed (remove this if SQL linting isn't required)
    # sqlfluff fix -f "Integration-elt" --dialect postgres

    # If the linter produces diffs, fail the linter
    if [ -z "$(git status --porcelain)" ]; then 
        echo "Working directory clean, linting passed"
        exit 0
    else
        echo "Linting failed. Please commit these changes:"
        git --no-pager diff HEAD
        exit 1
    fi
}

main