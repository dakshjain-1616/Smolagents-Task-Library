"""
Task 18: Argument Analyzer
Analyzes arguments and identifies logical fallacies using ToolCallingAgent.
"""
import os
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import get_model
from smolagents import ToolCallingAgent
from smolagents import Tool

class ArgumentAnalyzerTool(Tool):
    name = "argument_analyzer"
    description = "Analyzes arguments for logical fallacies and strength"
    inputs = {
        "argument": {"type": "string", "description": "The argument to analyze"},
        "context": {"type": "string", "description": "Additional context about the argument", "nullable": True}
    }
    output_type = "string"
    
    def forward(self, argument: str, context: str = "") -> str:
        return f"Analysis of argument: {argument[:50]}..."

def run(argument: str = "All cats are mammals. Some mammals are pets. Therefore, all cats are pets.", context: str = ""):
    """Run the argument analyzer task."""
    model = get_model()
    
    agent = ToolCallingAgent(
        tools=[ArgumentAnalyzerTool()],
        model=model
    )
    
    prompt = f"Analyze this argument for logical fallacies, strengths, and weaknesses: {argument}"
    if context:
        prompt += f"\nContext: {context}"
    
    result = agent.run(prompt)
    return result

if __name__ == "__main__":
    print(run())
