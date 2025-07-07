# {{Project Name}} - An AI-Assisted Project Template

This is a template repository for new projects designed for advanced, multi-agent AI development.

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
        source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
        ```
    *   Install project dependencies (e.g., `pip install -r requirements.txt` or `pip install .`).
6.  **Customize the `.gitignore` file** to suit your project's needs.
7.  **Update this `README.md`** to describe your project.
8.  **Write your code!**

## Project Structure & Documentation

This template is organized to support a robust, AI-driven development process.

*   **AI Rules & Agents (`.ai_rules/`):** The core of the AI collaboration framework.
    *   **Agent Instructions (`.ai_rules/agents/`):** Contains the operational guidelines for each AI agent (Memex, Warp, Jules, etc.).
    *   **Development Rules (`.ai_rules/rules/`):** Defines the standards for architecture, security, testing, and more. See the [Master Index](.ai_rules/rules/index.md).
*   **Knowledge Reinforcer (`knowledge_reinforcer/`):** A CLI tool for building a structured knowledge base for other AI agents.
*   **Source Code (`src/`):** The main application code resides here.
*   **Tests (`tests/`):** Contains all automated tests.
*   **Documentation (`docs/`): Includes project documentation.

## KnowledgeReinforcer Agent

The `KnowledgeReinforcer` is a CLI-based Python application designed to build a structured knowledge base for other AI agents. It extracts content from URLs (web pages, YouTube videos) or direct text and stores it as markdown files with rich metadata.

### Setup

1.  **Navigate to the `knowledge_reinforcer` directory:**
    ```bash
    cd knowledge_reinforcer
    ```
2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Usage

To extract content from a URL (web page or YouTube video) and save it to the knowledge base:

```bash
# Ensure your virtual environment is activated and you are in the knowledge_reinforcer directory
python main.py --url "https://example.com/your-article-link" --tags "AI,Learning" --purpose "New AI concept"
```

To store direct text content:

```bash
# Ensure your virtual environment is activated and you are in the knowledge_reinforcer directory
python main.py --text "Your direct text content here." --tags "MyNotes,Idea" --purpose "Personal thought on a new method"
```

The extracted markdown files will be saved in the `knowledge_base/` directory (e.g., `knowledge_base/articles/`, `knowledge_base/videos/`, `knowledge_base/direct_text/`) relative to the `knowledge_reinforcer` directory.

## Placeholder Values

This template uses the following placeholders that you should replace:

*   `{{Project Name}}`: The human-readable name of your project (e.g., "My Awesome Project").
*   `{{project_slug}}`: A short, lowercase, hyphenated version of your project name, suitable for use in filenames, package names, etc. (e.g., `my-awesome-project`).
*   `{{author_name}}`: Your name or your organization's name.
*   `{{author_email}}`: Your email address.

Happy coding!