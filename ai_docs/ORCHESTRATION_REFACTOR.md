# Orchestration System Improvements

The current orchestration architecture is primarily composed of claude-code configuration files(agents, commands, hooks) + external state_manager, event_stream, message_bus and observibility scripts.

The system updates/reads a json file as the centralized state store (`.claude/state/orchestration.json`).


---

# Hooks

https://docs.anthropic.com/en/docs/claude-code/hooks

#### `Stop`/`SubagentStop` Decision Control

`Stop` and `SubagentStop` hooks can control whether Claude must continue.
  - `"block"` prevents Claude from stopping. You must populate `reason` for Claude to know how to proceed.
  - `undefined` allows Claude to stop. `reason` is ignored.

```json
{
  "decision": "block" | undefined,
  "reason": "Must be provided when Claude is blocked from stopping"
}
```

#### `SessionStart` Decision Control

`SessionStart` hooks allow you to load in context at the start of a session.
  - `"hookSpecificOutput.additionalContext"` adds the string to the context.

```json
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "My additional context here"
  }
}
```
