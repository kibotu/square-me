# Face-Centered Square Crop

Crop portrait photos to square images centered on the detected face.

## Requirements

- macOS (Apple Silicon M1/M2/M3)
- [uv](https://github.com/astral-sh/uv) package manager

Install uv if you haven't:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Installation

```bash
./install.sh
```

## Usage

```bash
./run.sh <input_image>
```

### Examples

```bash
./run.sh photo.jpg
./run.sh portrait.png
./run.sh ~/Pictures/selfie.jpeg
```

### Output

The cropped image is saved with `-square` appended to the filename:

| Input | Output |
|-------|--------|
| `photo.jpg` | `photo-square.jpg` |
| `IMG_123.PNG` | `IMG_123-square.PNG` |

## Error Handling

- **No face detected**: Exits with error code 1 and prints message
- **File not found**: Exits with error code 1

## How It Works

1. Detects face using OpenCV Haar Cascade
2. Calculates face center point
3. Creates square crop sized to the larger dimension
4. Centers square on face, clamped to image bounds
5. Saves with original format preserved
