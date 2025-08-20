# Creative Team Enhancements

The goals of the creative team are:
- Define design direction, language, tone
- Define & maintain design system
- Create wireframes from spec (image-gen or python tool)
- Generate assets (photos, illustration, logos)
- Fetch stock photos, company logos, web assets

## MCP Servers

1. Server with tools to fetch stock photos from unsplash / pexels. Use a research agent to find available mcp servers. If none exist we may have to create one but I would be surprised.

**Research Summary:** Multiple production-ready MCP servers exist for stock photo integration. Key options include Unsplash Smart MCP Server (AI-powered with framework integration), Pexels MCP Server (comprehensive search and media access), and multi-platform servers like Stock Images MCP and Stocky that support both Unsplash and Pexels simultaneously. All servers handle attribution requirements and offer easy installation via Node.js. API requirements are minimal - Unsplash offers 50 requests/hour free, Pexels provides 200 requests/hour free. Installation methods include Desktop Extensions (DXT), manual setup, or Docker deployment.

https://github.com/Zulelee/stock-images-mcp

2. Server with tools to generate images. I think flux is the best model, but am interested to see what options are available. It may make sense to have multiple options and route based on request. Use a research agent to find available MCP solutions, we might want to create this one to get the flexibility we want.

**Research Summary:** Your instinct about Flux is correct - it leads in photorealism and text rendering quality. Multiple MCP servers exist: MCP Flux Studio (most comprehensive with flux.1.1-pro support), FAL FLUX.1 Kontext (frontier model), and various Replicate implementations. For multi-provider routing, consider combining Flux Studio (primary), Stability AI MCP Server (editing/manipulation), and PiAPI (Midjourney access). The ecosystem supports easy switching between providers with standardized MCP interfaces. Cost-effective options include local Stable Diffusion servers, while premium services range from $0.01-$0.25 per operation. Quality rankings show Flux > Midjourney > Stable Diffusion > DALL-E 3 for photorealism, with opposite ranking for ease of use.

## Wireframe Generation

1. Use a research agent to find available tools for programatically generating wireframes. Input should be some kind of data structure, Output should be jpg, png, svg. Think about how this could be implemented as an MCP server. Methods to generate programatically, or by natural language using an LLM.

**Research Summary:** Both programmatic and AI-powered wireframe generation are viable. For natural language approaches, Frame0 MCP Server already exists and demonstrates feasibility, while academic research shows WireGen achieving 77.5% success with fine-tuned GPT-3.5. Programmatic tools include JSON Crack (JSON/XML to visual graphs), svgwrite library for Python (including 3D wireframes), and React-based tools like Wireframe Studio. MCP server implementation is straightforward using Node.js 22+ with the Frame0 reference implementation. Input formats range from natural language prompts to JSON schemas, XML markup, and YAML configurations. Output supports SVG, PNG/JPEG, and direct HTML/CSS code generation. The ecosystem offers excellent workflow integration potential with design systems, real-time collaboration, and CI/CD pipeline integration.
