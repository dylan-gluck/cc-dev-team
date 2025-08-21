---
allowed-tools: Task
description: Generate multiple creative assets in a coordinated campaign
argument-hint: <asset-types> <brand/project> [theme]
model: sonnet
---

# Creative Assets Generation

Produce a comprehensive set of creative assets for marketing and branding needs.

## Context
Asset requirements: $ARGUMENTS

## Task
Delegate to the creative-director agent to orchestrate the creation of multiple creative assets.

Parse the request to identify:
1. **Asset types needed** (logos, banners, social media, email templates, etc.)
2. **Brand or project name**
3. **Campaign theme or message**
4. **Target platforms and sizes**
5. **Deadline or priority order**

### Delegation Instructions
Use the Task tool to delegate to creative-director with:
- Complete list of required assets with specifications
- Brand guidelines or style preferences
- Target audience and campaign goals
- Platform-specific requirements (social media sizes, etc.)
- Content themes and messaging
- Any existing assets to maintain consistency with

The creative-director should coordinate with:
- creative-illustrator for visual elements
- creative-copywriter for messaging
- creative-ux-lead for web/app assets
- creative-logo for brand marks
- Other specialists as needed

## Expected Output
- Complete asset package including:
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

## Examples
- `/creative-assets "social,email,banners" "Summer Sale Campaign" vibrant`
- `/creative-assets "full-brand-package" "StartupX" modern-tech`
- `/creative-assets "conference-materials" "DevConf 2024" professional`

## Constraints
- Maintain brand consistency across all assets
- Optimize file sizes for intended platforms
- Include source files and editable formats
- Follow platform-specific best practices
- Ensure accessibility in all designs