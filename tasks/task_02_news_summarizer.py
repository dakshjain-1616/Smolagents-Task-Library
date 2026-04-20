"""
Task 02: News Summarizer
Fetches and summarizes news articles from the web.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from smolagents import ToolCallingAgent, DuckDuckGoSearchTool
from config import get_model


def run(topic: str = "technology", count: int = 5) -> str:
    """
    Fetch and summarize news articles on a given topic.
    
    Args:
        topic: News topic to search for
        count: Number of articles to summarize
        
    Returns:
        Summarized news report
    """
    try:
        model = get_model()
        agent = ToolCallingAgent(
            tools=[DuckDuckGoSearchTool()],
            model=model,
            max_steps=5
        )
        
        prompt = f"""Find and summarize the top {count} news articles about: {topic}

For each article, provide:
1. Headline
2. Key points (bullet points)
3. Brief summary (2-3 sentences)
4. Source if available

Format as a clean news digest in markdown."""
        
        result = agent.run(prompt)
        return result
    except Exception as e:
        return f"Error in news summarizer task: {str(e)}"


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="News Summarizer")
    parser.add_argument("--topic", default="technology", help="News topic")
    parser.add_argument("--count", type=int, default=5, help="Number of articles")
    args = parser.parse_args()
    print(run(args.topic, args.count))
