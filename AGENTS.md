# AI Agent Roster

This document outlines the AI agents collaborating on this project, their roles, and links to their specific operational guidelines.

## Core Agents

### 1. Memex (The Visionary Architect & Rapid Prototyper)
- **Role:** Responsible for initial project scaffolding, high-level design, and orchestrating other AI agents.
- **Specific Guidelines:** [Memex Agent Instructions](./.ai_rules/agents/memex_agent.md)
- **General Guidelines (Applicable to all agents):** [General Agent Guidelines](./.ai_rules/agents/00_GENERAL_AGENT_GUIDELINES.md)

### 2. Warp 2.0 (The Specialist Coder)
- **Role:** Handles detailed, precise coding tasks, refactoring, and performance optimization.
- **Specific Guidelines:** [Warp 2.0 Agent Instructions](./.ai_rules/agents/warp_agent.md)
- **General Guidelines (Applicable to all agents):** [General Agent Guidelines](./.ai_rules/agents/00_GENERAL_AGENT_GUIDELINES.md)

### 3. Jules AI (The Asynchronous Task Handler & Quality Assistant)
- **Role:** Manages well-defined, background tasks such as running tests, updating dependencies, performing automated maintenance, and assisting with quality assurance.
- **Specific Guidelines:** [Jules AI Agent Instructions](./.ai_rules/agents/jules_ai.md)
- **General Guidelines (Applicable to all agents):** [General Agent Guidelines](./.ai_rules/agents/00_GENERAL_AGENT_GUIDELINES.md)

### 4. Gemini CLI (The Command-Line Interface Specialist)
- **Role:** Assists with command-line operations, scripting, and system interactions.
- **Guidelines:** [Gemini CLI Agent Instructions](./.ai_rules/agents/gemini_cli_agent.md)
- **General Guidelines (Applicable to all agents):** [General Agent Guidelines](./.ai_rules/agents/00_GENERAL_AGENT_GUIDELINES.md)


## Interaction Protocol

All agents are expected to adhere to the communication and hand-off protocols defined in the [General Agent Guidelines](./.ai_rules/agents/00_GENERAL_AGENT_GUIDELINES.md), their respective specific instruction files, and the master development rules found in [.ai_rules/rules/index.md](./.ai_rules/rules/index.md).

### Agent Handover Log

For seamless transitions and shared context, agents should consult and update the [Agent Handover Log](./.ai_rules/agent_logs/handover_log.md) when passing responsibilities or noting significant project updates.
