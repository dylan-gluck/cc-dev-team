# All Available Tools

This document lists all available tools in TypeScript function signature format with their purposes.

## Core Agent Orchestration

**Task(description: string, prompt: string, subagent_type: string): void**
Launch a new specialized agent to handle complex, multi-step tasks autonomously with access to specific tools based on agent type.


## File System Operations

**Read(file_path: string, limit?: number, offset?: number): string**
Reads a file from the local filesystem, supporting text, images, PDFs, and Jupyter notebooks with optional line limiting.


**Write(file_path: string, content: string): void**
Writes content to a file, overwriting existing content. Requires reading the file first if it already exists.


**Edit(file_path: string, old_string: string, new_string: string, replace_all?: boolean): void**
Performs exact string replacements in files with optional global replacement functionality.


**MultiEdit(file_path: string, edits: Array<{old_string: string, new_string: string, replace_all?: boolean}>): void**
Makes multiple edits to a single file in one atomic operation, applying changes sequentially.


**LS(path: string, ignore?: string[]): string[]**
Lists files and directories in a given absolute path with optional glob pattern exclusions.


**Glob(pattern: string, path?: string): string[]**
Fast file pattern matching tool supporting glob patterns, returns files sorted by modification time.


**Grep(pattern: string, path?: string, output_mode?: "content" | "files_with_matches" | "count", glob?: string, type?: string, multiline?: boolean, -A?: number, -B?: number, -C?: number, -i?: boolean, -n?: boolean, head_limit?: number): string**
Powerful search tool built on ripgrep with full regex syntax, file filtering, and various output modes.


## Command Execution

**Bash(command: string, description?: string, timeout?: number, run_in_background?: boolean): string**
Executes bash commands in a persistent shell session with proper quoting and security measures.


**BashOutput(bash_id: string, filter?: string): string**
Retrieves output from running or completed background bash shells with optional regex filtering.


**KillBash(shell_id: string): void**
Terminates a running background bash shell by its ID.


## Web Operations

**WebSearch(query: string, allowed_domains?: string[], blocked_domains?: string[]): string**
Searches the web and returns formatted search results for accessing current information beyond knowledge cutoff.


**WebFetch(url: string, prompt: string): string**
Fetches content from a URL, converts HTML to markdown, and processes it with AI for information extraction.


## Task Management

**TodoWrite(todos: Array<{content: string, status: "pending" | "in_progress" | "completed", id: string}>): void**
Creates and manages structured task lists for tracking progress and organizing complex multi-step tasks.


**ExitPlanMode(plan: string): void**
Prompts user to exit plan mode after presenting implementation plans for coding tasks.


## Notebook Operations

**NotebookEdit(notebook_path: string, new_source: string, cell_id?: string, cell_type?: "code" | "markdown", edit_mode?: "replace" | "insert" | "delete"): void**
Replaces, inserts, or deletes cells in Jupyter notebooks with support for both code and markdown cells.


## Docker Operations

**mcp__docker-mcp__create-container(image: string, name?: string, ports?: Record<string, string>, environment?: Record<string, string>): void**
Creates a new standalone Docker container with specified image and optional configuration.


**mcp__docker-mcp__deploy-compose(compose_yaml: string, project_name: string): void**
Deploys a Docker Compose stack from YAML configuration with specified project name.


**mcp__docker-mcp__list-containers(): string**
Lists all Docker containers with their current status and information.


**mcp__docker-mcp__get-logs(container_name: string): string**
Retrieves the latest logs for a specified Docker container.


## Audio/Speech Operations

**mcp__ElevenLabs__text_to_speech(text: string, voice_name?: string, voice_id?: string, model_id?: string, stability?: number, similarity_boost?: number, style?: number, use_speaker_boost?: boolean, speed?: number, output_directory?: string, language?: string, output_format?: string): string**
Converts text to speech with customizable voice parameters and saves audio file. ⚠️ COST WARNING: Incurs API costs.


**mcp__ElevenLabs__speech_to_text(input_file_path: string, language_code?: string, diarize?: boolean, save_transcript_to_file?: boolean, return_transcript_to_client_directly?: boolean, output_directory?: string): string**
Transcribes speech from audio files with optional speaker diarization. ⚠️ COST WARNING: Incurs API costs.


**mcp__ElevenLabs__text_to_sound_effects(text: string, duration_seconds?: number, output_directory?: string, output_format?: string): string**
Generates sound effects from text descriptions with specified duration. ⚠️ COST WARNING: Incurs API costs.


**mcp__ElevenLabs__speech_to_speech(input_file_path: string, voice_name?: string, output_directory?: string): string**
Transforms audio from one voice to another using voice conversion. ⚠️ COST WARNING: Incurs API costs.


**mcp__ElevenLabs__isolate_audio(input_file_path: string, output_directory?: string): string**
Isolates and extracts audio from media files. ⚠️ COST WARNING: Incurs API costs.


**mcp__ElevenLabs__play_audio(input_file_path: string): void**
Plays audio files in WAV and MP3 formats.


## Voice Management

**mcp__ElevenLabs__search_voices(search?: string, sort?: "created_at_unix" | "name", sort_direction?: "asc" | "desc"): string**
Searches for existing voices in the user's ElevenLabs voice library with filtering and sorting.


**mcp__ElevenLabs__get_voice(voice_id: string): string**
Retrieves detailed information about a specific voice by its ID.


**mcp__ElevenLabs__voice_clone(name: string, files: string[], description?: string): string**
Creates an instant voice clone using provided audio files. ⚠️ COST WARNING: Incurs API costs.


**mcp__ElevenLabs__text_to_voice(voice_description: string, text?: string, output_directory?: string): string**
Creates voice previews from text descriptions with slight variations. ⚠️ COST WARNING: Incurs API costs.


**mcp__ElevenLabs__create_voice_from_preview(generated_voice_id: string, voice_name: string, voice_description: string): string**
Adds a generated voice preview to the voice library. ⚠️ COST WARNING: Incurs API costs.


**mcp__ElevenLabs__search_voice_library(search?: string, page?: number, page_size?: number): string**
Searches the entire ElevenLabs voice library for available voices with pagination.


## AI Agents & Conversations

**mcp__ElevenLabs__create_agent(name: string, first_message: string, system_prompt: string, voice_id?: string, language?: string, llm?: string, temperature?: number, max_tokens?: number, asr_quality?: string, model_id?: string, optimize_streaming_latency?: number, stability?: number, similarity_boost?: number, turn_timeout?: number, max_duration_seconds?: number, record_voice?: boolean, retention_days?: number): string**
Creates a conversational AI agent with custom configuration. ⚠️ COST WARNING: Incurs API costs.


**mcp__ElevenLabs__add_knowledge_base_to_agent(agent_id: string, knowledge_base_name: string, url?: string, input_file_path?: string, text?: string): string**
Adds knowledge base content to an AI agent from various sources. ⚠️ COST WARNING: Incurs API costs.


**mcp__ElevenLabs__list_agents(): string**
Lists all available conversational AI agents in the account.


**mcp__ElevenLabs__get_agent(agent_id: string): string**
Retrieves detailed information about a specific AI agent.


**mcp__ElevenLabs__list_conversations(agent_id?: string, cursor?: string, call_start_before_unix?: number, call_start_after_unix?: number, page_size?: number, max_length?: number): string**
Lists agent conversations with filtering and pagination options.


**mcp__ElevenLabs__get_conversation(conversation_id: string): string**
Retrieves a complete conversation with transcript for analysis.


**mcp__ElevenLabs__make_outbound_call(agent_id: string, agent_phone_number_id: string, to_number: string): string**
Makes outbound calls using ElevenLabs agents with automatic provider detection. ⚠️ COST WARNING: Incurs API costs.


**mcp__ElevenLabs__list_phone_numbers(): string**
Lists all phone numbers associated with the ElevenLabs account.


## System Information

**mcp__ElevenLabs__list_models(): string**
Lists all available ElevenLabs AI models for speech synthesis.


**mcp__ElevenLabs__check_subscription(): string**
Checks current ElevenLabs subscription status and API usage metrics.


## MCP Resource Operations

**ListMcpResourcesTool(server?: string): string**
Lists available resources from configured MCP servers with optional server filtering.


**ReadMcpResourceTool(server: string, uri: string): string**
Reads specific resources from MCP servers by server name and resource URI.


## Browser Automation

**mcp__playwright__browser_navigate(url: string): void**
Navigates the browser to a specified URL.


**mcp__playwright__browser_snapshot(): string**
Captures accessibility snapshot of the current page for element interaction.


**mcp__playwright__browser_click(element: string, ref: string, button?: "left" | "right" | "middle", doubleClick?: boolean): void**
Performs click operations on web page elements.


**mcp__playwright__browser_type(element: string, ref: string, text: string, slowly?: boolean, submit?: boolean): void**
Types text into editable elements with optional slow typing and submission.


**mcp__playwright__browser_press_key(key: string): void**
Presses keyboard keys or generates characters on the current page.


**mcp__playwright__browser_take_screenshot(element?: string, ref?: string, filename?: string, fullPage?: boolean, type?: "png" | "jpeg"): string**
Takes screenshots of the current page or specific elements.


**mcp__playwright__browser_hover(element: string, ref: string): void**
Hovers over specified elements on the page.


**mcp__playwright__browser_select_option(element: string, ref: string, values: string[]): void**
Selects options in dropdown menus.


**mcp__playwright__browser_drag(startElement: string, startRef: string, endElement: string, endRef: string): void**
Performs drag and drop operations between elements.


**mcp__playwright__browser_evaluate(function: string, element?: string, ref?: string): string**
Executes JavaScript on the page or specific elements.


**mcp__playwright__browser_wait_for(text?: string, textGone?: string, time?: number): void**
Waits for text to appear/disappear or for specified time duration.


**mcp__playwright__browser_file_upload(paths: string[]): void**
Uploads one or multiple files through file input elements.


**mcp__playwright__browser_handle_dialog(accept: boolean, promptText?: string): void**
Handles browser dialogs (alerts, confirms, prompts).


**mcp__playwright__browser_resize(width: number, height: number): void**
Resizes the browser window to specified dimensions.


**mcp__playwright__browser_close(): void**
Closes the current browser page.


**mcp__playwright__browser_install(): void**
Installs the browser if not already installed.


**mcp__playwright__browser_navigate_back(): void**
Navigates back to the previous page in browser history.


**mcp__playwright__browser_navigate_forward(): void**
Navigates forward to the next page in browser history.


**mcp__playwright__browser_console_messages(): string**
Retrieves all console messages from the current page.


**mcp__playwright__browser_network_requests(): string**
Returns all network requests since loading the page.


## Tab Management

**mcp__playwright__browser_tab_list(): string**
Lists all open browser tabs with their information.


**mcp__playwright__browser_tab_new(url?: string): void**
Opens a new browser tab, optionally navigating to a URL.


**mcp__playwright__browser_tab_select(index: number): void**
Switches to a browser tab by its index.


**mcp__playwright__browser_tab_close(index?: number): void**
Closes a browser tab by index, or current tab if no index specified.


## Web Crawling & Research

**mcp__freecrawl__mcp__freecrawl__scrape(url: string, formats?: string[], javascript?: boolean, anti_bot?: boolean, cache?: boolean, timeout?: number, wait_for?: string, headers?: object, cookies?: object): string**
Scrapes content from a single URL with advanced options including JavaScript rendering and anti-bot detection.


**mcp__freecrawl__mcp__freecrawl__search(query: string, num_results?: number, scrape_results?: boolean, search_engine?: string): string**
Performs web search and optionally scrapes results from search engines.


**mcp__freecrawl__mcp__freecrawl__crawl(start_url: string, max_pages?: number, max_depth?: number, same_domain_only?: boolean, include_patterns?: string[], exclude_patterns?: string[]): string**
Crawls a website starting from a URL with configurable depth and filtering options.


**mcp__freecrawl__mcp__freecrawl__deep_research(topic: string, num_sources?: number, max_depth?: number, search_queries?: string[], include_academic?: boolean): string**
Performs comprehensive research on topics using multiple sources with academic options.
