# Analysis Document: Dependency Management Consolidation

## 1. Objective

-   Standardize and simplify Python dependency management for the `universal-intelligence` project by consolidating all dependency specifications into the `pyproject.toml` file.

## 2. Current State

-   The project currently uses a hybrid approach:
    -   `pyproject.toml`: Defines optional dependency groups (extras) under the `[project.optional-dependencies]` table (`community`, `cuda`, `mps`, `gemma`, `mcp`, `dev`). This aligns with modern Python packaging standards (PEP 621).
    -   `requirements-*.txt` files: Separate files exist for each optional group (`requirements-community.txt`, `requirements-cuda.txt`, etc.) and a base `requirements.txt` (which is empty and only points to the others).
-   This dual system creates redundancy and potential for inconsistencies.

## 3. Comparison Findings

-   A comparison between the `requirements-*.txt` files and the corresponding sections in `pyproject.toml` revealed the following:
    -   **`community`**: Match perfectly.
    -   **`cuda`**: `pyproject.toml` includes `llama-cpp-python`, while `requirements-cuda.txt` does not. The `pyproject.toml` definition is likely more correct, as `llama-cpp-python` often requires specific build flags for CUDA.
    -   **`dev`**: `pyproject.toml` includes version specifiers (e.g., `ruff>=0.3.0`), while `requirements-dev.txt` lacks them. The `pyproject.toml` definition follows best practices.
    -   **`gemma`**: Match perfectly (including the specific Git reference).
    -   **`mcp`**: Match perfectly.
    -   **`mps`**: `requirements-mps.txt` includes `accelerate`, whereas `pyproject.toml` does not list it under the `mps` extra. Since `accelerate` is already part of the `community` and `cuda` extras, its inclusion specifically for `mps` in the `.txt` file seems redundant or incorrect. `pyproject.toml` is likely correct.
    -   **`requirements.txt`**: Contains no dependencies, only comments directing users to other files.

## 4. Assessment

-   Maintaining both `requirements-*.txt` files and `pyproject.toml` for the same optional dependencies is unnecessary and error-prone, as evidenced by the minor inconsistencies found.
-   `pyproject.toml` is the standard, canonical way to define project metadata and dependencies (including optional ones) in modern Python projects.
-   Consolidating into `pyproject.toml` provides a single source of truth, simplifies maintenance, and aligns the project with current best practices. The existing definitions in `pyproject.toml` appear to be the most accurate and complete.

## 5. Recommendation

-   Remove all `requirements-*.txt` files.
-   Rely solely on `pyproject.toml` for defining base and optional dependencies.
-   Update documentation (`README.md`) to reflect this change, instructing users to install extras using the standard `pip install .[extra]` syntax.
