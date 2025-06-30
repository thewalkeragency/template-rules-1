# Part 1: Core Directives & Global Rules

These rules are foundational and apply to all interactions and generated code, regardless of the task or persona.

## 1.1. The Prime Directive: Absolute Prompt Fidelity
The AI must strictly follow user prompts without omissions, additions, or assumptions.

Do not reinterpret, restructure, or "optimize" instructions. The user always provides a plan.

Prioritize precise task completion over creativity or unsolicited enhancements.

## 1.2. The Universal Workflow: PRD to Prompt
All development work must follow this strict hierarchical order:

1.  **PRD (Product Requirements Document):** High-level feature definition.
2.  **Tasks:** (Derived from PRD) Decompose the PRD into major functional blocks.
3.  **Sub-tasks:** Break down tasks into smaller, manageable implementation steps.
4.  **Sub-sub-tasks:** Further refinement if necessary.
5.  **Prompts:** (Created for each specific task) Generate code for a single, specific sub-task, often referencing existing code for context.

Do not proceed to the next level until the current one is defined.

## 1.3. Contextual Prompting is Mandatory
Never generate code from a generic prompt if a relevant example exists in the codebase.

Always reference similar, existing components or files to guide the AI.

**Bad:** "Make a user settings page."

**Good:** "Make a user settings page, following the pattern and style of `@/components/ProfileEditor.tsx`."

## 1.4. Automatic Scaffolding at Project/Feature Start
This rule **must be activated by default** by the responsible AI Agent (typically the Architect/Memex persona) when a new coding project, feature, or module is requested, even if scaffolding is not explicitly mentioned by the user.

**Procedure:**

1.  **Initiate Smart Scaffolding Prompts (if not specified by user):**
    *   The AI Agent **must** proactively ask clarifying questions to guide scaffolding if the user's request is high-level:
        *   *"Would you like me to scaffold the base structure for this [project/feature/module]?"*
        *   *"What framework or architecture (e.g., MVC, RESTful, microservices, component-based) are you targeting?"*
        *   *"Should I generate starter files for common elements like models, views, controllers, services, routes, or tests?"*

2.  **Default to Best-Practice Scaffolding (if no user response or insufficient detail):**
    *   If the user doesn't respond to clarification prompts or provides minimal detail, the AI Agent should scaffold the most likely base structure using:
        *   Common conventions for the specified (or inferred) language/framework.
        *   Standard directory structures (e.g., `src/`, `tests/`, `docs/`, relevant subdirectories for components, services, etc.).
        *   Boilerplate for core modules (e.g., main application file, configuration placeholders, basic routing).

3.  **Output Structure Summary for Confirmation:**
    *   **Before** writing detailed functional code for the new feature/module, the AI Agent **must** present a summary of the proposed scaffolded structure to the user. This could be a file/folder tree view.
    *   The AI Agent **must** ask for user confirmation or edits before proceeding with populating the scaffold. Example: *"Here's the proposed structure. Does this look correct, or would you like any changes before I proceed?"*

4.  **Adhere to Scaffolding Consistency Standards:**
    *   All generated scaffolds **must**:
        *   Use clear, conventional naming for files and directories.
        *   Include `TODO:` placeholders or comments where user-specific customization or further implementation is needed.
        *   Be designed for modularity and maintainability.
        *   Include brief inline comments explaining the purpose of key generated files or boilerplate sections.

5.  **Link to User Intent and Context:**
    *   If the user has previously described project goals (e.g., in a PRD or initial discussion), the AI Agent should attempt to match the scaffold to:
        *   The expected functionality (e.g., if it's an API, scaffold route handlers and data models; if it's a UI component, scaffold the component file and a basic test).
        *   Existing architectural preferences or patterns evident in the project (e.g., monorepo structure, established component design patterns).

This structured approach to scaffolding ensures a consistent and well-organized start to new development efforts, aligning with project standards from the outset.

## 1.5. Versioning of Rules and Protocols
*   All rule documents (like this one), agent definitions, and inter-agent communication protocols (MCP, A2A schemas) **must** be versioned.
*   The `index.md` and individual rule/agent files should clearly state their version and last update date.
*   This ensures clarity and helps manage changes as the system evolves.

## 1.6. Stateless Interactions (General Principle)
*   When designing agent interactions and services, aim for statelessness where practical. Each request should contain all necessary information for processing.
*   This promotes scalability, resilience, and simplifies caching. Stateful interactions should be explicitly designed and justified.

## 1.7. Agent Handover Protocol: Code Review & Human Clarification
When an agent takes over a task or project from another agent (or from a human), the following protocol **must** be followed:

1.  **Review Handover Log:** The acquiring agent **must** first read the relevant entries in the [Agent Handover Log](./agent_logs/handover_log.md) to understand the current status, decisions, and pending items.
2.  **Code Comprehension:** The acquiring agent **must** then thoroughly review the relevant codebase changes and existing code to understand the implementation details. This involves reading the code, not just relying on summaries.
3.  **Clarification with Human-in-the-Loop:** If, after reviewing the log and the code, the acquiring agent has *any* questions, ambiguities, or requires further context to proceed confidently, it **must** ask the human user for clarification. The agent should clearly articulate its questions and the specific areas of confusion.
    *   **Do not proceed with coding if there is uncertainty.**
    *   **Prioritize clarity over independent assumptions.**

## 1.8. Complete and Error-Free Task Execution
*   **Full Task Completion:** Every task, whether explicitly requested or undertaken proactively to ensure overall success, must be completed to 100%. No task is considered finished until it is fully functional, tested, and integrated without introducing new issues.
*   **Zero-Error Tolerance:** All code modifications, new implementations, or system interactions must be executed without errors. If an error occurs, it must be immediately addressed and resolved before proceeding.
*   **Proactive Problem Solving:** If a necessary deviation or proactive step is taken, it must be executed with the same commitment to completion and error-free operation as a directly requested task. The agent is responsible for ensuring the entire job is done, not just its assigned part.

## (Associated File Formatting Rules - From Part 4 of Unified Cursor Rulebook)

These apply to all Markdown documentation generated or managed by AI agents.

### Markdown Formatting

*   **MD001 (heading-increment):** Heading levels must only increment by one level at a time (e.g., `#` -> `##`, not `#` -> `###`).
*   **MD003 (heading-style):** Use a consistent heading style (ATX `#` style preferred).
*   **MD004 (ul-style):** Maintain a consistent unordered list style (e.g., use `-` consistently).
*   **MD005 (list-indent):** Enforce consistent indentation for list items at the same level.
*   **MD007 (ul-indent):** Enforce consistent indentation across all unordered list items.
*   **MD009 (no-trailing-spaces):** No trailing spaces at the end of lines, except where required for hard line breaks.
*   **MD010 (no-hard-tabs):** Do not use hard tabs; use spaces instead for indentation.
*   **MD012 (no-multiple-blanks):** No more than one consecutive blank line is allowed.
*   **MD013 (line-length):** Keep line length reasonable (e.g., 80-120 characters) for readability.
*   **MD022 (blanks-around-headings):** Headings must be surrounded by blank lines (one blank line above and one below).
*   **MD023 (heading-start-left):** All headings must start at the beginning of the line (no leading spaces).
*   **MD024 (no-duplicate-heading):** Avoid duplicate heading content within the same document/section.
*   **MD025 (single-title/single-h1):** A document should ideally have only one top-level heading (H1 / `#`).
*   **MD026 (no-trailing-punctuation):** Avoid trailing punctuation (e.g., `.`, `:`, `!`) in headings.
*   **MD031 (blanks-around-fences):** Fenced code blocks must have a blank line before and after them for separation.
*   **MD040 (fenced-code-language):** Always specify the language for fenced code blocks to enable syntax highlighting.
