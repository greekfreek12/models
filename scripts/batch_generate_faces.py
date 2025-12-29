#!/usr/bin/env python3
"""
BATCH FACE GENERATION
Generate Step 1 (face closeup) for multiple models at once
"""

from google import genai
from google.genai import types
import os
import json
from dotenv import load_dotenv
import time

load_dotenv('.env.local')
client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))

# Load batch config (hot blondes and brunettes)
with open('scripts/batch_hot_blondes_brunettes.json', 'r') as f:
    models = json.load(f)

def generate_face(model_config):
    """Generate Step 1 face for one model"""

    name = model_config['model_name'].lower()
    model_dir = f"models/{name}"

    # Create model directory
    os.makedirs(model_dir, exist_ok=True)

    # Build prompt balancing beauty and realism
    prompt = f"""Professional headshot portrait of a beautiful young woman - attractive but realistic.

THE WOMAN - {model_config['model_name']}:
Age {model_config['age']}, {model_config['ethnicity']}
Vibe: {model_config['vibe']}

FACE:
- Face structure: {model_config['face_shape']}
- Eyes: {model_config['eye_color']}, {model_config['eye_shape']} - striking and captivating
- Lips: {model_config['lip_description']} - natural fullness
- Hair: {model_config['hair_color']}, {model_config['hair_length']}, {model_config['hair_texture']}
- Skin: {model_config['skin_tone']}

BEAUTY LEVEL:
- Attractive, model-like features but natural
- Large expressive eyes
- Full natural lips (not exaggerated)
- Defined cheekbones and bone structure
- Overall beautiful but realistic

SKIN TEXTURE (CRITICAL):
- Natural skin texture with VISIBLE PORES
- Slight imperfections are present (natural beauty marks, subtle texture)
- Real human skin, NOT AI-smoothed
- NO beauty filter applied
- NO artificial smoothing or perfection
- Natural lighting shows realistic skin texture
- This is a real person, not magazine-perfect

CAMERA & FRAMING:
- 85mm portrait lens at f/1.8
- Eye level, straight on, 3-4 feet distance
- FROM NECK UP TO TOP OF HEAD ONLY
- Head fills frame, face centered
- Looking directly at camera with warm genuine smile

LIGHTING & STYLE:
- Natural golden hour daylight, soft and flattering
- Soft blur background
- 2:3 vertical portrait
- Minimal natural makeup
- Simple casual top (not the focus)

REALISM REQUIREMENTS:
- Photorealistic with natural imperfections
- Beautiful but believable as a real person
- Natural skin texture throughout
- Balance between attractive and realistic

Create a beautiful headshot that looks like a real attractive woman, not an AI-generated perfect face.
"""

    output_path = f"{model_dir}/01_face.jpeg"

    print(f"\n{'='*60}")
    print(f"Generating: {model_config['model_name']}")
    print(f"{'='*60}")
    print(f"  {model_config['ethnicity']}")
    print(f"  {model_config['eye_color']} eyes, {model_config['hair_color']} hair")
    print(f"  {model_config['skin_tone']}")
    print(f"  Vibe: {model_config['vibe']}")

    try:
        response = client.models.generate_content(
            model="gemini-3-pro-image-preview",
            contents=prompt,
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
                image.save(output_path)
                print(f"  ✓ SUCCESS: {output_path}")

                # Save minimal profile
                profile_path = f"{model_dir}/profile.json"
                with open(profile_path, 'w') as f:
                    json.dump(model_config, f, indent=2)

                return True

        print(f"  ❌ ERROR: No image generated")
        return False

    except Exception as e:
        print(f"  ❌ ERROR: {str(e)}")
        return False

def main():
    """Generate all faces in batch"""

    print(f"\n{'='*60}")
    print(f"BATCH FACE GENERATION")
    print(f"{'='*60}")
    print(f"Total models: {len(models)}")
    print(f"Starting batch generation...")
    print(f"This will take approximately {len(models) * 2} minutes")
    print(f"{'='*60}\n")

    successful = []
    failed = []

    for i, model in enumerate(models):
        print(f"\n[{i+1}/{len(models)}] Processing {model['model_name']}...")

        if generate_face(model):
            successful.append(model['model_name'])
        else:
            failed.append(model['model_name'])

        # Brief pause between generations to avoid rate limits
        if i < len(models) - 1:
            print("  Waiting 3 seconds...")
            time.sleep(3)

    # Summary
    print(f"\n\n{'='*60}")
    print(f"BATCH GENERATION COMPLETE")
    print(f"{'='*60}")
    print(f"Successful: {len(successful)}/{len(models)}")
    print(f"Failed: {len(failed)}/{len(models)}")

    if successful:
        print(f"\n✓ SUCCESSFUL MODELS:")
        for name in successful:
            print(f"  - {name}: models/{name.lower()}/01_face.jpeg")

    if failed:
        print(f"\n❌ FAILED MODELS:")
        for name in failed:
            print(f"  - {name}")

    print(f"\n{'='*60}")
    print(f"NEXT STEPS:")
    print(f"{'='*60}")
    print(f"1. Review all generated faces in models/*/01_face.jpeg")
    print(f"2. Decide which models to keep")
    print(f"3. For approved models, complete Steps 2-3")
    print(f"4. Ready for content generation!")
    print(f"\n")

if __name__ == "__main__":
    main()
