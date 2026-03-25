#!/bin/bash
set -e

if [ -z "$1" ]; then
    echo "Usage: $0 <input_image>"
    echo "Example: $0 photo.jpg"
    exit 1
fi

INPUT="$1"

if [ ! -f "$INPUT" ]; then
    echo "Error: File not found: $INPUT"
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

python3 "$SCRIPT_DIR/crop_face.py" "$INPUT"
