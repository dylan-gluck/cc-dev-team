# TODO:

- [x] Creative team improvements
  - [x] MCP for Stock Images
  - [x] MCP for ArtDept (Wireframes, Logos, Assets)
  - [x] Update: Agent Prompts, Commands

- [ ] Orchestration improvements
  - [ ] Config vs Templates vs Workflows
  - [ ] Team Heirarchy, Delegation rules
  - [ ] Standard team roles (ScrumMaster, Director)
  - [ ] Multi-team orchestration
  - [ ] Dynamic Status line
  - [ ] Hooks Integration
  - [ ] Infinitite Execution

- [ ] Create Workflows
  - [ ] Team vs Org workflows
  - [ ] Intake: Idea > Team Directors > Research > Team Leads - Initial Specs > Directors - (Ready for Planning or Assign Refinements)
  - [ ] PlanEpic: ...

- [ ] Output Styles as Dashboards!
  - [ ] Task / Ticket Flow
  - [ ] Team Observability

## Completed

- [x] Create meta commands & meta-agent
- [x] Create dev team agents from collected examples
- [x] Specifications for UV & Bun scripting
- [x] Documentation
- [x] Spec Collaboration system using hooks
- [x] Script to install to specified dir or global claude-code
- [x] Custom MCP to replace Firecrawl
- [x] Implement Collaboration system


# Thoughts

**Agent Choice**
Refactor the following aspects of the spec using specialized agents.
- **engineering-lead**: General-purpose system design & review
- **research-project**: General-purpose project analysis, index files & extract context
- **meta-output-style**: Agent specialized in claude-code output-style config and SudoLang
- **meta-python-uv**: Agent specialized in writing single-file UV scripts
- **meta-config**: Agent specialized in claude-configuration
- **meta-agent**: Agent specialized in writing claude-code agent definitions
- **meta-command**: Agent specialized in writing claude-code slash-commands

**Output Styles**
`ai_docs/orchestration/v2-output-styles-design.md`
`ai_docs/orchestration/v2-output-style-*.md`
- The output-style logic is written in Python but these programs should be written in natural language or SudoLang. The designs look great though, this just needs to be converted to a format that makes sense.
- Sudolang may make sense for some slash-command prompts as well.
- SudoLang docs available in `ai_docs/sudolang/*`


**Inter-session API**
`ai_docs/orchestration/v2-inter-session-api.md`
- The inter-session-api design is written as a WebSocket API when we do not need that. This should instead describe an API that uses JSON for centralized state and scripts with params to fetch/update state.
- We are mainly concerned with individual sessions and making sure they maintain independent state. We want to share configurations, tools, even epics/sprint data, between sessions, but actual messages, events, hooks should be isolated.


**State-management Design**
`ai_docs/orchestration/v2-state-management-design.md`
- This generally looks correct and makes sense
- My only call-out is that tasks & state should be different from a planned Epic or Sprint. State contains refrence to the ACTIVE epic/sprint/tasks within the active session.
