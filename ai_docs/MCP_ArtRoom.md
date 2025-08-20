# MCP Server: ArtRoom

The purpose of this MCP is to provide a novel set of "design" tools to agents specialized in creative domains (graphic design, ux, illustration, etc), unlocking collaborative workflows with multi-modal coding agents.

## Feature Set:
- Wireframing
- Design Systems
- Logo design
- Icon design
- Photography
- Illustrations

## MCP Config:
- Save new server in `mcp/artroom-mcp/main.py`
- Configure new server in `.mcp.json`.
- Requires `OPENAI_API_KEY` env variable. (already added to .env)

---

## MCP Reference:

@ai_docs/mcp/*

## OpenAI Create Image API Reference:

@ai_docs/openai/create-image.md

---

# Tools to Implement:

## new_wireframe

Function to generate a wireframe based on natural language. Uses prompt engineering under the hood with specific instructions to get expected results (User prompt injected into a higher-order system prompt). Output image(s) saved to save directory with a standard formatted filename based on the id.

**Params:**
- `id` (str): The kebab-case identifier for the wireframe, eg "home-page", "global-nav"
- `prompt` (str): The natural language description of the wireframe.
- `device` (desktop|mobile|both): Sets size to either `1536x1024` or `1024x1536`, if both generate one then the other. Default to both.
- `style` (str): The style of the wireframe, e.g., "minimalist", "modern", "dense".
- `save` (str): The location to save the file eg: `creative/wires/` (default)

**Constants:**
- `background`: opaque
- `model`: gpt-image-1
- `output_format`: jpeg
- `n`: 1

## new_designsystem

Function to generate a design-system based on natural language. Uses prompt engineering under the hood with specific instructions to get expected results (User prompt injected into a higher-order system prompt). Output image(s) saved to save directory with a standard formatted filename based on the id.

**Params:**
- `id` (str): The kebab-case identifier for the design system.
- `prompt` (str): The natural language description of the design system.
- `n` (int): The number of variations to generate.
- `type` (brand|ui|ux): The type of design system. (default: brand)
- `style` (str): The style of the design system, e.g., "corporate", "modern", "ai".
- `colors` (str): The main color or palette to use, e.g., "blues", "orange yellow on white", "dark mode green".
- `save` (str): The location to save the file eg: `creative/design-systems/` (default)

**Constants:**
- `background`: opaque
- `model`: gpt-image-1
- `output_format`: jpeg
- `size`: 1536x1024


## new_logo

Function to generate a logo based on natural language. Uses prompt engineering under the hood with specific instructions to get expected results (User prompt injected into a higher-order system prompt). Output image(s) saved to save directory with a standard formatted filename based on the id.

**Params:**
- `id` (str): The kebab-case identifier for the logo.
- `prompt` (str): The natural language description of the logo.
- `n` (int): The number of variations to generate.
- `style` (str): The style of the logo, e.g., "corporate", "modern", "minimal".
- `colors` (str): The main color or palette to use, e.g., "black", "corporate", "#696969".
- `save` (str): The location to save the file eg: `creative/logos/` (default)

**Constants:**
- `background`: transparent
- `model`: gpt-image-1
- `output_format`: png
- `size`: 1024x1024


## new_icon

Function to generate a icon based on natural language. Uses prompt engineering under the hood with specific instructions to get expected results (User prompt injected into a higher-order system prompt). Output image(s) saved to save directory with a standard formatted filename based on the id.

**Params:**
- `id` (str): The kebab-case identifier for the icon.
- `prompt` (str): The natural language description of the icon.
- `n` (int): The number of variations to generate.
- `style` (str): The style of the icon, e.g., "corporate", "modern", "minimal".
- `colors` (str): The main color or palette to use, e.g., "black", "corporate", "#696969".
- `save` (str): The location to save the file eg: `creative/icons/` (default)

**Constants:**
- `background`: transparent
- `model`: gpt-image-1
- `output_format`: png
- `size`: 1024x1024


## new_illustration

Function to generate a illustration based on natural language. Uses prompt engineering under the hood with specific instructions to get expected results (User prompt injected into a higher-order system prompt). Output image(s) saved to save directory with a standard formatted filename based on the id.

**Params:**
- `id` (str): The kebab-case identifier for the illustration.
- `prompt` (str): The natural language description of the illustration.
- `n` (int): The number of variations to generate.
- `size` (string): The size of the image to generate. "1024x1024" (default), "1536x1024", "1024x1536"
- `style` (str): The style of the illustration, e.g., "corporate", "line drawing", "crayon".
- `save` (str): The location to save the file eg: `creative/illustrations/` (default)

**Constants:**
- `background`: transparent
- `model`: gpt-image-1
- `output_format`: png


## new_photo

Function to generate a photo based on natural language. Uses prompt engineering under the hood with specific instructions to get expected results (User prompt injected into a higher-order system prompt). Output image(s) saved to save directory with a standard formatted filename based on the id.

**Params:**
- `id` (str): The kebab-case identifier for the photo.
- `prompt` (str): The natural language description of the photo.
- `n` (int): The number of variations to generate.
- `size` (string): The size of the image to generate. "1024x1024" (default), "1536x1024", "1024x1536"
- `style` (str): The style of the photo, e.g., "cinematic", "black&white", "candid".
- `save` (str): The location to save the file eg: `creative/photos/` (default)

**Constants:**
- `background`: opaque
- `model`: gpt-image-1
- `output_format`: jpg
