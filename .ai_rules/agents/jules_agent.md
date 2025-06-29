# Agent Instructions for {{Project Name}}

This document provides guidelines for AI agents working on projects generated from this template.

## Project Initialization

1.  **Identify Placeholders:** This project template uses placeholders like `{{Project Name}}`, `{{project_slug}}`, `{{author_name}}`, and `{{author_email}}`.
    *   When a new project is created from this template, your first task is to ask the user for the correct values for these placeholders.
    *   Replace all occurrences of these placeholders throughout the entire codebase (including this file, `README.md`, and any configuration files).
2.  **Rename `src/{{project_slug}}`:** If a directory named `src/{{project_slug}}` exists, rename it to `src/actual-project-slug` using the value provided by the user.

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
    *   Be aware of the security best practices outlined in `SECURITY_GUIDELINES.md`.
    *   When implementing or modifying CI/CD pipelines, or handling sensitive data, refer to these guidelines.
    *   If a task involves security-sensitive changes, explicitly mention how security considerations from the guidelines have been addressed.

## Specific Instructions for This Template

*   **README.md:** After placeholder replacement, the initial "How to Use This Template" section in `README.md` should be updated or removed to reflect the actual project's documentation.
*   **AGENTS.md:** This file (`AGENTS.md`) should also have its `{{Project Name}}` placeholder updated. The rest of its content should generally be preserved unless the project has very specific agent interaction protocols.

## Communication

*   Provide clear updates on your progress.
*   If you encounter blocking issues or need significant changes to the plan, inform the user.
*   When asking for user input, be specific about the information you need.

## Agent-Specific Guidelines

This project may involve multiple AI agents with specialized roles. For detailed instructions pertaining to specific agents, please refer to their respective guideline files:

*   **`warp_agent.md`:** Instructions for Warp 2.0 (The Enterprise Implementer & Guardian of Standards).
*   **`gemini_cli_agent.md`:** Instructions for Gemini CLI (The Specialized Coder & Rapid Prototyper).
*   **(This file, `AGENTS.md`, primarily contains general instructions and those specific to Google Jules AI when acting in its defined role for asynchronous tasks and quality assistance).*

By following these guidelines, you can help ensure the project is developed efficiently and maintainably.
