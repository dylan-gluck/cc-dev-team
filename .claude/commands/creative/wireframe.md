---
allowed-tools: Task
description: Generate quick wireframe designs for apps and websites
argument-hint: <device-type> <description> [style-preference]
model: haiku
---

# Wireframe Generation

Create professional wireframe designs based on user requirements.

## Context
User request: $ARGUMENTS

## Task
Delegate to the creative-wireframe agent to generate a wireframe design based on the provided specifications.

Parse the user input to identify:
1. **Device type** (e.g., mobile, tablet, desktop, responsive)
2. **Description** of the interface/screen to wireframe
3. **Style preference** (optional: low-fidelity, high-fidelity, sketch-style)

If device type is not specified, ask for clarification.

### Delegation Instructions
Use the Task tool to delegate to creative-wireframe with:
- Clear device specifications and viewport dimensions
- Detailed description of required UI elements
- Any specific interactions or user flows
- Preferred wireframe style and detail level

## Expected Output
- ASCII or SVG wireframe visualization
- Component breakdown with annotations
- Interaction flow notes
- Responsive breakpoint considerations (if applicable)
- Suggestions for UI/UX improvements

## Examples
- `/wireframe mobile "login screen with social auth"`
- `/wireframe desktop "dashboard with analytics charts" high-fidelity`
- `/wireframe responsive "e-commerce product page"`

## Constraints
- Focus on structure and layout, not visual design
- Include clear annotations for interactive elements
- Consider accessibility in the wireframe structure