# Part 2: Architectural & Inter-Agent Protocols

These rules govern the high-level structure of the application and how different AI agents collaborate. They draw upon best practices for MCP, A2A, ACP, and general multi-agent system design.

## 2.1. Core AI Protocols: MCP, A2A, ACP, and AG-UI

The following protocols are foundational for enabling seamless collaboration among AI agents and integration with enterprise systems. All AI agents **must** incorporate these components as applicable to their role and interaction patterns.

### 2.1.1. Model Context Protocol (MCP) - The Universal Connector

*   **Purpose:** MCP standardizes AI agents' access to external tools, data sources, and shared context. It acts as a "USB-C for AI," providing a universal interface for tool invocation and data exchange. Its goal is to break tool/data silos by exposing capabilities and context uniformly.

*   **Server Development & Transport:**
    *   **Language Flexibility:** Develop MCP servers in any programming language capable of outputting to `stdout` or serving HTTP/SSE endpoints.
    *   **Transport Options:**
        *   **`stdio`:** For local development and tools, configure servers to communicate via standard input/output.
        *   **`HTTP/SSE` (Server-Sent Events):** For remote, distributed, or streamable setups, utilize HTTP-based communication. SSE is suitable for real-time updates.
    *   **Message Format:** JSON-RPC v2.0 is the standard for requests and responses.
    *   **Versioning:** MCP server capabilities, tool schemas, and resource definitions **must** be versioned to allow clients to adapt to changes and ensure backward compatibility where feasible.

*   **Configuration & Discovery:**
    *   **Project-Specific Config:** Place a `.vscode/mcp.json` (for VS Code integration) or a generic `mcp_manifest.json` in the project directory for tools/servers specific to that project.
    *   **Global Config:** User-level global configuration (e.g., `~/.cursor/mcp.json` or IDE settings) can make MCP servers available across all workspaces.
    *   **VS Code Integration:** VS Code can automatically discover MCP servers listed in `.vscode/mcp.json` (requires `chat.mcp.discovery.enabled": true` in settings).
    *   **Environment Variables:** Manage sensitive information like API keys for MCP servers through environment variables (e.g., specified in the `env` field of `mcp.json` configurations).

*   **Tool & Resource Management:**
    *   **Tool Definition:** Servers **must** expose a directory of available tools with clear names, detailed descriptions, input/output schemas (e.g., using OpenAPI, JSON Schema), and defined permissions.
    *   **Resource Types:**
        *   **Text Resources:** UTF-8 encoded text (source code, config files).
        *   **Binary Resources:** Base64 encoded data (images, PDFs, audio).
    *   **URI Schemes:** Define and use custom URI schemes (e.g., `file://`, `git://`, `db://`, `mcp://`) to uniquely identify resources. URIs **must** be validated to prevent unauthorized access.
    *   **Resource Discovery:**
        *   **Direct Resources:** Expose a list of concrete resources via a `resources/list` endpoint.
        *   **Resource Templates:** Provide URI templates for dynamic resource construction (e.g., `git://{repo_url}/blob/{commit_sha}/{file_path}`).
    *   **Resource Access:**
        *   Implement `resources/read` method for clients to retrieve resource contents.
        *   Support `resources/subscribe` and `resources/unsubscribe` methods for real-time updates on resource changes.

*   **Security & Best Practices:**
    *   **Access Control:** Implement appropriate, granular access controls for sensitive resources and tools.
    *   **Tool Approval:**
        *   **Default Mode:** Require explicit user approval before an agent executes an MCP tool, especially for write-actions or sensitive data access.
        *   **"Yolo Mode" (Auto-Approval):** Allow agents to run specific, trusted MCP tools automatically without user approval only if explicitly configured by the user (e.g., per session, workspace, or universally for read-only tools).
    *   **Error Handling:** Return standard JSON-RPC error codes and messages for common failures (e.g., resource not found, unauthorized, internal server error).
    *   **Logging and Auditing:** Maintain comprehensive logs of AI data access, tool usage, and MCP interactions for compliance, debugging, and auditing.
    *   **Input Validation:** Rigorously validate all inputs to tools and resource access methods.
    *   **Prompt Injection & Tool Poisoning:** Be aware of these risks. Consider using tools like `MCPSafetyScanner` or `MCP Guardian` (hypothetical or actual) for proactive auditing of MCP configurations and traffic.

*   **Agent Interaction & Advanced Features:**
    *   **VS Code Agent Mode:** In IDEs like VS Code, enabling Agent Mode (`chat.agent.enabled`) allows agents to perform multi-step coding tasks using MCP-configured tools (e.g., `#workspace.search`, `#fetch`, file edits, terminal commands). Tool invocations are logged and typically require approval. Multiple agent sessions can run concurrently.
    *   **Multi-Modal Communication:** Support various data modalities (text, audio, video) through appropriate resource type definitions and handling.
    *   **Compatibility:** Design MCP interfaces aiming for compatibility across various AI models and client platforms.
    *   **Sampling Integration:** MCP can expose sampling parameters (e.g., `n_samples`, `top_k`, `temperature`) for tools that wrap LLMs, allowing clients to request varied outputs.
    *   **LSP Inspiration:** MCP draws inspiration from the Language Server Protocol (LSP), extending standardized tool discovery and agentic workflows.

*   **Scaffolding & Examples:**
    *   **MCP Server:** See `src/mcp_server_example.py` for a Python/FastAPI example.
    *   **MCP Configuration:** See `.vscode/mcp.json` for an example client-side configuration.
*   **Future Considerations:**
    *   Contribute to and adopt standardized packaging formats and installation tools for MCP servers.
    *   Explore support for additional data modalities and hierarchical agent systems.
    *   Participate in community-led standards development.

### 2.1.2. Agent-to-Agent (A2A) Protocol - Standardized Collaboration
*Purpose, Key Features, Scaffolding, and Further Reading remain largely the same as the previous version, but ensure they align with the idea that A2A builds upon MCP for tool access if needed by individual agents.*
*   **Purpose:** A2A enables AI agents to discover each other, advertise capabilities, negotiate tasks, and coordinate actions across diverse systems and platforms. It uses HTTP/JSON-RPC and Server-Sent Events (SSE) for structured, real-time communication.
*   **Key Features & Rules:**
    *   **Capability Advertisement & Negotiation (Agent Cards):** Agents **must** publish their capabilities, version, supported modalities, endpoints, and security requirements via a JSON-formatted "Agent Card" (typically at `/.well-known/agent.json` or registered with an orchestrator). See `.well-known/agent_example.json`. During initial interaction or discovery, agents should be able to negotiate or confirm compatible capabilities.
    *   **Discovery & Interaction:** Agents discover others via their Agent Cards and interact using defined communication patterns/speech acts (e.g., REQUEST, INFORM, OFFER, NEGOTIATE, ACCEPT, DECLINE, FORWARD, ACK) for intent-rich collaboration.
    *   **Task Lifecycle Management:** A2A should support managing task lifecycles with real-time status updates (e.g., `submitted`, `in_progress`, `completed`, `failed`) often streamed via SSE.
    *   **Secure Communication:** Utilize established standards like HTTPS. Authentication and authorization (e.g., OpenAPI-style API keys, OAuth) **must** be clearly defined in Agent Cards and enforced.
    *   **Stateless Design:** A2A interactions **should be designed to be stateless** wherever possible. All necessary context for a task should be passed explicitly in the message payload. This enhances scalability, resilience, and simplifies agent logic. Stateful interactions must be carefully justified and managed (e.g., via an orchestration layer or defined session semantics).
*   **A2A + MCP Interoperability:** Use A2A for high-level agent-to-agent messages, task delegation, and workflow coordination. Individual agents then use MCP for their internal tool access and resource interactions needed to fulfill their assigned A2A tasks.
*   **Further Reading:** O'Reilly’s “Designing Collaborative Multi-Agent Systems with the A2A Protocol.”

### 2.1.3. Agent Communication Protocol (ACP) - Low-Latency Local Interaction
*(Content remains largely the same)*
*   **Purpose:** ACP is designed for local-first, event-driven, low-latency communication in shared runtimes (e.g., on-device agents, robotics, browser extensions).
*   **Use Case:** Employ when near-instant, decentralized coordination is needed with minimal overhead, and where HTTP might be too slow. Examples: WebSockets, shared memory, platform-specific IPC.

### 2.1.4. AI-Augmented User Interface (AG-UI) - Seamless Human-AI Interaction
*(Content remains largely the same)*
*   **Purpose:** AG-UI enhances traditional user interfaces by integrating natural language capabilities, allowing users to interact with AI agents and the application more intuitively.
*   **Implementation Principles:** Wrap existing UI, preserve original functionality, ensure context-awareness, and provide real-time feedback.

## 2.2. Multi-Agent System (MAS) Design & Orchestration Layer
*(Content remains largely the same, but emphasize the use of A2A/MCP for agent dispatch)*
*   **Core Principle:** Start simple, iterate. Orchestrator-Worker pattern is recommended.
*   **AI Orchestration Layer Responsibilities:** Agent discovery (via A2A Agent Cards), task decomposition (LangGraph - `08_TOOLING.md`), agent dispatch (via A2A/MCP), context management, results aggregation, error handling, logging, state management.
*   **Platform-Specific SDKs:** When building with specific LLM provider platforms (e.g., OpenAI), leverage their agent-specific SDKs (like OpenAI's Agents SDK) for potentially tighter integration with their models and built-in tools (see `08_TOOLING.md` for more on OpenAI's framework).

## 2.3. Interpretable AI & LLM-as-a-Judge
*(Content remains largely the same)*
*   **Interpretability:** Prioritize architectures exposing intermediate reasoning.
*   **LLM-as-a-Judge:** Use one LLM to critique/score another's output based on a rubric. (See `06_ORCHESTRATION.md` for prompt examples).

*This document provides a foundational understanding of the AI agent architecture. For deeper dives into specific protocols or patterns, refer to their dedicated documentation or industry best practices.*
