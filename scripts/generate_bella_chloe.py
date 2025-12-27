#!/usr/bin/env python3
from generate_aria_headshots import generate_face_variations

# Same variations as Aria
variations = [
    "neutral expression, looking straight ahead",
    "smiling with teeth showing, looking straight ahead",
    "soft subtle smile, looking straight ahead",
    "three-quarter angle facing left, natural expression",
    "three-quarter angle facing right, natural expression"
]

print("=" * 60)
print("GENERATING BELLA FACE VARIATIONS")
print("=" * 60)
bella_results = generate_face_variations(
    model_name="bella",
    base_image_s3_key="bella/base.jpeg",
    output_subfolder="face_variations",
    variations=variations
)

print("\n" + "=" * 60)
print("GENERATING CHLOE FACE VARIATIONS")
print("=" * 60)
chloe_results = generate_face_variations(
    model_name="chloe",
    base_image_s3_key="chloe/base.jpeg",
    output_subfolder="face_variations",
    variations=variations
)

print("\n" + "=" * 60)
print("ALL DONE!")
print("=" * 60)
