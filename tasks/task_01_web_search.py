"""
Task 01: Web Search & Research
Performs web searches and compiles research reports using DuckDuckGo.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from smolagents import ToolCallingAgent, DuckDuckGoSearchTool
from config import get_model


def run(query: str = "latest AI developments 2024") -> str:
    """
    Perform web search and compile research findings.
    
    Args:
        query: Search query string
        
    Returns:
        Research report with search results
    """
    try:
        model = get_model()
        agent = ToolCallingAgent(
            tools=[DuckDuckGoSearchTool()],
            model=model,
            max_steps=5
        )
        
        prompt = f"""Search for information about: {query}

Compile a comprehensive research report including:
1. Key findings and facts
2. Recent developments
3. Sources and references
4. Summary of main points

Provide the report in markdown format."""
        
        result = agent.run(prompt)
        return result
    except Exception as e:
        return f"Error in web search task: {str(e)}"


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Web Search & Research")
    parser.add_argument("--query", default="latest AI developments 2024", help="Search query")
    args = parser.parse_args()
    print(run(args.query))
