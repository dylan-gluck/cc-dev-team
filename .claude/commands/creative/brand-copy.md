---
allowed-tools: Task, Write
description: Generate brand messaging, taglines, and marketing copy
argument-hint: <brand-name> <content-type> [tone] [audience]
model: sonnet
---

# Brand Copy Generation

Create compelling brand messaging and marketing copy aligned with brand voice.

## Context
Copy requirements: $ARGUMENTS

## Task
Delegate to the creative-copywriter agent to develop brand messaging and copy.

Extract from the request:
1. **Brand name** and industry
2. **Content type** (tagline, website copy, ad copy, email, social media, etc.)
3. **Brand tone** (professional, friendly, bold, inspirational, etc.)
4. **Target audience** (demographics, interests, pain points)
5. **Key messages** or value propositions
6. **Call-to-action** requirements

### Delegation Instructions
Use the Task tool to delegate to creative-copywriter with:
- Brand identity and positioning details
- Specific content types and formats needed
- Tone of voice guidelines
- Target audience personas
- Key benefits and differentiators
- Competitor messaging to differentiate from
- SEO keywords (if applicable)
- Character/word limits for each piece

Request creation of:
- Primary brand tagline
- Alternative tagline options
- Elevator pitch (30-second version)
- Website hero copy
- Product/service descriptions
- Social media bio variations
- Email subject lines
- Call-to-action variations

## Expected Output
- **Brand Tagline:** 3-5 options with rationale
- **Hero Copy:** Headline, subheadline, and body text
- **Value Propositions:** Clear benefit statements
- **Social Media Copy:** Platform-specific variations
- **Email Templates:** Subject lines and body copy
- **Ad Copy:** Multiple versions for A/B testing
- **Tone Guide:** Examples of do's and don'ts
- **Messaging Framework:** Key themes and proof points

## Examples
- `/brand-copy "EcoTech" website-copy sustainable professional`
- `/brand-copy "FitLife App" social-media motivational millennials`
- `/brand-copy "Quantum Security" tagline innovative enterprise`

## Constraints
- Maintain consistent brand voice across all copy
- Include emotional and rational appeals
- Optimize for readability and scannability
- Consider SEO without sacrificing quality
- Avoid jargon unless audience-appropriate
- Include clear calls-to-action
- Test different message angles