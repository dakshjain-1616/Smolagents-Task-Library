"""
Task 12: Decision Analyzer
Analyzes decisions using pros/cons, weighted factors, and recommendations.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from smolagents import ToolCallingAgent
from config import get_model


def run(decision: str = "Should I learn Python or JavaScript first?", 
        context: str = "I want to start a career in tech") -> str:
    """
    Analyze a decision with structured reasoning.
    
    Args:
        decision: The decision to analyze
        context: Additional context for the decision
        
    Returns:
        Decision analysis with recommendation
    """
    try:
        model = get_model()
        agent = ToolCallingAgent(tools=[], model=model, max_steps=5)
        
        prompt = f"""Analyze this decision comprehensively:

DECISION: {decision}
CONTEXT: {context}

Provide a structured analysis:

1. DECISION FRAMEWORK
   - What are the options?
   - What criteria matter most?

2. PROS AND CONS ANALYSIS
   - For each option, list pros and cons
   - Consider short-term and long-term impacts

3. FACTOR WEIGHTING
   - Assign importance weights to key factors
   - Score each option against factors

4. RISK ASSESSMENT
   - What could go wrong with each option?
   - How can risks be mitigated?

5. FINAL RECOMMENDATION
   - Clear recommendation with justification
   - Confidence level (High/Medium/Low)
   - Next steps to implement"""
        
        result = agent.run(prompt)
        return result
    except Exception as e:
        return f"Error in decision analyzer: {str(e)}"


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Decision Analyzer")
    parser.add_argument("--decision", default="Should I learn Python or JavaScript first?",
                       help="Decision to analyze")
    parser.add_argument("--context", default="I want to start a career in tech",
                       help="Additional context")
    args = parser.parse_args()
    print(run(args.decision, args.context))
