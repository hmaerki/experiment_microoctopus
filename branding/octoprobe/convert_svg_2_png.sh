#!/bin/bash
set -euo pipefail

# Get the absolute path of the directory containing the script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Remove all PNG files in the directory
rm -f "$SCRIPT_DIR"/*.png

for file in "$SCRIPT_DIR"/*.svg; do
  if [[ -f "$file" ]]; then
    echo "Processing $file"
    inkscape "$file" -w 1024 --export-filename="${file%.svg}.png"
  fi
done
