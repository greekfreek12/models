#!/usr/bin/env python3
"""
Generate 2x2 grids (4 faces each) for testing
Usage: python generate_grid.py 1  (for batch 1)
       python generate_grid.py 2  (for batch 2)
"""

from google import genai
from google.genai import types
import os
import json
from dotenv import load_dotenv
import sys

load_dotenv('../.env.local')
client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))

# Get batch number from command line
if len(sys.argv) != 2:
    print("Usage: python generate_grid.py <batch_number>")
    print("Example: python generate_grid.py 1")
    sys.exit(1)

batch_num = sys.argv[1]
batch_file = f"faces_batch{batch_num}.json"

# Load face specs
with open(batch_file, 'r') as f:
    models = json.load(f)

# Build panel descriptions with full detail
panel_descriptions = []
for i, model in enumerate(models):
    panel_num = i + 1
    face = model['face']
    hair = model['hair']

    panel_desc = f"""
PANEL {panel_num} - {model['model_name'].upper()} - AGE {model['age']}:

FACE STRUCTURE:
- Face shape: {face['shape']}
- Cheekbones: {face['face_structure']['cheekbones']}
- Jawline: {face['face_structure']['jawline']}
- Chin: {face['face_structure']['chin']}

EYES (CRITICAL):
- Color: {face['eyes']['color']}
- Shape: {face['eyes']['shape']}
- Size: {face['eyes']['size']}

NOSE:
- Shape: {face['nose']['shape']}
- Size: {face['nose']['size']}

LIPS:
- Fullness: {face['lips']['fullness']}
- Shape: {face['lips']['shape']}
- Color: {face['lips']['color']}

HAIR:
- Color: {hair['color']}
- Length: {hair['length']}
- Texture: {hair['texture']}

SKIN (CRITICAL):
- Tone: {face['skin']['tone']}
- Texture: {face['skin']['texture']}

VIBE: {model['vibe']}
"""
    panel_descriptions.append(panel_desc)

PROMPT = f"""Generate a 2x2 GRID (4 panels) showing 4 DIFFERENT YOUNG WOMEN.

=== CRITICAL REQUIREMENTS - READ FIRST ===

TOP 3 MOST IMPORTANT THINGS:

1. VISIBLE PORES (ABSOLUTELY CRITICAL):
   - You MUST be able to SEE individual pores on every face
   - Natural skin texture throughout - NOT smooth or filtered
   - Real human skin with slight imperfections
   - NO AI smoothing, NO beauty filter whatsoever
   - This is MANDATORY - if skin looks too smooth, you FAILED

2. DEEP GOLDEN TAN (CRITICAL):
   - Medium to DEEP golden tan on all faces
   - NOT light, NOT fair, NOT pale
   - Sun-kissed warm tan throughout
   - Year-round beach tan appearance

3. NATURAL OUTDOOR LIGHTING (CRITICAL):
   - Natural daylight, NOT studio lighting
   - Slightly imperfect lighting, real photography feel
   - Soft natural shadows, outdoor portrait style

=== GRID LAYOUT - 2x2 (4 FACES) ===

Row 1: Panel 1 (Top Left), Panel 2 (Top Right)
Row 2: Panel 3 (Bottom Left), Panel 4 (Bottom Right)

Create ONE image with 4 equally-sized panels in a 2x2 grid.

=== DETAILED SPECIFICATIONS FOR EACH PANEL ===

{''.join(panel_descriptions)}

=== CAMERA & FRAMING (ALL PANELS) ===

- 85mm portrait lens at f/1.8
- Eye level, straight on
- FROM NECK UP TO TOP OF HEAD ONLY
- Face centered in frame
- Looking directly at camera
- Sweet genuine smile (not sultry)
- Warm friendly expression
- Thin white borders between panels

=== AESTHETIC - SWEET YOUTHFUL BEAUTY ===

These are YOUNG (age 20-21) women with:
- Sweet innocent expression (NOT sultry or seductive)
- Soft youthful baby-faced features
- Warm approachable girl-next-door charm
- Natural genuine smile, bright friendly eyes
- Fresh-faced natural beauty
- Think: college girl, cheerleader, sorority sister
- NOT: Model-intense, dramatic, mature, or sultry

=== MAKEUP & STYLING ===

- MINIMAL natural makeup only
- Dewy fresh skin (not matte)
- Nude or soft pink lip gloss
- Natural rosy cheeks
- Light mascara only
- Fresh college girl look
- NO heavy makeup, NO contouring

=== SKIN TEXTURE - MOST IMPORTANT ===

I cannot emphasize this enough:
- VISIBLE PORES throughout the entire face
- Natural skin texture is MANDATORY
- You should see individual pores on inspection
- Slight imperfections, beauty marks, natural variations
- Real human skin behavior with lighting
- NOT perfect, NOT smoothed, NOT filtered
- NO beauty filter applied
- NO AI smoothing or perfection
- Must look like REAL photography of REAL skin

Think: Natural outdoor portrait of a real person
NOT: Magazine cover with beauty filter

If the skin looks too smooth or perfect, YOU HAVE FAILED.

=== WHAT TO ABSOLUTELY AVOID ===

- NO mature or older-looking faces
- NO sultry, seductive, or intense expressions
- NO heavy makeup or contouring
- NO sharp or overly dramatic features
- NO beauty filter or skin smoothing
- NO model-like striking dramatic features
- NO perfect studio lighting
- NO AI-smooth perfect skin
- NO fair or pale skin

=== TECHNICAL SPECIFICATIONS ===

- 16:9 aspect ratio for 2x2 grid
- High resolution (2K)
- 2x2 grid with thin white borders
- 4 different women, each unique
- Each panel equally sized
- Professional but natural photography

=== FINAL CRITICAL REMINDER ===

MANDATORY REQUIREMENTS for ALL 4 faces:

1. VISIBLE PORES - see individual pores (MOST IMPORTANT)
2. DEEP GOLDEN TAN - medium to deep throughout (CRITICAL)
3. NATURAL OUTDOOR LIGHTING - not studio perfect (CRITICAL)
4. Age 20-21 - soft youthful baby-faced features
5. Sweet innocent vibe - warm genuine smiles
6. Large expressive eyes as specified
7. Natural proportionate lips as specified
8. Detailed face structure as specified

The visible pores and natural skin texture is THE #1 requirement.
Do NOT generate smooth perfect skin.
It MUST have visible natural pores and texture.

Generate 4 beautiful young women matching these exact specifications.
"""

print(f"\n{'='*60}")
print(f"GENERATING BATCH {batch_num} - 2x2 GRID (4 FACES)")
print(f"{'='*60}")
print(f"Models: {', '.join([m['model_name'] for m in models])}")
print(f"\nCRITICAL REQUIREMENTS:")
print(f"  1. Visible pores (MOST IMPORTANT)")
print(f"  2. Deep golden tan")
print(f"  3. Natural outdoor lighting")
print(f"  4. Age 20-21, soft youthful features")
print(f"  5. Sweet innocent Southern Belle vibe")
print(f"\nUsing Madison-level detailed specifications")
print(f"Generating...")
print(f"This may take 60-90 seconds...\n")

output_path = f"grid_batch{batch_num}.png"

try:
    response = client.models.generate_content(
        model="gemini-3-pro-image-preview",
        contents=PROMPT,
        config=types.GenerateContentConfig(
            response_modalities=['IMAGE'],
            image_config=types.ImageConfig(
                aspect_ratio="16:9",
                image_size="2K"
            )
        )
    )

    # Save generated grid
    for part in response.parts:
        if image := part.as_image():
            image.save(output_path)
            print(f"✓ SUCCESS!")
            print(f"\nGrid saved: {output_path}")
            print(f"\n{'='*60}")
            print(f"REVIEW BATCH {batch_num}:")
            print(f"{'='*60}")
            print(f"Check for:")
            print(f"  - Visible pores and natural skin texture")
            print(f"  - Deep golden tan (not light/fair)")
            print(f"  - Natural outdoor lighting (not studio)")
            print(f"  - Soft youthful sweet faces (age 20-21)")
            print(f"  - Large expressive eyes as specified")
            print(f"  - Natural proportionate features")
            print(f"\nTell me which ones you like!\n")
            break
    else:
        print("❌ Error: No image generated in response")

except Exception as e:
    print(f"❌ Error generating image: {str(e)}")
