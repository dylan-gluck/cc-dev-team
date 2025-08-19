---
allowed-tools: Task, Read, Write, Edit, TodoWrite, WebSearch, WebFetch, mcp__firecrawl__*
argument-hint: <package-name> [url | feature to scrape | --depth=0-3]
description: Fetch and condense technical documentation for a package or library
---

# Fetch Technical Documentation

Use the doc-expert agent to fetch, analyze, and condense technical documentation for a specified package or library.

## Arguments
- Package name: $ARGUMENTS

## Task for doc-expert Agent

You are tasked with fetching and condensing technical documentation for a package or library. Parse the arguments to determine:
1. **Package name** (required) - the first argument
2. **URL or feature** (optional) - if provided, specific documentation to fetch
3. **Depth** (optional) - if --depth=X is specified, crawl depth (0-3)

### Your responsibilities:

1. **Research Phase**:
   - If a URL is provided, scrape that specific documentation
   - If a feature/topic is provided, search for relevant documentation
   - If neither is provided, find the official documentation for the package
   - Use the specified depth for crawling (default to 1 if not specified)

2. **Analysis Phase**:
   - Extract key information: installation, configuration, API reference, common patterns
   - Identify core concepts and best practices
   - Note important warnings, deprecations, or version-specific information
   - Focus on practical, actionable information for developers

3. **Documentation Creation**:
   - Create the output directory: `ai_docs/<package-name>/`
   - Decide whether to create a single consolidated document or multiple focused documents based on:
     - Volume of content (split if > 500 lines)
     - Logical separation of topics (e.g., API reference vs guides)
     - User's likely access patterns
   - Write clear, well-structured markdown with:
     - Table of contents
     - Code examples where relevant
     - Links to original sources
     - Last updated date and version info

4. **File Organization**:
   - Single file: `ai_docs/<package-name>/README.md` or `ai_docs/<package-name>/<package-name>.md`
   - Multiple files: Use descriptive names like:
     - `api-reference.md`
     - `getting-started.md`
     - `configuration.md`
     - `examples.md`

### Output Requirements:
- All documentation must be in markdown format
- Include source URLs and fetch dates
- Preserve important code examples
- Maintain a balance between comprehensiveness and conciseness
- Focus on information most useful for active development

### Example Usage Patterns:
- `/agent:doc-fetch react` - Fetch general React documentation
- `/agent:doc-fetch fastapi https://fastapi.tiangolo.com/tutorial/` - Fetch specific FastAPI tutorial
- `/agent:doc-fetch pandas dataframes --depth=2` - Search for pandas dataframe docs with depth 2

Begin by parsing the provided arguments and determining your fetch strategy.