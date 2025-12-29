# Veronica - Scripts & Generation Log

## Model Setup
- **Created:** 2025-12-29
- **Base source:** Copied from Brooke's base.jpeg (dark-haired woman)

## Generation History

### 1. Base Image
- **Script:** N/A (copied from models/brooke/base.jpeg)
- **File:** `base.jpeg`
- **Description:** Split view (front + back) showing dark-haired woman in black bikini
- **Source:** Copy of Brooke's base

### 2. Face Angles Grid (2x3)
- **Script:** `scripts/generate_veronica_face_grid.py`
- **Date:** 2025-12-29
- **Input:**
  - base.jpeg (identity reference)
- **Output:** `face_grid_2x3.png`
- **Description:** 6 face angle variations (front neutral, front smile, 3/4 left, 3/4 right, profile, over shoulder)
- **Model:** gemini-3-pro-image-preview
- **Aspect ratio:** 16:9
- **Result:** Successfully generated 6 angles of same person from base

### 3. Greek Island Grid (3x3)
- **Script:** `scripts/generate_veronica_greek_grid.py`
- **Date:** 2025-12-29
- **Inputs:**
  - Reference 1: `bikinis/universal/GameDay_Luxe/teams/Alabama_Crimson_White.jpg` (bikini design only)
  - Reference 2: `base.jpeg` (body/identity reference)
  - Reference 3: `face_grid_2x3.png` (face angles reference)
- **Output:** `greek_island_grid_3x3.png`
- **Description:** 9 poses across Greek islands in Alabama crimson/white bikini
- **Locations:** Santorini (Oia, Pool), Mykonos (Windmills, Little Venice), Zakynthos, Crete, Milos, Corfu, Paros
- **Model:** gemini-3-pro-image-preview
- **Aspect ratio:** 1:1 (square grid)
- **Result:** Generated 9 panels, identity matches base references (dark-haired woman)

## Notes

### Identity Consistency
- Veronica's identity is: dark-haired, bronze skin (from base.jpeg)
- Face grid: dark-haired woman with 6 angle variations
- Greek grid: Same dark-haired woman in all 9 panels with Alabama bikini

### Reference Upload Order (Greek Grid)
1. Bikini design (extract pattern only)
2. Body/identity reference (base.jpeg)
3. Face angles reference (face_grid_2x3.png)

## Current Files
```
models_2.0/veronica/
├── base.jpeg                      # Split view: front + back (dark hair)
├── face_grid_2x3.png             # 6 face angles (dark hair)
├── greek_island_grid_3x3.png     # 9 Greek poses in Alabama bikini
└── SCRIPTS_USED.md               # This file
```
