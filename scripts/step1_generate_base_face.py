#!/usr/bin/env python3
"""
STEP 1: Generate Base Face Portrait (Chest Up)
Creates the initial face reference with detailed facial features
"""

from google import genai
from google.genai import types
from PIL import Image
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv('.env.local')
client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))

# Model configuration
MODEL_NAME = "savannah"
MODEL_AGE = "22"
OUTPUT_DIR = f"models/{MODEL_NAME}"

# Create output directory
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Step 1 Prompt: Base Face Portrait (Chest Up)
PROMPT = """Generate a photorealistic portrait of a young woman. This will be used as a base reference for identity consistency.

{
  "meta": {
    "aspect_ratio": "2:3",
    "quality": "ultra_photorealistic",
    "resolution": "8k",
    "camera": "iPhone 15 Pro Max",
    "lens": "35mm portrait",
    "style": "natural social media realism, soft natural beauty"
  },

  "scene": {
    "location": "outdoor natural setting, soft background blur",
    "environment": [
      "neutral natural background",
      "soft bokeh effect",
      "daylight setting",
      "clean simple composition"
    ],
    "time": "late afternoon golden hour"
  },

  "lighting": {
    "type": "natural soft daylight",
    "key_light": "soft diffused sunlight from side",
    "fill_light": "natural ambient light",
    "effect": "realistic skin tones, soft shadows, no harsh highlights",
    "constraints": [
      "no artificial glow on skin",
      "no beauty filter effect",
      "no cinematic face bloom",
      "light falls naturally on face"
    ]
  },

  "camera_perspective": {
    "shot_type": "portrait, chest up",
    "angle": "STRAIGHT HEAD-ON, direct face-forward, eye level",
    "framing": "from chest to top of head, perfectly centered, symmetrical",
    "distance": "2-3 meters for natural perspective",
    "focus": "sharp focus on face, soft background blur",
    "requirements": "FACE MUST BE DIRECTLY FACING CAMERA, NO TILT, NO ANGLE"
  },

  "subject": {
    "name": "Savannah",
    "gender": "female",
    "age": "22 years old (clearly adult)",
    "ethnicity": "American, Caucasian with sun-kissed complexion",

    "face": {
      "shape": "soft oval with gentle cheekbones",
      "eyes": {
        "color": "bright blue-green hazel eyes",
        "shape": "almond shaped, natural size",
        "expression": "warm, friendly, approachable gaze",
        "detail": "natural eye reflections, no exaggerated sparkle"
      },
      "nose": "straight, proportionate, refined but natural",
      "lips": {
        "shape": "full natural lips, soft cupid's bow",
        "color": "natural pink tone",
        "detail": "no heavy lipstick, natural texture"
      },
      "expression": "gentle natural smile, relaxed and friendly",
      "makeup": {
        "level": "minimal natural makeup",
        "details": "light mascara, natural brows, soft pink lip gloss, no heavy contouring",
        "style": "fresh-faced girl next door"
      },
      "skin": {
        "tone": "fair to light with golden sun-kissed glow",
        "texture": "natural skin texture visible, pores visible on close inspection, slight imperfections",
        "detail": "no beauty filter, no airbrushing, no artificial smoothing",
        "characteristics": "healthy natural glow, real human skin"
      }
    },

    "hair": {
      "color": "blonde with natural highlights, golden tones",
      "length": "long, flowing past shoulders",
      "style": "loose natural waves, beachy texture",
      "detail": "windswept natural movement, sun-lightened strands",
      "behavior": "soft movement, natural fall"
    },

    "body": {
      "visible_area": "chest and upper torso",
      "build": "athletic but feminine, naturally fit",
      "shoulders": "relaxed, natural posture",
      "chest": "natural proportions, clearly visible in frame",
      "skin_tone": "consistent golden tan, natural sun exposure"
    },

    "pose": {
      "posture": "relaxed natural standing pose",
      "shoulders": "square to camera, straight on",
      "head_position": "DIRECTLY facing camera, NO tilt, perfectly straight",
      "expression": "warm approachable smile, confident but not posed",
      "energy": "natural, friendly, girl-next-door charm",
      "critical": "HEAD-ON SHOT FOR IDENTITY LOCKING - face must be straight forward"
    },

    "outfit": {
      "type": "simple casual summer top",
      "style": "light cotton tank top or simple tee",
      "color": "white or soft neutral tone",
      "fit": "casual relaxed fit",
      "detail": "minimal styling, natural everyday look"
    },

    "signature_details": {
      "tattoos": [
        "small delicate wave line on inner left wrist",
        "tiny outline star behind right ear (barely visible)",
        "small botanical/floral piece on right ribcage (not visible in this shot)"
      ],
      "accessories": {
        "necklace": "thin gold chain with small pendant, always worn",
        "earrings": "small gold hoops or studs",
        "rings": "thin stacked rings on right hand"
      },
      "note": "These are subtle, tasteful details that add character without overpowering her natural look"
    }
  },

  "realism_constraints": [
    "no beauty filter",
    "no face perfection or AI smoothing",
    "no cinematic grading",
    "no glowing skin effect",
    "visible pores and natural skin texture",
    "slight asymmetry in features (real human)",
    "natural proportions throughout",
    "realistic lighting behavior on skin",
    "no artificial highlights or glow"
  ],

  "overall_vibe": "Natural American girl-next-door beauty. Approachable, warm, fresh-faced. The kind of girl you'd see at the beach or coffee shop. Real, relatable, naturally beautiful."
}

TECHNICAL REQUIREMENTS:
- This is a BASE REFERENCE image for identity consistency
- Capture clear facial features for future identity locking
- Natural skin texture with visible pores is CRITICAL
- No filters, no artificial beauty enhancement
- Professional quality but natural realism
"""

def generate_base_face():
    """Generate the base face portrait"""

    print(f"Generating base face portrait for {MODEL_NAME}...")
    print(f"Age: {MODEL_AGE}")
    print("Style: Natural blonde girl-next-door")
    print("\nThis may take 30-60 seconds...\n")

    try:
        response = client.models.generate_content(
            model="gemini-3-pro-image-preview",
            contents=[PROMPT],
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
                output_path = f"{OUTPUT_DIR}/base_face.jpeg"
                image.save(output_path)
                print(f"✓ Base face portrait saved: {output_path}")
                print(f"\nNext steps:")
                print(f"1. Review the image at: {output_path}")
                print(f"2. If approved, run Step 2 to generate full body")
                return output_path

        print("Error: No image generated in response")
        return None

    except Exception as e:
        print(f"Error generating image: {str(e)}")
        return None

if __name__ == "__main__":
    generate_base_face()
