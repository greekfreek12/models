#!/usr/bin/env python3
"""
Crop left panel from Bailey upper body grid
"""

from PIL import Image

# Load grid
grid = Image.open("bailey_upper_body_grid.jpg")
width, height = grid.size

# Crop left half (panel 1)
left_panel = grid.crop((0, 0, width//2, height))
left_panel.save("bailey_upper_body_final.jpg", quality=95)

print("✓ Cropped left panel: bailey_upper_body_final.jpg")
