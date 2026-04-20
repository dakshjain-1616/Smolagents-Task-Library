"""
Task 15: Email Drafter
Drafts professional emails based on context and tone using ToolCallingAgent.
"""
import os
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import get_model
from smolagents import ToolCallingAgent
from smolagents import Tool

class EmailDrafterTool(Tool):
    name = "email_drafter"
    description = "Drafts professional emails based on context and tone"
    inputs = {
        "purpose": {"type": "string", "description": "Purpose of the email"},
        "recipient": {"type": "string", "description": "Who the email is for"},
        "tone": {"type": "string", "description": "Tone of the email (formal, casual, friendly)", "nullable": True}
    }
    output_type = "string"
    
    def forward(self, purpose: str, recipient: str, tone: str = "professional") -> str:
        return f"Email to {recipient} about {purpose} in {tone} tone"

def run(purpose: str = "meeting request", recipient: str = "team", tone: str = "professional"):
    """Run the email drafter task."""
    model = get_model()
    
    agent = ToolCallingAgent(
        tools=[EmailDrafterTool()],
        model=model
    )
    
    result = agent.run(
        f"Draft a {tone} email to {recipient} regarding: {purpose}. "
        "Include appropriate subject line and signature."
    )
    return result

if __name__ == "__main__":
    print(run())
