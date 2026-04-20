"""
Task 10: Math Problem Solver
Solves mathematical problems with step-by-step explanations.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from smolagents import CodeAgent
from config import get_model


def run(problem: str = "Calculate the area of a circle with radius 5") -> str:
    """
    Solve a mathematical problem with detailed steps.
    
    Args:
        problem: The math problem to solve
        
    Returns:
        Step-by-step solution
    """
    try:
        model = get_model()
        agent = CodeAgent(tools=[], model=model, max_steps=5)
        
        prompt = f"""Solve this mathematical problem step by step:

PROBLEM: {problem}

Requirements:
1. Identify the mathematical concepts involved
2. Write out the formula(s) needed
3. Substitute values and show calculations
4. Provide the final answer with units
5. Verify the answer is reasonable

Use Python code execution if needed for calculations."""
        
        result = agent.run(prompt)
        return result
    except Exception as e:
        return f"Error in math solver: {str(e)}"


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Math Problem Solver")
    parser.add_argument("--problem", default="Calculate the area of a circle with radius 5",
                       help="Math problem to solve")
    args = parser.parse_args()
    print(run(args.problem))
