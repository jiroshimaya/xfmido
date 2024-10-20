#!/bin/bash

# Get the current version
current_version=$(git describe --tags --abbrev=0)

# Remove the leading 'v'
current_version=${current_version#v}

# Split the version number
IFS='.' read -r -a version_parts <<< "$current_version"

# Update the version based on the argument
case "$1" in
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
  *)
    echo "Invalid version type: $1"
    exit 1
    ;;
esac

# Output the new version
new_version="v${version_parts[0]}.${version_parts[1]}.${version_parts[2]}"
echo $new_version