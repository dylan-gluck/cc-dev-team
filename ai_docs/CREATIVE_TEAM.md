# Creative Team Implementation

The creative team provides comprehensive visual design and content creation capabilities through a coordinated team of specialists orchestrated by the creative-director agent.

## Team Architecture

### Core Agents

**Creative Director** (`creative-director`)
- **Role**: Team orchestrator and design leadership
- **Tools**: Task, Read, Grep, LS, TodoWrite
- **Responsibilities**: Coordinates all creative team members, maintains brand integrity, ensures design excellence
- **Model**: Opus (for complex creative coordination)

**Copywriter** (`creative-copywriter`)
- **Role**: Brand messaging and content creation
- **Tools**: Read, Write, Edit, Grep, LS, TodoWrite
- **Responsibilities**: Website copy, email campaigns, social media content, product descriptions, brand voice development
- **Model**: Sonnet

**Asset Creation Specialists**:
- **UX Lead** (`creative-ux-lead`): Design systems, component libraries, accessibility standards
- **Wireframe Designer** (`creative-wireframe`): Information architecture, user flows, prototypes
- **Logo Designer** (`creative-logo`): Brand identity, logo variations, usage guidelines
- **Illustrator** (`creative-illustrator`): Custom graphics, icon systems, visual metaphors
- **Photographer** (`creative-photographer`): Photography style guides, image editing, asset optimization

All asset-focused creative agents have access to:
- Read, Write, LS, TodoWrite
- Relevant MCP tools (artdept-mcp, stock-images-mcp)

### Orchestration Pattern

The creative-director uses the **Task delegation pattern** to coordinate team members:

```python
# Parallel execution for foundation work
await Task.run([
    {"agent": "creative-ux-lead", "task": "Define design system"},
    {"agent": "creative-logo", "task": "Develop brand identity"},
    {"agent": "creative-copywriter", "task": "Establish brand voice"}
])

# Sequential for dependent work
wireframes = await Task.run("creative-wireframe", "Create page layouts")
visuals = await Task.run([
    {"agent": "creative-illustrator", "task": "Design icons and graphics"},
    {"agent": "creative-photographer", "task": "Plan photography needs"}
])
```

## Available Slash Commands

The creative team provides several slash commands for quick asset generation:

### `/creative-assets`
**Generate multiple creative assets in a coordinated campaign**
```bash
/creative-assets <asset-types> <brand/project> [theme]
```

**Examples:**
- `/creative-assets "social,email,banners" "Summer Sale Campaign" vibrant`
- `/creative-assets "full-brand-package" "StartupX" modern-tech`
- `/creative-assets "conference-materials" "DevConf 2024" professional`

**Output:**
- Social media templates (multiple platforms)
- Email newsletter designs
- Web banners (various sizes)
- Print materials (if requested)
- Presentation templates
- Brand collateral
- Consistent visual language across all assets
- Copywriting for each asset
- Export specifications and file formats
- Usage guidelines document

### `/wireframe`
**Generate quick wireframe designs for apps and websites**
```bash
/wireframe <device-type> <description> [style-preference]
```

**Examples:**
- `/wireframe mobile "login screen with social auth"`
- `/wireframe desktop "dashboard with analytics charts" high-fidelity`
- `/wireframe responsive "e-commerce product page"`

**Output:**
- ASCII or SVG wireframe visualization
- Component breakdown with annotations
- Interaction flow notes
- Responsive breakpoint considerations
- UI/UX improvement suggestions

### `/logo`
**Design logos with brand identity considerations**
```bash
/logo <brand-name> [industry] [style-keywords]
```

**Examples:**
- `/logo "TechNova" software minimal`
- `/logo "Green Earth Cafe" restaurant eco-friendly organic`
- `/logo "Phoenix Financial" consulting professional trustworthy`

**Output:**
- Multiple logo concepts (3-5 variations)
- ASCII art or SVG representations
- Color palette recommendations with hex codes
- Typography choices and rationale
- Logo variations (horizontal, vertical, icon-only)
- Usage guidelines and minimum sizes
- Mockups showing logo in context

### `/stock-photos`
**Search for stock photos across multiple platforms**
```bash
/stock-photos <search-terms> [style] [usage-type]
```

**Examples:**
- `/stock-photos "remote work laptop coffee" minimal commercial`
- `/stock-photos "nature sustainability" abstract editorial`
- `/stock-photos "diverse team meeting" realistic horizontal`

**Output:**
- Curated list of 10-15 best matches
- Image previews with descriptions
- Direct download links
- License information for each image
- Attribution requirements
- Color palette of selected images

### `/design-system`
**Create comprehensive design systems**
```bash
/design-system <project-name> <style-direction> [platform]
```

**Output:**
- Color palettes and design tokens
- Typography scales and font choices
- Spacing systems and grid layouts
- Component libraries
- Design patterns and guidelines

### `/brand-copy`
**Generate brand messaging and marketing copy**
```bash
/brand-copy <content-type> <brand/product> [tone]
```

**Output:**
- Headlines and taglines
- Website copy sections
- Email campaign content
- Social media copy variations
- SEO-optimized content

## Creative Workflow Examples

### Quick Brand Package Generation
```bash
# Generate a complete brand package
/creative-assets "full-brand-package" "EcoTech Startup" modern-sustainable

# This triggers the creative-director to:
# 1. Coordinate logo design with creative-logo
# 2. Develop brand copy with creative-copywriter  
# 3. Create design system with creative-ux-lead
# 4. Generate marketing assets with creative-illustrator
# 5. Plan photography with creative-photographer
```

### Rapid Prototyping Workflow
```bash
# Step 1: Create wireframes
/wireframe responsive "SaaS dashboard with analytics"

# Step 2: Generate supporting assets
/stock-photos "business analytics dashboard screens" modern
/logo "DataFlow Pro" saas minimal clean

# Step 3: Create complete design system
/design-system "DataFlow Pro" modern-saas web
```

### Campaign Asset Creation
```bash
# Generate coordinated campaign materials
/creative-assets "social,email,web-banners,print" "Q4 Product Launch" bold-innovative

# Follow up with specific copy
/brand-copy "email-campaign" "Q4 Product Launch" excited-professional
```

## MCP Tools Integration

The creative team leverages two main MCP servers for asset generation:

### ArtDept MCP Server (`artdept-mcp`)
Located at `/mcp/artdept-mcp/main.py`, this server provides AI-powered creative asset generation:

#### `mcp__artdept-mcp__new_wireframe`
```typescript
mcp__artdept-mcp__new_wireframe(id: string, prompt: string, device?: string, style?: string, save?: string): ImageResult
```
Generates UI/UX wireframes for desktop, mobile, or both platforms.

#### `mcp__artdept-mcp__new_designsystem`
```typescript
mcp__artdept-mcp__new_designsystem(id: string, prompt: string, n: number, type?: string, colors?: string, style?: string, save?: string): ImageResult[]
```
Generates comprehensive design systems with multiple variations.

#### `mcp__artdept-mcp__new_logo`
```typescript
mcp__artdept-mcp__new_logo(id: string, prompt: string, n: number, colors?: string, style?: string, save?: string): ImageResult[]
```
Generates professional logo designs with specified styles and colors.

#### `mcp__artdept-mcp__new_icon`
```typescript
mcp__artdept-mcp__new_icon(id: string, prompt: string, n: number, colors?: string, style?: string, save?: string): ImageResult[]
```
Generates scalable icon designs for various uses.

#### `mcp__artdept-mcp__new_illustration`
```typescript
mcp__artdept-mcp__new_illustration(id: string, prompt: string, n: number, size?: string, style?: string, save?: string): ImageResult[]
```
Generates custom illustrations in various styles and sizes.

#### `mcp__artdept-mcp__new_photo`
```typescript
mcp__artdept-mcp__new_photo(id: string, prompt: string, n: number, size?: string, style?: string, save?: string): ImageResult[]
```
Generates photorealistic images with specified dimensions.

### Stock Images MCP Server (`stock-images-mcp`)
Provides access to royalty-free stock images from multiple platforms:

#### `mcp__stock-images-mcp__search_stock_images`
```typescript
mcp__stock-images-mcp__search_stock_images(query: string, platform?: string, per_page?: number): StockImages[]
```
Searches for stock images across multiple platforms (Pexels, Unsplash, Pixabay).

## Best Practices for Creative Asset Generation

### Quick Asset Creation
1. **Use slash commands for rapid prototyping**: Start with `/wireframe` or `/logo` for immediate results
2. **Leverage the creative-director for complex projects**: Delegate comprehensive campaigns to the orchestrator
3. **Combine MCP tools with human creativity**: Use AI-generated assets as starting points for refinement

### Brand Consistency
1. **Always begin with design system establishment**: Use `/design-system` or creative-ux-lead for foundation
2. **Document brand guidelines**: Maintain consistent color palettes, typography, and messaging
3. **Review all assets through creative-director**: Ensure brand alignment across all deliverables

### Efficient Workflows
1. **Parallel execution for independent assets**: Generate logos, copy, and graphics simultaneously
2. **Sequential dependencies**: Create design system first, then component libraries and specific assets
3. **Iterative refinement**: Use feedback loops between creative team members

### Team Coordination
1. **Creative-director orchestrates complex projects**: Use Task delegation for multi-agent coordination
2. **Specialist agents for focused work**: Direct specific tasks to relevant team members
3. **Cross-team collaboration**: Interface with product, engineering, and marketing teams

## Configuration and Setup

### MCP Server Configuration
The creative team requires the following MCP servers to be configured in `.mcp.json`:

```json
{
  "mcpServers": {
    "artdept-mcp": {
      "command": "uv",
      "args": ["run", "mcp/artdept-mcp/main.py"],
      "env": {
        "OPENAI_API_KEY": "${OPENAI_API_KEY}"
      }
    },
    "stock-images-mcp": {
      "command": "uvx",
      "args": ["git+https://github.com/Zulelee/stock-images-mcp"],
      "env": {
        "UNSPLASH_API_KEY": "${UNSPLASH_API_KEY}",
        "PEXELS_API_KEY": "${PEXELS_API_KEY}",
        "PIXABAY_API_KEY": "${PIXABAY_API_KEY}"
      }
    }
  }
}
```

### Required Environment Variables
- `OPENAI_API_KEY`: For AI-powered asset generation through artdept-mcp
- `UNSPLASH_API_KEY`: For Unsplash stock image access
- `PEXELS_API_KEY`: For Pexels stock image access  
- `PIXABAY_API_KEY`: For Pixabay stock image access

## Error Handling and Troubleshooting

### Common Issues
1. **MCP Server Connection Failures**: Verify environment variables and server startup
2. **Asset Generation Timeouts**: Reduce complexity or break into smaller tasks
3. **Brand Inconsistency**: Always route through creative-director for coordination
4. **Tool Access Errors**: Ensure agents have proper tool permissions

### Recovery Strategies
1. **Fallback to manual creation**: Use traditional design tools when MCP fails
2. **Incremental generation**: Create assets piece by piece rather than all at once
3. **Alternative platforms**: Switch between stock image platforms if one fails
4. **Simplified prompts**: Reduce complexity if AI generation struggles

## Future Enhancements

### Planned Features
1. **Interactive design reviews**: Real-time collaboration between team members
2. **Version control integration**: Automatic asset versioning and rollback
3. **Performance optimization**: Faster asset generation and processing
4. **Extended platform support**: Additional stock image and design platforms
5. **Advanced brand governance**: Automated brand compliance checking

### Integration Opportunities
1. **Development workflow integration**: Direct handoff to engineering teams
2. **Marketing automation**: Automated campaign asset deployment
3. **User feedback loops**: Direct user testing integration for design validation
4. **Analytics integration**: Performance tracking for creative assets
