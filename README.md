# {{Project Name}} - A Project Template

This is a template repository for new Python projects.

## How to Use This Template

1.  **Click the "Use this template" button** on GitHub to create a new repository based on this template.
2.  **Clone your new repository:**
    ```bash
    git clone https://github.com/your-username/your-new-repository-name.git
    cd your-new-repository-name
    ```
3.  **Rename the project:**
    *   Search globally for `{{Project Name}}` and replace it with your actual project name.
    *   Search globally for `{{project_slug}}` and replace it with a short, lowercase, hyphenated version of your project name (e.g., `my-awesome-project`).
    *   Rename the main package directory if applicable (e.g., `src/{{project_slug}}`).
4.  **Update project metadata:**
    *   Modify `pyproject.toml` (if it exists) with your project's details (name, version, author, etc.).
    *   Update any other configuration files (e.g., `setup.py`, `Makefile`).
5.  **Install dependencies:**
    *   Set up a virtual environment:
        ```bash
        python -m venv .venv
        source .venv/bin/activate  # On Windows use: .venv\\Scripts\\activate
        ```
    *   Install project dependencies (e.g., `pip install -r requirements.txt` or `pip install .`).
6.  **Customize the `.gitignore` file** to suit your project's needs.
7.  **Update this `README.md`** to describe your project.
8.  **Write your code!**

## Placeholder Values

This template uses the following placeholders that you should replace:

*   `{{Project Name}}`: The human-readable name of your project (e.g., "My Awesome Project").
*   `{{project_slug}}`: A short, lowercase, hyphenated version of your project name, suitable for use in filenames, package names, etc. (e.g., `my-awesome-project`).
*   `{{author_name}}`: Your name or your organization's name.
*   `{{author_email}}`: Your email address.

## AI-Assisted Development Rules & Agent Guidelines

This project template is designed for advanced AI-assisted development and incorporates a comprehensive set of rules and agent-specific guidelines. These are located in the `.ai_rules/` directory:

*   **Master Development Rules:** For the complete set of development standards, architectural principles, persona-specific rules, and tooling guidelines, please refer to the master index at [`.ai_rules/rules/index.md`](./.ai_rules/rules/index.md).
*   **Agent-Specific Instructions:** Guidelines for individual AI agents collaborating on this project (Memex, Warp 2.0, Jules, Gemini CLI) can be found in the `.ai_rules/agents/` directory. See:
    *   [Memex Agent Instructions](./.ai_rules/agents/memex_agent.md)
    *   [Warp 2.0 Agent Instructions](./.ai_rules/agents/warp_agent.md)
    *   [Jules AI Agent Instructions](./.ai_rules/agents/jules_agent.md)
    *   [Gemini CLI Agent Instructions](./.ai_rules/agents/gemini_cli_agent.md)

Adherence to these documented rules and guidelines is crucial for all AI agents and human developers contributing to projects based on this template. The "Unified Cursor Rulebook" (contents now within `.ai_rules/rules/`) serves as the primary source of truth.

Happy coding!
