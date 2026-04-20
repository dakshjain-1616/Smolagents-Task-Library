"""
Task 04: Trend Tracker
Tracks and analyzes trends across various domains.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from smolagents import ToolCallingAgent, DuckDuckGoSearchTool
from config import get_model


def run(domain: str = "technology", timeframe: str = "past month") -> str:
    """
    Track and analyze trends in a specific domain.
    
    Args:
        domain: Domain to track trends (e.g., technology, finance, health)
        timeframe: Time period to analyze
        
    Returns:
        Trend analysis report
    """
    try:
        model = get_model()
        agent = ToolCallingAgent(
            tools=[DuckDuckGoSearchTool()],
            model=model,
            max_steps=5
        )
        
        prompt = f"""Analyze trends in {domain} over the {timeframe}.

Provide:
1. Top 5 emerging trends
2. Key statistics or metrics
3. Notable companies/people involved
4. Future predictions
5. Impact assessment

Format as a professional trend report."""
        
        result = agent.run(prompt)
        return result
    except Exception as e:
        return f"Error in trend tracker task: {str(e)}"


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Trend Tracker")
    parser.add_argument("--domain", default="technology", help="Domain to analyze")
    parser.add_argument("--timeframe", default="past month", help="Time period")
    args = parser.parse_args()
    print(run(args.domain, args.timeframe))
