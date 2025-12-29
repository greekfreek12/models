#!/usr/bin/env python3
"""
Generate Veronica Greek Island Grid (3x3 - 9 poses)
Using Gemini 3 Pro with multiple identity references
"""

from google import genai
from google.genai import types
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv('.env.local')
client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))

# Reference images
BIKINI_REF = Path("bikinis/universal/GameDay_Luxe/teams/Alabama_Crimson_White.jpg")
VERONICA_BASE = Path("models_2.0/veronica/base.jpeg")
VERONICA_FACE_GRID = Path("models_2.0/veronica/face_grid_2x3.png")
OUTPUT_PATH = Path("models_2.0/veronica/greek_island_grid_3x3.png")

# Ensure output directory exists
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

GRID_PROMPT = """Generate a 3x3 GRID (9 panels) showing the SAME WOMAN in different poses across Greek islands.

=== CRITICAL REFERENCE USAGE ===

REFERENCE IMAGE 1 (Bikini Design ONLY):
This image is ONLY for extracting the BIKINI DESIGN.
- Extract ONLY the bikini: Crimson red triangle top with white trim, crimson red bottoms with white trim
- DO NOT use this person's face, body, or identity
- ONLY use the bikini pattern and design
- Apply this bikini to the woman from Reference Images 2 & 3

REFERENCE IMAGE 2 (Body/Identity):
This shows the woman's body proportions and identity.
- Use for body proportions: athletic hourglass, bust size, waist-hip ratio, glutes
- Use for overall body structure and build
- This is the PRIMARY IDENTITY reference

REFERENCE IMAGE 3 (Face Angles):
This shows the same woman's face from multiple angles.
- Use for facial identity consistency
- Shows different expressions and angles
- Same person as Reference Image 2

CRITICAL: The woman in References 2 & 3 is THE SAME PERSON who appears in all 9 panels.
DO NOT use the face or body from Reference 1 (bikini image).
ONLY extract the bikini design from Reference 1.

=== GRID LAYOUT - 3x3 (9 PANELS) ===

Create ONE square image with 9 panels arranged in 3 rows and 3 columns.
Thin white borders separating each panel.
Each panel is a distinct photograph at a different Greek location.

=== IDENTITY REQUIREMENTS (CRITICAL) ===

SAME WOMAN in all 9 panels:
- Face from References 2 & 3 (preserved exactly)
- Body proportions from Reference 2 (athletic hourglass)
- DO NOT change her face, features, eye color, hair, or body between panels
- ONLY the pose, angle, and location change
- 100% identity consistency across all 9 panels

BIKINI (from Reference 1):
- Crimson red triangle bikini top with white trim
- Crimson red bikini bottoms with white trim
- Same bikini in all 9 panels
- Alabama team colors (crimson and white)

=== THE 9 GREEK ISLAND PANELS ===

PANEL 1 - SANTORINI (Oia Sunset):
VIEW: Front 3/4 view
SCENE: Leaning against white stucco wall with blue trim, iconic Santorini architecture
BACKGROUND: Blue-domed churches, pink sunset sky, caldera view
POSE: One hand on hip, looking at camera, warm smile, relaxed confident stance
LIGHTING: Golden hour warm orange/pink sunset light
MOOD: Romantic, dreamy, classic Greek island

PANEL 2 - MYKONOS (Windmills):
VIEW: Full body front view
SCENE: Standing in front of famous white windmills with straw roofs
BACKGROUND: Row of Kato Mili windmills, bright blue sky, view of town below
POSE: Standing straight, both hands in hair (casual windblown look), smiling
LIGHTING: Bright afternoon sunlight, windy conditions
MOOD: Iconic landmark, Instagram-worthy, cheerful

PANEL 3 - ZAKYNTHOS (Navagio Beach Cliff):
VIEW: Back view over shoulder
SCENE: Standing at edge of limestone cliff overlooking Shipwreck Beach far below
BACKGROUND: Electric turquoise water, famous shipwreck on white sand, towering cliffs
POSE: Back to camera, looking back over shoulder at camera, hair blowing in wind
LIGHTING: Bright midday sun, vivid colors
MOOD: Adventurous, breathtaking vista, dramatic

PANEL 4 - CRETE (Elafonisi Pink Sand):
VIEW: Low angle front view
SCENE: Kneeling in shallow crystal-clear water on famous pink sand beach
BACKGROUND: Pink coral sand visible through water, turquoise shallows, blue sky
POSE: Kneeling in water, hands on thighs, looking at camera with playful expression
LIGHTING: Bright sun, water glistening, skin wet
MOOD: Serene, tropical paradise, unique natural wonder

PANEL 5 - MILOS (Sarakiniko Moonscape):
VIEW: Full body side profile
SCENE: Standing on smooth white volcanic rock formations
BACKGROUND: Sarakiniko's lunar landscape, white volcanic rocks, deep blue sky and sea
POSE: Standing with one leg forward, hand shielding eyes, gazing at horizon
LIGHTING: High noon harsh light, strong shadows, high contrast
MOOD: Otherworldly, editorial, striking landscape

PANEL 6 - SANTORINI (Infinity Pool):
VIEW: Front view upper body
SCENE: In luxury infinity pool carved into cliff, arms resting on pool edge
BACKGROUND: White Cycladic architecture, blue pool water, caldera view through opening
POSE: In water, arms on pool edge, upper body visible, relaxed smile at camera
LIGHTING: Soft afternoon light, blue reflections from water
MOOD: Luxurious, exclusive, resort lifestyle

PANEL 7 - MYKONOS (Little Venice):
VIEW: Walking action shot front view
SCENE: Walking along waterfront path with colorful buildings behind
BACKGROUND: Little Venice buildings (white with blue/red/green balconies), waves splashing
POSE: Mid-stride walking toward camera, hair flowing, natural candid smile
LIGHTING: Late afternoon golden light, wave spray creating sparkle
MOOD: Carefree, energetic, joyful, authentic moment

PANEL 8 - CORFU (Canal d'Amour):
VIEW: Swimming/water action front view
SCENE: Treading water in narrow turquoise channel between sandstone cliffs
BACKGROUND: Golden-brown eroded sandstone formations, bright turquoise water
POSE: In water treading/swimming, wet hair slicked back, joyful expression
LIGHTING: Bright natural daylight, water droplets sparkling
MOOD: Fun, adventurous, playful, cooling off

PANEL 9 - PAROS (Beach Sunset):
VIEW: Back view full body
SCENE: Standing in shallow surf at beach during sunset, facing ocean
BACKGROUND: Endless Aegean Sea, orange/pink sunset sky, gentle waves
POSE: Back to camera, standing in ankle-deep water, hands by sides, facing sunset
LIGHTING: Golden sunset backlight, silhouette effect with warm rim light
MOOD: Peaceful, contemplative, end of perfect day

=== SETTING & AESTHETIC ===

OVERALL VIBE: Expensive Greek island vacation, luxury travel, Mediterranean summer
STYLE: High-end travel influencer photography, editorial quality
COLOR PALETTE: White (buildings/rocks), blue (sky/sea), crimson/white (bikini), warm golden tones (sunset), turquoise (water)
PHOTOGRAPHY: Professional quality, shot on high-end camera, natural lighting, travel magazine level

=== CRITICAL SKIN TEXTURE & REALISM ===

SKIN:
- Natural skin texture with visible pores
- Real human skin, NOT AI-smoothed
- NO beauty filter
- NO artificial smoothing or perfection
- Realistic lighting behavior on skin
- Sun-kissed glow, natural tan
- Wet skin in water shots (Panels 4, 6, 8)

OVERALL REALISM:
- Natural poses, not stiff or forced
- Realistic body proportions
- Authentic expressions and emotions
- Real person, not AI-perfect
- Natural hair movement (wind, water)

=== TECHNICAL REQUIREMENTS ===

COMPOSITION:
- 3x3 grid layout (3 across, 3 down)
- Square aspect ratio (1:1) for grid
- Thin white borders between panels
- Each panel equally sized
- High resolution (2K or 8K)

CONSISTENCY:
- SAME WOMAN in all 9 panels (from References 2 & 3)
- SAME facial features in all panels
- SAME body proportions in all panels
- SAME bikini (Alabama crimson & white) in all panels
- ONLY pose, angle, location vary between panels
- Professional photography quality throughout

=== FINAL CRITICAL REMINDER ===

This is ONE image containing 9 photographs of the SAME WOMAN from References 2 & 3.

IDENTITY LOCKING:
- Face and body from References 2 & 3 MUST be preserved exactly
- DO NOT change her appearance between panels
- DO NOT use face or body from Reference 1 (bikini image)
- ONLY use the bikini design from Reference 1
- Same person across all 9 panels - absolute consistency

BIKINI:
- Crimson red with white trim from Reference 1
- Apply this bikini to the woman from References 2 & 3

QUALITY:
- Each panel is distinct and separate (not blended)
- Clear borders between all 9 panels
- Natural skin texture, realistic beauty
- Professional Greek island travel photography
- Authentic and believable

Generate a stunning 3x3 travel grid showing this woman exploring Greek islands.
"""

def generate_greek_grid():
    """Generate 3x3 Greek island grid with references"""

    print(f"\n{'='*60}")
    print(f"VERONICA - GREEK ISLAND GRID (3x3)")
    print(f"{'='*60}")
    print(f"Model: gemini-3-pro-image-preview")
    print(f"Bikini reference: {BIKINI_REF}")
    print(f"Body/identity reference: {VERONICA_BASE}")
    print(f"Face angles reference: {VERONICA_FACE_GRID}")
    print(f"Output: {OUTPUT_PATH}")
    print(f"\nGenerating 9 Greek island poses...")
    print(f"Locations: Santorini, Mykonos, Zakynthos, Crete, Milos, Corfu, Paros")
    print(f"This may take 120-180 seconds...")
    print(f"")

    try:
        # Upload reference images
        print("Uploading bikini design reference...")
        with open(BIKINI_REF, 'rb') as f:
            bikini_file = client.files.upload(
                file=f,
                config={"mime_type": "image/jpeg"}
            )
        print(f"Bikini reference uploaded: {bikini_file.name}")

        print("Uploading body/identity reference...")
        with open(VERONICA_BASE, 'rb') as f:
            base_file = client.files.upload(
                file=f,
                config={"mime_type": "image/jpeg"}
            )
        print(f"Body reference uploaded: {base_file.name}")

        print("Uploading face angles reference...")
        with open(VERONICA_FACE_GRID, 'rb') as f:
            face_file = client.files.upload(
                file=f,
                config={"mime_type": "image/png"}
            )
        print(f"Face reference uploaded: {face_file.name}")

        print("Generating 3x3 Greek island grid...")

        # Generate with all references
        response = client.models.generate_content(
            model="gemini-3-pro-image-preview",
            contents=[
                types.Part.from_uri(
                    file_uri=bikini_file.uri,
                    mime_type=bikini_file.mime_type
                ),
                types.Part.from_uri(
                    file_uri=base_file.uri,
                    mime_type=base_file.mime_type
                ),
                types.Part.from_uri(
                    file_uri=face_file.uri,
                    mime_type=face_file.mime_type
                ),
                GRID_PROMPT
            ],
            config=types.GenerateContentConfig(
                response_modalities=['IMAGE'],
                image_config=types.ImageConfig(
                    aspect_ratio="1:1",
                    image_size="2K"
                )
            )
        )

        # Save generated grid
        for part in response.parts:
            if image := part.as_image():
                image.save(OUTPUT_PATH)
                file_size = OUTPUT_PATH.stat().st_size / (1024 * 1024)

                print(f"\n{'='*60}")
                print(f"✓ SUCCESS!")
                print(f"{'='*60}")
                print(f"Saved: {OUTPUT_PATH}")
                print(f"Size: {file_size:.2f} MB")
                print(f"\nGrid contains 9 panels (3x3 layout):")
                print(f"  Row 1: Santorini Oia | Mykonos Windmills | Zakynthos Cliff")
                print(f"  Row 2: Crete Pink Sand | Milos Moonscape | Santorini Pool")
                print(f"  Row 3: Mykonos Venice | Corfu Canal | Paros Sunset")
                print(f"\nSame woman (Veronica) in Alabama bikini across all panels!")
                return True

        print("❌ Error: No image generated in response")
        return False

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    generate_greek_grid()
