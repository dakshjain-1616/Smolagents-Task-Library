"""
Task 14: Code Explainer
Explains code snippets in plain English using ToolCallingAgent.
"""
import os
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import get_model
from smolagents import ToolCallingAgent
from smolagents import Tool

class CodeExplainerTool(Tool):
    name = "code_explainer"
    description = "Explains code snippets in plain English"
    inputs = {
        "code": {"type": "string", "description": "The code snippet to explain"},
        "language": {"type": "string", "description": "Programming language of the code", "nullable": True}
    }
    output_type = "string"
    
    def forward(self, code: str, language: str = "python") -> str:
        return f"Explanation of {language} code"

def run(code: str = "print('Hello World')", language: str = "python"):
    """Run the code explainer task."""
    model = get_model()
    
    agent = ToolCallingAgent(
        tools=[CodeExplainerTool()],
        model=model
    )
    
    result = agent.run(
        f"Explain this {language} code in detail: ```{language}\n{code}\n```"
    )
    return result

if __name__ == "__main__":
    print(run())
