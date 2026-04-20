"""
Task 03: Website Analyzer
Analyzes website content, structure, and extracts key information.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import requests
from bs4 import BeautifulSoup
from smolagents import ToolCallingAgent
from config import get_model


def fetch_website_content(url: str) -> str:
    """Fetch and extract text content from a website."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get text
        text = soup.get_text(separator='\n', strip=True)
        
        # Clean up text
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        return '\n'.join(lines[:100])  # Limit to first 100 lines
    except Exception as e:
        return f"Error fetching website: {str(e)}"


def run(url: str = "https://example.com") -> str:
    """
    Analyze a website and extract key information.
    
    Args:
        url: Website URL to analyze
        
    Returns:
        Website analysis report
    """
    try:
        content = fetch_website_content(url)
        
        if content.startswith("Error"):
            return content
        
        model = get_model()
        agent = ToolCallingAgent(tools=[], model=model, max_steps=3)
        
        prompt = f"""Analyze this website content from {url}:

{content[:3000]}

Provide:
1. Website purpose/main topic
2. Key sections or pages mentioned
3. Main content summary
4. Contact information if available
5. Overall assessment"""
        
        result = agent.run(prompt)
        return result
    except Exception as e:
        return f"Error in website analyzer task: {str(e)}"


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Website Analyzer")
    parser.add_argument("--url", default="https://example.com", help="Website URL")
    args = parser.parse_args()
    print(run(args.url))
