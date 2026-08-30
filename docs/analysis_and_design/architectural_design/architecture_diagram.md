# Architectural Design

## 1.1 Architecture Diagram
*(Insert Architecture Diagram Image Here)*

### 1.1.1 System Decomposition & Component Specifications

*   **Presentation Layer (Frontend Client)**
    *   **Component:** React SPA (Single Page Application).
    *   **Responsibility:** Renders the interactive user interface, including the Chat Workspace and the 7-Day Visual Calendar. It collects user inputs, manages local session states, and asynchronously communicates with the backend via RESTful APIs.

*   **Web Router Layer (API Gateway)**
    *   **Component:** FastAPI Server Gateway.
    *   **Responsibility:** Acts as the central traffic controller, authenticating incoming requests and monitoring the health of the external AI provider.
    *   **Fault Tolerance:** Implements the Active Routing Protocol to automatically reroute requests to the local Fallback Controller if the external LLM API times out.

*   **Orchestration Layer (AI Agentic Layer)**
    *   **Component:** LLM Planning Agent & MCP Interface.
    *   **Responsibility:** Processes natural language inputs and uses a Model Context Protocol (MCP) to trigger specific internal tools (e.g., `check_prerequisites()`) rather than relying on internal LLM knowledge.

*   **Core Logic & Data Layer (Deterministic Engine)**
    *   **Component:** Rule-Based Python Engine & MySQL Database.
    *   **Responsibility:** The absolute source of truth that calculates graduation progress, validates credit limits (14-24 credits), and traverses prerequisite trees using DAG algorithms.
    *   **Data Security:** The LLM does not have direct database access; all data retrieval passes through this strictly typed layer to ensure data integrity.