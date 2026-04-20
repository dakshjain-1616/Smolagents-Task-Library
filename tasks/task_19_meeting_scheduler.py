"""
Task 19: Meeting Scheduler
Suggests optimal meeting times based on constraints using ToolCallingAgent.
"""
import os
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import get_model
from smolagents import ToolCallingAgent
from smolagents import Tool

class MeetingSchedulerTool(Tool):
    name = "meeting_scheduler"
    description = "Suggests optimal meeting times based on constraints"
    inputs = {
        "participants": {"type": "string", "description": "List of participants or number of people"},
        "duration": {"type": "string", "description": "Meeting duration", "nullable": True},
        "constraints": {"type": "string", "description": "Any scheduling constraints", "nullable": True}
    }
    output_type = "string"
    
    def forward(self, participants: str, duration: str = "1 hour", constraints: str = "") -> str:
        return f"Meeting scheduled for {participants}, duration: {duration}"

def run(participants: str = "team of 5", duration: str = "1 hour", constraints: str = "weekdays only"):
    """Run the meeting scheduler task."""
    model = get_model()
    
    agent = ToolCallingAgent(
        tools=[MeetingSchedulerTool()],
        model=model
    )
    
    prompt = f"Suggest optimal meeting times for {participants}, duration: {duration}"
    if constraints:
        prompt += f" with constraints: {constraints}"
    prompt += ". Consider time zones, typical work hours, and best practices."
    
    result = agent.run(prompt)
    return result

if __name__ == "__main__":
    print(run())
