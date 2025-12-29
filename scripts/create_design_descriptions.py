#!/usr/bin/env python3
"""Create detailed TXT descriptions for final bikini designs with placement info."""
import os

FINAL_DESIGNS = {
    "Alabama": {
        "colors": "Crimson (#9E1B32), Gray (#828A8F), White (#FFFFFF)",
        "designs": [
            {
                "name": "Houndstooth Classic",
                "variations": ["Houndstooth Classic"],
                "description": "Triangle bikini top and brazilian bottom in iconic crimson and white houndstooth pattern. Classic Bear Bryant pattern covering entire bikini.",
                "placement": "Houndstooth pattern covers entire bikini - both top cups and bottom piece. Pattern is repeated uniformly across all fabric. Thin straps, minimal coverage.",
                "style": "Sophisticated preppy style",
                "colors_used": "Crimson and White houndstooth"
            },
            {
                "name": "Script A Logo",
                "variations": ["Script A Logo", "Script A Logo V2"],
                "description": "Solid crimson bikini with LARGE white Alabama Script A logos printed all over in dense repeated pattern. 15-20 logos total covering more surface area than typical prints.",
                "placement": "Multiple Script A logos scattered across: 3-4 logos on each breast cup, 5-6 logos across bikini bottom front, 3-4 logos on bikini bottom back. Logos vary in size from small (1 inch) to large (3 inches). Dense coverage.",
                "style": "Bold team branding, modern college spirit aesthetic",
                "colors_used": "Crimson base with White logos"
            },
            {
                "name": "Elephant Stampede",
                "variations": ["Elephant Stampede"],
                "description": "Gray bikini with subtle crimson elephant silhouettes scattered across fabric. Minimalist mascot design.",
                "placement": "Elephant silhouettes scattered: 2-3 small elephants on each breast cup, 4-5 elephants across bikini bottom front, 2-3 on back. Elephants face different directions creating stampede effect.",
                "style": "Elegant animal print, bandeau top with high-waisted bottom",
                "colors_used": "Gray base with Crimson elephant prints"
            },
            {
                "name": "Roll Tide Stripes Championship",
                "variations": ["Roll Tide Stripes", "Roll Tide Stripes V2", "Roll Tide Stripes Championship"],
                "description": "ELEGANT diagonal stripes in Crimson, Gray, and White (triple color). Thin refined stripes at 45-degree angle with subtle shimmer/metallic finish. Championship quality premium fabric.",
                "placement": "Diagonal stripes at 45-degree angle running from top-left to bottom-right across entire bikini. Stripes repeat in sequence: Crimson (0.5 inch), Gray (0.5 inch), White (0.5 inch). Pattern continuous across both top cups and bottom piece.",
                "style": "Sophisticated preppy aesthetic, triangle top and cheeky bottom",
                "colors_used": "Crimson, Gray, and White striped"
            },
            {
                "name": "Big Al Mascot",
                "variations": ["Big Al Mascot", "Big Al Mascot Face"],
                "description": "White bikini with large crimson Big Al elephant mascot face prints. Cute cartoon Alabama elephant graphics.",
                "placement": "Large Big Al faces: One centered on each breast cup (2-3 inches), one large face centered on bikini bottom front (3-4 inches covering lower abdomen/bikini area), one on bikini bottom back. Faces show full elephant head with happy expression and Alabama branding.",
                "style": "Playful team spirit, triangle top with brazilian bottom",
                "colors_used": "White base with Crimson mascot prints"
            }
        ]
    },
    "Auburn": {
        "colors": "Navy Blue (#03244D), Burnt Orange (#DD550C), White (#FFFFFF)",
        "designs": [
            {
                "name": "War Eagle Navy",
                "variations": ["War Eagle", "War Eagle Navy"],
                "description": "Navy blue bikini with burnt orange eagle silhouettes flying across fabric. NO TEXT, just pure eagle graphics. Fierce bird of prey theme.",
                "placement": "Eagle silhouettes scattered: 2-3 eagles on each breast cup showing eagles in flight, 4-5 eagles across bikini bottom front, 2-3 on back. Eagles positioned at different angles suggesting flight pattern.",
                "style": "Bold mascot print, triangle top with brazilian bottom",
                "colors_used": "Navy base with Burnt Orange eagles"
            },
            {
                "name": "War Eagle White",
                "variations": ["War Eagle White"],
                "description": "WHITE bikini with navy blue and burnt orange eagle silhouettes flying across. NO TEXT, just eagle graphics. Clean colorway variation.",
                "placement": "Eagle silhouettes in two colors scattered: 2-3 eagles per breast cup (alternating navy and orange), 4-5 eagles across bikini bottom front (mixed colors), 2-3 on back. Flight pattern with varied eagle poses.",
                "style": "Fresh take on War Eagle design, triangle top with brazilian bottom",
                "colors_used": "White base with Navy and Burnt Orange eagles"
            },
            {
                "name": "Tiger Stripes Navy",
                "variations": ["Tiger Stripes Auburn", "Tiger Stripes Navy"],
                "description": "Navy and burnt orange bold tiger stripe pattern. NO TEXT, pure animal print. Diagonal stripes mimicking tiger fur pattern.",
                "placement": "Tiger stripes run diagonally across entire bikini. Stripes alternate: Navy (0.75 inch), Burnt Orange (0.5 inch), Navy (1 inch), creating irregular pattern like real tiger. Stripes continuous across top cups and bottom.",
                "style": "Fierce Auburn Tigers aesthetic, bandeau top with cheeky bottom",
                "colors_used": "Navy and Burnt Orange striped"
            },
            {
                "name": "Tiger Stripes White",
                "variations": ["Tiger Stripes White"],
                "description": "WHITE base with navy and burnt orange tiger stripe pattern overlay. NO TEXT, pure pattern. Clean fresh colorway.",
                "placement": "Tiger stripes over white base running diagonally. Navy and burnt orange stripes (0.5-1 inch varying widths) create tiger pattern. White shows between stripes. Pattern covers entire bikini top and bottom.",
                "style": "Light version of tiger stripes, triangle top with brazilian bottom",
                "colors_used": "White base with Navy and Burnt Orange stripes"
            },
            {
                "name": "Toomer's Oaks",
                "variations": ["Toomer's Oaks", "Toomer's Oaks V2"],
                "description": "White bikini with ENHANCED Toomer's Corner celebration design. Navy oak tree silhouettes with orange and white toilet paper streams ATTACHED to branches and flowing dramatically. Iconic Auburn tradition.",
                "placement": "Oak tree designs: Small navy tree silhouette centered on each breast cup with white/orange toilet paper draped over branches. Larger navy oak tree (3-4 inches) centered on bikini bottom front with dramatic toilet paper streams hanging from branches and flowing down. Toilet paper attached to tree branches, not floating.",
                "style": "Campus tradition celebration, halter top with tie-side bottom",
                "colors_used": "White base with Navy trees and Orange/White toilet paper"
            }
        ]
    }
}

def create_txt_file(school, design, output_dir):
    """Create detailed TXT file for a design."""
    filename = f"{school}_{design['name'].replace(' ', '_')}.txt"
    filepath = os.path.join(output_dir, filename)

    content = f"""Design Name: {design['name']}
School: {school}
School Colors: {FINAL_DESIGNS[school]['colors']}

=== VARIATIONS ===
{', '.join(design['variations'])}

=== DESCRIPTION ===
{design['description']}

=== PLACEMENT DETAILS ===
{design['placement']}

=== STYLE ===
{design['style']}

=== COLORS USED ===
{design['colors_used']}

=== NOTES FOR GENERATION ===
This design is optimized for image generation models. The placement details specify exact locations for patterns, logos, and graphics to ensure accurate reproduction. When generating:
- Follow placement specifications for graphic locations
- Maintain color accuracy using provided hex codes
- Preserve the style characteristics described
- Ensure all design elements are clearly visible and well-defined

Generated: 2025-12-27
Version: V3 Final
"""

    with open(filepath, 'w') as f:
        f.write(content)

    print(f"  ✓ {filename}")
    return filepath

if __name__ == "__main__":
    print("📝 Creating Design Descriptions\n")

    for school in ["Alabama", "Auburn"]:
        print(f"🎓 {school}:")
        output_dir = f"bikinis/{school}/design_descriptions"
        os.makedirs(output_dir, exist_ok=True)

        for design in FINAL_DESIGNS[school]["designs"]:
            create_txt_file(school, design, output_dir)

        print()

    print("✅ All descriptions created!")
