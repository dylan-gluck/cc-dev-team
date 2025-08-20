# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2025-08-20

### 🚀 Features

#### Project Template System
- **New comprehensive JSON-based project template system** - Enables rapid project scaffolding with best practices built-in
- **8 initial project templates** - Includes web, api, cli, library, static, MCP, microservice, and pipeline templates
- **Template validation and testing framework** - Ensures template quality and consistency
- **Research phase integration** - Automatically gathers integration documentation during template selection
- **Multi-stack support** - Templates support various technology stacks and configurations

#### Command System Enhancements
- **49 new slash commands** across 6 categories for complete orchestration control:
  - `/orchestrate` - Sprint, task, team, and epic management
  - `/state` - Direct state operations with jq-style queries and validation  
  - `/monitor` - Real-time monitoring with live dashboards and metrics
  - `/team` - Team coordination with capacity planning and handoffs
  - `/config` - Configuration management with validation and auto-fix
  - `/debug` - Comprehensive debugging tools and system diagnostics
- **Rich console formatting** - Tables, progress bars, and visual indicators
- **Multiple output formats** - JSON, table, CSV support for flexibility
- **Interactive workflows** - Step-by-step guidance with preview and confirmation flows

#### New Project Commands
- `/project:readme` - Parallel README updates across projects
- `/git:tag` - Automated release management
- Enhanced `/git:commit` - Now supports push options (--push, --push-force, --set-upstream)

#### New Specialized Agents
- **engineering-svelte** - Svelte/SvelteKit development specialist
- **research-crawl** - Web scraping and crawling specialist  
- **research-project** - Project analysis and exploration specialist
- **meta-init-enhancer** - Template system implementation specialist
- **meta-rename** - Comprehensive rename operations with reference updates

#### Meta Commands
- `/meta:rename:agent` - Rename agents with reference updates
- `/meta:rename:command` - Rename commands with reference updates
- `/meta:list:tools` - List available tools (renamed from /meta:all-tools)

### 📚 Documentation

- **Comprehensive Svelte framework guides** - Runes, styling, transitions documentation
- **Complete SvelteKit documentation** - Concepts, deployment, features
- **Template system documentation** - Comprehensive guides for all template types
- **Command documentation** - Complete reference with examples and quick start guide
- **Updated README** - Latest agent roster and command listings

### 🔧 Refactoring

- **Command hierarchy improvements** - Better organization following category:subcategory:command pattern
- **Meta commands reorganization** - Commands moved to new/ subdirectory for clarity

### 💥 Breaking Changes

- **Meta command reorganization** - `/meta:gen-agent-command` is now `/meta:new:agent-command`
- **Config command restructure** - `/config` moved to `/config:help` for consistent subcategory structure

### 🎯 Key Improvements

- **Enterprise-grade orchestration** - Complete framework with state management, event streaming, and observability
- **Enhanced developer experience** - Intuitive navigation, helpful error messages, safety features
- **Template-driven development** - Rapid project setup with built-in best practices
- **Comprehensive monitoring** - Real-time dashboards with configurable refresh intervals
- **Advanced debugging** - Interactive workflows with rollback capabilities

---

## [0.0.1] - Initial Release

### 🚀 Features

- Initial project structure for Claude Code development team scaffolding
- Basic agent configuration and workflow setup
- Core development team orchestration framework

[Unreleased]: https://github.com/your-username/cc-dev-team/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/your-username/cc-dev-team/compare/v0.0.1...v0.1.0
[0.0.1]: https://github.com/your-username/cc-dev-team/releases/tag/v0.0.1