# Part 4: Core Development Principles

These principles guide general software development practices and decision-making for all agents.

## 4.1. M.I.N.T. Principle (When to use OOP)

Default to functional programming paradigms where possible, especially in languages like JavaScript/TypeScript and Python, due to benefits like immutability, predictability, and easier testing.

Only introduce Object-Oriented Programming (OOP) classes and structures when the **M.I.N.T.** principle clearly applies:

*   **M - Multiple Instances:**
    *   You foresee needing many instances of a complex data structure, each with its own state.
    *   *Example:* A `User` class where you'll have many `User` objects, each holding different profile information.

*   **I - Instances with Not-Serialized (or In-memory) Data:**
    *   The data associated with each instance is complex and not easily or efficiently passed around as plain JSON or simple serialized values.
    *   This includes instances that might hold references to functions (methods), complex internal objects, or manage resources like network connections or file handles that are inherently stateful and live in memory.
    *   *Example:* A `WebSocketConnection` class that manages an active connection and its associated buffers and event handlers.

*   **N - Non-trivial Structures & Behavior:**
    *   The data structure itself is non-trivial (many fields, nested structures) AND it has significant behavior (multiple methods) associated directly with its data.
    *   If it's just a data container with simple getters/setters, a plain object or a dictionary/struct might be sufficient.

*   **T - Tightly-Coupled Functions (Methods):**
    *   Multiple functions (which would become methods) operate on the exact same underlying data structure (the instance's state).
    *   Encapsulating this data and behavior together within a class improves organization, reduces the need to pass the data structure around to many free functions, and can make the code easier to reason about.
    *   *Example:* A `ShoppingCart` class with methods like `addItem()`, `removeItem()`, `calculateTotal()`, `applyDiscount()`, all operating on the cart's internal list of items.

**Guidance for AI:**
When asked to design a feature, if the above conditions (particularly M, N, and T) are met, proposing an OOP approach is appropriate. Otherwise, lean towards functional approaches, data structures (like Pydantic models in Python or interfaces/types in TypeScript), and utility functions.

## 4.2. SPARC Framework (For Documentation, Reasoning, and Planning)

Incorporate the SPARC framework when generating documentation, explaining reasoning behind decisions, creating commit messages, or outlining plans. This provides a structured way to communicate context and outcomes.

*   **S - Situation:**
    *   What is the current context or background? What was the state of affairs before the action?
    *   *Example:* "The user login page was experiencing slow load times due to unoptimized image assets."

*   **P - Problem/Purpose:**
    *   What specific problem was being addressed? What was the goal or objective of the task/action?
    *   *Example:* "The problem was to reduce page load time and improve user experience. The purpose of this task was to implement image optimization."

*   **A - Action/Approach:**
    *   What specific steps were taken to address the problem or achieve the objective? What was the implemented solution?
    *   *Example:* "Action taken: Compressed all JPEG and PNG assets using an image optimization library, implemented lazy loading for off-screen images, and converted some icons to SVG format."

*   **R - Result:**
    *   What was the outcome of the action? Were the objectives met? Include quantitative data if possible.
    *   *Example:* "Result: Page load time for the login page decreased by 60% (from 5s to 2s). Lighthouse performance score improved by 20 points."

*   **C - Conclusion/Key Learnings/Next Steps:**
    *   What was learned from this process? What are the key takeaways? Are there any follow-up actions or recommendations?
    *   *Example:* "Conclusion: Image optimization significantly impacts perceived performance. Key learning is to integrate image optimization into the build process for all new assets. Next step: Monitor performance metrics to ensure sustained improvement."

**Guidance for AI:**
When generating commit messages, PR descriptions, or explaining a complex piece of code you've written, structure your explanation using SPARC elements to provide clarity.

## 4.3. CRUD Operations

When designing data models, APIs, or any feature that involves managing persistent data, ensure that standard CRUD operations are considered and, where appropriate, implemented.

*   **C - Create:**
    *   The ability to add new data records or resources.
    *   *API Example:* `POST /users` to create a new user.

*   **R - Read:**
    *   The ability to retrieve existing data records or resources, both individually and as collections, often with filtering and pagination.
    *   *API Example:* `GET /users` to list users, `GET /users/{id}` to retrieve a specific user.

*   **U - Update:**
    *   The ability to modify existing data records or resources. This can be a full update (PUT) or a partial update (PATCH).
    *   *API Example:* `PUT /users/{id}` to replace a user record, `PATCH /users/{id}` to modify specific fields.

*   **D - Delete:**
    *   The ability to remove data records or resources. Consider soft deletes (marking as inactive) vs. hard deletes.
    *   *API Example:* `DELETE /users/{id}` to delete a user.

**Guidance for AI:**
When tasked with creating a feature that manages any kind of data (e.g., "user profiles," "product inventory," "blog posts"), inherently consider what CRUD operations are needed and either implement them or scaffold them if the prompt is high-level. If the prompt is very specific (e.g., "create only the read endpoint for products"), then stick to that, but be aware of the broader CRUD context.

These core principles should underpin the development process, leading to more robust, maintainable, and well-documented software.
