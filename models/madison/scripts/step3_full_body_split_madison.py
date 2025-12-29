#!/usr/bin/env python3
"""
STEP 3: Full Body Split View (Front + Back)
Generate full body reference with front and back views in one image
"""

from google import genai
from google.genai import types
from PIL import Image as PILImage
import os
import json
from dotenv import load_dotenv

load_dotenv('.env.local')
client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))

MODEL_NAME = "madison"
PROFILE_PATH = f"models/{MODEL_NAME}/profile_v1.json"
FACE_REF_PATH = f"models/{MODEL_NAME}/01_face.jpeg"
UPPER_REF_PATH = f"models/{MODEL_NAME}/02_upper_body.jpeg"
OUTPUT_PATH = f"models/{MODEL_NAME}/03_full_body_split.jpeg"

# Load profile
with open(PROFILE_PATH, 'r') as f:
    profile = json.load(f)

# Load reference images for upload
face_ref = PILImage.open(FACE_REF_PATH)
upper_ref = PILImage.open(UPPER_REF_PATH)

# Build full body split view prompt with identity locking
PROMPT = f"""CRITICAL IDENTITY PRESERVATION - READ CAREFULLY:

Generate a SPLIT VIEW image showing the SAME WOMAN from two angles in ONE image.

=== UPLOADED REFERENCES ===
Reference Image 1: Her face close-up - FACIAL IDENTITY
Reference Image 2: Her upper body in bikini top - BODY PROPORTIONS AND FACE

=== IDENTITY REQUIREMENTS - DO NOT CHANGE ANY OF THESE ===

FACE - KEEP 100% IDENTICAL TO REFERENCES:
- Eye color: {profile['face']['eyes']['color']}
- Eye shape: {profile['face']['eyes']['shape']}
- Nose: {profile['face']['nose']['shape']}, {profile['face']['nose']['size']}
- Lips: {profile['face']['lips']['fullness']}, {profile['face']['lips']['shape']}
- Face shape: {profile['face']['shape']}
- Cheekbones: {profile['face']['face_structure']['cheekbones']}
- Jawline: {profile['face']['face_structure']['jawline']}

SKIN - CRITICAL PRESERVATION:
- Skin tone: {profile['skin_overall']['baseline_tone']} (can tan to {profile['skin_overall']['tan_capability']})
- Skin texture: {profile['skin_overall']['texture']}
- NO beauty filter on face OR body
- NO artificial smoothing anywhere
- NO glowing skin effect
- Natural lighting behavior throughout
- Same skin characteristics from face to entire body

HAIR - KEEP 100% IDENTICAL:
- Color: {profile['hair']['color']}
- Length: {profile['hair']['length']}
- Texture: {profile['hair']['texture']}

UPPER BODY - KEEP IDENTICAL TO REFERENCE 2:
- Breast size: {profile['body']['upper_body']['breast']['size']}
- Breast shape: {profile['body']['upper_body']['breast']['shape']}
- Shoulder width: {profile['body']['upper_body']['shoulders']['width']}
- Upper body build: athletic but feminine

=== SPLIT IMAGE FORMAT ===

Create ONE image divided vertically down the middle:

LEFT HALF - FRONT VIEW:
- FULL body facing camera, HEAD TO FEET - feet must be visible
- Standing pose, natural and relaxed
- Weight slightly on one leg (natural hip curve)
- Arms at sides or one hand on hip
- CRITICAL: Frame must show complete body from top of head to bottom of feet
- Clear view of:
  * Face (same as references)
  * Chest and breasts
  * Waist definition
  * Hips and curves
  * Full legs including knees, calves, ankles
  * FEET must be visible at bottom of frame
- Full bikini (matching top and bottoms)
- Beach/outdoor setting
- Stand far enough back to capture ENTIRE body

RIGHT HALF - BACK VIEW:
- FULL body, back to camera, HEAD TO FEET - feet must be visible
- Natural back pose, NOT looking at camera
- Just natural standing from behind, relaxed
- CRITICAL: Frame must show complete body from top of head to bottom of feet
- Clear view of:
  * Back of head and hair
  * Back and shoulders
  * Waist taper from behind
  * GLUTES (CRITICAL - this is a key feature, must be prominent and clearly visible)
  * Full legs from behind including calves, ankles
  * FEET must be visible at bottom of frame
- Same bikini as front view
- Same beach/outdoor setting
- Same lighting as front
- Stand far enough back to capture ENTIRE body

BOTH VIEWS MUST SHOW THE SAME WOMAN:
- Identical facial features
- Identical hair
- Identical body proportions
- Identical skin tone
- Same bikini
- Same setting and lighting

=== BODY SPECIFICATIONS FROM PROFILE ===

FULL BODY REQUIREMENTS:
- Height: {profile['body']['height_description']}
- Build: {profile['body']['overall_build']}

WAIST:
- {profile['body']['waist']['description']}
- {profile['body']['waist']['definition_level']}

HIPS:
- {profile['body']['hips']['width']}
- {profile['body']['hips']['curve']}

WAIST-TO-HIP RATIO:
- {profile['body']['waist_to_hip_ratio']}

GLUTES (CRITICAL FEATURE - VERY IMPORTANT):
- Overall shape: {profile['body']['glutes']['overall_shape']}
- Volume: {profile['body']['glutes']['volume']}
- Lift: {profile['body']['glutes']['lift']}
- Roundness: {profile['body']['glutes']['roundness']}
- Upper glutes: {profile['body']['glutes']['fullness']['upper_glutes']}
- Mid glutes: {profile['body']['glutes']['fullness']['mid_glutes']}
- Lower glutes: {profile['body']['glutes']['fullness']['lower_glutes']}
- Shape description: {profile['body']['glutes']['shape_description']}
- Width: {profile['body']['glutes']['width']}
- Firmness: {profile['body']['glutes']['firmness']}
- Side view characteristics: {profile['body']['glutes']['side_view']}
- Back view characteristics: {profile['body']['glutes']['back_view']}
- CRITICAL: Glutes must be prominent, lifted, round, and shapely - this is a defining feature

LEGS:
- Length: {profile['body']['legs']['length']}
- Thighs: {profile['body']['legs']['thighs']['shape']}
- Thigh gap: {profile['body']['legs']['thighs']['gap']}
- Calves: {profile['body']['legs']['calves']['shape']}

OVERALL PROPORTIONS:
- {profile['body']['proportions']}
- Body type: {profile['body']['body_type']}

=== TECHNICAL SPECIFICATIONS ===

{{
  "meta": {{
    "aspect_ratio": "16:9",
    "quality": "ultra_photorealistic",
    "resolution": "8k",
    "camera": "professional camera",
    "style": "split screen, two views side by side, natural beach photography"
  }},

  "layout": {{
    "format": "vertical split down center",
    "left_side": "front view",
    "right_side": "back view",
    "divider": "thin white line or seamless blend"
  }},

  "scene": {{
    "location": "beach or tropical outdoor setting",
    "time": "golden hour or bright daylight",
    "lighting": "natural, flattering, same on both sides",
    "background": "beach, ocean, palm trees, tropical"
  }},

  "outfit": {{
    "type": "full bikini set (top and bottoms)",
    "color": "white, black, or neutral solid color",
    "style": "simple, clean, shows body clearly",
    "consistency": "SAME bikini in both front and back views"
  }},

  "pose_requirements": {{
    "front": "natural standing, confident, one leg slightly bent, arms relaxed, FULL BODY HEAD TO FEET VISIBLE",
    "back": "same pose from behind, NOT looking at camera, natural back view, FULL BODY HEAD TO FEET VISIBLE",
    "energy": "confident, natural, athletic",
    "camera_distance": "far enough to capture complete body from head to feet in both views"
  }}
}}

=== CRITICAL CONSTRAINTS ===

IDENTITY CONSISTENCY:
- This is the SAME PERSON from both reference images
- Her face MUST match references exactly
- Her upper body MUST match reference 2 exactly
- Use references to understand her complete identity
- DO NOT create a different person
- DO NOT alter any facial features
- DO NOT change body proportions from what's specified
- PRESERVE exact identity in both front and back views

BODY REALISM:
- Natural realistic body proportions
- Athletic hourglass build as specified
- NO exaggerated anatomy
- NO AI body distortions
- Real human proportions throughout
- Natural body physics and posing

GLUTES REQUIREMENT (CRITICAL):
- The glutes MUST match the detailed specifications
- Prominent, lifted, round, full bubble butt shape
- Clearly visible and shapely in back view
- This is a KEY DEFINING FEATURE of her physique
- Athletic but feminine, not overly muscular
- Natural development, realistic appearance

REALISM REQUIREMENTS:
- Natural skin texture on face and entire body
- Visible pores where appropriate
- Slight imperfections are natural
- NO beauty filter anywhere
- NO artificial smoothing
- NO glowing skin effect
- Realistic lighting with natural shadows
- Real human appearance throughout

=== FINAL CRITICAL REMINDER ===

This split image shows the SAME WOMAN from front and back. Every feature must be consistent between views. Her facial identity from the references must be preserved exactly. Her body must match the detailed specifications, especially the prominent lifted glutes which are a defining feature. This is a reference image for future content generation - complete identity consistency is CRITICAL.

BOTH SIDES: Same person, same bikini, same setting, same lighting.
FRONT VIEW: Shows her face, chest, waist, hips, full legs clearly.
BACK VIEW: Shows her back, glutes (PROMINENT AND SHAPELY), full legs from behind.
"""

def generate_step3():
    """Generate Step 3: Full Body Split View"""

    print(f"\n{'='*60}")
    print(f"STEP 3: FULL BODY SPLIT VIEW (FRONT + BACK)")
    print(f"{'='*60}")
    print(f"Model: {profile['model_name']}")
    print(f"\nUploading reference images for identity locking:")
    print(f"  - {FACE_REF_PATH}")
    print(f"  - {UPPER_REF_PATH}")
    print(f"\nGenerating split view with complete body specifications...")
    print(f"\nThis may take 90-120 seconds...\n")

    try:
        response = client.models.generate_content(
            model="gemini-3-pro-image-preview",
            contents=[face_ref, upper_ref, PROMPT],
            config=types.GenerateContentConfig(
                response_modalities=['IMAGE'],
                image_config=types.ImageConfig(
                    aspect_ratio="16:9",
                    image_size="2K"
                )
            )
        )

        # Save generated image
        for part in response.parts:
            if image := part.as_image():
                image.save(OUTPUT_PATH)
                print(f"✓ SUCCESS!")
                print(f"\nStep 3 complete: {OUTPUT_PATH}")
                print(f"\n{'='*60}")
                print(f"NEXT STEPS:")
                print(f"{'='*60}")
                print(f"1. Review the split view image: {OUTPUT_PATH}")
                print(f"2. Verify front view shows proportions correctly")
                print(f"3. Verify back view shows glutes as specified")
                print(f"4. Verify identity matches previous steps")
                print(f"5. If approved, proceed to Step 4 (face angles grid)")
                print(f"\n")
                return OUTPUT_PATH

        print("❌ Error: No image generated in response")
        return None

    except Exception as e:
        print(f"❌ Error generating image: {str(e)}")
        return None

if __name__ == "__main__":
    generate_step3()
