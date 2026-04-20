"""
Task 16: Data Formatter
Formats and structures unstructured data using ToolCallingAgent.
"""
import os
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import get_model
from smolagents import ToolCallingAgent
from smolagents import Tool

class DataFormatterTool(Tool):
    name = "data_formatter"
    description = "Formats unstructured data into structured formats"
    inputs = {
        "data": {"type": "string", "description": "The unstructured data to format"},
        "format": {"type": "string", "description": "Target format (JSON, CSV, table)", "nullable": True}
    }
    output_type = "string"
    
    def forward(self, data: str, format: str = "JSON") -> str:
        return f"Data formatted as {format}"

def run(data: str = "Name: John, Age: 30, City: NYC", format: str = "JSON"):
    """Run the data formatter task."""
    model = get_model()
    
    agent = ToolCallingAgent(
        tools=[DataFormatterTool()],
        model=model
    )
    
    result = agent.run(
        f"Convert this data to {format} format: {data}"
    )
    return result

if __name__ == "__main__":
    print(run())
