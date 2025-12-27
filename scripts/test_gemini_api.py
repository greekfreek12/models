#!/usr/bin/env python3
import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

load_dotenv('.env.local')

# Configure Gemini API
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

# Test prompt from user
prompt_data = {
    "task": {
        "type": "character_reference_sheet",
        "layout": "Side-by-side Diptych (Split Screen). Two full-body images of the same woman combined into one wide frame.",
        "composition": "LEFT PANEL: Full Body Front View. RIGHT PANEL: Full Body Back View (turned 180 degrees)."
    },
    "subject": {
        "demographics": "Young adult female (approx 20-25 years old). Height 5'4\" (Short/Petite stature). Weight 157 lbs (High density/curvy). Hair is Straight/Layered Blonde. Eyes are HAZEL. No tattoos. No piercings.",
        "facial_features": "Friendly, approachable, naturally pretty face ('Girl next door' aesthetic). Hazel eyes, healthy complexion. Expression is confident and happy.",
        "body_type": {
            "overall": "'Thin but Thick' (Bottom-Heavy / Pear Shape) aesthetic. Significant contrast between the upper and lower body.",
            "measurements": "Visual translation of stats: 32B Bust (Small) - 26\" Waist (Medium/Defined) - 37\"+ Hips (Curvy).",
            "structure": "Short stack physique (5'4\"). The torso is slender and 'thin'. The weight (157 lbs) is almost entirely distributed in the lower body—thick thighs, heavy legs, and a large gluteal shelf."
        },
        "chest_details": {
            "size": "Natural 32B Cup / Small Bust.",
            "visuals": "Modest, athletic chest size. Slight curve but no heavy cleavage. The chest is proportional to the 'thin' upper body description, contrasting with the heavy bottom.",
            "physics": "Perky, natural shape. No push-up effect needed."
        },
        "glute_and_leg_details": {
            "shape": "Thick, heavy, and voluptuous.",
            "rear_view_specifics": "The focal point of the physique. A 'Big Butt' that looks dense and muscular (carrying the 157 lbs). Thighs are thick and touching (no thigh gap). The glutes are round and protrude significantly in the profile/back view, creating a deep curve from the lower back."
        },
        "apparel": {
            "top": "Black sliding triangle bikini top. Fits flush against the smaller chest (B-cup).",
            "bottom": "Matte black string bikini bottoms. 'Brazilian' cut to showcase the glutes. The side strings dig slightly into the softer/thicker hips, emphasizing the density of the lower body.",
            "accessories": "NONE. No necklace. No earrings. Clean, natural look."
        },
        "skin_details": "Natural skin texture. Smooth but with realistic weight/softness on the thighs and hips."
    },
    "pose": {
        "left_panel_front": "Standing upright facing the camera, hands on hips. showcasing the 'Thin' upper body vs 'Thick' lower body ratio.",
        "right_panel_back": "Standing upright facing away. Emphasizing the width of the hips and the projection of the 'Big Butt' relative to the smaller back."
    },
    "environment": {
        "location": "Backyard patio interface between tiled area and grass.",
        "background_continuity": "Left side: White weatherboard house siding. Right side: Green artificial turf and tropical plants."
    },
    "camera": {
        "shot_type": "Wide Full-Body Shot.",
        "angle": "Eye-level.",
        "focal_length": "50mm.",
        "lighting": "Natural daylight. Highlighting the curves of the lower body."
    },
    "aspect_ratio_and_output": {
        "ratio": "16:9",
        "framing": "Wide landscape orientation."
    },
    "negative_prompt": {
        "forbidden_elements": [
            "large breasts",
            "fake boobs",
            "silicone",
            "D cup",
            "DD cup",
            "skinny legs",
            "thigh gap",
            "anorexic",
            "necklace",
            "jewelry",
            "tattoos",
            "piercings",
            "merged bodies",
            "cartoon",
            "3d render"
        ]
    }
}

# Convert to string prompt
prompt_text = json.dumps(prompt_data, indent=2)

print("Testing Gemini API...")
print(f"API Key: {os.getenv('GOOGLE_API_KEY')[:20]}...")
print(f"\nPrompt length: {len(prompt_text)} characters")

# Use Gemini 2.0 Flash image generation model
try:
    model = genai.ImageGenerationModel("imagen-3.0-generate-001")

    print("\nGenerating image...")
    response = model.generate_images(
        prompt=prompt_text,
        number_of_images=1,
        aspect_ratio="16:9",
        safety_filter_level="block_only_high",
        person_generation="allow_adult"
    )

    if response.images:
        output_path = "test_gemini_output.jpeg"
        response.images[0].save(output_path)
        print(f"\n✓ Success! Image saved to: {output_path}")
    else:
        print("\n✗ No images generated")

except Exception as e:
    print(f"\n✗ Error: {e}")
    print("\nTrying alternative approach...")

    # Try with standard generative model
    try:
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        response = model.generate_content(
            f"Generate an image based on this specification:\n\n{prompt_text}"
        )
        print(response.text)
    except Exception as e2:
        print(f"✗ Also failed: {e2}")
