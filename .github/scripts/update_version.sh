#!/bin/bash

# Initialize variables
version=""
type=""
dryrun=false

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        -v|--version) version="$2"; shift ;;
        -t|--type) type="$2"; shift ;;
        -dr|--dryrun) dryrun=true ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

# Validate type
if [[ "$type" && "$type" != "major" && "$type" != "minor" && "$type" != "patch" && "$type" != "recreate" ]]; then
    echo "Invalid version type: $type"
    exit 1
fi

# Output the new version
if [[ -n "$version" ]]; then
    new_version=$version
else 
    # Get the current version if not provided
    current_version=$(git describe --tags --abbrev=0)

    # Remove the leading 'v'
    current_version=${current_version#v}

    # Split the version number
    IFS='.' read -r -a version_parts <<< "$current_version"

    # Update the version based on the type
    case "$type" in
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

# Tag the new version
if [ "$dryrun" = false ]; then
    if ! git tag "$new_version"; then
        if [[ "$type" == "recreate" ]]; then
            echo "Deleting tag $new_version"
            git tag -d "$new_version"
            echo "Recreating tag $new_version"
            git tag "$new_version"
        else
            echo "Failed to create the new tag"
            exit 1
        fi
    fi
    # Push the new tag to the origin
    if ! git push origin "$new_version"; then
        if [[ "$type" == "recreate" ]]; then
            echo "Deleting tag $new_version"
            git push --delete origin "$new_version"
            echo "Pushing tag $new_version"
            git push origin "$new_version"
        else
            echo "Failed to push the new tag"
            exit 1
        fi
    fi
else
    echo "Dry run enabled, not tagging or pushing."
fi
