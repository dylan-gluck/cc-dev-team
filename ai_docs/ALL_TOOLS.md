# Available Tools

Here are all available tools in TypeScript function signature format:

  Task(description: string, prompt: string, subagent_type: string): void
  Launch specialized sub-agents for complex, multi-step tasks

  Bash(command: string, description?: string, run_in_background?: boolean, timeout?:
  number): void
  Execute bash commands with optional timeout and background execution

  Glob(pattern: string, path?: string): void
  Fast file pattern matching with glob patterns

  Grep(pattern: string, path?: string, output_mode?: string, glob?: string, type?:
  string, ...options): void
  Powerful search tool built on ripgrep for file content searching

  LS(path: string, ignore?: string[]): void
  List files and directories in a given absolute path

  ExitPlanMode(plan: string): void
  Exit plan mode after presenting implementation plan

  Read(file_path: string, limit?: number, offset?: number): void
  Read files from filesystem, including images, PDFs, and notebooks

  Edit(file_path: string, old_string: string, new_string: string, replace_all?:
  boolean): void
  Perform exact string replacements in files

  MultiEdit(file_path: string, edits: EditOperation[]): void
  Make multiple edits to a single file in one operation

  Write(file_path: string, content: string): void
  Write content to a file (overwrites existing)

  NotebookEdit(notebook_path: string, new_source: string, cell_id?: string,
  cell_type?: string, edit_mode?: string): void
  Edit Jupyter notebook cells

  WebFetch(url: string, prompt: string): void
  Fetch and process web content with AI analysis

  TodoWrite(todos: Todo[]): void
  Create and manage structured task lists

  WebSearch(query: string, allowed_domains?: string[], blocked_domains?: string[]):
  void
  Search the web for current information

  BashOutput(bash_id: string, filter?: string): void
  Retrieve output from background bash shells

  KillBash(shell_id: string): void
  Terminate a background bash shell

  mcp__docker-mcp__create-container(image: string, name?: string, environment?:
  object, ports?: object): void
  Create standalone Docker container

  mcp__docker-mcp__deploy-compose(compose_yaml: string, project_name: string): void
  Deploy Docker Compose stack

  mcp__docker-mcp__get-logs(container_name: string): void
  Retrieve Docker container logs

  mcp__docker-mcp__list-containers(): void
  List all Docker containers

  mcp__firecrawl__firecrawl_scrape(url: string, formats?: string[], maxAge?: number,
  ...options): void
  Scrape content from single URL with advanced options

  mcp__firecrawl__firecrawl_map(url: string, ignoreSitemap?: boolean,
  includeSubdomains?: boolean, ...options): void
  Map website to discover all indexed URLs

  mcp__firecrawl__firecrawl_crawl(url: string, maxDepth?: number, limit?: number,
  ...options): void
  Start asynchronous crawl job on website

  mcp__firecrawl__firecrawl_check_crawl_status(id: string): void
  Check status of crawl job

  mcp__firecrawl__firecrawl_search(query: string, limit?: number, lang?: string,
  country?: string, ...options): void
  Search web and optionally extract content

  mcp__firecrawl__firecrawl_extract(urls: string[], prompt?: string, schema?: object,
  ...options): void
  Extract structured information using LLM

  mcp__firecrawl__firecrawl_deep_research(query: string, maxDepth?: number,
  timeLimit?: number, maxUrls?: number): void
  Conduct deep web research with intelligent crawling

  mcp__firecrawl__firecrawl_generate_llmstxt(url: string, maxUrls?: number,
  showFullText?: boolean): void
  Generate standardized llms.txt file for domain

  mcp__playwright__browser_close(): void
  Close browser page

  mcp__playwright__browser_resize(width: number, height: number): void
  Resize browser window

  mcp__playwright__browser_console_messages(): void
  Return all console messages

  mcp__playwright__browser_handle_dialog(accept: boolean, promptText?: string): void
  Handle browser dialog

  mcp__playwright__browser_evaluate(function: string, element?: string, ref?: string):
   void
  Execute JavaScript on page/element

  mcp__playwright__browser_file_upload(paths: string[]): void
  Upload files to browser

  mcp__playwright__browser_install(): void
  Install browser if not available

  mcp__playwright__browser_press_key(key: string): void
  Press keyboard key

  mcp__playwright__browser_type(element: string, ref: string, text: string, slowly?:
  boolean, submit?: boolean): void
  Type text into editable element

  mcp__playwright__browser_navigate(url: string): void
  Navigate to URL

  mcp__playwright__browser_navigate_back(): void
  Go back to previous page

  mcp__playwright__browser_navigate_forward(): void
  Go forward to next page

  mcp__playwright__browser_network_requests(): void
  Return all network requests

  mcp__playwright__browser_take_screenshot(element?: string, ref?: string, fullPage?:
  boolean, ...options): void
  Take screenshot of page/element

  mcp__playwright__browser_snapshot(): void
  Capture accessibility snapshot

  mcp__playwright__browser_click(element: string, ref: string, button?: string,
  doubleClick?: boolean): void
  Click on web page element

  mcp__playwright__browser_drag(startElement: string, startRef: string, endElement:
  string, endRef: string): void
  Drag and drop between elements

  mcp__playwright__browser_hover(element: string, ref: string): void
  Hover over page element

  mcp__playwright__browser_select_option(element: string, ref: string, values:
  string[]): void
  Select dropdown option

  mcp__playwright__browser_tab_list(): void
  List browser tabs

  mcp__playwright__browser_tab_new(url?: string): void
  Open new browser tab

  mcp__playwright__browser_tab_select(index: number): void
  Select tab by index

  mcp__playwright__browser_tab_close(index?: number): void
  Close browser tab

  mcp__playwright__browser_wait_for(text?: string, textGone?: string, time?: number):
  void
  Wait for text/time conditions

  mcp__ElevenLabs__text_to_speech(text: string, voice_name?: string, model_id?:
  string, ...options): void
  Convert text to speech with voice synthesis

  mcp__ElevenLabs__speech_to_text(input_file_path: string, language_code?: string,
  diarize?: boolean, ...options): void
  Transcribe speech from audio file

  mcp__ElevenLabs__text_to_sound_effects(text: string, duration_seconds?: number,
  output_directory?: string, output_format?: string): void
  Generate sound effects from text description

  mcp__ElevenLabs__search_voices(search?: string, sort?: string, sort_direction?:
  string): void
  Search existing voices in library

  mcp__ElevenLabs__list_models(): void
  List all available voice models

  mcp__ElevenLabs__get_voice(voice_id: string): void
  Get details of specific voice

  mcp__ElevenLabs__voice_clone(name: string, files: string[], description?: string):
  void
  Create instant voice clone from audio

  mcp__ElevenLabs__isolate_audio(input_file_path: string, output_directory?: string):
  void
  Isolate audio from file

  mcp__ElevenLabs__check_subscription(): void
  Check subscription status and usage

  mcp__ElevenLabs__create_agent(name: string, first_message: string, system_prompt:
  string, ...options): void
  Create conversational AI agent

  mcp__ElevenLabs__add_knowledge_base_to_agent(agent_id: string, knowledge_base_name:
  string, url?: string, ...options): void
  Add knowledge base to agent

  mcp__ElevenLabs__list_agents(): void
  List all conversational AI agents

  mcp__ElevenLabs__get_agent(agent_id: string): void
  Get details about specific agent

  mcp__ElevenLabs__get_conversation(conversation_id: string): void
  Get conversation with transcript

  mcp__ElevenLabs__list_conversations(agent_id?: string, cursor?: string, ...options):
   void
  List agent conversations with metadata

  mcp__ElevenLabs__speech_to_speech(input_file_path: string, voice_name?: string,
  output_directory?: string): void
  Transform audio between voices

  mcp__ElevenLabs__text_to_voice(voice_description: string, text?: string,
  output_directory?: string): void
  Create voice previews from text prompt

  mcp__ElevenLabs__create_voice_from_preview(generated_voice_id: string, voice_name:
  string, voice_description: string): void
  Add generated voice to library

  mcp__ElevenLabs__make_outbound_call(agent_id: string, agent_phone_number_id: string,
   to_number: string): void
  Make outbound call using agent

  mcp__ElevenLabs__search_voice_library(page?: number, page_size?: number, search?:
  string): void
  Search entire ElevenLabs voice library

  mcp__ElevenLabs__list_phone_numbers(): void
  List phone numbers associated with account

  mcp__ElevenLabs__play_audio(input_file_path: string): void
  Play audio file (WAV/MP3)

  ListMcpResourcesTool(server?: string): void
  List available resources from MCP servers

  ReadMcpResourceTool(server: string, uri: string): void
  Read specific resource from MCP server
