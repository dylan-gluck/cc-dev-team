---
allowed-tools: Task, Write
description: Create comprehensive design systems with brand guidelines
argument-hint: <brand-name> [primary-color] [style-direction]
model: opus
---

# Design System Creation

Develop a complete design system with components, patterns, and brand guidelines.

## Context
Design system requirements: $ARGUMENTS

## Task
Delegate to the creative-ux-lead agent to architect a comprehensive design system for the brand.

Parse user input for:
1. **Brand name** and identity basics
2. **Primary brand color** (hex or description)
3. **Style direction** (modern, classic, playful, corporate, etc.)
4. **Target platforms** (web, mobile, both)
5. **Existing brand assets** to incorporate

### Delegation Instructions
Use the Task tool to delegate to creative-ux-lead with instructions to create:

**Foundation Elements:**
- Color system (primary, secondary, semantic colors)
- Typography scale and font pairings
- Spacing and grid system
- Border radius and shadow standards
- Animation and transition guidelines

**Component Library:**
- Buttons (all states and variants)
- Form elements and inputs
- Cards and containers
- Navigation patterns
- Modals and overlays
- Data display components

**Documentation:**
- Usage guidelines for each component
- Accessibility requirements
- Responsive behavior rules
- Do's and don'ts examples

## Expected Output
- Complete color palette with accessibility ratios
- Typography system with hierarchy
- Component specifications in CSS/design tokens
- Layout grid and spacing system
- Icon style guidelines
- Motion and interaction principles
- Code snippets for implementation
- Visual examples and documentation

## Examples
- `/design-system "ModernCo" #0066CC minimal`
- `/design-system "PlayfulBrand" vibrant friendly`
- `/design-system "Enterprise Solutions" navy corporate professional`

## Constraints
- Ensure WCAG 2.1 AA compliance minimum
- Support both light and dark modes
- Maintain consistency across all components
- Include responsive breakpoints
- Document all design decisions