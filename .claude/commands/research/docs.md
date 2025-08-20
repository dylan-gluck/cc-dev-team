---
allowed-tools: Task, Read, Write, Edit, TodoWrite, WebSearch, WebFetch, mcp__freecrawl__*
argument-hint: <package-name> [url1 url2 ...] [--depth=0-3]
description: Fetch and condense technical documentation for packages or libraries (supports multiple URLs)
---

# Fetch Technical Documentation

Use the engineering-docs agent(s) to fetch, analyze, and condense technical documentation for specified packages or libraries. When multiple URLs are provided, agents will work in parallel for efficient fetching.

## Arguments
- Package name: $ARGUMENTS

## Parallel Fetching Strategy

Parse the arguments to determine the fetching approach:
1. **Single package with no URLs**: Use one engineering-docs agent to find and fetch official docs
2. **Single package with one URL**: Use one engineering-docs agent for that specific URL
3. **Multiple URLs provided**: Launch multiple engineering-docs agents in parallel, one per URL
4. **Depth flag**: Apply --depth=X (0-3) to all fetch operations

### For Multiple URL Handling:

When multiple URLs are detected in the arguments:
1. Split the URLs into separate fetch tasks
2. Launch engineering-docs agents in parallel using multiple Task tool invocations in a single message
3. Each agent should:
   - Focus on their assigned URL
   - Create documentation in a structured subfolder
   - Return a summary of what was fetched
4. After all agents complete, provide a consolidated summary

### Task Template for Each engineering-docs Agent

You are tasked with fetching and condensing technical documentation. Your specific assignment:

**URL to fetch**: [Assigned URL from the argument list]
**Package context**: [Package name if provided]
**Crawl depth**: [Depth value if --depth specified, otherwise 1]

### Your responsibilities:

1. **Research Phase**:
   - Fetch documentation from your assigned URL
   - Use freecrawl tools (mcp__freecrawl__scrape, crawl, search, deep_research) as primary method
   - Fall back to WebFetch only if freecrawl fails
   - Apply the specified crawl depth for comprehensive coverage

2. **Analysis Phase**:
   - Extract key information: installation, configuration, API reference, common patterns
   - Identify core concepts and best practices
   - Note important warnings, deprecations, or version-specific information
   - Focus on practical, actionable information for developers

3. **Documentation Creation**:
   - Create the output directory: `ai_docs/<package-name>/` or `ai_docs/<url-based-name>/`
   - For parallel fetches, use descriptive subfolder names to avoid conflicts
   - Decide on single vs multiple document structure based on content volume
   - Write clear, well-structured markdown with proper metadata

4. **File Organization**:
   - For parallel fetches, organize by source:
     - `ai_docs/<package-name>/<source-1>/`
     - `ai_docs/<package-name>/<source-2>/`
   - Use descriptive filenames that indicate content type

### Output Requirements:
- All documentation must be in markdown format
- Include source URLs and fetch dates
- Preserve important code examples
- Maintain a balance between comprehensiveness and conciseness
- Return a clear summary of what was fetched and where it was saved

### Example Usage Patterns:
- `/research:fetch react` - Fetch general React documentation
- `/research:fetch fastapi https://fastapi.tiangolo.com/tutorial/` - Single URL fetch
- `/research:fetch mcp https://modelcontextprotocol.io https://github.com/modelcontextprotocol/python-sdk` - Parallel fetch from multiple sources
- `/research:fetch tensorflow https://tensorflow.org/guide https://tensorflow.org/api_docs --depth=2` - Multiple URLs with depth

Begin by parsing the provided arguments and determining whether to use single or parallel agent strategy.
