# {{Project Name}} - An AI-Assisted Project Template

This is a template repository for new Python projects designed for advanced, multi-agent AI development.

## How to Use This Template

1.  **Clone this repository.**
2.  **Set up a virtual environment:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows use: .venv\\Scripts\\activate
    ```
3.  **Run the setup script:**
    ```bash
    python setup_project.py
    ```
    This script will prompt you to enter your project's name, slug, and author details, and it will automatically replace all placeholder values.
4.  **Install dependencies:**
    ```bash
    pip install -e .
    ```
5.  **Delete the setup script:**
    ```bash
    rm setup_project.py
    ```
6.  **Write your code!**

## Project Structure & Documentation

This template is organized to support a robust, AI-driven development process.

*   **AI Rules & Agents (`.ai_rules/`):** The core of the AI collaboration framework.
    *   **Agent Instructions (`.ai_rules/agents/`):** Contains the operational guidelines for each AI agent (Memex, Warp, Jules, etc.).
    *   **Development Rules (`.ai_rules/rules/`):** Defines the standards for architecture, security, testing, and more. See the [Master Index](.ai_rules/rules/index.md).
*   **Source Code (`src/`):** The main application code resides here.
*   **Tests (`tests/`):** Contains all automated tests.
*   **Documentation (`docs/`):** Includes project documentation, such as:
    *   [**Technology Stack**](docs/TECH_STACK.md): An overview of the key technologies used.
    *   [**Code Examples**](docs/examples/): Practical examples and snippets.
    *   [**PRD Template**](docs/PRD_TEMPLATE.md): A template for Product Requirements Documents.

## Placeholder Values

The setup script will handle the replacement of these values:

*   `{{Project Name}}`: The human-readable name of your project.
*   `{{project_slug}}`: A short, lowercase, hyphenated version of your project name.
*   `{{author_name}}`: Your name or your organization's name.
*   `{{author_email}}`: Your email address.

Happy coding!
