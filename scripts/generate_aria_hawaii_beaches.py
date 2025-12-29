from google import genai
from google.genai import types
from PIL import Image
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv('.env.local')
client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))

# Beach configurations
beaches = {
    'wailea_beach': {
        'name': 'Wailea Beach, Maui',
        'description': 'pristine golden sand beach, calm turquoise water, luxury resort setting, palm trees swaying, gentle waves, golden hour lighting, warm sunset glow',
        'mood': 'luxurious, elegant, serene'
    },
    'lanikai_beach': {
        'name': 'Lanikai Beach, Oahu',
        'description': 'crystal clear turquoise water, powder white sand, Mokulua Islands in background, morning light, vibrant blue sky, tropical paradise',
        'mood': 'vibrant, energetic, paradise vibes'
    },
    'hanalei_bay': {
        'name': 'Hanalei Bay, Kauai',
        'description': 'dramatic green mountains backdrop, crescent bay, lush tropical rainforest, pristine beach, adventure setting, cliffs in distance',
        'mood': 'adventurous, dramatic, wild beauty'
    },
    'black_sand_beach': {
        'name': 'Punaluu Black Sand Beach, Big Island',
        'description': 'volcanic black sand beach, tropical palm trees, green sea turtles, dramatic contrast, unique exotic setting, lush vegetation',
        'mood': 'edgy, dramatic, exotic'
    }
}

# LSU Bikini variations
bikini_styles = [
    "LSU purple and gold tiger stripe pattern bikini with black accents, athletic cut, high-waisted bottoms with gold chain details",
    "LSU gameday bikini, purple base with metallic gold accents, sporty elegant design, halter top",
    "LSU purple reign bikini with gold trim, luxe athletic wear, modern cut"
]

# Pose variations for the 3x3 grid
poses = [
    "walking along shoreline, water at ankles, looking back over shoulder with smile",
    "standing confidently facing camera, hand on hip, slight smile",
    "sitting on sand, legs extended, leaning back on hands, relaxed",
    "running through shallow water, creating splash, hair flowing",
    "lying on beach towel, propped up on elbows, looking at camera",
    "jumping in air with arms raised, celebrating, joyful mid-action",
    "looking over shoulder at camera, standing in shallow water",
    "playful pose touching hair, wind blown, natural candid moment",
    "kneeling in sand, confident pose, ocean in background"
]

def generate_single_image(beach_key, pose_idx, bikini_idx, aria_references, output_folder):
    """Generate a single image - keep Aria, swap background and outfit"""

    beach = beaches[beach_key]
    pose = poses[pose_idx]
    bikini = bikini_styles[bikini_idx]

    # Very explicit prompt about identity preservation
    prompt = f"""CRITICAL: These reference images show the SAME WOMAN from multiple angles. You MUST keep her EXACT identity.

KEEP IDENTICAL (DO NOT CHANGE):
- Her exact facial features (eyes, nose, mouth, face shape)
- Her exact eye color
- Her exact hair color and style (blonde with highlights)
- Her exact skin tone
- Her exact body type and physique
- Her facial structure and proportions

ONLY CHANGE:
- Background: {beach['name']} - {beach['description']}
- Outfit: {bikini}
- Pose: {pose}
- Lighting: {beach['mood']}

This is the SAME PERSON in a different location and outfit. Maintain 100% facial identity consistency. Professional beach photoshoot quality, natural lighting.

DO NOT create a different person. Use these reference images to understand her identity from all angles and PRESERVE IT EXACTLY."""

    try:
        response = client.models.generate_content(
            model="gemini-3-pro-image-preview",
            contents=aria_references + [prompt],
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
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"{beach_key}_pose{pose_idx+1}_bikini{bikini_idx+1}_{timestamp}.png"
                output_path = f"{output_folder}/{filename}"
                image.save(output_path)
                return output_path

        return None

    except Exception as e:
        print(f"    ✗ Error: {str(e)[:100]}")
        return None

def generate_beach_grid(beach_key, aria_references, output_folder='models/aria/hawaii_beaches'):
    """Generate 3 test images for a beach, one at a time"""

    os.makedirs(output_folder, exist_ok=True)
    beach = beaches[beach_key]

    print(f"\n{'='*60}")
    print(f"Generating {beach['name']} - 3 TEST images")
    print(f"{'='*60}\n")

    generated_images = []

    # Generate only 3 images to test identity consistency
    for i in range(3):
        pose_idx = i
        bikini_idx = i % 3

        print(f"  [{i+1}/3] Bikini {bikini_idx+1}, {poses[pose_idx][:40]}...")

        output_path = generate_single_image(beach_key, pose_idx, bikini_idx, aria_references, output_folder)

        if output_path:
            print(f"        ✓ {output_path.split('/')[-1]}")
            generated_images.append(output_path)
        else:
            print(f"        ✗ Failed")

    success = len(generated_images) > 0
    print(f"\n  {'✓' if success else '✗'} Generated {len(generated_images)}/3 images for {beach['name']}\n")

    return success

def generate_one_beach(beach_key='wailea_beach'):
    """Generate 3 test images for one beach"""

    print("\n" + "="*60)
    print("ARIA - LSU HAWAII BEACH PHOTOSHOOT (TEST)")
    print(f"Generating {beaches[beach_key]['name']}")
    print("="*60)

    # Load all Aria reference images for identity consistency
    print("\nLoading Aria's reference images...")
    aria_references = [
        Image.open('models/aria/base.jpeg'),
        Image.open('models/aria/face_variations/neutral.jpeg'),
        Image.open('models/aria/face_variations/smile_soft.jpeg'),
        Image.open('models/aria/face_variations/smile_teeth.jpeg'),
        Image.open('models/aria/face_variations/threequarter_left.jpeg'),
        Image.open('models/aria/face_variations/threequarter_right.jpeg')
    ]
    print(f"✓ Loaded {len(aria_references)} reference images")

    success = generate_beach_grid(beach_key, aria_references)

    print("\n" + "="*60)
    print("COMPLETE")
    print("="*60 + "\n")

    status = "✓" if success else "✗"
    print(f"{status} {beaches[beach_key]['name']}\n")

    return success

if __name__ == "__main__":
    # Change beach_key to: 'wailea_beach', 'lanikai_beach', 'hanalei_bay', or 'black_sand_beach'
    generate_one_beach('wailea_beach')
