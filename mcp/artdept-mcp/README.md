# ArtDept MCP Server

A creative design toolkit that provides AI-powered image generation tools through the Model Context Protocol (MCP). Generate professional wireframes, design systems, logos, icons, illustrations, and photorealistic images using natural language descriptions.

## Overview

ArtDept MCP Server bridges the gap between natural language descriptions and visual design assets. It leverages OpenAI's `gpt-image-1` model to create high-quality design assets based on your creative requirements. The server generates images as base64-encoded data and saves them directly to your local filesystem, ensuring fast and reliable asset creation. Perfect for designers, developers, and creative professionals who need quick visual prototypes and design assets.

### Key Features

- **Wireframe Generation**: Create UI/UX wireframes for desktop, mobile, or both
- **Design Systems**: Generate comprehensive brand, UI, or UX design systems
- **Logo Design**: Professional logo creation with multiple variations
- **Icon Design**: Scalable icons suitable for UI/UX applications
- **Illustration**: Custom illustrations in various artistic styles
- **Photography**: Photorealistic images for any use case

## Prerequisites

- Python 3.11 or higher
- OpenAI API key with access to `gpt-image-1` model
- MCP-compatible client (such as Claude Desktop)

## Technical Details

### Image Generation Model
- **Model**: OpenAI's `gpt-image-1` (not DALL-E 3)
- **Response Format**: Base64-encoded JSON (`b64_json`)
- **Quality**: Standard (optimized for speed and cost)
- **Local Storage**: Images saved directly from base64 data without URL downloads

### Image Specifications
- **Wireframes**: 1536x1024 (desktop), 1024x1536 (mobile) - saved as JPG
- **Design Systems**: 1536x1024 - saved as JPG  
- **Logos**: 1024x1024 - saved as PNG
- **Icons**: 1024x1024 - saved as PNG
- **Illustrations**: Configurable (1024x1024, 1536x1024, 1024x1536) - saved as PNG
- **Photos**: Configurable (1024x1024, 1536x1024, 1024x1536) - saved as JPG

### Limitations
- Background transparency may not be supported by the `gpt-image-1` model
- Single image per API request (variations achieved through multiple calls)
- Maximum 4 variations per tool call

## Installation

### 1. Environment Setup

Ensure you have an OpenAI API key:

```bash
export OPENAI_API_KEY="your-openai-api-key-here"
```

Or add it to your `.env` file:

```env
OPENAI_API_KEY=your-openai-api-key-here
```

### 2. Server Installation

The server uses `uv` for dependency management and can be run directly:

```bash
# Make the script executable
chmod +x main.py

# Run the server
./main.py
```

### 3. MCP Client Configuration

Add the server to your MCP client configuration (e.g., `.mcp.json`):

```json
{
  "mcpServers": {
    "artdept": {
      "command": "/path/to/artdept-mcp/main.py",
      "env": {
        "OPENAI_API_KEY": "your-openai-api-key-here"
      }
    }
  }
}
```

## Quick Start Guide

### Basic Usage

Once connected through your MCP client, you can use natural language to generate design assets:

```
Generate a wireframe for a modern e-commerce homepage with header navigation, hero section, and product grid
```

```
Create a logo for a tech startup called "CloudSync" with a modern, minimalist style in blue and gray
```

```
Design a flat icon for a settings menu using a gear symbol
```

### Tool Examples

#### 1. Wireframe Generation

**Desktop wireframe:**
```json
{
  "tool": "new_wireframe",
  "arguments": {
    "id": "homepage-desktop",
    "prompt": "Modern SaaS landing page with navigation, hero section with CTA, feature highlights, testimonials, and footer",
    "device": "desktop",
    "style": "clean and minimal"
  }
}
```

**Mobile wireframe:**
```json
{
  "tool": "new_wireframe",
  "arguments": {
    "id": "checkout-mobile",
    "prompt": "Mobile checkout flow with product summary, shipping form, payment options, and confirmation",
    "device": "mobile",
    "style": "detailed with annotations"
  }
}
```

#### 2. Design System Creation

**Brand design system:**
```json
{
  "tool": "new_designsystem",
  "arguments": {
    "id": "fintech-brand",
    "prompt": "Professional fintech brand system with typography, colors, and visual identity elements",
    "n": 2,
    "type": "brand",
    "style": "corporate and trustworthy",
    "colors": "navy blue and gold accents"
  }
}
```

**UI component system:**
```json
{
  "tool": "new_designsystem",
  "arguments": {
    "id": "dashboard-ui",
    "prompt": "Admin dashboard UI components including buttons, forms, cards, and navigation elements",
    "n": 3,
    "type": "ui",
    "style": "modern dark theme",
    "colors": "dark gray with blue accents"
  }
}
```

#### 3. Logo Design

```json
{
  "tool": "new_logo",
  "arguments": {
    "id": "eco-solutions",
    "prompt": "Environmental consultancy logo with leaf or earth elements",
    "n": 3,
    "style": "modern and organic",
    "colors": "green and earth tones"
  }
}
```

#### 4. Icon Creation

```json
{
  "tool": "new_icon",
  "arguments": {
    "id": "notification-bell",
    "prompt": "Notification bell icon for mobile app",
    "n": 2,
    "style": "outline style",
    "colors": "monochrome"
  }
}
```

#### 5. Illustrations

```json
{
  "tool": "new_illustration",
  "arguments": {
    "id": "team-collaboration",
    "prompt": "Team of diverse professionals collaborating around a digital workspace",
    "n": 2,
    "size": "1536x1024",
    "style": "modern flat illustration"
  }
}
```

#### 6. Photography

```json
{
  "tool": "new_photo",
  "arguments": {
    "id": "office-workspace",
    "prompt": "Modern office workspace with natural lighting and plants",
    "n": 1,
    "size": "1536x1024",
    "style": "professional architectural photography"
  }
}
```

## Tool Reference

### new_wireframe

Generate UI/UX wireframes for desktop, mobile, or both platforms.

**Parameters:**
- `id` (required): Kebab-case identifier (e.g., "home-page", "checkout-flow")
- `prompt` (required): Natural language description of the wireframe
- `device`: Target device type ("desktop", "mobile", "both") - default: "both"
- `style`: Wireframe style (e.g., "minimalist", "detailed", "annotated")
- `save`: Directory to save images - default: "creative/wires/"

**Output:** JPG files with device-specific dimensions
- Desktop: 1536x1024
- Mobile: 1024x1536

### new_designsystem

Create comprehensive design systems for brand, UI, or UX purposes.

**Parameters:**
- `id` (required): Kebab-case identifier for the design system
- `prompt` (required): Natural language description
- `n` (required): Number of variations to generate (1-4)
- `type`: Type of design system ("brand", "ui", "ux") - default: "brand"
- `style`: Design style (e.g., "corporate", "modern", "playful")
- `colors`: Color palette specification
- `save`: Directory to save images - default: "creative/design-systems/"

**Output:** JPG files at 1536x1024 resolution

### new_logo

Generate professional logos with multiple variations.

**Parameters:**
- `id` (required): Kebab-case identifier for the logo
- `prompt` (required): Natural language description
- `n` (required): Number of variations to generate (1-4)
- `style`: Logo style (e.g., "minimalist", "vintage", "tech")
- `colors`: Color specification
- `save`: Directory to save images - default: "creative/logos/"

**Output:** PNG files at 1024x1024 resolution

### new_icon

Create scalable icons suitable for UI/UX applications.

**Parameters:**
- `id` (required): Kebab-case identifier for the icon
- `prompt` (required): Natural language description
- `n` (required): Number of variations to generate (1-4)
- `style`: Icon style (e.g., "flat", "outline", "3D")
- `colors`: Color specification
- `save`: Directory to save images - default: "creative/icons/"

**Output:** PNG files at 1024x1024 resolution

### new_illustration

Generate custom illustrations in various artistic styles.

**Parameters:**
- `id` (required): Kebab-case identifier for the illustration
- `prompt` (required): Natural language description
- `n` (required): Number of variations to generate (1-4)
- `size`: Image dimensions ("1024x1024", "1536x1024", "1024x1536") - default: "1024x1024"
- `style`: Illustration style (e.g., "watercolor", "vector", "sketch")
- `save`: Directory to save images - default: "creative/illustrations/"

**Output:** PNG files at specified dimensions

### new_photo

Create photorealistic images for any use case.

**Parameters:**
- `id` (required): Kebab-case identifier for the photo
- `prompt` (required): Natural language description
- `n` (required): Number of variations to generate (1-4)
- `size`: Image dimensions ("1024x1024", "1536x1024", "1024x1536") - default: "1024x1024"
- `style`: Photography style (e.g., "portrait", "landscape", "macro")
- `save`: Directory to save images - default: "creative/photos/"

**Output:** JPG files at specified dimensions

## Configuration

### Environment Variables

- `OPENAI_API_KEY` (required): Your OpenAI API key with `gpt-image-1` model access

### Output Directory Structure

The server creates organized directories for different asset types:

```
creative/
├── wires/              # Wireframes
├── design-systems/     # Design systems
├── logos/              # Logos
├── icons/              # Icons
├── illustrations/      # Illustrations
└── photos/             # Photorealistic images
```

### File Naming Convention

Generated files follow a consistent naming pattern:

- Single files: `{id}.{ext}`
- Multiple variations: `{id}-v{number}.{ext}`
- Device-specific: `{id}-{device}.{ext}`

Examples:
- `homepage-desktop.jpg`
- `logo-v1.png`
- `design-system-v2.jpg`

## Troubleshooting

### Common Issues

**1. Missing API Key**
```
Error: OPENAI_API_KEY environment variable is required
```
Solution: Set your OpenAI API key in the environment or .env file.

**2. API Rate Limits**
```
Error: Rate limit exceeded
```
Solution: Wait and retry, or upgrade your OpenAI plan for higher limits.

**3. Invalid Image Size**
```
Error: Invalid size parameter
```
Solution: Use only supported sizes: "1024x1024", "1536x1024", "1024x1536".

**4. File Save Errors**
```
Error: Failed to save image
```
Solution: Check directory permissions and ensure sufficient disk space.

### Debug Mode

Enable debug logging by setting the log level:

```python
logging.basicConfig(level=logging.DEBUG)
```

### API Limits

- `gpt-image-1` generates 1 image per request
- Maximum 4 variations per tool call
- Standard quality by default (faster, more cost-effective)
- Base64 response format for direct file saving

## Cost Considerations

Each image generation request to OpenAI incurs costs based on the `gpt-image-1` model pricing. The server uses standard quality by default for cost efficiency.

## Testing

The server includes a comprehensive test suite located in `test_server.py`:

```bash
# Run the test suite
uv run test_server.py
# or
python test_server.py
```

### Test Coverage

The test suite covers:
- All 6 image generation tools
- Parameter validation and constraints
- Error handling (API failures, file save errors)
- Base64 image saving functionality
- Prompt builder functions
- Tool call routing
- Multi-device wireframe generation
- Variation generation for multiple image types

## Support

For issues and feature requests:

1. Check the troubleshooting section above
2. Review OpenAI API documentation for `gpt-image-1` model
3. Verify MCP client configuration
4. Check server logs for detailed error information
5. Run the test suite to verify functionality

## License

This project follows the same license as the parent repository.
