---
allowed-tools: WebSearch, WebFetch
description: Search for stock photos across multiple platforms
argument-hint: <search-terms> [style] [usage-type]
model: haiku
---

# Stock Photo Search

Find relevant stock images across multiple platforms for creative projects.

## Context
Photo search criteria: $ARGUMENTS

## Task
Search for high-quality stock photos that match the specified requirements across multiple stock photo platforms.

Parse search requirements:
1. **Search terms** (subject, concept, mood)
2. **Style preference** (realistic, illustration, abstract, minimal)
3. **Usage type** (commercial, editorial, both)
4. **Color preferences** (if specified)
5. **Orientation** (landscape, portrait, square)

### Search Strategy
Use WebSearch to find images from:
- Unsplash (free high-quality photos)
- Pexels (free stock photos)
- Pixabay (free images and videos)
- Burst by Shopify (free stock photos)
- StockVault (free photos and graphics)
- Freepik (free and premium resources)

For each platform, search with variations of the terms and collect:
- Direct image URLs
- Photographer/creator attribution
- License type and restrictions
- Available resolutions
- Related/similar images

## Expected Output
- Curated list of 10-15 best matches
- Image previews with descriptions
- Direct download links
- License information for each image
- Attribution requirements
- Similar image suggestions
- Color palette of selected images
- Usage recommendations based on project type

## Examples
- `/stock-photos "remote work laptop coffee" minimal commercial`
- `/stock-photos "nature sustainability" abstract editorial`
- `/stock-photos "diverse team meeting" realistic horizontal`

## Constraints
- Prioritize royalty-free and CC0 licensed images
- Clearly indicate any attribution requirements
- Filter for high resolution (minimum 2000px wide)
- Avoid watermarked previews
- Check usage rights for commercial projects