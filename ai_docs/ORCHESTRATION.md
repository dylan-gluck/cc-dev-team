# Enterprise Orchestration Framework

Multi-agent orchestration with state management, team heirarchy, coordination & observability.

Uses claude-code agents, commands & hooks with mcp & system tools.

---

## Components

**Agents**
- Task-specific agent definitions for efficient and effective collaboration
- Agents have specific system prompts, tool access, and recieve context at runtime from orchestrator and shared state management system.

**Teams**
- Teams are composed of multiple agents. Some are responsible for research and documentation tasks, others on feature implementation, others on review/testing/reporting.
- Every team has one Orchestrator agent which has the ability to initialize sprints, assign tasks, kick off sub-agents and workflows.

**Hooks (State Management System)**
- Shared state & context using JSON or MCP
  - Active tasks, Task Queue, Dependencies
  - Bugs Intake, handoff & observe
  - Cross-agent/team Communication: Questions, Findings, Coordination, Handoffs
  - Locked files, Worktrees
- Logs

**Output Styles**
- JSON / Yaml / XML
- HTML / React (`bun create`)
- Python Script (`uv run`)
- Markdown Readme / CC Template

**Status Line**
- Team
- Current Epic
- Current Sprint
- Active / Queued / Completed Tasks in Sprint
- Test Coverage / Failing / Passing
- Open Issues
- Active Agents (Color Dots ?)

---

## Teams

Each team runs in it's own claude-code instance in a terminal. A team is initialized with a slash command that specifies the team, epic and sprint to begin work on.

**Example:** .claude/commands/team/start.md
- `/teams:start <team> [options]`
- `/team:start product --epic=2 --sprint=0`

Uppon running the command, the root claude-code instance assumes the role of team orchestrator. If no options are passed, the orchestrator checks the state for active or next pending sprint & spawns specified agents / tasks.

**Product**
- CPO / Product Director (Orchestrator)
- Team Strategy & Coordination manager (Track Epic / Sprint Process & State, Cross-team Collaboration & Observability)
- Product Manager (Feature Requirements / PRD, Feature Review & Signoff)
- Business Analyst (Research & Design Business Logic, Analyze & Review Implementation)
- Data Scientist (Research & Design Data Models, Analyze & Review Implementation)
- Deep Research / Investigation (Parallel Web Search & Summary)
- Team Analytics & Reporting (Observe Logs, Analytics, Reports)

**Marketing**
- Director of Marketing (Orchestrator)
- Content Strategist (Research, Content Inventory)
- SEO Researcher (SEO Research & Strategy)
- SEO Engineer (Implement SEO)
- SEO Analyst (Track Performance & Write Reports)
- Copywriter (Write Specific Copy)

**Creative**
- Creative Director (Orchestrator)
- UX Lead (Design System -- Colors, Fonts, Spacing)
- Wireframe designer (Image gen)
- Photographer (Image gen)
- Illustrator (Image gen)
- Logo designer (Image gen)

**Engineering**
- CTO / Director of Engineering (Orchestrator)
- Engineering Manager (Track Epic / Sprint Process & State, Team Observability, Sign off on sprints)
- Documentation Research Specialist (Web Search / Scrape / Summarize)
- Tech Lead / Architect (Write Specs & Data Models)
- Fullstack Engineer (Business Logic E2E Implementation)
- UX Engineer (Components, Layouts, Design System, Desktop/Mobile)
- API Engineer (Backend Business Logic from Spec)
- Test Engineer (Write & Maintain Valid tests from Spec)
- Documentation Writer (Write & Maintain Project Docs)
- Tech Lead (Code review, Consistency Check, Test Passing)

**QA**
- QA Director (Orchestrator)
- QA Engineer (e2e testing)
- QA Engineer (Write test scripts, data, etc)
- QA Analyst (Reports, Issue tracking)

**DevOps**
- DevOps Manager (Orchestrator)
- CI/CD Engineer (Github Actions, Scripts)
- Infrastructure Engineer (Containerization, Infra as Code)
- Cleanup Engineer (Delete extra tests, organize files)
- Release Manager (Release Notes, Changelog)

---

# Project Flow & Task Delegation

The purpose of this system is to mirror that of a real software company, composed of teams with internal heirarchy and specialized contributors. Additionally, this system must implement each aspect of the SDLC and have specific commands & workflows for each phase of development.

### SLDC

- Discovery / Planning / Requirements
- Specs / Data Model / Designs / User Stories
- Epics / Sprints / Tasks / Deliverables & Dependencies
- Implementation Loop (Epics, Sprints, Bugs)
- Monitoring, Reports
- Releases, Issue tracking, CI/CD

### Workflows

- Brainstorm Loop (Leadership)
- Project spec > Project SDLC
- Feature spec > Feature SDLC
- Epic (Plan, Start, Status)
- Sprint (Plan, Start, Status, Continue, Next)
- Task (Start, Status, Fix, Dependencies)
- Bugs (Review, Status, Fix)
- Release (New, Status, Schedule)
- Code Review & Consistency Check
- End-to-end Test Suite
- Security Audit, Compliance, Accessibility
- Update Docs, User Stories
- Generate Test Data, Test Scripts
- Infinite Agent loop 🤔 How ?

---

## Questions & Ideas

- Cross agent coordination, memory (Hooks)
  - Epics, Sprint, Tasks
  - State, Logs, Queue, Dependencies & Handoff
  - Create specific Mcp tools?
- Team > Orchestrator > Agent
- How can we implement a real schedule ? Burndown ? Reporting ?
- When does it make most sense to use worktrees?
  - For each feature? Per team? Per Sprint?

---
