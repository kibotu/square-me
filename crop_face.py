#!/usr/bin/env python3
"""Face-centered square crop tool."""

import argparse
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image


def get_face_bbox(image: Image.Image) -> tuple[float, float, float, float] | None:
    """Detect face and return normalized bounding box (x_min, y_min, x_max, y_max)."""
    img_array = np.asarray(image)
    gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, 1.05, 3)
    
    if len(faces) == 0:
        return None
    
    x, y, w, h = faces[0]
    width, height = image.size
    return (x / width, y / height, (x + w) / width, (y + h) / height)


def crop_to_square(image: Image.Image, bbox: tuple[float, float, float, float]) -> Image.Image:
    """Crop image to square centered on face bounding box."""
    width, height = image.size
    
    x_min, y_min, x_max, y_max = bbox
    face_center_x = (x_min + x_max) / 2 * width
    face_center_y = (y_min + y_max) / 2 * height
    
    square_size = min(width, height)
    
    crop_x = face_center_x - square_size / 2
    crop_y = face_center_y - square_size / 2
    
    crop_x = max(0, min(crop_x, width - square_size))
    crop_y = max(0, min(crop_y, height - square_size))
    
    return image.crop((
        int(crop_x),
        int(crop_y),
        int(crop_x + square_size),
        int(crop_y + square_size)
    ))


SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def process_image(input_path: Path, output_dir: Path | None = None) -> bool:
    """Process a single image. Returns True if successful."""
    image = Image.open(input_path)
    
    if image.mode not in ("RGB", "RGBA"):
        image = image.convert("RGBA")
    
    bbox = get_face_bbox(image)
    
    if bbox is None:
        print(f"Error: No face detected in {input_path}", file=sys.stderr)
        return False
    
    square = crop_to_square(image, bbox)
    
    stem = input_path.stem
    ext = input_path.suffix
    
    if output_dir:
        output_dir.mkdir(parents=True, exist_ok=True)
        output = output_dir / f"{stem}-square{ext}"
    else:
        output = input_path.parent / f"{stem}-square{ext}"
    
    if ext.lower() in (".jpg", ".jpeg"):
        square.save(output, "JPEG", quality=95)
    elif ext.lower() == ".png":
        square.save(output, "PNG")
    else:
        square.save(output)
    
    print(f"Saved: {output}")
    return True


def process_folder(folder: Path, output_dir: Path | None = None) -> int:
    """Process all images in a folder. Returns number of successfully processed images."""
    image_files = [f for f in folder.iterdir() if f.suffix.lower() in SUPPORTED_EXTENSIONS]
    
    if not image_files:
        print(f"No supported images found in {folder}", file=sys.stderr)
        return 0
    
    success_count = 0
    for image_file in image_files:
        if process_image(image_file, output_dir):
            success_count += 1
    
    print(f"Processed {success_count}/{len(image_files)} images successfully")
    return success_count


def main():
    parser = argparse.ArgumentParser(description="Crop image to square centered on face")
    parser.add_argument("input", type=Path, nargs="?", help="Input image path")
    parser.add_argument("--folder", "-f", type=Path, help="Input folder to process in batch mode")
    parser.add_argument("--output", "-o", type=Path, help="Output directory (for batch mode)")
    args = parser.parse_args()
    
    if args.folder:
        if not args.folder.exists() or not args.folder.is_dir():
            print(f"Error: Folder not found: {args.folder}", file=sys.stderr)
            sys.exit(1)
        process_folder(args.folder, args.output)
    elif args.input:
        if not args.input.exists():
            print(f"Error: File not found: {args.input}", file=sys.stderr)
            sys.exit(1)
        process_image(args.input)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
