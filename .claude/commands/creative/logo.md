---
allowed-tools: Task
description: Design logos with brand identity considerations
argument-hint: <brand-name> [industry] [style-keywords]
model: sonnet
---

# Logo Design Workflow

Create unique logo designs aligned with brand identity requirements.

## Context
Brand requirements: $ARGUMENTS

## Task
Delegate to the creative-logo agent to develop a comprehensive logo design based on the brand specifications.

Extract from user input:
1. **Brand name** (required)
2. **Industry/sector** (helps determine appropriate style)
3. **Style keywords** (modern, classic, playful, minimal, etc.)
4. **Color preferences** (if mentioned)
5. **Target audience** (if specified)

### Delegation Instructions
Use the Task tool to delegate to creative-logo with:
- Complete brand name and any tagline
- Industry context and competitor landscape
- Style preferences and inspiration keywords
- Color palette suggestions or restrictions
- Usage contexts (web, print, merchandise, etc.)
- Any symbols or imagery to incorporate or avoid

## Expected Output
- Multiple logo concepts (3-5 variations)
- ASCII art or SVG representations
- Color palette recommendations with hex codes
- Typography choices and rationale
- Logo variations (horizontal, vertical, icon-only)
- Usage guidelines and minimum sizes
- Mockups showing logo in context

## Examples
- `/logo "TechNova" software minimal`
- `/logo "Green Earth Cafe" restaurant eco-friendly organic`
- `/logo "Phoenix Financial" consulting professional trustworthy`

## Constraints
- Ensure scalability from business card to billboard
- Consider both color and monochrome versions
- Maintain legibility at small sizes
- Avoid trending elements that may quickly date the design
