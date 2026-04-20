"""
Task 13: Story Generator
Generates creative stories based on user prompts using ToolCallingAgent.
"""
import os
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import get_model
from smolagents import ToolCallingAgent
from smolagents import Tool

class StoryGeneratorTool(Tool):
    name = "story_generator"
    description = "Generates creative stories based on a theme, genre, and length"
    inputs = {
        "theme": {"type": "string", "description": "The main theme or topic of the story"},
        "genre": {"type": "string", "description": "Genre of the story (e.g., fantasy, sci-fi, mystery)"},
        "length": {"type": "string", "description": "Length of the story (short, medium, long)", "nullable": True}
    }
    output_type = "string"
    
    def forward(self, theme: str, genre: str, length: str = "short") -> str:
        return f"Story about {theme} in {genre} genre, {length} length"

def run(theme: str = "adventure", genre: str = "fantasy", length: str = "short"):
    """Run the story generator task."""
    model = get_model()
    
    agent = ToolCallingAgent(
        tools=[StoryGeneratorTool()],
        model=model
    )
    
    result = agent.run(
        f"Generate a {length} {genre} story about {theme}. Be creative and engaging."
    )
    return result

if __name__ == "__main__":
    print(run())
