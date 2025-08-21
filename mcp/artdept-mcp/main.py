#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "mcp>=1.0.0",
#     "openai>=1.0.0",
#     "pydantic>=2.0.0",
# ]
# ///
"""
ArtDept MCP Server - Creative Design Tools using OpenAI Image Generation.

This MCP server provides creative design tools for generating wireframes,
design systems, logos, icons, illustrations, and photos using OpenAI's
gpt-image-1 model via base64 responses.

Usage:
    ./main.py
    # or
    uv run main.py

Environment Variables:
    OPENAI_API_KEY: Required OpenAI API key for image generation

Note:
    - Uses gpt-image-1 model with base64 response format
    - Background transparency might not be supported by gpt-image-1 model
    - Images are saved directly from base64 data without URL downloads
"""

import asyncio
import base64
import json
import logging
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Literal
from datetime import datetime
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
from openai import AsyncOpenAI
from pydantic import BaseModel, Field

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Check for required environment variable
if not os.getenv("OPENAI_API_KEY"):
    logger.error("OPENAI_API_KEY environment variable is required")
    sys.exit(1)

# Initialize OpenAI client
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Initialize MCP server
server = Server("artdept-mcp")


class ImageGenerationResult(BaseModel):
    """Result from image generation."""
    success: bool
    message: str
    paths: List[str] = Field(default_factory=list)
    errors: List[str] = Field(default_factory=list)


async def save_base64_image(b64_data: str, filepath: Path) -> bool:
    """Save base64 encoded image data to filesystem."""
    try:
        # Create parent directories if they don't exist
        filepath.parent.mkdir(parents=True, exist_ok=True)

        # Decode base64 data and save the image
        image_data = base64.b64decode(b64_data)
        filepath.write_bytes(image_data)
        logger.info(f"Saved image to {filepath}")
        return True
    except Exception as e:
        logger.error(f"Failed to save base64 image: {e}")
        return False


async def generate_images(
    prompt: str,
    n: int = 1,
    size: str = "1024x1024",
    model: str = "gpt-image-1",
    quality: str = "standard",
    response_format: str = "b64_json"
) -> List[str]:
    """Generate images using OpenAI API."""
    try:
        response = await client.images.generate(
            model=model,
            prompt=prompt,
            n=n,
            size=size,
            quality=quality,
            response_format=response_format
        )
        # Return base64 data instead of URLs
        return [image.b64_json for image in response.data]
    except Exception as e:
        logger.error(f"Image generation failed: {e}")
        raise


def build_wireframe_prompt(user_prompt: str, device: str, style: str) -> str:
    """Build enhanced prompt for wireframe generation."""
    device_context = {
        "desktop": "desktop/laptop screen (landscape orientation, 1536x1024)",
        "mobile": "mobile phone screen (portrait orientation, 1024x1536)",
        "both": "responsive design showing both desktop and mobile layouts"
    }

    return f"""Create a professional UI/UX wireframe design:

REQUIREMENTS:
- Device: {device_context.get(device, device_context['both'])}
- Style: {style if style else 'clean, minimalist wireframe'}
- Format: Low-fidelity wireframe with clear layout structure
- Elements: Use standard wireframe conventions (boxes for images, lines for text, rectangles for buttons)
- Annotations: Include subtle labels for key components
- Color: Grayscale/monochrome wireframe style
- Professional wireframe quality

USER SPECIFICATION:
{user_prompt}

Create a clear, professional wireframe that focuses on layout, hierarchy, and user flow."""


def build_design_system_prompt(user_prompt: str, design_type: str, style: str, colors: str) -> str:
    """Build enhanced prompt for design system generation."""
    type_context = {
        "brand": "brand design system with logo variations, color palette, typography, and brand elements",
        "ui": "UI component design system with buttons, forms, cards, navigation, and interface elements",
        "ux": "UX design system with user flows, interaction patterns, and experience guidelines"
    }

    color_spec = f"Color scheme: {colors}" if colors else "Professional color palette"

    return f"""Create a comprehensive design system presentation:

TYPE: {type_context.get(design_type, type_context['brand'])}
STYLE: {style if style else 'modern, professional design system'}
{color_spec}

INCLUDE:
- Clear visual hierarchy
- Consistent spacing and alignment
- Professional presentation layout
- Component variations and states
- Typography samples
- Color swatches with hex codes
- Spacing and grid guidelines
- Example usage contexts

USER SPECIFICATION:
{user_prompt}

Present as a single, well-organized design system board suitable for design handoff."""


def build_logo_prompt(user_prompt: str, style: str, colors: str) -> str:
    """Build enhanced prompt for logo generation."""
    color_spec = f"using {colors} color scheme" if colors else "with appropriate colors"

    return f"""Design a professional logo:

REQUIREMENTS:
- Style: {style if style else 'modern, scalable logo design'}
- Colors: {color_spec}
- Format: Clean vector-style design (note: transparent background may not be supported)
- Versatility: Works at different sizes
- Simplicity: Clear and memorable
- Professional quality
- Centered composition
- Adequate padding around the logo

USER SPECIFICATION:
{user_prompt}

Create a distinctive, professional logo that would work across various media."""


def build_icon_prompt(user_prompt: str, style: str, colors: str) -> str:
    """Build enhanced prompt for icon generation."""
    color_spec = f"using {colors} colors" if colors else "with clear, simple colors"

    return f"""Design a clean, scalable icon:

REQUIREMENTS:
- Style: {style if style else 'modern, minimalist icon'}
- Colors: {color_spec}
- Format: Simple, clear design (note: transparent background may not be supported)
- Scalability: Readable at small and large sizes
- Clarity: Instantly recognizable
- Consistency: Suitable for icon sets
- Centered with appropriate padding

USER SPECIFICATION:
{user_prompt}

Create a professional icon suitable for UI/UX applications."""


def build_illustration_prompt(user_prompt: str, style: str) -> str:
    """Build enhanced prompt for illustration generation."""
    return f"""Create a professional illustration:

STYLE: {style if style else 'modern digital illustration'}
FORMAT: High-quality illustration (note: transparent background may not be supported)
COMPOSITION: Balanced, visually appealing
QUALITY: Professional, polished artwork

USER SPECIFICATION:
{user_prompt}

Deliver a captivating illustration suitable for professional use."""


def build_photo_prompt(user_prompt: str, style: str) -> str:
    """Build enhanced prompt for photo generation."""
    return f"""Generate a photorealistic image:

STYLE: {style if style else 'professional photography'}
QUALITY: High-resolution, sharp details
LIGHTING: Professional lighting setup
COMPOSITION: Well-composed, balanced shot
REALISM: Photographic quality

USER SPECIFICATION:
{user_prompt}

Create a stunning photograph that looks professionally shot."""


@server.list_tools()
async def list_tools() -> List[Tool]:
    """List all available creative design tools."""
    return [
        Tool(
            name="new_wireframe",
            description="Generate UI/UX wireframes for desktop, mobile, or both",
            inputSchema={
                "type": "object",
                "properties": {
                    "id": {
                        "type": "string",
                        "description": "Kebab-case identifier (e.g., 'home-page', 'checkout-flow')"
                    },
                    "prompt": {
                        "type": "string",
                        "description": "Natural language description of the wireframe"
                    },
                    "device": {
                        "type": "string",
                        "enum": ["desktop", "mobile", "both"],
                        "description": "Target device type",
                        "default": "both"
                    },
                    "style": {
                        "type": "string",
                        "description": "Wireframe style (e.g., 'minimalist', 'detailed', 'annotated')"
                    },
                    "save": {
                        "type": "string",
                        "description": "Directory to save images",
                        "default": "creative/wires/"
                    }
                },
                "required": ["id", "prompt"]
            }
        ),
        Tool(
            name="new_designsystem",
            description="Generate comprehensive design systems",
            inputSchema={
                "type": "object",
                "properties": {
                    "id": {
                        "type": "string",
                        "description": "Kebab-case identifier for the design system"
                    },
                    "prompt": {
                        "type": "string",
                        "description": "Natural language description of the design system"
                    },
                    "n": {
                        "type": "integer",
                        "description": "Number of variations to generate",
                        "minimum": 1,
                        "maximum": 4
                    },
                    "type": {
                        "type": "string",
                        "enum": ["brand", "ui", "ux"],
                        "description": "Type of design system",
                        "default": "brand"
                    },
                    "style": {
                        "type": "string",
                        "description": "Design style (e.g., 'corporate', 'modern', 'playful')"
                    },
                    "colors": {
                        "type": "string",
                        "description": "Color palette (e.g., 'blues', 'warm tones', '#FF6B6B')"
                    },
                    "save": {
                        "type": "string",
                        "description": "Directory to save images",
                        "default": "creative/design-systems/"
                    }
                },
                "required": ["id", "prompt", "n"]
            }
        ),
        Tool(
            name="new_logo",
            description="Generate professional logos",
            inputSchema={
                "type": "object",
                "properties": {
                    "id": {
                        "type": "string",
                        "description": "Kebab-case identifier for the logo"
                    },
                    "prompt": {
                        "type": "string",
                        "description": "Natural language description of the logo"
                    },
                    "n": {
                        "type": "integer",
                        "description": "Number of variations to generate",
                        "minimum": 1,
                        "maximum": 4
                    },
                    "style": {
                        "type": "string",
                        "description": "Logo style (e.g., 'minimalist', 'vintage', 'tech')"
                    },
                    "colors": {
                        "type": "string",
                        "description": "Color specification (e.g., 'black', 'blue and gold')"
                    },
                    "save": {
                        "type": "string",
                        "description": "Directory to save images",
                        "default": "creative/logos/"
                    }
                },
                "required": ["id", "prompt", "n"]
            }
        ),
        Tool(
            name="new_icon",
            description="Generate scalable icons",
            inputSchema={
                "type": "object",
                "properties": {
                    "id": {
                        "type": "string",
                        "description": "Kebab-case identifier for the icon"
                    },
                    "prompt": {
                        "type": "string",
                        "description": "Natural language description of the icon"
                    },
                    "n": {
                        "type": "integer",
                        "description": "Number of variations to generate",
                        "minimum": 1,
                        "maximum": 4
                    },
                    "style": {
                        "type": "string",
                        "description": "Icon style (e.g., 'flat', 'outline', '3D')"
                    },
                    "colors": {
                        "type": "string",
                        "description": "Color specification"
                    },
                    "save": {
                        "type": "string",
                        "description": "Directory to save images",
                        "default": "creative/icons/"
                    }
                },
                "required": ["id", "prompt", "n"]
            }
        ),
        Tool(
            name="new_illustration",
            description="Generate custom illustrations",
            inputSchema={
                "type": "object",
                "properties": {
                    "id": {
                        "type": "string",
                        "description": "Kebab-case identifier for the illustration"
                    },
                    "prompt": {
                        "type": "string",
                        "description": "Natural language description of the illustration"
                    },
                    "n": {
                        "type": "integer",
                        "description": "Number of variations to generate",
                        "minimum": 1,
                        "maximum": 4
                    },
                    "size": {
                        "type": "string",
                        "enum": ["1024x1024", "1536x1024", "1024x1536"],
                        "description": "Image dimensions",
                        "default": "1024x1024"
                    },
                    "style": {
                        "type": "string",
                        "description": "Illustration style (e.g., 'watercolor', 'vector', 'sketch')"
                    },
                    "save": {
                        "type": "string",
                        "description": "Directory to save images",
                        "default": "creative/illustrations/"
                    }
                },
                "required": ["id", "prompt", "n"]
            }
        ),
        Tool(
            name="new_photo",
            description="Generate photorealistic images",
            inputSchema={
                "type": "object",
                "properties": {
                    "id": {
                        "type": "string",
                        "description": "Kebab-case identifier for the photo"
                    },
                    "prompt": {
                        "type": "string",
                        "description": "Natural language description of the photo"
                    },
                    "n": {
                        "type": "integer",
                        "description": "Number of variations to generate",
                        "minimum": 1,
                        "maximum": 4
                    },
                    "size": {
                        "type": "string",
                        "enum": ["1024x1024", "1536x1024", "1024x1536"],
                        "description": "Image dimensions",
                        "default": "1024x1024"
                    },
                    "style": {
                        "type": "string",
                        "description": "Photography style (e.g., 'portrait', 'landscape', 'macro')"
                    },
                    "save": {
                        "type": "string",
                        "description": "Directory to save images",
                        "default": "creative/photos/"
                    }
                },
                "required": ["id", "prompt", "n"]
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """Handle tool calls for image generation."""

    try:
        if name == "new_wireframe":
            return await generate_wireframe(**arguments)
        elif name == "new_designsystem":
            return await generate_design_system(**arguments)
        elif name == "new_logo":
            return await generate_logo(**arguments)
        elif name == "new_icon":
            return await generate_icon(**arguments)
        elif name == "new_illustration":
            return await generate_illustration(**arguments)
        elif name == "new_photo":
            return await generate_photo(**arguments)
        else:
            return [TextContent(
                type="text",
                text=json.dumps({
                    "success": False,
                    "message": f"Unknown tool: {name}",
                    "paths": [],
                    "errors": [f"Tool '{name}' not found"]
                })
            )]
    except Exception as e:
        logger.error(f"Tool execution failed: {e}")
        return [TextContent(
            type="text",
            text=json.dumps({
                "success": False,
                "message": f"Tool execution failed: {str(e)}",
                "paths": [],
                "errors": [str(e)]
            })
        )]


async def generate_wireframe(
    id: str,
    prompt: str,
    device: str = "both",
    style: Optional[str] = None,
    save: str = "creative/wires/"
) -> List[TextContent]:
    """Generate wireframe images."""
    result = ImageGenerationResult(success=False, message="")

    try:
        devices_to_generate = []
        if device == "both":
            devices_to_generate = [("desktop", "1536x1024"), ("mobile", "1024x1536")]
        elif device == "desktop":
            devices_to_generate = [("desktop", "1536x1024")]
        elif device == "mobile":
            devices_to_generate = [("mobile", "1024x1536")]

        for device_name, size in devices_to_generate:
            enhanced_prompt = build_wireframe_prompt(prompt, device_name, style)

            try:
                b64_images = await generate_images(
                    prompt=enhanced_prompt,
                    n=1,
                    size=size,
                    model="gpt-image-1",
                    quality="standard"
                )

                for idx, b64_data in enumerate(b64_images):
                    filename = f"{id}-{device_name}.jpg"
                    filepath = Path(save) / filename

                    if await save_base64_image(b64_data, filepath):
                        result.paths.append(str(filepath))
                    else:
                        result.errors.append(f"Failed to save {filename}")

            except Exception as e:
                result.errors.append(f"Failed to generate {device_name} wireframe: {str(e)}")

        result.success = len(result.paths) > 0
        result.message = f"Generated {len(result.paths)} wireframe(s) for '{id}'"

    except Exception as e:
        result.message = f"Wireframe generation failed: {str(e)}"
        result.errors.append(str(e))

    return [TextContent(
        type="text",
        text=json.dumps(result.model_dump())
    )]


async def generate_design_system(
    id: str,
    prompt: str,
    n: int,
    type: str = "brand",
    style: Optional[str] = None,
    colors: Optional[str] = None,
    save: str = "creative/design-systems/"
) -> List[TextContent]:
    """Generate design system images."""
    result = ImageGenerationResult(success=False, message="")

    try:
        enhanced_prompt = build_design_system_prompt(prompt, type, style, colors)

        # Generate variations
        for i in range(n):
            variation_prompt = f"{enhanced_prompt}\n\nVariation {i+1} of {n}"

            try:
                b64_images = await generate_images(
                    prompt=variation_prompt,
                    n=1,
                    size="1536x1024",
                    model="gpt-image-1",
                    quality="standard"
                )

                for b64_data in b64_images:
                    filename = f"{id}-v{i+1}.jpg"
                    filepath = Path(save) / filename

                    if await save_base64_image(b64_data, filepath):
                        result.paths.append(str(filepath))
                    else:
                        result.errors.append(f"Failed to save {filename}")

            except Exception as e:
                result.errors.append(f"Failed to generate variation {i+1}: {str(e)}")

        result.success = len(result.paths) > 0
        result.message = f"Generated {len(result.paths)} design system(s) for '{id}'"

    except Exception as e:
        result.message = f"Design system generation failed: {str(e)}"
        result.errors.append(str(e))

    return [TextContent(
        type="text",
        text=json.dumps(result.model_dump())
    )]


async def generate_logo(
    id: str,
    prompt: str,
    n: int,
    style: Optional[str] = None,
    colors: Optional[str] = None,
    save: str = "creative/logos/"
) -> List[TextContent]:
    """Generate logo images."""
    result = ImageGenerationResult(success=False, message="")

    try:
        enhanced_prompt = build_logo_prompt(prompt, style, colors)

        # Generate variations
        for i in range(n):
            variation_prompt = f"{enhanced_prompt}\n\nUnique variation {i+1} of {n}"

            try:
                b64_images = await generate_images(
                    prompt=variation_prompt,
                    n=1,
                    size="1024x1024",
                    model="gpt-image-1",
                    quality="standard"
                )

                for b64_data in b64_images:
                    filename = f"{id}-v{i+1}.png"
                    filepath = Path(save) / filename

                    if await save_base64_image(b64_data, filepath):
                        result.paths.append(str(filepath))
                    else:
                        result.errors.append(f"Failed to save {filename}")

            except Exception as e:
                result.errors.append(f"Failed to generate variation {i+1}: {str(e)}")

        result.success = len(result.paths) > 0
        result.message = f"Generated {len(result.paths)} logo(s) for '{id}'"

    except Exception as e:
        result.message = f"Logo generation failed: {str(e)}"
        result.errors.append(str(e))

    return [TextContent(
        type="text",
        text=json.dumps(result.model_dump())
    )]


async def generate_icon(
    id: str,
    prompt: str,
    n: int,
    style: Optional[str] = None,
    colors: Optional[str] = None,
    save: str = "creative/icons/"
) -> List[TextContent]:
    """Generate icon images."""
    result = ImageGenerationResult(success=False, message="")

    try:
        enhanced_prompt = build_icon_prompt(prompt, style, colors)

        # Generate variations
        for i in range(n):
            variation_prompt = f"{enhanced_prompt}\n\nVariation {i+1} of {n}"

            try:
                b64_images = await generate_images(
                    prompt=variation_prompt,
                    n=1,
                    size="1024x1024",
                    model="gpt-image-1",
                    quality="standard"
                )

                for b64_data in b64_images:
                    filename = f"{id}-v{i+1}.png"
                    filepath = Path(save) / filename

                    if await save_base64_image(b64_data, filepath):
                        result.paths.append(str(filepath))
                    else:
                        result.errors.append(f"Failed to save {filename}")

            except Exception as e:
                result.errors.append(f"Failed to generate variation {i+1}: {str(e)}")

        result.success = len(result.paths) > 0
        result.message = f"Generated {len(result.paths)} icon(s) for '{id}'"

    except Exception as e:
        result.message = f"Icon generation failed: {str(e)}"
        result.errors.append(str(e))

    return [TextContent(
        type="text",
        text=json.dumps(result.model_dump())
    )]


async def generate_illustration(
    id: str,
    prompt: str,
    n: int,
    size: str = "1024x1024",
    style: Optional[str] = None,
    save: str = "creative/illustrations/"
) -> List[TextContent]:
    """Generate illustration images."""
    result = ImageGenerationResult(success=False, message="")

    try:
        enhanced_prompt = build_illustration_prompt(prompt, style)

        # Generate variations
        for i in range(n):
            variation_prompt = f"{enhanced_prompt}\n\nCreative variation {i+1} of {n}"

            try:
                b64_images = await generate_images(
                    prompt=variation_prompt,
                    n=1,
                    size=size,
                    model="gpt-image-1",
                    quality="standard"
                )

                for b64_data in b64_images:
                    filename = f"{id}-v{i+1}.png"
                    filepath = Path(save) / filename

                    if await save_base64_image(b64_data, filepath):
                        result.paths.append(str(filepath))
                    else:
                        result.errors.append(f"Failed to save {filename}")

            except Exception as e:
                result.errors.append(f"Failed to generate variation {i+1}: {str(e)}")

        result.success = len(result.paths) > 0
        result.message = f"Generated {len(result.paths)} illustration(s) for '{id}'"

    except Exception as e:
        result.message = f"Illustration generation failed: {str(e)}"
        result.errors.append(str(e))

    return [TextContent(
        type="text",
        text=json.dumps(result.model_dump())
    )]


async def generate_photo(
    id: str,
    prompt: str,
    n: int,
    size: str = "1024x1024",
    style: Optional[str] = None,
    save: str = "creative/photos/"
) -> List[TextContent]:
    """Generate photorealistic images."""
    result = ImageGenerationResult(success=False, message="")

    try:
        enhanced_prompt = build_photo_prompt(prompt, style)

        # Generate variations
        for i in range(n):
            variation_prompt = f"{enhanced_prompt}\n\nUnique shot {i+1} of {n}"

            try:
                b64_images = await generate_images(
                    prompt=variation_prompt,
                    n=1,
                    size=size,
                    model="gpt-image-1",
                    quality="standard"
                )

                for b64_data in b64_images:
                    filename = f"{id}-v{i+1}.jpg"
                    filepath = Path(save) / filename

                    if await save_base64_image(b64_data, filepath):
                        result.paths.append(str(filepath))
                    else:
                        result.errors.append(f"Failed to save {filename}")

            except Exception as e:
                result.errors.append(f"Failed to generate variation {i+1}: {str(e)}")

        result.success = len(result.paths) > 0
        result.message = f"Generated {len(result.paths)} photo(s) for '{id}'"

    except Exception as e:
        result.message = f"Photo generation failed: {str(e)}"
        result.errors.append(str(e))

    return [TextContent(
        type="text",
        text=json.dumps(result.model_dump())
    )]


async def main() -> int:
    """Main execution function."""
    try:
        logger.info("Starting ArtDept MCP Server")
        logger.info("Available tools: new_wireframe, new_designsystem, new_logo, new_icon, new_illustration, new_photo")

        # Run the stdio server
        async with stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream,
                write_stream,
                server.create_initialization_options()
            )

        logger.info("ArtDept MCP Server stopped")
        return 0

    except KeyboardInterrupt:
        logger.info("Server interrupted by user")
        return 0
    except Exception as e:
        logger.error(f"Server failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
