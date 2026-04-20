"""
Smolagents Task Library - Configuration Module
Central configuration for models, API keys, and agent settings.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent / ".env"
if env_path.exists():
    load_dotenv(env_path)

# Base paths
PROJECT_ROOT = Path(__file__).parent
TASKS_DIR = PROJECT_ROOT / "tasks"
NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"
TEST_DATA_DIR = PROJECT_ROOT / "test_data"

# HuggingFace Configuration
HF_TOKEN = os.getenv("HF_TOKEN", os.getenv("HF_API_KEY", ""))
HF_API_KEY = HF_TOKEN

# OpenRouter Configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

# Default Model Settings
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "deepseek-ai/DeepSeek-V3.2")
DEFAULT_PROVIDER = os.getenv("DEFAULT_PROVIDER", "novita")
DEFAULT_AGENT_TYPE = os.getenv("DEFAULT_AGENT_TYPE", "ToolCallingAgent")

# Model provider mapping
MODEL_PROVIDERS = {
    "huggingface": {
        "base_url": "https://api-inference.huggingface.co",
        "api_key": HF_TOKEN,
    },
    "openrouter": {
        "base_url": OPENROUTER_BASE_URL,
        "api_key": OPENROUTER_API_KEY,
    },
}

# Task categories
TASK_CATEGORIES = {
    "web_research": {
        "name": "Web & Research",
        "tasks": [1, 2, 3, 4],
        "description": "Web scraping, research, and information gathering tasks"
    },
    "file_data": {
        "name": "File & Data Processing",
        "tasks": [5, 6, 7, 8],
        "description": "CSV, JSON, file processing and data transformation"
    },
    "code": {
        "name": "Code Tasks",
        "tasks": [9, 10, 11, 12],
        "description": "Code generation, documentation, and analysis"
    },
    "api_integration": {
        "name": "API & Integration",
        "tasks": [13, 14, 15, 16],
        "description": "API interactions and third-party integrations"
    },
    "productivity": {
        "name": "Productivity",
        "tasks": [17, 18, 19, 20],
        "description": "Meeting notes, scheduling, and productivity tools"
    }
}

# Task metadata
TASKS = {
    1: {"name": "Research Report Generator", "category": "web_research", "file": "01_research_report.py"},
    2: {"name": "News Summarizer", "category": "web_research", "file": "02_news_summarizer.py"},
    3: {"name": "Web Page Analyzer", "category": "web_research", "file": "03_web_analyzer.py"},
    4: {"name": "Trend Tracker", "category": "web_research", "file": "04_trend_tracker.py"},
    5: {"name": "CSV Summarizer", "category": "file_data", "file": "05_csv_summarizer.py"},
    6: {"name": "JSON Transformer", "category": "file_data", "file": "06_json_transformer.py"},
    7: {"name": "File Organizer", "category": "file_data", "file": "07_file_organizer.py"},
    8: {"name": "Data Validator", "category": "file_data", "file": "08_data_validator.py"},
    9: {"name": "Docstring Generator", "category": "code", "file": "09_docstring_generator.py"},
    10: {"name": "Code Refactorer", "category": "code", "file": "10_code_refactorer.py"},
    11: {"name": "Test Generator", "category": "code", "file": "11_test_generator.py"},
    12: {"name": "Code Explainer", "category": "code", "file": "12_code_explainer.py"},
    13: {"name": "HF Model Ranker", "category": "api_integration", "file": "13_hf_model_ranker.py"},
    14: {"name": "API Connector", "category": "api_integration", "file": "14_api_connector.py"},
    15: {"name": "Webhook Handler", "category": "api_integration", "file": "15_webhook_handler.py"},
    16: {"name": "Service Integrator", "category": "api_integration", "file": "16_service_integrator.py"},
    17: {"name": "Meeting Action Items", "category": "productivity", "file": "17_meeting_action_items.py"},
    18: {"name": "Email Draft Generator", "category": "productivity", "file": "18_email_draft_generator.py"},
    19: {"name": "Task Prioritizer", "category": "productivity", "file": "19_task_prioritizer.py"},
    20: {"name": "Document Formatter", "category": "productivity", "file": "20_document_formatter.py"},
}


def get_model():
    """Return the configured model instance."""
    from smolagents import InferenceClientModel
    return InferenceClientModel(
        model_id=DEFAULT_MODEL,
        token=HF_TOKEN or None,
        provider=DEFAULT_PROVIDER,
    )


def get_task_path(task_number: int) -> Path:
    """Get the file path for a specific task."""
    task_info = TASKS.get(task_number)
    if task_info:
        return TASKS_DIR / task_info["file"]
    return None


def get_notebook_path(task_number: int) -> Path:
    """Get the notebook path for a specific task."""
    task_info = TASKS.get(task_number)
    if task_info:
        notebook_name = task_info["file"].replace(".py", ".ipynb")
        return NOTEBOOKS_DIR / notebook_name
    return None


def check_api_keys() -> dict:
    """Check which API keys are configured."""
    return {
        "huggingface": bool(HF_TOKEN),
        "openrouter": bool(OPENROUTER_API_KEY),
    }


if __name__ == "__main__":
    # Test configuration loading
    print("Configuration loaded successfully!")
    print(f"Project root: {PROJECT_ROOT}")
    print(f"Tasks directory: {TASKS_DIR}")
    print(f"API keys configured: {check_api_keys()}")
    print(f"Default model: {DEFAULT_MODEL}")
