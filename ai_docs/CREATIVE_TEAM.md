# Creative Team Enhancements

The goals of the creative team are:
- Define design direction, language, tone
- Define & maintain design system
- Create wireframes from spec (image-gen or python tool)
- Generate assets (photos, illustration, logos)
- Fetch stock photos, company logos, web assets

## MCP Servers

1. Server with tools to fetch stock photos from unsplash / pexels. Use a research agent to find available mcp servers. If none exist we may have to create one but I would be surprised.
2. Server with tools to generate images. I think flux is the best model, but am interested to see what options are available. It may make sense to have multiple options and route based on request. Use a research agent to find available MCP solutions, we might want to create this one to get the flexibility we want.

## Wireframe Generation

1. Use a research agent to find available tools for programatically generating wireframes. Input should be some kind of data structure, Output should be jpg, png, svg.
2. Think about how this could be implemented as an MCP server. Methods to generate programatically, or by natural language using an LLM.
