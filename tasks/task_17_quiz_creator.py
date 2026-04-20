"""
Task 17: Quiz Creator
Creates quizzes on specified topics using ToolCallingAgent.
"""
import os
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import get_model
from smolagents import ToolCallingAgent
from smolagents import Tool

class QuizCreatorTool(Tool):
    name = "quiz_creator"
    description = "Creates quizzes with questions and answers on specified topics"
    inputs = {
        "topic": {"type": "string", "description": "The topic for the quiz"},
        "num_questions": {"type": "integer", "description": "Number of questions to generate", "nullable": True},
        "difficulty": {"type": "string", "description": "Difficulty level (easy, medium, hard)", "nullable": True}
    }
    output_type = "string"
    
    def forward(self, topic: str, num_questions: int = 5, difficulty: str = "medium") -> str:
        return f"Quiz on {topic} with {num_questions} {difficulty} questions"

def run(topic: str = "general knowledge", num_questions: int = 5, difficulty: str = "medium"):
    """Run the quiz creator task."""
    model = get_model()
    
    agent = ToolCallingAgent(
        tools=[QuizCreatorTool()],
        model=model
    )
    
    result = agent.run(
        f"Create a {difficulty} level quiz on '{topic}' with {num_questions} multiple choice questions. "
        "Include the correct answers at the end."
    )
    return result

if __name__ == "__main__":
    print(run())
