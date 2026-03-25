#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ -n "$1" ] && [ -d "$1" ]; then
    FOLDER="$1"
    OUTPUT="${2:-}"

    if [ -n "$OUTPUT" ]; then
        python3 "$SCRIPT_DIR/crop_face.py" --folder "$FOLDER" --output "$OUTPUT" --recursive
    else
        python3 "$SCRIPT_DIR/crop_face.py" --folder "$FOLDER" --recursive
    fi
elif [ -n "$1" ] && [ -f "$1" ]; then
    python3 "$SCRIPT_DIR/crop_face.py" "$1"
else
    echo "Usage: $0 <input_image>"
    echo "   or: $0 <input_folder> [output_folder]"
    echo "Examples:"
    echo "  $0 photo.jpg"
    echo "  $0 photos/"
    echo "  $0 photos/ output/  (recursive)"
    exit 1
fi
