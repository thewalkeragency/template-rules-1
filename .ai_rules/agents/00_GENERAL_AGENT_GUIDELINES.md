# Agent Instructions for memex.tech

This document provides guidelines for AI agents working on projects generated from this template.

## Project Initialization

1.  **Identify Placeholders:** This project template uses placeholders like `memex.tech`, `memex-tech`, `AI Developer`, and `ai@developer.com`.
    *   When a new project is created from this template, your first task is to ask the user for the correct values for these placeholders.
    *   Replace all occurrences of these placeholders throughout the entire codebase (including this file, `README.md`, and any configuration files).
2.  **Rename `src/memex-tech`:** If a directory named `src/memex-tech` exists, rename it to `src/actual-project-slug` using the value provided by the user.

## Development Guidelines

1.  **Understand Project Goals:** Before making changes, ensure you understand the specific goals of the project. Ask for clarification if needed.
2.  **Follow Coding Standards:**
    *   Adhere to PEP 8 for Python code.
    *   Write clear, concise, and well-documented code.
    *   Use meaningful variable and function names.
3.  **Testing:**
    *   Write unit tests for all new functionalities.
    *   Ensure all tests pass before submitting changes.
    *   Place tests in the `tests/` directory, mirroring the structure of the `src/` directory.
4.  **Dependencies:**
    *   If new dependencies are added, update the relevant files (e.g., `requirements.txt`, `pyproject.toml`). Clearly state the reason for adding a new dependency.
5.  **Documentation:**
    *   Update the `README.md` with any relevant changes to setup, usage, or project features.
    *   Document new functions, classes, and modules with docstrings.
6.  **Commit Messages:**
    *   Follow conventional commit message formats (e.g., a short imperative subject line, followed by a more detailed body if necessary).
    *   Example: `feat: Add user authentication module`
6.  **Security Awareness:**
    *   Be aware of the security best practices outlined in `../rules/05_SECURITY.md`.
    *   When implementing or modifying CI/CD pipelines, or handling sensitive data, refer to these guidelines.
    *   If a task involves security-sensitive changes, explicitly mention how security considerations from the guidelines have been addressed.

## Specific Instructions for This Template

*   **README.md:** After placeholder replacement, the initial "How to Use This Template" section in `README.md` should be updated or removed to reflect the actual project's documentation.
*   **AGENTS.md:** This file (`AGENTS.md`) should also have its `memex.tech` placeholder updated. The rest of its content should generally be preserved unless the project has very specific agent interaction protocols.

## Communication

*   Provide clear updates on your progress.
*   If you encounter blocking issues or need significant changes to the plan, inform the user.
*   When asking for user input, be specific about the information you need.

## Utilizing the Project Knowledge Base

A core component of this project's AI-assisted development approach is the `knowledge_base/` directory, located at the root of the repository. This curated collection of information serves as a dynamic, evolving source of context, best practices, code examples, and domain-specific knowledge relevant to the project.

*   **Purpose:** The Knowledge Base (KB) is designed to augment the formal rules and general knowledge of AI agents, providing them with up-to-date, project-specific context. This enables more accurate, relevant, and efficient task completion.
*   **Population:** The KB is primarily populated and updated using the `KnowledgeReinforcer` tool (see project `README.md` for usage). Users are encouraged to add relevant articles, documentation snippets, code examples, and other information to the KB.
*   **Access (General Principle):** AI agents should actively consult the Knowledge Base when:
    *   Researching a new topic, technology, or best practice.
    *   Seeking clarification on a project-specific convention not explicitly covered in the `.ai_rules/`.
    *   Looking for examples relevant to their current task.
    *   The information needed is likely to be highly contextual or rapidly evolving.
*   **Querying Mechanism (To Be Fully Defined):**
    *   The primary way to access information within the KB will be through a dedicated "Knowledge Access Protocol" (details to be specified in `../rules/00_GLOBAL.md` or `../rules/01_ARCHITECTURE.md`). This protocol will likely involve:
        *   Searching the `knowledge_base/kb_index.json` for relevant entries based on metadata (tags, keywords, source type).
        *   Performing semantic/vector searches on the content of the markdown files within `knowledge_base/` for more nuanced queries.
    *   This may be exposed to agents as an MCP tool (e.g., `#knowledge.search(query="your query", tags=["tag1", "tag2"])`).
*   **Agent-Specific Usage:** Detailed instructions on *how* and *when* each specific agent persona should utilize the Knowledge Base are provided in their respective guideline files (e.g., `memex_agent.md`, `warp_agent.md`).

By leveraging the Knowledge Base, AI agents can enhance their understanding and contribute more effectively to the project's goals.

## Agent-Specific Guidelines

This document provides general guidelines applicable to all AI agents. For detailed instructions pertaining to specific agent roles, please refer to their respective guideline files:

*   **[Memex Agent Instructions](./memex_agent.md):** For The Visionary Architect & Rapid Prototyper.
*   **[Warp 2.0 Agent Instructions](./warp_agent.md):** For The Enterprise Implementer & Guardian of Standards.
*   **[Jules AI Agent Instructions](./jules_ai.md):** For The Asynchronous Task Handler & Quality Assistant.
*   **[Gemini CLI Agent Instructions](./gemini_cli_agent.md):** For The Specialized Coder & Rapid Prototyper.

By following these general guidelines and the specific instructions for their roles, agents can help ensure the project is developed efficiently and maintainably.
