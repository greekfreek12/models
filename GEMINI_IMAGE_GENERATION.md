# Gemini Image Generation API

## Model
- **gemini-3-pro-image-preview** (Nano Banana Pro Preview) - Advanced model for professional asset production

## Basic Python Usage

```python
from google import genai
from google.genai import types
from PIL import Image

client = genai.Client(api_key="YOUR_API_KEY")

# Text to Image
response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents="Your prompt here",
    config=types.GenerateContentConfig(
        response_modalities=['TEXT', 'IMAGE'],
        image_config=types.ImageConfig(
            aspect_ratio="16:9",  # Options: 1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9
            image_size="2K"  # Options: 1K, 2K, 4K
        )
    )
)

# Save images
for part in response.parts:
    if part.text:
        print(part.text)
    elif image := part.as_image():
        image.save("output.png")
```

## Image to Image

```python
image_input = Image.open('path/to/image.jpg')

response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents=[image_input, "Your edit prompt here"]
)
```

## Supported Aspect Ratios

| Aspect Ratio | 2K Resolution | 4K Resolution |
|--------------|---------------|---------------|
| 1:1          | 2048x2048     | 4096x4096     |
| 16:9         | 2752x1536     | 5504x3072     |
| 9:16         | 1536x2752     | 3072x5504     |
| 3:4          | 1792x2400     | 3584x4800     |
| 4:3          | 2400x1792     | 4800x3584     |

## Key Features
- High-resolution output (1K, 2K, 4K)
- Google Search grounding
- Multi-turn conversational editing
- Up to 14 reference images
