"""
Smolagents Task Library - Gradio UI
Dynamically discovers all task_XX_*.py files from the tasks/ directory
and exposes them through a unified web interface with a dropdown selector.
"""

import sys
import importlib.util
import inspect
import re
from pathlib import Path

# Ensure the project root is on sys.path so task files can import config
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

import gradio as gr


# ---------------------------------------------------------------------------
# Task discovery
# ---------------------------------------------------------------------------

def discover_tasks() -> dict:
    """
    Scan tasks/ for files named task_XX_*.py and return an ordered dict:
        { "01 - Web Search": <module>, ... }
    Legacy files that do NOT match the task_NN_ prefix are skipped.
    """
    tasks_dir = PROJECT_ROOT / "tasks"
    pattern = re.compile(r"^task_(\d{2})_(.+)\.py$")
    discovered = []

    for path in sorted(tasks_dir.glob("task_*.py")):
        m = pattern.match(path.name)
        if not m:
            continue
        number = m.group(1)
        slug = m.group(2).replace("_", " ").title()
        label = f"{number} - {slug}"
        discovered.append((label, path))

    task_map = {}
    for label, path in discovered:
        spec = importlib.util.spec_from_file_location(path.stem, path)
        mod = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(mod)
            if hasattr(mod, "run"):
                task_map[label] = mod
        except Exception as exc:
            # Keep broken tasks so the UI can surface the error message
            task_map[label] = exc

    return task_map


TASK_MAP = discover_tasks()
TASK_LABELS = list(TASK_MAP.keys())


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _get_run_first_param(mod) -> tuple[str, str]:
    """Return (param_name, default_value_str) for the first run() parameter."""
    if isinstance(mod, Exception):
        return "input", ""
    try:
        sig = inspect.signature(mod.run)
        params = list(sig.parameters.values())
        if params:
            p = params[0]
            default = "" if p.default is inspect.Parameter.empty else str(p.default)
            return p.name, default
        return "input", ""
    except Exception:
        return "input", ""


# ---------------------------------------------------------------------------
# Callbacks
# ---------------------------------------------------------------------------

def update_input_on_task_change(task_label: str):
    """When the user picks a new task, reset the input box to that task's default."""
    mod = TASK_MAP.get(task_label)
    if mod is None or isinstance(mod, Exception):
        return gr.update(placeholder="Enter input for this task...", value="")
    _, default = _get_run_first_param(mod)
    placeholder = default if default else "Enter input for this task..."
    return gr.update(placeholder=placeholder, value="")


def run_task(task_label: str, user_input: str) -> str:
    """Call the selected task's run() with the provided input string."""
    if not task_label:
        return "Please select a task from the dropdown."

    mod = TASK_MAP.get(task_label)
    if mod is None:
        return f"Task '{task_label}' not found."
    if isinstance(mod, Exception):
        return f"Task failed to load:\n\n{mod}"

    _, default = _get_run_first_param(mod)
    effective_input = user_input.strip() if user_input.strip() else default

    try:
        result = mod.run(effective_input)
        return str(result)
    except TypeError:
        # run() may accept multiple params — call with no args as last resort
        try:
            return str(mod.run())
        except Exception as exc:
            return f"Error running task: {exc}"
    except Exception as exc:
        return f"Error running task: {exc}"


# ---------------------------------------------------------------------------
# UI
# ---------------------------------------------------------------------------

_HEADER = """
# Smolagents Task Library

Select a task from the dropdown, enter your input (or leave blank to use the
built-in default), then click **Run Task**.
"""

with gr.Blocks(title="Smolagents Task Library", theme=gr.themes.Soft()) as demo:
    gr.Markdown(_HEADER)

    with gr.Row():
        with gr.Column(scale=1, min_width=280):
            task_dropdown = gr.Dropdown(
                choices=TASK_LABELS,
                label="Select Task",
                value=TASK_LABELS[0] if TASK_LABELS else None,
                interactive=True,
            )
            task_input = gr.Textbox(
                label="Task Input",
                placeholder="Enter input for this task...",
                lines=5,
            )
            run_btn = gr.Button("Run Task", variant="primary", size="lg")

        with gr.Column(scale=2):
            output_box = gr.Textbox(
                label="Output",
                lines=22,
                show_copy_button=True,
                interactive=False,
            )

    # Reset input placeholder when a new task is selected
    task_dropdown.change(
        fn=update_input_on_task_change,
        inputs=task_dropdown,
        outputs=task_input,
    )

    # Run on button click
    run_btn.click(
        fn=run_task,
        inputs=[task_dropdown, task_input],
        outputs=output_box,
    )

    # Also run on Enter inside the input box
    task_input.submit(
        fn=run_task,
        inputs=[task_dropdown, task_input],
        outputs=output_box,
    )

    gr.Markdown(
        f"**{len(TASK_LABELS)} tasks loaded**  |  "
        "Powered by [smolagents](https://github.com/huggingface/smolagents)"
    )


if __name__ == "__main__":
    demo.launch()
