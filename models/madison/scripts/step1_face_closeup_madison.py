#!/usr/bin/env python3
"""
STEP 1: Face Close-Up Portrait (Madison)
Generate detailed face reference with natural skin texture for identity locking
"""

from google import genai
from google.genai import types
import os
import json
from dotenv import load_dotenv

load_dotenv('.env.local')
client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))

MODEL_NAME = "madison"
PROFILE_PATH = f"models/{MODEL_NAME}/profile_v1.json"
OUTPUT_PATH = f"models/{MODEL_NAME}/01_face.jpeg"

# Load profile
with open(PROFILE_PATH, 'r') as f:
    profile = json.load(f)

# Build prompt from profile specifications
PROMPT = f"""Generate a photorealistic close-up portrait of a beautiful young woman.

This is {profile['model_name']}, age {profile['age']}, {profile['ethnicity']}.

=== FACE SPECIFICATIONS ===

{{
  "face": {{
    "shape": "{profile['face']['shape']}",

    "eyes": {{
      "color": "{profile['face']['eyes']['color']}",
      "shape": "{profile['face']['eyes']['shape']}",
      "size": "{profile['face']['eyes']['size']}",
      "detail": "expressive, warm, engaging with camera"
    }},

    "nose": {{
      "shape": "{profile['face']['nose']['shape']}",
      "size": "{profile['face']['nose']['size']}"
    }},

    "lips": {{
      "fullness": "{profile['face']['lips']['fullness']}",
      "shape": "{profile['face']['lips']['shape']}",
      "color": "{profile['face']['lips']['color']}",
      "expression": "soft, natural, slightly parted"
    }},

    "face_structure": {{
      "cheekbones": "{profile['face']['face_structure']['cheekbones']}",
      "jawline": "{profile['face']['face_structure']['jawline']}",
      "chin": "{profile['face']['face_structure']['chin']}"
    }},

    "skin": {{
      "tone": "{profile['face']['skin']['tone']}",
      "texture": "CRITICAL REQUIREMENT: {profile['face']['skin']['texture']}",
      "detail": "natural imperfections, real human skin, NO beauty filter"
    }}
  }},

  "hair": {{
    "color": "{profile['hair']['color']}",
    "length": "{profile['hair']['length']}",
    "texture": "{profile['hair']['texture']}",
    "style": "loose and natural, flowing, face-framing"
  }},

  "expression": {{
    "mood": "warm and genuine",
    "smile": "soft natural smile with warmth in eyes",
    "energy": "confident but approachable, engaging"
  }},

  "framing": {{
    "shot_type": "close-up portrait",
    "composition": "from upper chest/neck to top of head",
    "angle": "STRAIGHT HEAD-ON, no tilt, directly facing camera",
    "focus": "face is the complete focus, sharp and detailed"
  }},

  "lighting": {{
    "quality": "natural soft daylight, golden hour warmth",
    "direction": "soft front lighting with gentle shadows",
    "mood": "warm, flattering, natural"
  }},

  "background": {{
    "setting": "neutral outdoor setting",
    "detail": "soft blur, not distracting",
    "atmosphere": "natural, peaceful, beach or park vibes"
  }},

  "outfit": {{
    "type": "simple casual top",
    "color": "white tank top or simple tee",
    "note": "outfit is NOT the focus, just shoulders visible"
  }},

  "meta": {{
    "aspect_ratio": "2:3",
    "quality": "ultra_photorealistic",
    "resolution": "8k",
    "camera": "professional portrait photography, 50mm lens equivalent",
    "style": "natural beauty portrait, no fashion photography artifice"
  }}
}}

=== CRITICAL REALISM CONSTRAINTS ===

SKIN TEXTURE (MOST IMPORTANT):
- Natural skin texture with VISIBLE PORES
- Slight imperfections are REQUIRED (natural human characteristics)
- NO beauty filter applied - this is CRITICAL
- NO AI smoothing or perfection
- NO glowing skin effect
- NO artificial airbrushing
- Realistic lighting behavior on skin with natural shadows
- Real human skin, not magazine-perfect

FACIAL REALISM:
- Natural asymmetry (humans are not perfectly symmetrical)
- Real human proportions (not exaggerated or stylized)
- Genuine expression (not forced or artificial)
- Eyes have depth and life (not flat or doll-like)
- Natural eye whites with slight imperfections
- Realistic hair with individual strands visible

LIGHTING REALISM:
- Natural shadows under nose, chin, eye sockets
- Realistic contrast (not flat, not overexposed)
- Natural color temperature (warm daylight)
- No artificial ring lights or studio perfection

=== WHAT THIS IS FOR ===

This is a reference image for future content generation. It must capture her EXACT facial identity with all natural characteristics preserved. This face will be used as a reference to maintain consistency across all future images of {profile['model_name']}.

=== FINAL REMINDER ===

Generate a stunning but REALISTIC portrait. Natural beauty means NATURAL - visible pores, slight imperfections, real human skin. No beauty filter. This is not a glamour magazine shot, it's a reference photo that captures her true appearance.

Beautiful, yes. Perfect, no. Real human, absolutely.
"""

def generate_step1():
    """Generate Step 1: Face Close-Up"""

    print(f"\n{'='*60}")
    print(f"STEP 1: FACE CLOSE-UP PORTRAIT")
    print(f"{'='*60}")
    print(f"Model: {profile['model_name']}")
    print(f"Age: {profile['age']}")
    print(f"\nKey Features:")
    print(f"  - Eyes: {profile['face']['eyes']['color']}, {profile['face']['eyes']['shape']}")
    print(f"  - Face: {profile['face']['shape']}")
    print(f"  - Hair: {profile['hair']['color']}, {profile['hair']['length']}")
    print(f"  - Skin: {profile['face']['skin']['tone']}")
    print(f"\nGenerating face close-up...")
    print(f"Using Gemini Pro (gemini-3-pro-image-preview)")
    print(f"\nThis may take 60-90 seconds...\n")

    try:
        response = client.models.generate_content(
            model="gemini-3-pro-image-preview",
            contents=PROMPT,
            config=types.GenerateContentConfig(
                response_modalities=['IMAGE'],
                image_config=types.ImageConfig(
                    aspect_ratio="2:3",
                    image_size="2K"
                )
            )
        )

        # Save generated image
        for part in response.parts:
            if image := part.as_image():
                image.save(OUTPUT_PATH)
                print(f"✓ SUCCESS!")
                print(f"\nStep 1 complete: {OUTPUT_PATH}")
                print(f"\n{'='*60}")
                print(f"REVIEW CHECKLIST:")
                print(f"{'='*60}")
                print(f"Verify the generated face matches profile specs:")
                print(f"  ✓ Eye color: {profile['face']['eyes']['color']}")
                print(f"  ✓ Face shape: {profile['face']['shape']}")
                print(f"  ✓ Hair color: {profile['hair']['color']}")
                print(f"  ✓ Natural skin texture (pores visible, no filter)")
                print(f"  ✓ Straight-on angle")
                print(f"  ✓ Overall vibe matches design")
                print(f"\nIf approved, proceed to Step 2 (upper body)")
                print(f"\n")
                return OUTPUT_PATH

        print("❌ Error: No image generated in response")
        return None

    except Exception as e:
        print(f"❌ Error generating image: {str(e)}")
        return None

if __name__ == "__main__":
    generate_step1()
