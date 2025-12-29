# Savannah - Scripts & Generation Log

## Model Setup
- **Created:** 2025-12-29
- **Face source:** Madison's face (blonde, blue eyes)
- **Body reference:** Brooke's base (for proportions/format)

## Generation History

### 1. Face Reference
- **Script:** N/A (copied from models/madison/01_face.jpeg)
- **File:** `face_reference.jpg`
- **Description:** Blonde woman with blue eyes, friendly smile, girl-next-door look
- **Source:** Madison's face close-up

### 2. Base Image (Split View)
- **Script:** `scripts/generate_savannah_base.py`
- **Date:** 2025-12-29
- **Inputs:**
  - Reference 1: `face_reference.jpg` (Savannah's face - blonde)
  - Reference 2: `models/brooke/base.jpeg` (body proportions/format reference)
- **Output:** `base.jpeg`
- **Description:** Split view (front + back) with blonde face, athletic hourglass body, black bikini
- **Model:** gemini-3-pro-image-preview
- **Aspect ratio:** 16:9
- **Background:** Outdoor patio setting (similar to Brooke's)
- **Result:** Successfully combined blonde face with athletic body, natural result

## Notes

### Identity
- Savannah's identity: Blonde hair, blue eyes, golden tan (from Madison's face)
- Body proportions: Athletic hourglass similar to Brooke's reference
- Natural combination, not a direct copy

### Reference Usage
- Face from Madison (blonde, blue eyes, friendly)
- Body format/proportions from Brooke (athletic hourglass, same setting)
- Black bikini, outdoor patio background

## Current Files
```
models_2.0/savannah/
├── face_reference.jpg    # Madison's face (blonde)
├── base.jpeg            # Split view: front + back (blonde in black bikini)
└── SCRIPTS_USED.md      # This file
```

## Next Steps
- Could generate face_grid_2x3.png for angle variations
- Could generate content grids (Greek islands, other themes)
