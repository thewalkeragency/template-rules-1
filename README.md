# memex.tech - An AI-Assisted Project Template

This is a template repository for new projects designed for advanced, multi-agent AI development.

## How to Use This Template

1.  **Clone this repository.**
2.  **Run the setup script:**
    ```bash
    ./setup_project.sh
    ```
    This script will prompt you to enter your project's name, slug, and author details, and it will automatically replace all placeholder values.
3.  **Delete the setup scripts:**
    ```bash
    rm setup_project.py setup_project.sh
    ```
4.  **Write your code!**

## Project Structure & Documentation

This template is organized to support a robust, AI-driven development process.

*   **AI Rules & Agents (`.ai_rules/`):** The core of the AI collaboration framework.
    *   **Agent Instructions (`.ai_rules/agents/`):** Contains the operational guidelines for each AI agent (Memex, Warp, Jules, etc.).
    *   **Development Rules (`.ai_rules/rules/`):** Defines the standards for architecture, security, testing, and more. See the [Master Index](.ai_rules/rules/index.md).
*   **Source Code (`src/`):** The main application code resides here.
*   **Tests (`tests/`):** Contains all automated tests.
*   **Documentation (`docs/`): Includes project documentation, such as:
    *   [**Technology Stack**](docs/TECH_STACK.md): An overview of the key technologies used.
    *   [**Code Examples**](docs/examples/): Practical examples and snippets.
    *   [**PRD Template**](docs/PRD_TEMPLATE.md): A template for Product Requirements Documents.

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
# Ensure your virtual environment is activated and you are in the template-rules-1 directory
python -m knowledge_reinforcer.main --url "https://example.com/your-article-link" --tags "AI,Learning" --purpose "New AI concept"
```

To store direct text content:

```bash
# Ensure your virtual environment is activated and you are in the template-rules-1 directory
python -m knowledge_reinforcer.main --text "Your direct text content here." --tags "MyNotes,Idea" --purpose "Personal thought on a new method"
```

The extracted markdown files will be saved in the `knowledge_base/` directory (e.g., `knowledge_base/articles/`, `knowledge_base/videos/`, `knowledge_base/direct_text/`) relative to the `knowledge_reinforcer` directory.

## Placeholder Values

The setup script will handle the replacement of these values:

*   `memex.tech`: The human-readable name of your project.
*   `memex-tech`: A short, lowercase, hyphenated version of your project name.
*   `AI Developer`: Your name or your organization's name.
*   `ai@developer.com`: Your email address.

Happy coding!
