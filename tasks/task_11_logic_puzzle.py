"""
Task 11: Logic Puzzle Solver
Solves logic puzzles and brain teasers with detailed reasoning.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from smolagents import ToolCallingAgent
from config import get_model


def run(puzzle: str = "Three houses are in a row. The red house is to the left of the blue house. The green house is in the middle. Which house is on the right?") -> str:
    """
    Solve a logic puzzle with detailed reasoning.
    
    Args:
        puzzle: The logic puzzle to solve
        
    Returns:
        Solution with reasoning
    """
    try:
        model = get_model()
        agent = ToolCallingAgent(tools=[], model=model, max_steps=5)
        
        prompt = f"""Solve this logic puzzle:

PUZZLE: {puzzle}

Requirements:
1. Identify the type of puzzle (deductive, lateral thinking, etc.)
2. List all given facts and constraints
3. Work through the logic step by step
4. Consider alternative interpretations
5. Provide the final answer with justification
6. Explain why other answers are incorrect

Format clearly with sections for: Given Facts, Reasoning Process, and Final Answer."""
        
        result = agent.run(prompt)
        return result
    except Exception as e:
        return f"Error in logic puzzle solver: {str(e)}"


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Logic Puzzle Solver")
    parser.add_argument("--puzzle", default="Three houses are in a row. The red house is to the left of the blue house. The green house is in the middle. Which house is on the right?",
                       help="Logic puzzle to solve")
    args = parser.parse_args()
    print(run(args.puzzle))
