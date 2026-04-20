# Smolagents Task Library

## Goal
Build a curated library of 20 real-world agentic tasks using `smolagents`, including scripts, notebooks, and a Gradio UI.

## Research Summary
- `smolagents` is a lightweight library by HuggingFace for building agents.
- It supports `CodeAgent` (executes Python code) and `ToolCallingAgent`.
- Integration with OpenRouter can be achieved using `OpenAIModel` with `base_url="https://openrouter.ai/api/v1"`.
- Standard tools include `DuckDuckGoSearchTool`, `GoogleSearchTool`, and custom Python functions decorated with `@tool`.

## Approach
1.  **Infrastructure**: Create `config.py` for model initialization (HF Inference API / OpenRouter) and `requirements.txt`.
2.  **Task Development**: Implement 20 tasks across 5 categories. Each task will have a standalone `.py` script and a corresponding `.ipynb`.
3.  **UI Layer**: Build a Gradio `app.py` that dynamically loads and runs these tasks.
4.  **Documentation**: Comprehensive `README.md` and docstrings.

## Subtasks
1. Set up project structure and core files (`requirements.txt`, `config.py`, `.env.example`).
2. Implement Category 1: Web & Research (Tasks 1-4).
3. Implement Category 2: File & Data Processing (Tasks 5-8).
4. Implement Category 3: Code Tasks (Tasks 9-12).
5. Implement Category 4: API & Integration (Tasks 13-16).
6. Implement Category 5: Productivity (Tasks 17-20).
7. Generate Jupyter notebooks for all 20 tasks based on the `.py` scripts.
8. Build the Gradio `app.py` dashboard to run any task.
9. Finalize `README.md` and verify all scripts are runnable.

## Deliverables
| File Path | Description |
|-----------|-------------|
| `tasks/*.py` | 20 standalone agent scripts |
| `notebooks/*.ipynb` | 20 corresponding Jupyter notebooks |
| `app.py` | Gradio UI for the library |
| `config.py` | Centralized model/API configuration |
| `requirements.txt` | Project dependencies |
| `README.md` | Documentation |

## Evaluation Criteria
- All 20 scripts run without errors.
- Gradio UI successfully executes tasks.
- Support for both HF Inference API and OpenRouter is verified.
- Code follows production standards (type hints, docstrings).
