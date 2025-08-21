# Orchestration System Improvements

The current orchestration architecture is primarily composed of claude-code configuration files(agents, commands, hooks) + external state_manager, event_stream, message_bus and observibility scripts.

**Existing Components:**
- Configuration files are located in `.claude/orchestration/*`.
- The system updates/reads `.claude/state/orchestration.json` as the centralized state store using python scripts located in `.claude/scripts/*`
- Cross-team messages are stored in `.claude/messages/*`
- Session id & initial prompt are stored in `.claude/data/sessions/*`
- All agent definitions live in `.claude/agents/*`. Agents are triggered in self-contained threads and have access to specific tools. Agent definitions are essentially system-prompts that only apply to that agent's thread. Some agents have the capability to spawn sub-agents through Task tool. The `subagent_stop` hook is fired when a subagent has completed it's task.
- Slash commands `.claude/commands/**/*` are essentially re-usable user-prompts that run in the main thread. These commands load specific context and provide instructions to the main agent which then acts on these instructions making tool calls and spawning subagents until the task is complete. Slash commands are always triggered by the user and correlate with the `user_prompt_submit` hook.
- Hooks are user-defined shell commands that execute at various points in Claude Code’s lifecycle. Hooks provide deterministic control over Claude Code’s behavior, ensuring certain actions always happen rather than relying on the LLM to choose to run them. Currently we are only using hooks for logging, however they have potential to be a lot more powerful in the context of this orchestration system. They use JSON to pass data back and forth and can fire different commands based on "matchers" (primarily used for `PreToolUse` and `PostToolUse`).

**Components to Add:**
- Output Styles are a new feature of claude-code that directly affect the main agent loop and only affect the system prompt. They replace the default claude-code behavior and can be used in this orchestration system in combination with slash-commands to support different "modes".
- Status-lines allow customization of the status line with a user-defined script. We can combine the status-line script with our observibility system and hook into the statefull data in real-time.

---

# Thoughts on Session Management & Orchestration

## Sessions

We are not doing anything useful with the SessionStart hook, just logging the id and user-prompt. What if the session-id can be used to isolate state to a single claude-code instance. All subagents within this session share the same state but are isolated from other sessions.

The current system uses a property in the settings to determine if orchestration mode is enabled. This is limiting because it is a shared setting that would effect all individual sessions. Instead, we should set this property at runtime in each individual session's state file. Then we can access it's value inside of our hooks to determine if we should fire the orchestratio-related functions. Every hook input includes the current session ID which can be used for routing.

## Hooks & Workflows

https://docs.anthropic.com/en/docs/claude-code/hooks

In the last major iteration of this system we transitioned from using hooks for orchestration / state updates to a command-based approach. The reasoning was being able to opt-in to orchestration workflows and still maintain default claude-code behavior.

By utilizing output-styles as stored system prompts for the main thread and shash-commands to trigger specific workflows we should be able to maintain flexibility. Slash commands have a particular feature where bash commands can be run at execution by using `!` syntax. These can be used to update the state for a given session or fetch session data.

As mentioned above: once we move the orchestration_mode_enabled flag to the session-specific state, we can use this value in our hook scripts to enable the orchestration features. Additionally, we can customize behavior within the hook scripts with conditional logic based on session state, eg: workflow type, active agents, or if messages exist in the communication queue.

Hooks also have the ability to return JSON in stdout. This allows us to perform logical operations in our scripts and modify execution behavior. For example: PreToolUse can block execution of a tool call while PostToolUse can block subsequent tool calls for a given agent. Stop and SubagentStop can block the main thread or a subagent thread from stopping, providing a reason that the agent can act uppon. At session start additionalContext is passed back to the agent, this can be a useful way to surface state/orchestration information to the agent, eg: Which teams and agents were activated based on config, type of workflow etc. Combined with slash-commands we can now trigger specific workflows/team configurations at runtime and load stateful context into the agent thread.

### Interesting Hook Functionality

#### `Stop`/`SubagentStop` Decision Control
`Stop` and `SubagentStop` hooks can control whether Claude must continue.
  - `"block"` prevents Claude from stopping. You must populate `reason` for Claude to know how to proceed.
  - `undefined` allows Claude to stop. `reason` is ignored.

#### `SessionStart` Decision Control
`SessionStart` hooks allow you to load in context at the start of a session.
  - `"hookSpecificOutput.additionalContext"` adds the string to the context.

#### Configure Hooks for MCP tool calls
`PreToolUse` & `PostToolUse` hooks can use matcher syntax to fire specific commands for certain MCP tools. Eg: `mcp__memory__create_entities`

---

# Agent Heirarchy

The original idea was to have each Team running in its own terminal and have the main thread assume the identity of the team's director; that system design introduced limitations we already touched on, each team would be running in its own session and we would have to use the shared `.claude/orchestration/settings.json` to enable orchestration features.

The updated system design utilizes agent heirarchy and subagent calling with the `Task` tool to properly delegate tasks & recude context bloat. Rather than running each team in separate terminals, the user now triggers multi-team workflows from a single session-thread. The type of workflow / task is determined by the user at runtime.


### Full Cross-team Orchestration Example:
1. User enables an output-style. This overrides the main system prompt and modifies the behavior of the main agent.
2. User executes a slash-command. This kicks off a specific task or action in the main thread but also has the ability to directly update the state object by executing bash with the `!` syntax. Additionally we can return any data we want to to the main agent for context or to modify their behavior eg: what subagents to spawn, active epic/sprint/task, remaining tasks, message/bug backlog.
3. The main agent recieves orchestration context from initial bash commands and combines with slash-command instructions for a full understanding of what actions to take next. (A powerful slash-command pattern is to use the state as input params for logical operations described in natural language)
4. The main agent delegates tasks to team directors who in turn assign specific tasks to their team. Recursively, agents who have the capability to will delegate work to subagents. Each agent will have a specific task defined in their prompt as well as strict instructions on orchestration script usage to fetch/update state in addition to the automatic updates through hooks.

---

# Output Styles

https://docs.anthropic.com/en/docs/claude-code/output-styles

Output Styles are a feature of claude-code that have a very specific function, essentially serving as modified system prompts for the main agent thread.

> Output styles directly affect the main agent loop and only affect the system prompt. Agents are invoked to handle specific tasks and can include additional settings like the model to use, the tools they have available, and some context about when to use the agent.

> You can think of output styles as “stored system prompts” and custom slash commands as “stored prompts”.

## Output Styles as Orchestration Layer

In the context of this orchestration system, these output-styles can be used to:
1. Visually present state in a dashboard style view
2. Toggle different orchestration configurations or modes

### Orchestration Modes & Views

Let's assume we use the output-styles as system prompts that turn the main agent thread into a specific "program" or LLM powerd app. Each app may have a specific use case, for example one runtime specifically for multi-team collaboration that provides specific instructions for the main agent that can modify how slash-commands are interpreted. This output-style may specify instructions for displaying information in a TUI style dashboard layout where each message from the main agent becomes a UI screen for the runtime. Data may be fetched from the orchestration layer state during runtime in addition to returned context from subagents.

Another use-case may be facilitating brainstorming sessions between team leaders: reviewing performance metrics, logs, optimizing team configuration based on backlog. This layout may resemble some kind of chat-thread or visualization of stats.

Most likely there will be many variations of these output styles. It might make sense to name/categorize them by `<function|scope>_<display>` eg: `all-team_dashboard`, `leadership_chat`, `config-settings_tui`. Additionally, user can interact with program using their responses as input. Think commands more than prompts, but it's an LLM so anything goes.

There is a really interesting concept called SudoLang which is a programming language for LLMs. I've used it to create some really cool TUI programs. We should probably create a meta-sudolang agent that specializes in writing these programs.

### LLMs are Already Stateful

In experimenting with SudoLang and writing programs that have visual layouts, I learned that LLMs by nature maintain statefulness in the session chat. This enables us to maintain data-structures in memory or perform simple logic operations at runtime.

This state is not accessable to other agents outside the main chat thread which is why we need the orchestration layer to exist outside of the chat; hooks and direct command execution enable the main agent to fetch/update state data to display visually to the user in addition to the summaries returned by subagents.

---

# Status Lines

https://docs.anthropic.com/en/docs/claude-code/statusline

## How It Works

Directly add a statusLine command to `.claude/settings.json`. This can run a single-file `uv` script that interacts with the orchestration data layer.
```json
{
  "statusLine": {
    "type": "command",
    "command": "~/.claude/statusline.sh",
    "padding": 0 // Optional: set to 0 to let status line go to edge
  }
}
```

Your status line command receives structured data via `stdin` in JSON format:
```json
{
  "hook_event_name": "Status",
  "session_id": "abc123...",
  "transcript_path": "/path/to/transcript.json",
  "cwd": "/current/working/directory",
  "model": {
    "id": "claude-opus-4-1",
    "display_name": "Opus"
  },
  "workspace": {
    "current_dir": "/current/working/directory",
    "project_dir": "/original/project/directory"
  },
  "version": "1.0.80",
  "output_style": {
    "name": "default"
  },
  "cost": {
    "total_cost_usd": 0.01234,
    "total_duration_ms": 45000,
    "total_api_duration_ms": 2300,
    "total_lines_added": 156,
    "total_lines_removed": 23
  }
}
```

**Update Frequency:**
- The status line is updated when the conversation messages update.
- Updates run at most every 300ms

### Python Example (From claude-code docs)

```python
#!/usr/bin/env python3
import json
import sys
import os

# Read JSON from stdin
data = json.load(sys.stdin)

# Extract values
model = data['model']['display_name']
current_dir = os.path.basename(data['workspace']['current_dir'])

# Check for git branch
git_branch = ""
if os.path.exists('.git'):
    try:
        with open('.git/HEAD', 'r') as f:
            ref = f.read().strip()
            if ref.startswith('ref: refs/heads/'):
                git_branch = f" | 🌿 {ref.replace('ref: refs/heads/', '')}"
    except:
        pass

print(f"[{model}] 📁 {current_dir}{git_branch}")
```

### Tips

- Keep your status line concise - it should fit on one line
- Use emojis (if your terminal supports them) and colors to make information scannable
- Use `jq` for JSON parsing in Bash (see examples above)
- Test your script by running it manually with mock JSON input: `echo '{"model":{"display_name":"Test"},"workspace":{"current_dir":"/test"}}' | ./statusline.sh`
- Consider caching expensive operations (like git status) if needed

---

# Summary of New Orchestration System Design

**Output Styles** become the new "program" that is run in the main thread. These styles specify both behavioral instructions as well as display style, eg: TUI dashboard.

**Slash Commands** are reusable user-prompts that can trigger specific workflows or actions in the main thread which may be augmented by the output-style system prompt. Slash commands can directly execute bash at initialization to fetch context or update state, but do not extrapolate variables or fire conditionally.

**Agents** are task-specific subagents that run in their own thread but are still part of the main session. They have a detailed system prompt with behavioral instructions and constraints and limited tool access. Some agents can delegate tasks to subagents with the `Task` tool, this may happen recursively. Each agent plays a specific role on the team, some implement changes, some fetch context and condense for team members, some review work and check for consistency, others primarily plan and facilitate cross-team communication. Agents are independent entities, however we have given the teams structure through the configuration system. This heirarchy can be consumed at runtime by agents to modify their behavior and enforced by logic in their system prompts.

**Hooks** automatically fire during lifecycle events across all agents and subagents in a given session. Hooks typically execute a script which accepts and returns JSON payloads which are used to communicate with the main agent thread. The hook scripts communicate with the orchestration system and contain logic to conditionally call functions and route data based on session, cwd, hook_event_name (tool_name, tool_input). Orchestration functionality may be enabled/disabled for a session by the main agent (when a slash-command is initialized) or when a hook is fired.

**Satus Lines** are single-file scripts that run continuously during a session and display real-time information to the user. This script recieves JSON state from the main claude-code thread via `stdin` and can fetch live state data for the session based on id. The status-line script should contain logic to change its diplay/output based on the running workflow, current state, last hook_event_name, etc.
