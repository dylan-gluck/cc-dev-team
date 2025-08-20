---
allowed-tools: Task
description: Generate new slash commands using the command-creator agent
argument-hint: /command:name <params> [description]
---

# Generate Command
Use the command-creator agent to create new slash commands with proper structure and filepath.

## User Input:
$ARGUMENTS

## Task for command-creator Agent

You are tasked with creating a new slash command based on the user's specifications. Parse the input to extract:

1. **Command syntax** (e.g., "/research:fetch <package-name>")
2. **Command description** and purpose
3. **Any specified parameters or arguments**

### Critical Requirements:

#### Filepath Determination:
- Extract the command path from the syntax (e.g., "/research:fetch" → ".claude/commands/research/fetch.md")
- For commands with colons, split into directory and filename:
  - `/category:action` → `.claude/commands/category/action.md`
  - `/simple-command` → `.claude/commands/simple-command.md`
- Always create the necessary directory structure

#### Command Structure:
- Include proper frontmatter with:
  - `allowed-tools`: Minimal set of required tools
  - `argument-hint`: Clear parameter format
  - `description`: Concise one-line description
  - `model`: (optional) Specific model if needed

#### Implementation:
- If the description mentions using a specific agent, configure the command to use the Task tool and delegate to that agent
- Include all specified parameters as `$ARGUMENTS` placeholders
- Provide clear instructions for parsing and handling arguments

### Example Input Format:
```
"/research:fetch <package-name> [url | feature to scrape | --depth=0-3]" "Use the doc-expert agent to Fetch technical documentation for a package or library. Optionally specify a URL to scrape and depth of crawl. Agent writes condensed document(s) in ai_docs/<package-name>/ with key information extracted."
```

### Expected Output:
- Create the command file at the correct path
- Ensure the command properly delegates to the specified agent if mentioned
- Include comprehensive argument parsing instructions
- Follow all command template best practices
- Argument hint: First argument should AWAYS be wrapped in angle brackets < >, UNLESS it is a slash command /example:command where it should have no wrapping characters. (Argument hint in this file as an example)

## Context Files:
Note: The agent will read these files if needed:
- .claude/templates/command.md (command template reference)
- ai_docs/cc/anthropic_custom_slash_commands.md (documentation)

## Important Token Usage:
- **DO NOT use `!` tokens** in the generated command unless the command MUST execute something during initialization
- **DO NOT use `@` tokens** in the generated command unless specific files MUST be loaded into context
- Commands should describe what needs to be done, not force specific executions
- When delegating to agents, pass requirements and let the agent decide how to execute

Begin by parsing the user's input to identify the command syntax, description, and any specified implementation details.
