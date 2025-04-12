# Task: Repository Analysis and Architectural Documentation

**Objective:** Analyze the `universal-intelligence` repository codebase and generate comprehensive, visually rich architectural documentation.

**Scope:**

1.  **Initial Review:** Start with `README.md` to understand the project's stated goals and overview.
2.  **Codebase Analysis:** Systematically review the entire codebase located primarily within the `universal_intelligence/` directory. Pay attention to:
    *   Core components (`universal_intelligence/core/`)
    *   Community contributions (`universal_intelligence/community/`) including agents, models, and tools.
    *   Directory structure and module organization.
    *   Key classes, functions, and their interactions.
    *   Data flow and control flow patterns.
    *   Dependencies and external integrations (e.g., MCP servers).
3.  **Documentation Generation:** Create a new `docs/` directory (if it doesn't exist) and populate it with architectural documentation. This should include:
    *   High-level architecture diagrams (e.g., using Mermaid). PlantUML is also welcome where it enhances clarity. Focus on visual illustration and readability.
    *   Component diagrams detailing major parts of the system.
    *   Sequence diagrams for key workflows (if applicable).
    *   Descriptions of core modules and their responsibilities.
    *   Explanation of the plugin system (community agents, models, tools).
    *   Notes on design patterns and best practices observed.

**Deliverables:**

*   A `docs/` directory containing well-structured Markdown files and diagrams.
*   Visual aids (Mermaid diagrams) embedded within the documentation.
*   Clear explanations of the architecture, components, and interactions.

**Process:**

*   Iteratively analyze sections of the codebase.
*   Generate documentation concurrently with analysis.
*   Seek clarification or feedback as needed during the process.

**Proposed Plan:**

*   **Directory Structure:**
    ```ascii
    docs/
    ├── 00_system_architecture.md
    ├── 01_overview.md
    ├── 02_core_architecture.md
    └── 03_plugin_architecture.md
    ```

*   **Steps:**
    1.  **Setup:** Create the `docs/` directory.
    2.  **Initial Overview:** Analyze `README.md`, create `docs/01_overview.md`.
    3.  **Core Architecture:** Analyze `universal_intelligence/core/`, create `docs/02_core_architecture.md`.
        *   Identify key classes/functions (e.g., using `list_code_definition_names`).
        *   Read main files (`universal_agent.py`, `universal_model.py`, `universal_tool.py`).
        *   Include a core component diagram (Mermaid/PlantUML).
    4.  **Plugin Architecture:** Analyze `universal_intelligence/community/`, create `docs/03_plugin_architecture.md`.
        *   Analyze directory structure (`agents/`, `models/`, `tools/`).
        *   Explain the extension mechanism.
        *   Include a plugin interaction diagram.
        *   *Optional:* Analyze specific examples for illustration.
    5.  **Overall System Diagram:** Create or update `docs/00_system_architecture.md` with a high-level diagram showing core and plugin interactions.
    6.  **Review & Refine:** Iterate through the generated documents, ensuring clarity, accuracy, consistency, and strong visual representation.
