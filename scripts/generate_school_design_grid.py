from google import genai
from google.genai import types
from PIL import Image
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv('.env.local')
client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))

# SEC Schools with colors and vibes
schools = {
    'ole_miss': {
        'name': 'Ole Miss',
        'colors': 'team colors',  # Let AI figure it out
        'vibe': 'Southern elegance, classic rebel style, sophisticated gameday'
    },
    'alabama': {
        'name': 'Alabama',
        'colors': 'team colors',
        'vibe': 'championship elegance, Southern tradition, dominant energy'
    },
    'lsu': {
        'name': 'LSU',
        'colors': 'team colors',
        'vibe': 'Saturday night lights, tiger fierce, Louisiana swagger'
    },
    'georgia': {
        'name': 'Georgia',
        'colors': 'team colors',
        'vibe': 'bulldog attitude, between the hedges, dominant'
    },
    'texas': {
        'name': 'Texas',
        'colors': 'team colors',
        'vibe': 'Longhorn pride, Texas bold, big state energy'
    },
    'florida': {
        'name': 'Florida',
        'colors': 'team colors',
        'vibe': 'swamp energy, gator tough, Florida sunshine'
    },
    'tennessee': {
        'name': 'Tennessee',
        'colors': 'team colors',
        'vibe': 'Rocky Top spirit, smokey mountain, Vol energy'
    },
    'auburn': {
        'name': 'Auburn',
        'colors': 'team colors',
        'vibe': 'war eagle spirit, tiger power, iron bowl ready'
    },
    'texas_am': {
        'name': 'Texas A&M',
        'colors': 'team colors',
        'vibe': '12th man spirit, Aggie pride, military tradition'
    },
    'oklahoma': {
        'name': 'Oklahoma',
        'colors': 'team colors',
        'vibe': 'Sooner magic, boomer spirit, championship swagger'
    },
    'arkansas': {
        'name': 'Arkansas',
        'colors': 'team colors',
        'vibe': 'razorback tough, hog call energy, SEC grit'
    },
    'kentucky': {
        'name': 'Kentucky',
        'colors': 'team colors',
        'vibe': 'wildcat fierce, bluegrass pride, Kentucky blue'
    },
    'south_carolina': {
        'name': 'South Carolina',
        'colors': 'team colors',
        'vibe': 'gamecock fighting spirit, sandstorm energy, Southern grit'
    },
    'missouri': {
        'name': 'Missouri',
        'colors': 'team colors',
        'vibe': 'tiger stripes, Mizzou pride, show-me state'
    },
    'mississippi_state': {
        'name': 'Mississippi State',
        'colors': 'team colors',
        'vibe': 'cowbell tradition, bulldog toughness, maroon pride'
    },
    'vanderbilt': {
        'name': 'Vanderbilt',
        'colors': 'team colors',
        'vibe': 'anchor strong, Nashville style, sophisticated'
    }
}

# Beach setting
beach_setting = {
    'location': 'Wailea Beach, Maui',
    'description': 'pristine golden sand beach, turquoise water, luxury resort setting, palm trees, golden hour lighting'
}

def generate_school_grid(school_key, model_name='savannah', output_folder='bikinis'):
    """Generate 2x5 grid: 5 different bikini designs, each shown front and back"""

    school = schools[school_key]
    school_folder = f"{output_folder}/SEC/{school['name'].replace(' ', '_')}"
    os.makedirs(school_folder, exist_ok=True)

    # Load model reference images
    print(f"\n{'='*60}")
    print(f"Loading {model_name}'s reference images...")
    print(f"{'='*60}")

    try:
        model_references = [
            Image.open(f'models/{model_name}/base.jpeg'),
            Image.open(f'models/{model_name}/face_variations/neutral.jpeg'),
            Image.open(f'models/{model_name}/face_variations/smile_soft.jpeg'),
            Image.open(f'models/{model_name}/face_variations/smile_teeth.jpeg'),
            Image.open(f'models/{model_name}/face_variations/threequarter_left.jpeg'),
            Image.open(f'models/{model_name}/face_variations/threequarter_right.jpeg')
        ]
        print(f"✓ Loaded {len(model_references)} reference images\n")
    except Exception as e:
        print(f"✗ Error loading model references: {e}")
        return None

    # Generate 2x5 grid with 5 unique bikini designs
    prompt = f"""CRITICAL: These reference images show the SAME WOMAN from multiple angles. You MUST keep her EXACT identity in ALL 10 panels.

KEEP IDENTICAL (DO NOT CHANGE):
- Her exact facial features (eyes, nose, mouth, face shape)
- Her exact eye color
- Her exact hair color and style
- Her exact skin tone
- Her exact body type and physique

=== GRID LAYOUT SPECIFICATION ===
Create a 2x5 grid (2 columns, 5 rows = 10 panels total) combined into ONE final image.
Thin white borders between panels. Each panel is a distinct photograph.

Layout:
Row 1: [Design 1 - Front View] [Design 1 - Back View]
Row 2: [Design 2 - Front View] [Design 2 - Back View]
Row 3: [Design 3 - Front View] [Design 3 - Back View]
Row 4: [Design 4 - Front View] [Design 4 - Back View]
Row 5: [Design 5 - Front View] [Design 5 - Back View]

=== SETTING FOR ALL PANELS ===
Location: {beach_setting['location']}
Background: {beach_setting['description']}
Same beach location for all 10 panels.
This is the SAME PERSON in 5 DIFFERENT bikini designs.

=== BIKINI DESIGN BRIEF ===
School: {school['name']}
Team Colors: Use {school['name']} {school['colors']} (you know what they are)
Style Vibe: {school['vibe']}

CREATE 5 COMPLETELY DIFFERENT gameday luxury bikini designs for {school['name']}.

Each design should:
- Use the school's team colors CREATIVELY
- Represent the school's vibe and spirit
- Be UNIQUE and DISTINCT from the other 4 designs
- Look like a premium sportswear brand designed it
- Be athletic luxury aesthetic - gameday ready but fashion-forward

DESIGN VARIETY - Make each of the 5 designs different:
- Design 1: Classic elegant interpretation
- Design 2: Bold athletic statement piece
- Design 3: Modern fashion-forward
- Design 4: Sophisticated luxury
- Design 5: Sporty chic

Use creative freedom to interpret team spirit through:
- Color patterns (stripes, color blocking, gradients, geometric)
- Materials look (metallic accents, chain details, modern cuts)
- Style variations (triangle tops, bandeau, halter, athletic crops, etc.)
- Different bottom styles (brazilian, cheeky, high-waist, tie-sides)

Make each design Instagram-worthy, professional beach photoshoot quality.

=== POSE SPECIFICATIONS ===

FRONT VIEW (Left column - Rows 1-5, left panels):
- Standing confidently facing camera
- Hand on hip or arms relaxed
- Full body visible head to below knees
- Clear view of bikini design from front
- Natural smile, beach vibes
- Golden hour lighting

BACK VIEW (Right column - Rows 1-5, right panels):
- Standing with back to camera
- Looking back over shoulder at camera
- Full body visible head to below knees
- Clear view of bikini design from back
- Same confident energy
- Shows complete back of bikini design
- Golden hour lighting

=== CONSISTENCY REQUIREMENTS ===
- SAME WOMAN (from reference images) in all 10 panels - no face changes
- SAME BEACH LOCATION in all 10 panels
- SAME LIGHTING (golden hour) in all 10 panels
- 5 DIFFERENT bikini designs (each shown front + back)
- Each row shows ONE design from front and back
- Professional beach catalog photography quality

=== TECHNICAL SPECS ===
- High resolution final image
- 2 columns × 5 rows layout
- Aspect ratio: Portrait (2:5 ratio)
- Thin white borders separating panels clearly
- Each panel is complete and distinct
- Each design should be clearly different from others
- Premium gameday bikini catalog quality

DO NOT use any trademarked logos, school names on clothing, or official mascots.
Use colors and vibes to represent the school spirit.

This is the SAME PERSON wearing 5 different {school['name']} gameday bikini designs."""

    try:
        print(f"{'='*60}")
        print(f"GENERATING: {school['name']} Bikini Design Grid")
        print(f"{'='*60}")
        print(f"Model: {model_name}")
        print(f"School: {school['name']}")
        print(f"Vibe: {school['vibe']}")
        print(f"Format: 2×5 grid (5 designs × 2 views)")
        print(f"{'='*60}\n")
        print("Calling Gemini API...\n")

        response = client.models.generate_content(
            model="gemini-3-pro-image-preview",
            contents=model_references + [prompt],
            config=types.GenerateContentConfig(
                response_modalities=['IMAGE'],
                image_config=types.ImageConfig(
                    aspect_ratio="9:16",
                    image_size="2K"
                )
            )
        )

        # Save generated grid
        for part in response.parts:
            if image := part.as_image():
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"{school_key}_designs_grid_{timestamp}.png"
                output_path = f"{school_folder}/{filename}"
                image.save(output_path)

                print(f"{'='*60}")
                print(f"✓ SUCCESS!")
                print(f"{'='*60}")
                print(f"Saved: {output_path}")
                print(f"\nGrid contains:")
                print(f"  5 different {school['name']} bikini designs")
                print(f"  Each shown from front and back views")
                print(f"  10 total panels (2×5 grid)")
                print(f"{'='*60}\n")

                return output_path

        print("✗ No image generated")
        return None

    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return None

def main(school_key='ole_miss', model_name='savannah'):
    """Generate bikini design grid for specified school"""

    if school_key not in schools:
        print(f"✗ Error: School '{school_key}' not found")
        print(f"Available schools: {', '.join(schools.keys())}")
        return

    print("\n" + "="*60)
    print(f"{schools[school_key]['name'].upper()} - BIKINI DESIGN GRID")
    print("="*60)
    print(f"Creating 5 unique designs for {schools[school_key]['name']}")
    print(f"Each design shown from front and back")
    print("="*60)

    output_path = generate_school_grid(school_key, model_name)

    if output_path:
        print(f"\n✓ Grid generation complete!")
        print(f"Review the designs and let me know which you like!")
    else:
        print(f"\n✗ Generation failed")

if __name__ == "__main__":
    # Generate grid for Ole Miss with Aria as model
    main(school_key='ole_miss', model_name='aria')
