# Seedream 4.5 API Usage Guide

## Overview
Seedream 4.5 is an image generation model available on Replicate. This guide covers the API schema and usage patterns.

## Authentication
The Replicate API token is stored in `.env.local`:
```
REPLICATE_API_TOKEN=r8_RuQIWz1vYKKVC9QxUXHurQCk88PYrUn4fTwu4
```

## API Parameters

### Required Parameters
- **prompt** (string): Text prompt for image generation

### Optional Parameters

#### Image Input
- **image_input** (array of URIs, default: []):
  - Input images for image-to-image generation
  - Can provide 1-14 images for single or multi-reference generation
  - Useful for style transfer, variations, or reference-based generation

#### Resolution Settings
- **size** (enum: "2K", "4K", "custom", default: "2K"):
  - 2K: 2048px resolution
  - 4K: 4096px resolution
  - custom: Use specific width/height values
  - Note: 1K resolution is NOT supported

- **aspect_ratio** (enum, default: "match_input_image"):
  - Options: "match_input_image", "1:1", "4:3", "3:4", "16:9", "9:16", "3:2", "2:3", "21:9"
  - Only used when size is not "custom"
  - "match_input_image" automatically matches input image aspect ratio

- **width** (integer, default: 2048):
  - Range: 1024-4096 pixels
  - Only used when size="custom"

- **height** (integer, default: 2048):
  - Range: 1024-4096 pixels
  - Only used when size="custom"

#### Sequential Generation
- **sequential_image_generation** (enum: "disabled", "auto", default: "disabled"):
  - "disabled": Generate a single image
  - "auto": Let model decide whether to generate multiple related images
  - Useful for story scenes, character variations, or series

- **max_images** (integer, default: 1):
  - Range: 1-15
  - Maximum number of images when sequential_image_generation="auto"
  - Total images (input + generated) cannot exceed 15

## Example Usage Patterns

### Basic Text-to-Image
```json
{
  "prompt": "A serene beach at sunset with palm trees"
}
```

### High Resolution Generation
```json
{
  "prompt": "Detailed cityscape at night",
  "size": "4K",
  "aspect_ratio": "16:9"
}
```

### Custom Dimensions
```json
{
  "prompt": "Portrait of a character",
  "size": "custom",
  "width": 3072,
  "height": 4096
}
```

### Image-to-Image Generation
```json
{
  "prompt": "Transform this photo into a watercolor painting",
  "image_input": ["https://example.com/photo.jpg"],
  "aspect_ratio": "match_input_image"
}
```

### Sequential Generation (Story/Variations)
```json
{
  "prompt": "A character's journey through a magical forest",
  "sequential_image_generation": "auto",
  "max_images": 5,
  "size": "2K",
  "aspect_ratio": "16:9"
}
```

### Multi-Reference Generation
```json
{
  "prompt": "Combine the styles and elements from these reference images",
  "image_input": [
    "https://example.com/ref1.jpg",
    "https://example.com/ref2.jpg",
    "https://example.com/ref3.jpg"
  ]
}
```

## Key Features

1. **Flexible Resolution**: 2K, 4K, or custom dimensions (1024-4096px)
2. **Multiple Aspect Ratios**: 9 standard ratios plus input matching
3. **Image-to-Image**: Support for 1-14 reference images
4. **Sequential Generation**: Auto-generate related image series
5. **High Quality**: Optimized for detailed, high-fidelity outputs

## Limitations

- Minimum dimension: 1024px
- Maximum dimension: 4096px
- Maximum images in sequential mode: 15 total (input + generated)
- 1K resolution is not supported
- Sequential generation only with "auto" mode
