# Technology Stack

This document outlines the primary technologies, frameworks, and platforms utilized in projects based on this template.

## Communication Protocols

- **Model-to-Client Protocol (MCP):** A standardized protocol for communication between AI models and client applications, ensuring consistent interaction patterns.
- **Agent-to-Agent (A2A) Communication:** A conceptual framework for enabling direct communication and collaboration between different AI agents.

## AI & Machine Learning

- **CopilotKit:** A framework for building in-app AI chatbots and AI-powered user interfaces.
- **LangGraph:** A library for building stateful, multi-actor applications with LLMs, based on graph structures.

## Frontend

- **Next.js:** A React framework for building server-side rendered and statically generated web applications.
- **Vite:** A modern frontend build tool that provides a faster and leaner development experience for modern web projects.
- **Three.js:** A cross-browser JavaScript library and API used to create and display animated 3D computer graphics in a web browser.

## Backend

- **FastAPI:** A modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.
- **Flask:** A lightweight WSGI web application framework in Python.

## Python Project Setup Example

For Python projects, you can use the following setup:

1.  **Set up a virtual environment:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows use: .venv\\Scripts\\activate
    ```
2.  **Install dependencies:
    ```bash
    pip install -e .
    ```

## Deployment & Infrastructure

- **DigitalOcean:** A cloud infrastructure provider for deploying and scaling applications.
- **ngrok:** A reverse proxy service that creates a secure tunnel from a public endpoint to a locally running web service.

## Project Structure

This project's structure and agent interaction rules are defined in the `.ai_rules/` directory, providing a comprehensive framework for AI-assisted development.


---

### Code Examples

For practical examples of how these technologies work together, see the following files:

- **MCP Request:** [`mcp_request_example.json`](./examples/mcp_request_example.json)
- **FastAPI Endpoint:** [`fastapi_endpoint_example.py`](./examples/fastapi_endpoint_example.py)
- **LangGraph Setup:** [`langgraph_example.py`](./examples/langgraph_example.py)
- **CopilotKit Component:** [`copilotkit_example.jsx`](./examples/copilotkit_example.jsx)

