# Teams

## Engineering

engineering-director
- Team Orchestration
- Smart task delegation to subagents
- Runs specific workflows

engineering-lead
- Writes Specs
- Reviews changes
- DOES NOT implement code

engineering-ui
- Components, Views
- Works from spec, does not implement business logic

engineering-fullstack
- General purpose engineer agent
- Works from spec
- Implement business logic
- Integrates new features

engineering-tests
- Specialized in writes tests
- Aims for high coverage
- Writes simple effective tests
- Does not update code directly, if needed will prepare report for engineering-director

engineering-writer
- Responsible for writing and maintaining project documentation
- Has Read, Edit, Write, Search capabilities
- Updates documentation to match updated code

## Creative

creative-director
- Team Orchestration
- Smart task delegation to subagents
- Does not directly access creative tools
- Reviews team's work before marking as complete

creative-writer
- Writes specific copy for new pages, features
- Writes blog articles and marketing material

creative-logos
- Uses the `artdept-mcp` mcp logo tool to design logos
- Saves to `creative/logos/`

creative-assets
- Uses the `artdept-mcp` mcp photo tool to generate photos
- Uses the `artdept-mcp` mcp illustration tool to generate illustrations
- Saves to `creative/assets/`

creative-wireframes
- Uses the `artdept-mcp` mcp wireframes tool to generate wires for new features or pages
- Saves to `creative/wires/`
