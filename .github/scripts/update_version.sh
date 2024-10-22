#!/bin/bash

# Initialize variables
version=""
increment=""
dryrun=false
recreate=false
nopush=false

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        -v|--version) version="$2"; shift ;;
        -i|--increment) increment="$2"; shift ;;
        -d|--dryrun) dryrun=true ;;
        -r|--recreate) recreate=true ;;
        -n|--nopush) nopush=true ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

# Validate increment
if [[ "$increment" && "$increment" != "major" && "$increment" != "minor" && "$increment" != "patch" ]]; then
    echo "Invalid version increment: $increment"
    exit 1
fi

# Output the new version
if [[ -n "$version" ]]; then
    new_version=$version
else 
    # Get the current version if not provided
    current_version=$(git ls-remote --tags origin | awk -F'/' '{print $3}' | grep '^v' | sort -V | tail -n1)

    # Remove the leading 'v'
    current_version=${current_version#v}

    # Split the version number
    IFS='.' read -r -a version_parts <<< "$current_version"

    # Update the version based on the increment
    case "$increment" in
        major)
            ((version_parts[0]++))
            version_parts[1]=0
            version_parts[2]=0
            ;;
        minor)
            ((version_parts[1]++))
            version_parts[2]=0
            ;;
        patch)
            ((version_parts[2]++))
            ;;
        
    esac

    new_version="v${version_parts[0]}.${version_parts[1]}.${version_parts[2]}"
fi
echo $new_version

# 新しいバージョンのタグを作成
create_tag() {
    if [ "$recreate" = true ]; then
        if git rev-parse "$new_version" >/dev/null 2>&1; then
            git tag -d "$new_version"
        fi
    fi
    git tag "$new_version"
}

# 新しいバージョンのタグをプッシュ
push_tag() {
    if [ "$recreate" = true ]; then
        if git ls-remote --tags origin | grep -q "refs/tags/$new_version"; then
            git push --delete origin "$new_version"
        fi
    fi
    git push origin "$new_version"
}

if [ "$dryrun" = false ]; then
    create_tag
    if [ "$nopush" = false ]; then
        push_tag
    fi
else
    echo "Dry run enabled, not tagging or pushing."
fi
