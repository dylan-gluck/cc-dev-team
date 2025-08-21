# Claude Code Tools Documentation

This document provides a comprehensive reference of all available tools in Claude Code, organized by category.

## Table of Contents

- [Core Agent Tool](#core-agent-tool)
- [File System Tools](#file-system-tools)
- [Search Tools](#search-tools)
- [Shell Tools](#shell-tools)
- [Web Tools](#web-tools)
- [Task Management](#task-management)
- [MCP Server Tools](#mcp-server-tools)
- [Docker MCP Tools](#docker-mcp-tools)
- [FreeCrawl MCP Tools](#freecrawl-mcp-tools)
- [Playwright Browser Tools](#playwright-browser-tools)
- [ArtDept MCP Tools](#artdept-mcp-tools)
- [Stock Images MCP Tool](#stock-images-mcp-tool)
- [Creative Team Slash Commands](#creative-team-slash-commands)
- [ElevenLabs Audio Tools](#elevenlabs-audio-tools)

## Core Agent Tool

### Task
```typescript
Task(description: string, prompt: string, subagent_type: string): void
```
Launches specialized sub-agents for complex, multi-step tasks. The agent handles the task autonomously and returns a final report.

## File System Tools

### Read
```typescript
Read(file_path: string, limit?: number, offset?: number): string
```
Reads files from the filesystem. Supports text files, images (PNG, JPG), PDFs, and Jupyter notebooks.

### Write
```typescript
Write(file_path: string, content: string): void
```
Writes a file to the filesystem. Overwrites existing files if present.

### Edit
```typescript
Edit(file_path: string, old_string: string, new_string: string, replace_all?: boolean): void
```
Performs exact string replacements in files. Requires reading the file first.

### MultiEdit
```typescript
MultiEdit(file_path: string, edits: Array<{old_string: string, new_string: string, replace_all?: boolean}>): void
```
Makes multiple sequential edits to a single file in one atomic operation.

### NotebookEdit
```typescript
NotebookEdit(notebook_path: string, new_source: string, cell_id?: string, cell_type?: string, edit_mode?: string): void
```
Edits specific cells in Jupyter notebooks. Supports replace, insert, and delete operations.

## Search Tools

### Glob
```typescript
Glob(pattern: string, path?: string): string[]
```
Fast file pattern matching with glob patterns like `**/*.js` or `src/**/*.ts`.

### Grep
```typescript
Grep(pattern: string, path?: string, glob?: string, type?: string, output_mode?: string, 
     multiline?: boolean, -i?: boolean, -n?: boolean, -A?: number, -B?: number, 
     -C?: number, head_limit?: number): SearchResults
```
Powerful regex search built on ripgrep. Supports multiple output modes and filtering options.

### LS
```typescript
LS(path: string, ignore?: string[]): FileInfo[]
```
Lists files and directories at a given absolute path with optional ignore patterns.

## Shell Tools

### Bash
```typescript
Bash(command: string, description?: string, timeout?: number, run_in_background?: boolean): string
```
Executes bash commands in a persistent shell session with optional timeout and background execution.

### BashOutput
```typescript
BashOutput(bash_id: string, filter?: string): string
```
Retrieves output from running or completed background bash shells with optional regex filtering.

### KillBash
```typescript
KillBash(shell_id: string): void
```
Terminates a running background bash shell by its ID.

## Web Tools

### WebSearch
```typescript
WebSearch(query: string, allowed_domains?: string[], blocked_domains?: string[]): SearchResults
```
Searches the web for current information with domain filtering support.

### WebFetch
```typescript
WebFetch(url: string, prompt: string): string
```
Fetches web content and processes it with AI analysis using the provided prompt.

## Task Management

### TodoWrite
```typescript
TodoWrite(todos: Array<{content: string, status: 'pending'|'in_progress'|'completed', id: string}>): void
```
Creates and manages structured task lists for tracking progress and organizing complex tasks.

### ExitPlanMode
```typescript
ExitPlanMode(plan: string): void
```
Exits plan mode and prompts user approval for coding tasks implementation.

## MCP Server Tools

### ListMcpResourcesTool
```typescript
ListMcpResourcesTool(server?: string): Resource[]
```
Lists available resources from configured MCP servers.

### ReadMcpResourceTool
```typescript
ReadMcpResourceTool(server: string, uri: string): ResourceContent
```
Reads a specific resource from an MCP server by URI.

## Docker MCP Tools

### mcp__docker-mcp__create-container
```typescript
mcp__docker-mcp__create-container(image: string, name?: string, environment?: object, ports?: object): Container
```
Creates a new standalone Docker container with specified configuration.

### mcp__docker-mcp__deploy-compose
```typescript
mcp__docker-mcp__deploy-compose(compose_yaml: string, project_name: string): void
```
Deploys a Docker Compose stack from YAML configuration.

### mcp__docker-mcp__get-logs
```typescript
mcp__docker-mcp__get-logs(container_name: string): string
```
Retrieves the latest logs for a specified Docker container.

### mcp__docker-mcp__list-containers
```typescript
mcp__docker-mcp__list-containers(): Container[]
```
Lists all Docker containers with their status and configuration.

## FreeCrawl MCP Tools

### mcp__freecrawl__scrape
```typescript
mcp__freecrawl__scrape(url: string, formats?: string[], javascript?: boolean, 
                       anti_bot?: boolean, cache?: boolean, timeout?: number, 
                       wait_for?: string, headers?: object, cookies?: object): ScrapedContent
```
Scrapes content from a single URL with advanced options including JavaScript rendering and anti-bot detection.

### mcp__freecrawl__search
```typescript
mcp__freecrawl__search(query: string, num_results?: number, scrape_results?: boolean, 
                       search_engine?: string): SearchResults
```
Performs web search and optionally scrapes the result pages.

### mcp__freecrawl__crawl
```typescript
mcp__freecrawl__crawl(start_url: string, max_pages?: number, max_depth?: number, 
                      same_domain_only?: boolean, include_patterns?: string[], 
                      exclude_patterns?: string[]): CrawlResults
```
Crawls a website starting from a URL with configurable depth and filtering.

### mcp__freecrawl__deep_research
```typescript
mcp__freecrawl__deep_research(topic: string, num_sources?: number, max_depth?: number, 
                              include_academic?: boolean, search_queries?: string[]): ResearchResults
```
Performs comprehensive research on a topic using multiple sources and custom queries.

## Playwright Browser Tools

### Browser Navigation

#### mcp__playwright__browser_navigate
```typescript
mcp__playwright__browser_navigate(url: string): void
```
Navigates to a specified URL.

#### mcp__playwright__browser_navigate_back
```typescript
mcp__playwright__browser_navigate_back(): void
```
Goes back to the previous page in browser history.

#### mcp__playwright__browser_navigate_forward
```typescript
mcp__playwright__browser_navigate_forward(): void
```
Goes forward to the next page in browser history.

### Browser Interaction

#### mcp__playwright__browser_click
```typescript
mcp__playwright__browser_click(element: string, ref: string, button?: string, doubleClick?: boolean): void
```
Performs click actions on web page elements.

#### mcp__playwright__browser_type
```typescript
mcp__playwright__browser_type(element: string, ref: string, text: string, 
                              slowly?: boolean, submit?: boolean): void
```
Types text into editable elements with optional submission.

#### mcp__playwright__browser_select_option
```typescript
mcp__playwright__browser_select_option(element: string, ref: string, values: string[]): void
```
Selects options in dropdown menus.

#### mcp__playwright__browser_hover
```typescript
mcp__playwright__browser_hover(element: string, ref: string): void
```
Hovers over page elements.

#### mcp__playwright__browser_drag
```typescript
mcp__playwright__browser_drag(startElement: string, startRef: string, 
                              endElement: string, endRef: string): void
```
Performs drag and drop operations between elements.

#### mcp__playwright__browser_press_key
```typescript
mcp__playwright__browser_press_key(key: string): void
```
Presses keyboard keys or key combinations.

### Browser Information

#### mcp__playwright__browser_snapshot
```typescript
mcp__playwright__browser_snapshot(): AccessibilitySnapshot
```
Captures accessibility snapshot of the current page for analysis.

#### mcp__playwright__browser_take_screenshot
```typescript
mcp__playwright__browser_take_screenshot(filename?: string, fullPage?: boolean, 
                                         type?: string, element?: string, ref?: string): void
```
Takes screenshots of the page or specific elements.

#### mcp__playwright__browser_console_messages
```typescript
mcp__playwright__browser_console_messages(): ConsoleMessage[]
```
Returns all console messages from the page.

#### mcp__playwright__browser_network_requests
```typescript
mcp__playwright__browser_network_requests(): NetworkRequest[]
```
Returns all network requests made since loading the page.

### Browser Control

#### mcp__playwright__browser_evaluate
```typescript
mcp__playwright__browser_evaluate(function: string, element?: string, ref?: string): any
```
Evaluates JavaScript expressions on the page or specific elements.

#### mcp__playwright__browser_file_upload
```typescript
mcp__playwright__browser_file_upload(paths: string[]): void
```
Uploads one or multiple files to the page.

#### mcp__playwright__browser_wait_for
```typescript
mcp__playwright__browser_wait_for(text?: string, textGone?: string, time?: number): void
```
Waits for text to appear/disappear or for a specified time.

#### mcp__playwright__browser_handle_dialog
```typescript
mcp__playwright__browser_handle_dialog(accept: boolean, promptText?: string): void
```
Handles browser dialogs (alerts, confirms, prompts).

### Tab Management

#### mcp__playwright__browser_tab_new
```typescript
mcp__playwright__browser_tab_new(url?: string): void
```
Opens a new browser tab with optional URL.

#### mcp__playwright__browser_tab_select
```typescript
mcp__playwright__browser_tab_select(index: number): void
```
Selects a tab by its index.

#### mcp__playwright__browser_tab_close
```typescript
mcp__playwright__browser_tab_close(index?: number): void
```
Closes a specific tab or the current tab.

#### mcp__playwright__browser_tab_list
```typescript
mcp__playwright__browser_tab_list(): Tab[]
```
Lists all open browser tabs.

### Browser Setup

#### mcp__playwright__browser_resize
```typescript
mcp__playwright__browser_resize(width: number, height: number): void
```
Resizes the browser window to specified dimensions.

#### mcp__playwright__browser_close
```typescript
mcp__playwright__browser_close(): void
```
Closes the browser page.

#### mcp__playwright__browser_install
```typescript
mcp__playwright__browser_install(): void
```
Installs the browser specified in configuration.

## ArtDept MCP Tools

### mcp__artdept-mcp__new_wireframe
```typescript
mcp__artdept-mcp__new_wireframe(id: string, prompt: string, device?: string, 
                                style?: string, save?: string): ImageResult
```
Generates UI/UX wireframes for desktop, mobile, or both platforms.

### mcp__artdept-mcp__new_designsystem
```typescript
mcp__artdept-mcp__new_designsystem(id: string, prompt: string, n: number, type?: string, 
                                   colors?: string, style?: string, save?: string): ImageResult[]
```
Generates comprehensive design systems with multiple variations.

### mcp__artdept-mcp__new_logo
```typescript
mcp__artdept-mcp__new_logo(id: string, prompt: string, n: number, colors?: string, 
                           style?: string, save?: string): ImageResult[]
```
Generates professional logo designs with specified styles and colors.

### mcp__artdept-mcp__new_icon
```typescript
mcp__artdept-mcp__new_icon(id: string, prompt: string, n: number, colors?: string, 
                          style?: string, save?: string): ImageResult[]
```
Generates scalable icon designs for various uses.

### mcp__artdept-mcp__new_illustration
```typescript
mcp__artdept-mcp__new_illustration(id: string, prompt: string, n: number, size?: string, 
                                   style?: string, save?: string): ImageResult[]
```
Generates custom illustrations in various styles and sizes.

### mcp__artdept-mcp__new_photo
```typescript
mcp__artdept-mcp__new_photo(id: string, prompt: string, n: number, size?: string, 
                           style?: string, save?: string): ImageResult[]
```
Generates photorealistic images with specified dimensions.

## Stock Images MCP Tool

### mcp__stock-images-mcp__search_stock_images
```typescript
mcp__stock-images-mcp__search_stock_images(query: string, platform?: string, per_page?: number): StockImages[]
```
Searches for stock images across multiple platforms (Pexels, Unsplash, Pixabay).

## Creative Team Slash Commands

The creative team provides specialized slash commands for rapid asset generation through the orchestrated creative team. All commands delegate to the creative-director who coordinates appropriate team members.

### /creative-assets
```bash
/creative-assets <asset-types> <brand/project> [theme]
```
Generates multiple creative assets in a coordinated campaign including social media templates, email designs, web banners, brand collateral, and consistent copywriting across all assets.

**Examples:**
- `/creative-assets "social,email,banners" "Summer Sale Campaign" vibrant`
- `/creative-assets "full-brand-package" "StartupX" modern-tech`

### /wireframe
```bash
/wireframe <device-type> <description> [style-preference]
```
Creates professional wireframe designs for apps and websites with component breakdowns, interaction flows, and responsive considerations.

**Examples:**
- `/wireframe mobile "login screen with social auth"`
- `/wireframe desktop "dashboard with analytics charts" high-fidelity`

### /logo
```bash
/logo <brand-name> [industry] [style-keywords]
```
Designs multiple logo concepts with brand identity considerations, including color palettes, typography choices, and usage guidelines.

**Examples:**
- `/logo "TechNova" software minimal`
- `/logo "Green Earth Cafe" restaurant eco-friendly organic`

### /stock-photos
```bash
/stock-photos <search-terms> [style] [usage-type]
```
Searches for high-quality stock photos across multiple platforms with license information and attribution requirements.

**Examples:**
- `/stock-photos "remote work laptop coffee" minimal commercial`
- `/stock-photos "nature sustainability" abstract editorial`

### /design-system
```bash
/design-system <project-name> <style-direction> [platform]
```
Creates comprehensive design systems including color palettes, typography scales, spacing systems, and component libraries.

### /brand-copy
```bash
/brand-copy <content-type> <brand/product> [tone]
```
Generates brand messaging and marketing copy including headlines, website content, email campaigns, and social media variations.

**Note**: All creative slash commands leverage the creative team's orchestration pattern, automatically delegating to appropriate specialists (creative-ux-lead, creative-wireframe, creative-logo, creative-illustrator, creative-photographer, creative-copywriter) as coordinated by the creative-director.

## ElevenLabs Audio Tools

### Text-to-Speech

#### mcp__ElevenLabs__text_to_speech
```typescript
mcp__ElevenLabs__text_to_speech(text: string, voice_name?: string, voice_id?: string, 
                                model_id?: string, stability?: number, similarity_boost?: number, 
                                style?: number, use_speaker_boost?: boolean, speed?: number, 
                                output_directory?: string, language?: string, 
                                output_format?: string): AudioFile
```
Converts text to speech with customizable voice parameters and output formats.

#### mcp__ElevenLabs__text_to_sound_effects
```typescript
mcp__ElevenLabs__text_to_sound_effects(text: string, duration_seconds?: number, 
                                       output_directory?: string, output_format?: string): AudioFile
```
Generates sound effects from text descriptions.

#### mcp__ElevenLabs__text_to_voice
```typescript
mcp__ElevenLabs__text_to_voice(voice_description: string, text?: string, 
                               output_directory?: string): VoicePreviews
```
Creates voice previews from text prompts with variations.

### Speech Processing

#### mcp__ElevenLabs__speech_to_text
```typescript
mcp__ElevenLabs__speech_to_text(input_file_path: string, language_code?: string, 
                                diarize?: boolean, save_transcript_to_file?: boolean, 
                                return_transcript_to_client_directly?: boolean, 
                                output_directory?: string): Transcript
```
Transcribes speech from audio files with optional speaker diarization.

#### mcp__ElevenLabs__speech_to_speech
```typescript
mcp__ElevenLabs__speech_to_speech(input_file_path: string, voice_name?: string, 
                                  output_directory?: string): AudioFile
```
Transforms audio from one voice to another.

#### mcp__ElevenLabs__isolate_audio
```typescript
mcp__ElevenLabs__isolate_audio(input_file_path: string, output_directory?: string): AudioFile
```
Isolates and enhances audio from files.

### Voice Management

#### mcp__ElevenLabs__search_voices
```typescript
mcp__ElevenLabs__search_voices(search?: string, sort?: string, sort_direction?: string): Voice[]
```
Searches voices in the user's ElevenLabs library.

#### mcp__ElevenLabs__search_voice_library
```typescript
mcp__ElevenLabs__search_voice_library(search?: string, page?: number, page_size?: number): SharedVoices
```
Searches the entire ElevenLabs voice library.

#### mcp__ElevenLabs__get_voice
```typescript
mcp__ElevenLabs__get_voice(voice_id: string): VoiceDetails
```
Gets detailed information about a specific voice.

#### mcp__ElevenLabs__voice_clone
```typescript
mcp__ElevenLabs__voice_clone(name: string, files: string[], description?: string): Voice
```
Creates an instant voice clone from audio files.

#### mcp__ElevenLabs__create_voice_from_preview
```typescript
mcp__ElevenLabs__create_voice_from_preview(generated_voice_id: string, voice_name: string, 
                                           voice_description: string): Voice
```
Adds a generated voice preview to the voice library.

### Conversational AI Agents

#### mcp__ElevenLabs__create_agent
```typescript
mcp__ElevenLabs__create_agent(name: string, first_message: string, system_prompt: string, 
                              voice_id?: string, language?: string, llm?: string, 
                              temperature?: number, max_tokens?: number, model_id?: string, 
                              stability?: number, similarity_boost?: number, 
                              turn_timeout?: number, max_duration_seconds?: number, 
                              record_voice?: boolean, retention_days?: number): Agent
```
Creates a conversational AI agent with custom configuration.

#### mcp__ElevenLabs__add_knowledge_base_to_agent
```typescript
mcp__ElevenLabs__add_knowledge_base_to_agent(agent_id: string, knowledge_base_name: string, 
                                             url?: string, input_file_path?: string, 
                                             text?: string): void
```
Adds knowledge base resources to an agent.

#### mcp__ElevenLabs__list_agents
```typescript
mcp__ElevenLabs__list_agents(): Agent[]
```
Lists all available conversational AI agents.

#### mcp__ElevenLabs__get_agent
```typescript
mcp__ElevenLabs__get_agent(agent_id: string): AgentDetails
```
Gets detailed information about a specific agent.

### Conversation Management

#### mcp__ElevenLabs__get_conversation
```typescript
mcp__ElevenLabs__get_conversation(conversation_id: string): ConversationWithTranscript
```
Retrieves a conversation with its full transcript.

#### mcp__ElevenLabs__list_conversations
```typescript
mcp__ElevenLabs__list_conversations(agent_id?: string, cursor?: string, 
                                    call_start_before_unix?: number, 
                                    call_start_after_unix?: number, 
                                    page_size?: number, max_length?: number): Conversation[]
```
Lists agent conversations with filtering and pagination.

### Phone and Calling

#### mcp__ElevenLabs__make_outbound_call
```typescript
mcp__ElevenLabs__make_outbound_call(agent_id: string, agent_phone_number_id: string, 
                                    to_number: string): CallInfo
```
Makes outbound calls using an ElevenLabs agent.

#### mcp__ElevenLabs__list_phone_numbers
```typescript
mcp__ElevenLabs__list_phone_numbers(): PhoneNumber[]
```
Lists all phone numbers associated with the account.

### Utility Functions

#### mcp__ElevenLabs__list_models
```typescript
mcp__ElevenLabs__list_models(): Model[]
```
Lists all available TTS models.

#### mcp__ElevenLabs__check_subscription
```typescript
mcp__ElevenLabs__check_subscription(): SubscriptionStatus
```
Checks current subscription status and API usage.

#### mcp__ElevenLabs__play_audio
```typescript
mcp__ElevenLabs__play_audio(input_file_path: string): void
```
Plays audio files in WAV or MP3 format.

---

*Generated on: 2025-08-21*
*Total Tools: 129 (includes 6 Creative Team slash commands)*