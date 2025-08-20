Agent & Task Management Tools

Task(description: string, prompt: string, subagent_type: string): void
// Launch specialized agents for complex, multi-step tasks

TodoWrite(todos: Array<{content: string, status:
"pending"|"in_progress"|"completed", id: string}>): void
// Create and manage structured task lists for tracking progress

File System Tools

Read(file_path: string, limit?: number, offset?: number): string
// Read files from filesystem, including images, PDFs, and notebooks

Write(file_path: string, content: string): void
// Write new files to the filesystem

Edit(file_path: string, old_string: string, new_string: string, replace_all?:
boolean): void
// Perform exact string replacements in files

MultiEdit(file_path: string, edits: Array<{old_string: string, new_string:
string, replace_all?: boolean}>): void
// Make multiple edits to a single file in one operation

NotebookEdit(notebook_path: string, new_source: string, cell_id?: string,
cell_type?: "code"|"markdown", edit_mode?: "replace"|"insert"|"delete"): void
// Edit specific cells in Jupyter notebooks

Search & Navigation Tools

Glob(pattern: string, path?: string): string[]
// Fast file pattern matching across codebase

Grep(pattern: string, path?: string, glob?: string, type?: string,
output_mode?: "content"|"files_with_matches"|"count", multiline?: boolean,
-i?: boolean, -n?: boolean, -A?: number, -B?: number, -C?: number,
head_limit?: number): string
// Powerful regex search built on ripgrep

LS(path: string, ignore?: string[]): string[]
// List files and directories at given path

Command Execution Tools

Bash(command: string, description?: string, timeout?: number,
run_in_background?: boolean): string
// Execute bash commands with optional timeout and background execution

BashOutput(bash_id: string, filter?: string): string
// Retrieve output from running or completed background bash shells

KillBash(shell_id: string): void
// Terminate a running background bash shell

Web & Research Tools

WebSearch(query: string, allowed_domains?: string[], blocked_domains?:
string[]): SearchResults
// Search the web with domain filtering support

WebFetch(url: string, prompt: string): string
// Fetch and process web content with AI analysis

Planning & Control Tools

ExitPlanMode(plan: string): void
// Exit plan mode after presenting implementation steps

MCP Integration Tools

FreeCrawl MCP

mcp__freecrawl__scrape(url: string, formats?: string[], javascript?: boolean,
cache?: boolean, anti_bot?: boolean, timeout?: number, wait_for?: string,
headers?: object, cookies?: object): ScrapedContent
// Scrape content from single URL with advanced options

mcp__freecrawl__search(query: string, num_results?: number, scrape_results?:
boolean, search_engine?: string): SearchResults
// Web search with optional result scraping

mcp__freecrawl__crawl(start_url: string, max_depth?: number, max_pages?:
number, same_domain_only?: boolean, include_patterns?: string[],
exclude_patterns?: string[]): CrawlResults
// Crawl website starting from URL

mcp__freecrawl__deep_research(topic: string, num_sources?: number, max_depth?:
  number, include_academic?: boolean, search_queries?: string[]):
ResearchResults
// Comprehensive research using multiple sources

Playwright Browser MCP

mcp__playwright__browser_navigate(url: string): void
// Navigate browser to URL

mcp__playwright__browser_click(element: string, ref: string, button?:
"left"|"right"|"middle", doubleClick?: boolean): void
// Click on web page element

mcp__playwright__browser_type(element: string, ref: string, text: string,
slowly?: boolean, submit?: boolean): void
// Type text into editable element

mcp__playwright__browser_snapshot(): AccessibilitySnapshot
// Capture accessibility snapshot of current page

mcp__playwright__browser_take_screenshot(filename?: string, fullPage?:
boolean, type?: "png"|"jpeg", element?: string, ref?: string): void
// Take screenshot of page or element

mcp__playwright__browser_evaluate(function: string, element?: string, ref?:
string): any
// Execute JavaScript on page or element

Docker MCP

mcp__docker-mcp__create-container(image: string, name?: string, environment?:
object, ports?: object): ContainerInfo
// Create new Docker container

mcp__docker-mcp__deploy-compose(compose_yaml: string, project_name: string):
void
// Deploy Docker Compose stack

mcp__docker-mcp__get-logs(container_name: string): string
// Retrieve container logs

mcp__docker-mcp__list-containers(): ContainerList
// List all Docker containers

ElevenLabs MCP

mcp__ElevenLabs__text_to_speech(text: string, voice_name?: string, voice_id?:
string, model_id?: string, stability?: number, similarity_boost?: number,
style?: number, use_speaker_boost?: boolean, speed?: number,
output_directory?: string, language?: string, output_format?: string): string
// Convert text to speech with voice options

mcp__ElevenLabs__speech_to_text(input_file_path: string, language_code?:
string, diarize?: boolean, save_transcript_to_file?: boolean,
return_transcript_to_client_directly?: boolean, output_directory?: string):
string
// Transcribe speech from audio file

mcp__ElevenLabs__play_audio(input_file_path: string): void
// Play audio file (WAV/MP3)

mcp__ElevenLabs__create_agent(name: string, first_message: string,
system_prompt: string, voice_id?: string, language?: string, llm?: string,
temperature?: number, max_tokens?: number): AgentInfo
// Create conversational AI agent

Stock Images MCP

mcp__stock-images-mcp__search_stock_images(query: string, platform?: string,
per_page?: number): StockImages
// Search for stock images across platforms

General MCP Tools

ListMcpResourcesTool(server?: string): McpResources
// List available resources from MCP servers

ReadMcpResourceTool(server: string, uri: string): ResourceContent
// Read specific resource from MCP server
