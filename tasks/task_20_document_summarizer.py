"""
Task 20: Document Summarizer
Summarizes long documents into concise summaries using ToolCallingAgent.
"""
import os
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import get_model
from smolagents import ToolCallingAgent
from smolagents import Tool

class DocumentSummarizerTool(Tool):
    name = "document_summarizer"
    description = "Summarizes long documents into concise summaries"
    inputs = {
        "document": {"type": "string", "description": "The document text to summarize"},
        "style": {"type": "string", "description": "Summary style (brief, detailed, bullet points)"},
        "max_length": {"type": "integer", "description": "Maximum length of summary in sentences"}
    }
    output_type = "string"
    
    def forward(self, document: str, style: str = "brief", max_length: int = 3) -> str:
        return f"{style.capitalize()} summary of document ({max_length} sentences max)"

def run(document: str = "This is a sample document that needs to be summarized.", style: str = "brief", max_length: int = 3):
    """Run the document summarizer task."""
    model = get_model()
    
    agent = ToolCallingAgent(
        tools=[DocumentSummarizerTool()],
        model=model
    )
    
    result = agent.run(
        f"Summarize the following document in {style} style with maximum {max_length} sentences:\n\n{document}"
    )
    return result

if __name__ == "__main__":
    print(run())
