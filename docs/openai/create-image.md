# OpenAI: Create Image API Reference

### [Create image](https://api.openai.com/v1/images/generations)
Creates an image given a prompt. Learn more.

**Request body**

prompt
  string
  Required
  A text description of the desired image(s). The maximum length is 32000 characters for gpt-image-1, 1000 characters for dall-e-2 and 4000 characters for dall-e-3.

background
  string or null
  Optional
  Defaults to auto
  Allows to set transparency for the background of the generated image(s). This parameter is only supported for gpt-image-1. Must be one of transparent, opaque or auto (default value). When auto is used, the model will automatically determine the best background for the image.
  If transparent, the output format needs to support transparency, so it should be set to either png (default value) or webp.

model
  string
  Optional
  Defaults to dall-e-2
  The model to use for image generation. One of dall-e-2, dall-e-3, or gpt-image-1. Defaults to dall-e-2 unless a parameter specific to gpt-image-1 is used.

n
  integer or null
  Optional
  Defaults to 1
  The number of images to generate. Must be between 1 and 10. For dall-e-3, only n=1 is supported.

output_format
  string or null
  Optional
  Defaults to png
  The format in which the generated images are returned. This parameter is only supported for gpt-image-1. Must be one of png, jpeg, or webp.

size
  string or null
  Optional
  Defaults to auto
  The size of the generated images. Must be one of 1024x1024, 1536x1024 (landscape), 1024x1536 (portrait), or auto (default value) for gpt-image-1, one of 256x256, 512x512, or 1024x1024 for dall-e-2, and one of 1024x1024, 1792x1024, or 1024x1792 for dall-e-3.

**Example request:**
```python
import base64
from openai import OpenAI
client = OpenAI()

img = client.images.generate(
    model="gpt-image-1",
    prompt="A cute baby sea otter",
    n=1,
    size="1024x1024"
)

image_bytes = base64.b64decode(img.data[0].b64_json)
with open("output.png", "wb") as f:
    f.write(image_bytes)
```

**Response:**
```json
{
  "created": 1713833628,
  "data": [
    {
      "b64_json": "..."
    }
  ],
  "usage": {
    "total_tokens": 100,
    "input_tokens": 50,
    "output_tokens": 50,
    "input_tokens_details": {
      "text_tokens": 10,
      "image_tokens": 40
    }
  }
}
```
