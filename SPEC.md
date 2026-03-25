# Technical Implementation Spec: Face-Centered Square Crop

## Problem Statement
Convert a portrait photo to a square cropped image by detecting the person's face and centering the crop around it, maximizing the visible face area while maintaining a square aspect ratio.

## Constraints
- Single person in photo
- Platform: macOS M2 (Apple Silicon)
- Use `uv` for Python package management

## Solution Overview

### Face Detection
- **Library**: OpenCV Haar Cascade
- **Model**: `haarcascade_frontalface_default.xml` (bundled with OpenCV)
- **Parameters**: scaleFactor=1.05, minNeighbors=3
- **Output**: Bounding box (x, y, w, h) in pixels, normalized to [0, 1]

### Cropping Algorithm

```
1. Load image, get dimensions (W, H)
2. Detect face → get bounding box
3. face_center = ((x_min + x_max)/2 * W, (y_min + y_max)/2 * H)
4. square_size = max(W, H)
5. crop_x = face_center.x - square_size/2
6. crop_y = face_center.y - square_size/2
7. Clamp crop_x to [0, W - square_size]
8. Clamp crop_y to [0, H - square_size]
9. Crop and save
```

### Edge Cases

| Scenario | Handling |
|----------|----------|
| No face detected | Exit with error code 1, print message |
| Face near edge | Clamp crop to image bounds |
| Already square | No crop needed, just save |
| Face bounding box invalid | Reject as "no face detected" |

## File Naming
- Input: `photo.jpg` → Output: `photo-square.jpg`
- Input: `IMG_1234.PNG` → Output: `IMG_1234-square.PNG`

## Dependencies
- `opencv-python-headless` - Face detection (Haar cascade)
- `Pillow` - Image I/O

## Performance Target
- < 500ms per image on M2 Mac
- Memory: < 200MB
