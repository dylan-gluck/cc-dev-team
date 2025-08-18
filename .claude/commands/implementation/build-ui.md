---
description: Build UI components and templates for a feature
argument-hint: [feature/component name]
---

## UI Implementation Task

Build the user interface for: $ARGUMENTS

### Workflow

Use the ux-eng agent to:

1. **Component Development**
   - Review design specifications
   - Search for existing shadcn-ui components
   - Build new components as needed
   - Ensure full responsiveness across all devices

2. **Template Creation**
   - Create page templates
   - Implement layouts
   - Add mock data matching data models
   - Ensure accessibility standards

3. **Testing**
   - Use Playwright to test across device sizes:
     - Mobile: 375px, 414px
     - Tablet: 768px, 1024px  
     - Desktop: 1280px, 1440px, 1920px
   - Validate touch interactions
   - Check accessibility

4. **Documentation**
   - Document component APIs
   - Provide usage examples
   - Note responsive behavior
   - Include visual examples

### Deliverables
- Reusable UI components
- Page templates
- Responsive design implementation
- Component documentation
- Playwright test results
- Mock data structures

All components must be beautiful, polished, and work seamlessly across all devices.