"""
Task 08: Code Reviewer
Analyzes code files for quality, bugs, and improvement suggestions.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from smolagents import CodeAgent
from config import get_model


def run(file_path: str = "script.py") -> str:
    """
    Review a code file and provide feedback.
    
    Args:
        file_path: Path to code file
        
    Returns:
        Code review report
    """
    try:
        # Read the code file
        with open(file_path, 'r', encoding='utf-8') as f:
            code_content = f.read()
        
        # Get file extension for language detection
        extension = Path(file_path).suffix.lower()
        language_map = {
            '.py': 'Python',
            '.js': 'JavaScript',
            '.ts': 'TypeScript',
            '.java': 'Java',
            '.cpp': 'C++',
            '.c': 'C',
            '.go': 'Go',
            '.rs': 'Rust',
            '.rb': 'Ruby',
            '.php': 'PHP'
        }
        language = language_map.get(extension, 'Unknown')
        
        # Use AI for code review
        model = get_model()
        agent = CodeAgent(tools=[], model=model, max_steps=3)
        
        prompt = f"""Review this {language} code file and provide comprehensive feedback:

```
{code_content[:3000]}
```

Provide:
1. Code quality assessment
2. Potential bugs or issues
3. Performance considerations
4. Security concerns
5. Style and best practice recommendations
6. Overall rating (1-10) with justification"""
        
        review = agent.run(prompt)
        
        return f"""# Code Review Report

## File Information
- **File:** {file_path}
- **Language:** {language}
- **Lines:** {len(code_content.splitlines())}

## Review
{review}
"""
    except Exception as e:
        return f"Error reviewing code: {str(e)}"


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Code Reviewer")
    parser.add_argument("--file", default="script.py", help="Path to code file")
    args = parser.parse_args()
    print(run(args.file))
