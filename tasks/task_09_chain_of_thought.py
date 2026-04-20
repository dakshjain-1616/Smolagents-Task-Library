"""
Task 09: Chain of Thought Reasoning
Breaks down complex problems into step-by-step reasoning.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from smolagents import ToolCallingAgent
from config import get_model


def run(problem: str = "How many days are in 5 years including one leap year?") -> str:
    """
    Solve a problem using chain of thought reasoning.
    
    Args:
        problem: The problem to solve
        
    Returns:
        Step-by-step reasoning and solution
    """
    try:
        model = get_model()
        agent = ToolCallingAgent(tools=[], model=model, max_steps=5)
        
        prompt = f"""Solve this problem using detailed chain of thought reasoning:

PROBLEM: {problem}

Requirements:
1. Break down the problem into clear steps
2. Show your reasoning at each step
3. State any assumptions you make
4. Provide the final answer clearly
5. Verify your answer makes sense

Format as:
Step 1: [reasoning]
Step 2: [reasoning]
...
Final Answer: [answer]
Verification: [check your work]"""
        
        result = agent.run(prompt)
        return result
    except Exception as e:
        return f"Error in chain of thought reasoning: {str(e)}"


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Chain of Thought Reasoning")
    parser.add_argument("--problem", default="How many days are in 5 years including one leap year?",
                       help="Problem to solve")
    args = parser.parse_args()
    print(run(args.problem))
