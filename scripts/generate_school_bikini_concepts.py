from google import genai
from google.genai import types
from PIL import Image
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv('.env.local')
client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))

# School configurations with brand colors
schools = {
    'alabama': {
        'name': 'Alabama Crimson Tide',
        'colors': 'crimson red and white',
        'vibe': 'classic Southern elegance, championship energy'
    },
    'auburn': {
        'name': 'Auburn Tigers',
        'colors': 'burnt orange and navy blue',
        'vibe': 'bold tiger stripes, athletic power'
    },
    'georgia': {
        'name': 'Georgia Bulldogs',
        'colors': 'red and black',
        'vibe': 'fierce bulldog attitude, dominant energy'
    },
    'florida': {
        'name': 'Florida Gators',
        'colors': 'orange and blue',
        'vibe': 'swamp attitude, gator scales texture'
    },
    'texas': {
        'name': 'Texas Longhorns',
        'colors': 'burnt orange and white',
        'vibe': 'Texas pride, longhorn bold'
    },
    'ohio_state': {
        'name': 'Ohio State Buckeyes',
        'colors': 'scarlet red and gray',
        'vibe': 'block O, buckeye leaf accents'
    },
    'michigan': {
        'name': 'Michigan Wolverines',
        'colors': 'maize yellow and blue',
        'vibe': 'classic M, wolverine fierce'
    },
    'tennessee': {
        'name': 'Tennessee Volunteers',
        'colors': 'bright orange and white',
        'vibe': 'Smokey checkerboard pattern, Vol energy'
    },
    'clemson': {
        'name': 'Clemson Tigers',
        'colors': 'orange and purple',
        'vibe': 'tiger paw prints, championship swagger'
    },
    'usc': {
        'name': 'USC Trojans',
        'colors': 'cardinal red and gold',
        'vibe': 'Trojan warrior, LA luxury'
    }
}

# Beach setting for photoshoot
beach_setting = {
    'location': 'Wailea Beach, Maui',
    'description': 'pristine golden sand beach, calm turquoise water, luxury resort setting, palm trees, golden hour lighting'
}

# Pose variations
poses = [
    "standing confidently facing camera, hand on hip",
    "walking along shoreline, looking back over shoulder",
    "sitting on sand, legs extended, relaxed pose"
]

def generate_school_bikini(school_key, pose_idx, aria_references, output_folder='bikinis'):
    """Generate bikini design concept for a specific school"""

    school = schools[school_key]
    pose = poses[pose_idx]

    school_folder = f"{output_folder}/{school['name'].replace(' ', '_')}"
    os.makedirs(school_folder, exist_ok=True)

    # Prompt to generate new bikini design concepts
    prompt = f"""CRITICAL: These reference images show the SAME WOMAN from multiple angles. You MUST keep her EXACT identity.

KEEP IDENTICAL (DO NOT CHANGE):
- Her exact facial features (eyes, nose, mouth, face shape)
- Her exact eye color
- Her exact hair color and style (blonde with highlights)
- Her exact skin tone
- Her exact body type and physique

ONLY CHANGE:
- Background: {beach_setting['location']} - {beach_setting['description']}
- Outfit: Create a NEW ORIGINAL {school['name']} gameday luxury bikini design
- Pose: {pose}

BIKINI DESIGN BRIEF:
School: {school['name']}
Colors: {school['colors']}
Style Vibe: {school['vibe']}

Design a stylish, athletic luxury bikini that represents {school['name']}. Use {school['colors']} creatively. Can include:
- Team color patterns (stripes, color blocking, gradients)
- Subtle logo placements
- Athletic luxury aesthetic
- Gameday ready but fashion-forward
- High-quality materials look (metallic accents, chain details, modern cuts)

Make it look like a premium sportswear brand designed a gameday bikini. Instagram-worthy, professional beach photoshoot quality.

This is the SAME PERSON in a different outfit. Maintain 100% facial identity consistency."""

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
                filename = f"{school_key}_concept_pose{pose_idx+1}_{timestamp}.png"
                output_path = f"{school_folder}/{filename}"
                image.save(output_path)
                return output_path

        return None

    except Exception as e:
        print(f"    ✗ Error: {str(e)[:100]}")
        return None

def generate_all_schools(num_poses=3):
    """Generate bikini concepts for all schools"""

    print("\n" + "="*60)
    print("ARIA - COLLEGE GAMEDAY BIKINI COLLECTION")
    print(f"{len(schools)} Schools × {num_poses} Designs Each")
    print("="*60)

    # Load Aria reference images
    print("\nLoading Aria's reference images...")
    aria_references = [
        Image.open('models/aria/base.jpeg'),
        Image.open('models/aria/face_variations/neutral.jpeg'),
        Image.open('models/aria/face_variations/smile_soft.jpeg'),
        Image.open('models/aria/face_variations/smile_teeth.jpeg'),
        Image.open('models/aria/face_variations/threequarter_left.jpeg'),
        Image.open('models/aria/face_variations/threequarter_right.jpeg')
    ]
    print(f"✓ Loaded {len(aria_references)} reference images\n")

    results = {}

    for school_key, school_info in schools.items():
        print(f"\n{'='*60}")
        print(f"{school_info['name']}")
        print(f"Colors: {school_info['colors']}")
        print(f"{'='*60}\n")

        school_results = []

        for pose_idx in range(num_poses):
            print(f"  [{pose_idx+1}/{num_poses}] {poses[pose_idx][:50]}...")

            output_path = generate_school_bikini(school_key, pose_idx, aria_references)

            if output_path:
                print(f"        ✓ {output_path.split('/')[-1]}")
                school_results.append(output_path)
            else:
                print(f"        ✗ Failed")

        results[school_key] = school_results
        print(f"\n  ✓ Generated {len(school_results)}/{num_poses} for {school_info['name']}")

    print("\n" + "="*60)
    print("GENERATION COMPLETE")
    print("="*60 + "\n")

    for school_key, paths in results.items():
        school_name = schools[school_key]['name']
        print(f"✓ {school_name}: {len(paths)} designs")

    total = sum(len(p) for p in results.values())
    print(f"\nTotal: {total} bikini design concepts generated\n")

    return results

if __name__ == "__main__":
    # Generate 3 designs per school for all 10 schools = 30 total designs
    generate_all_schools(num_poses=3)
