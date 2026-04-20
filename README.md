# Smolagents Task Library

> Made Autonomously Using [NEO - Your Autonomous AI Engineering Agent](https://heyneo.com)
>
> [![VS Code Extension](https://img.shields.io/badge/VS%20Code-NEO%20Extension-blue?logo=visualstudiocode)](https://marketplace.visualstudio.com/items?itemName=NeoResearchInc.heyneo)  [![Cursor Extension](https://img.shields.io/badge/Cursor-NEO%20Extension-purple?logo=cursor)](https://marketplace.cursorapi.com/items/?itemName=NeoResearchInc.heyneo)

## Architecture

![Architecture](architecture.svg)

## Overview

The **Smolagents Task Library** is a collection of 20 ready-to-run AI agent tasks built on top of [smolagents](https://github.com/huggingface/smolagents) and the HuggingFace Inference API. Every task exposes a simple `run()` function that can be called from the CLI or through the bundled Gradio web UI.

Tasks span five categories: web research, file & data processing, reasoning, creative & API, and productivity. All tasks share a common configuration layer (`config.py`) that reads credentials from a `.env` file, making it straightforward to swap models or API keys without touching task code.

## Installation

**Requirements:** Python 3.9+

```bash
# 1. Clone / download the project
cd smolagents-task-library

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure credentials
cp .env.example .env
# Edit .env and fill in your HF_TOKEN (required for inference)
```

## Configuration

Copy `.env.example` to `.env` and set at minimum:

| Variable | Description |
|---|---|
| `HF_TOKEN` | HuggingFace API token (required) — get one at https://huggingface.co/settings/tokens |
| `OPENROUTER_API_KEY` | Optional — only needed if routing through OpenRouter |
| `DEFAULT_MODEL` | Model ID to use (default: `deepseek-ai/DeepSeek-V3.2`) |
| `DEFAULT_PROVIDER` | Inference provider (default: `novita`) |

## Tasks

### Category 1 — Web Research (Tasks 01-04)

| # | File | Description |
|---|---|---|
| 01 | `task_01_web_search.py` | **Web Search & Research** — Runs a DuckDuckGo search and compiles a structured markdown research report. |
| 02 | `task_02_news_summarizer.py` | **News Summarizer** — Fetches the top N news articles on any topic and produces a clean news digest. |
| 03 | `task_03_website_analyzer.py` | **Website Analyzer** — Fetches a URL, strips HTML noise, and returns an AI-generated site analysis. |
| 04 | `task_04_trend_tracker.py` | **Trend Tracker** — Searches for trends in a domain (technology, finance, health, etc.) and produces a trend report with predictions. |

### Category 2 — File & Data Processing (Tasks 05-08)

| # | File | Description |
|---|---|---|
| 05 | `task_05_csv_summarizer.py` | **CSV Summarizer** — Loads a CSV file with pandas, generates descriptive statistics, and asks the model for deeper insights. |
| 06 | `task_06_docx_analyzer.py` | **DOCX Analyzer** — Extracts text and tables from a `.docx` file and classifies/structures the content (resume, invoice, meeting notes, etc.). |
| 07 | `task_07_log_analyzer.py` | **Log Analyzer** — Parses log files (common timestamp + level formats), counts error/warning distribution, and AI-prioritises issues into P1/P2/P3. |
| 08 | `task_08_code_reviewer.py` | **Code Reviewer** — Reads a source file, detects the language, and produces a full code-quality review with security and style notes. |

### Category 3 — Reasoning (Tasks 09-12)

| # | File | Description |
|---|---|---|
| 09 | `task_09_chain_of_thought.py` | **Chain of Thought** — Guides the agent to break any problem into explicit reasoning steps before answering. |
| 10 | `task_10_math_solver.py` | **Math Solver** — Solves mathematical problems step by step; uses `CodeAgent` so it can execute Python for numeric verification. |
| 11 | `task_11_logic_puzzle.py` | **Logic Puzzle Solver** — Accepts any logic/deductive puzzle and works through constraints to produce a justified solution. |
| 12 | `task_12_decision_analyzer.py` | **Decision Analyzer** — Structures a decision using pros/cons, weighted factors, and risk assessment to output a clear recommendation. |

### Category 4 — Creative & API Integration (Tasks 13-16)

| # | File | Description |
|---|---|---|
| 13 | `task_13_story_generator.py` | **Story Generator** — Generates creative short/medium/long stories from a theme and genre using a custom `StoryGeneratorTool`. |
| 14 | `task_14_code_explainer.py` | **Code Explainer** — Accepts a code snippet and language name, then produces a plain-English explanation with context. |
| 15 | `task_15_email_drafter.py` | **Email Drafter** — Drafts professional emails for any purpose, recipient, and tone (formal/casual/friendly). |
| 16 | `task_16_data_formatter.py` | **Data Formatter** — Takes unstructured text data and reformats it into JSON, CSV, or a markdown table. |

### Category 5 — Productivity (Tasks 17-20)

| # | File | Description |
|---|---|---|
| 17 | `task_17_quiz_creator.py` | **Quiz Creator** — Generates multiple-choice quizzes on any topic at a chosen difficulty level with answers. |
| 18 | `task_18_argument_analyzer.py` | **Argument Analyzer** — Evaluates the logical structure of an argument, identifies fallacies, and rates its strength. |
| 19 | `task_19_meeting_scheduler.py` | **Meeting Scheduler** — Suggests optimal meeting times given participants, duration, and scheduling constraints. |
| 20 | `task_20_document_summarizer.py` | **Document Summarizer** — Condenses long documents into brief, detailed, or bullet-point summaries of configurable length. |

## Usage

### CLI (run any task directly)

Each task is a self-contained Python script with a `run()` function and a CLI entry point:

```bash
# Task 01 — web search
python tasks/task_01_web_search.py --query "latest developments in quantum computing"

# Task 05 — CSV summarizer
python tasks/task_05_csv_summarizer.py --file my_data.csv

# Task 10 — math solver
python tasks/task_10_math_solver.py --problem "Integrate x^2 from 0 to 3"

# Task 13 — story generator
python tasks/task_13_story_generator.py

# Task 20 — document summarizer
python tasks/task_20_document_summarizer.py
```

Or import and call `run()` directly from Python:

```python
import sys; sys.path.insert(0, ".")
from tasks.task_01_web_search import run
report = run("open source LLMs 2025")
print(report)
```

### Gradio Web UI

```bash
python app.py
# Opens at http://localhost:7860
```

The UI dynamically discovers all `task_XX_*.py` files, presents them in a dropdown, and lets you enter custom input before clicking **Run Task**. Leave the input blank to use each task's built-in default.

## Project Structure

```
smolagents-task-library/
├── app.py                    # Gradio web UI
├── config.py                 # Shared configuration (model, tokens)
├── requirements.txt
├── .env.example              # Credential template
├── architecture.svg          # Architecture diagram
└── tasks/
    ├── task_01_web_search.py
    ├── task_02_news_summarizer.py
    ├── task_03_website_analyzer.py
    ├── task_04_trend_tracker.py
    ├── task_05_csv_summarizer.py
    ├── task_06_docx_analyzer.py
    ├── task_07_log_analyzer.py
    ├── task_08_code_reviewer.py
    ├── task_09_chain_of_thought.py
    ├── task_10_math_solver.py
    ├── task_11_logic_puzzle.py
    ├── task_12_decision_analyzer.py
    ├── task_13_story_generator.py
    ├── task_14_code_explainer.py
    ├── task_15_email_drafter.py
    ├── task_16_data_formatter.py
    ├── task_17_quiz_creator.py
    ├── task_18_argument_analyzer.py
    ├── task_19_meeting_scheduler.py
    └── task_20_document_summarizer.py
```

## Dependencies

| Package | Purpose |
|---|---|
| `smolagents>=1.0.0` | Agent framework (ToolCallingAgent, CodeAgent, HfApiModel) |
| `gradio>=4.0.0` | Web UI |
| `huggingface-hub>=0.20.0` | Model access |
| `python-dotenv>=1.0.0` | `.env` loading |
| `requests>=2.31.0` | HTTP requests (task 03) |
| `pandas>=2.0.0` | CSV analysis (task 05) |
| `beautifulsoup4>=4.12.0` | HTML parsing (task 03) |
| `python-docx` | DOCX extraction (task 06) |

## License

MIT
