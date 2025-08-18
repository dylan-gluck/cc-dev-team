# Available Tools

Here are all available tools in TypeScript function signature format:

  • Task(description: string, prompt: string, subagent_type: string): Promise
  - Launch a new agent to handle complex, multi-step tasks autonomously

  • Bash(command: string, description?: string, run_in_background?: boolean, timeout?: number): Promise
  - Execute bash commands in a persistent shell session with optional timeout

  • Glob(pattern: string, path?: string): Promise<string[]>
  - Fast file pattern matching tool for finding files by name patterns

  • Grep(pattern: string, path?: string, glob?: string, type?: string, output_mode?: string, multiline?: boolean,
  -i?: boolean, -n?: boolean, -A?: number, -B?: number, -C?: number, head_limit?: number): Promise
  - Powerful search tool built on ripgrep for searching file contents

  • LS(path: string, ignore?: string[]): Promise<FileSystemEntry[]>
  - List files and directories in a given absolute path

  • ExitPlanMode(plan: string): void
  - Exit plan mode and present implementation plan to user for approval

  • Read(file_path: string, limit?: number, offset?: number): Promise
  - Read files from the local filesystem including images, PDFs, and notebooks

  • Edit(file_path: string, old_string: string, new_string: string, replace_all?: boolean): Promise
  - Perform exact string replacements in files

  • MultiEdit(file_path: string, edits: EditOperation[]): Promise
  - Make multiple edits to a single file in one atomic operation

  • Write(file_path: string, content: string): Promise
  - Write a file to the local filesystem (overwrites existing files)

  • NotebookEdit(notebook_path: string, new_source: string, cell_id?: string, cell_type?: string, edit_mode?:
  string): Promise
  - Replace contents of a specific cell in a Jupyter notebook

  • WebFetch(url: string, prompt: string): Promise
  - Fetch content from a URL and process it with an AI model

  • TodoWrite(todos: TodoItem[]): Promise
  - Create and manage structured task lists for tracking progress

  • WebSearch(query: string, allowed_domains?: string[], blocked_domains?: string[]): Promise<SearchResult[]>
  - Search the web and return formatted search results

  • BashOutput(bash_id: string, filter?: string): Promise
  - Retrieve output from a running or completed background bash shell

  • KillBash(shell_id: string): Promise
  - Kill a running background bash shell by its ID

  • mcp__firecrawl__firecrawl_scrape(url: string, formats?: string[], maxAge?: number, actions?: Action[], extract?:
  object, ...options): Promise
  - Scrape content from a single URL with advanced options

  • mcp__firecrawl__firecrawl_map(url: string, search?: string, limit?: number, ignoreSitemap?: boolean,
  includeSubdomains?: boolean, sitemapOnly?: boolean): Promise<string[]>
  - Map a website to discover all indexed URLs on the site

  • mcp__firecrawl__firecrawl_crawl(url: string, maxDepth?: number, limit?: number, scrapeOptions?: object,
  ...options): Promise
  - Start an asynchronous crawl job on a website

  • mcp__firecrawl__firecrawl_check_crawl_status(id: string): Promise
  - Check the status of a crawl job

  • mcp__firecrawl__firecrawl_search(query: string, limit?: number, lang?: string, country?: string, scrapeOptions?:
  object): Promise
  - Search the web and optionally extract content from search results

  • mcp__firecrawl__firecrawl_extract(urls: string[], prompt?: string, schema?: object, systemPrompt?: string,
  ...options): Promise
  - Extract structured information from web pages using LLM capabilities

  • mcp__firecrawl__firecrawl_deep_research(query: string, maxDepth?: number, timeLimit?: number, maxUrls?: number):
  Promise
  - Conduct deep web research on a query using intelligent crawling

  • mcp__firecrawl__firecrawl_generate_llmstxt(url: string, maxUrls?: number, showFullText?: boolean): Promise
  - Generate a standardized llms.txt file for a given domain

  • mcp__ElevenLabs__text_to_speech(text: string, voice_name?: string, voice_id?: string, model_id?: string,
  output_directory?: string, ...params): Promise
  - Convert text to speech with a given voice (COST WARNING)

  • mcp__ElevenLabs__speech_to_text(input_file_path: string, language_code?: string, diarize?: boolean,
  save_transcript_to_file?: boolean, output_directory?: string): Promise
  - Transcribe speech from an audio file (COST WARNING)

  • mcp__ElevenLabs__text_to_sound_effects(text: string, duration_seconds?: number, output_directory?: string,
  output_format?: string): Promise
  - Convert text description to sound effects (COST WARNING)

  • mcp__ElevenLabs__search_voices(search?: string, sort?: string, sort_direction?: string): Promise<Voice[]>
  - Search for existing voices in ElevenLabs voice library

  • mcp__ElevenLabs__list_models(): Promise<Model[]>
  - List all available ElevenLabs models

  • mcp__ElevenLabs__get_voice(voice_id: string): Promise
  - Get details of a specific voice

  • mcp__ElevenLabs__voice_clone(name: string, files: string[], description?: string): Promise
  - Create an instant voice clone using audio files (COST WARNING)

  • mcp__ElevenLabs__isolate_audio(input_file_path: string, output_directory?: string): Promise
  - Isolate audio from a file (COST WARNING)

  • mcp__ElevenLabs__check_subscription(): Promise
  - Check current ElevenLabs subscription status

  • mcp__ElevenLabs__create_agent(name: string, first_message: string, system_prompt: string, voice_id?: string,
  ...params): Promise
  - Create a conversational AI agent (COST WARNING)

  • mcp__ElevenLabs__add_knowledge_base_to_agent(agent_id: string, knowledge_base_name: string, url?: string,
  input_file_path?: string, text?: string): Promise
  - Add knowledge base to ElevenLabs agent (COST WARNING)

  • mcp__ElevenLabs__list_agents(): Promise<Agent[]>
  - List all available conversational AI agents

  • mcp__ElevenLabs__get_agent(agent_id: string): Promise
  - Get details about a specific conversational AI agent

  • mcp__ElevenLabs__get_conversation(conversation_id: string): Promise
  - Get conversation with transcript

  • mcp__ElevenLabs__list_conversations(agent_id?: string, cursor?: string, ...params): Promise
  - List agent conversations with metadata

  • mcp__ElevenLabs__speech_to_speech(input_file_path: string, voice_name?: string, output_directory?: string):
  Promise
  - Transform audio from one voice to another (COST WARNING)

  • mcp__ElevenLabs__text_to_voice(voice_description: string, text?: string, output_directory?: string): Promise
  - Create voice previews from text prompt (COST WARNING)

  • mcp__ElevenLabs__create_voice_from_preview(generated_voice_id: string, voice_name: string, voice_description:
  string): Promise
  - Add generated voice to library (COST WARNING)

  • mcp__ElevenLabs__make_outbound_call(agent_id: string, agent_phone_number_id: string, to_number: string): Promise
  - Make outbound call using ElevenLabs agent (COST WARNING)

  • mcp__ElevenLabs__search_voice_library(search?: string, page?: number, page_size?: number): Promise
  - Search entire ElevenLabs voice library

  • mcp__ElevenLabs__list_phone_numbers(): Promise<PhoneNumber[]>
  - List all phone numbers associated with account

  • mcp__ElevenLabs__play_audio(input_file_path: string): Promise
  - Play an audio file (WAV/MP3)

  • ListMcpResourcesTool(server?: string): Promise<McpResource[]>
  - List available resources from configured MCP servers

  • ReadMcpResourceTool(server: string, uri: string): Promise
  - Read a specific resource from an MCP server

  • mcp__playwright__browser_close(): Promise
  - Close the browser page

  • mcp__playwright__browser_resize(width: number, height: number): Promise
  - Resize the browser window

  • mcp__playwright__browser_console_messages(): Promise<ConsoleMessage[]>
  - Return all console messages

  • mcp__playwright__browser_handle_dialog(accept: boolean, promptText?: string): Promise
  - Handle a dialog

  • mcp__playwright__browser_evaluate(function: string, element?: string, ref?: string): Promise
  - Evaluate JavaScript expression on page or element

  • mcp__playwright__browser_file_upload(paths: string[]): Promise
  - Upload one or multiple files

  • mcp__playwright__browser_install(): Promise
  - Install the browser specified in config

  • mcp__playwright__browser_press_key(key: string): Promise
  - Press a key on the keyboard

  • mcp__playwright__browser_type(element: string, ref: string, text: string, slowly?: boolean, submit?: boolean):
  Promise
  - Type text into editable element

  • mcp__playwright__browser_navigate(url: string): Promise
  - Navigate to a URL

  • mcp__playwright__browser_navigate_back(): Promise
  - Go back to the previous page

  • mcp__playwright__browser_navigate_forward(): Promise
  - Go forward to the next page

  • mcp__playwright__browser_network_requests(): Promise<NetworkRequest[]>
  - Return all network requests since loading page

  • mcp__playwright__browser_take_screenshot(filename?: string, fullPage?: boolean, type?: string, element?: string,
  ref?: string): Promise
  - Take a screenshot of the current page

  • mcp__playwright__browser_snapshot(): Promise
  - Capture accessibility snapshot of current page

  • mcp__playwright__browser_click(element: string, ref: string, button?: string, doubleClick?: boolean): Promise
  - Perform click on a web page

  • mcp__playwright__browser_drag(startElement: string, startRef: string, endElement: string, endRef: string):
  Promise
  - Perform drag and drop between two elements

  • mcp__playwright__browser_hover(element: string, ref: string): Promise
  - Hover over element on page

  • mcp__playwright__browser_select_option(element: string, ref: string, values: string[]): Promise
  - Select an option in a dropdown

  • mcp__playwright__browser_tab_list(): Promise<Tab[]>
  - List browser tabs

  • mcp__playwright__browser_tab_new(url?: string): Promise
  - Open a new tab

  • mcp__playwright__browser_tab_select(index: number): Promise
  - Select a tab by index

  • mcp__playwright__browser_tab_close(index?: number): Promise
  - Close a tab

  • mcp__playwright__browser_wait_for(text?: string, textGone?: string, time?: number): Promise
  - Wait for text to appear/disappear or specified time
