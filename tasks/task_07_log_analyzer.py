"""
Task 07: Log Analyzer
Parses and analyzes log files to extract insights and error patterns.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import re
from collections import Counter
from smolagents import ToolCallingAgent
from config import get_model


class LogEntry:
    def __init__(self, raw_line: str, line_number: int):
        self.raw_line = raw_line
        self.line_number = line_number
        self.timestamp = None
        self.level = "UNKNOWN"
        self.message = raw_line.strip()
        self.parsed = False


def parse_log_line(line: str, line_number: int) -> LogEntry:
    """Parse a single log line into structured data."""
    entry = LogEntry(line, line_number)
    
    patterns = [
        (r'(\d{4}-\d{2}-\d{2}[\sT]\d{2}:\d{2}:\d{2})\s+(INFO|WARN|ERROR|DEBUG|FATAL)\s+(.*)', 
         ['timestamp', 'level', 'message']),
        (r'\[(\w{3}\s+\w{3}\s+\d+\s+\d{2}:\d{2}:\d{2}\s+\d{4})\]\s+\[(\w+)\]\s+(.*)',
         ['timestamp', 'level', 'message']),
        (r'\[(INFO|WARN|ERROR|DEBUG|FATAL)\]\s+(.*)',
         ['level', 'message']),
    ]
    
    for pattern, fields in patterns:
        match = re.match(pattern, line.strip())
        if match:
            groups = match.groups()
            entry.parsed = True
            if 'level' in fields:
                entry.level = groups[fields.index('level')].upper()
            if 'message' in fields:
                entry.message = groups[fields.index('message')]
            break
    
    return entry


def run(file_path: str = "app.log") -> str:
    """
    Parse and analyze a log file.
    
    Args:
        file_path: Path to log file
        
    Returns:
        Log analysis report
    """
    try:
        # Parse log file
        entries = []
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line_number, line in enumerate(f, 1):
                if line.strip():
                    entries.append(parse_log_line(line, line_number))
        
        # Analyze entries
        level_counts = Counter(e.level for e in entries)
        error_messages = [e.message for e in entries if e.level in ['ERROR', 'FATAL']][:10]
        
        analysis = {
            "total_entries": len(entries),
            "level_distribution": dict(level_counts),
            "error_count": len([e for e in entries if e.level in ['ERROR', 'FATAL']]),
            "warning_count": level_counts.get('WARN', 0) + level_counts.get('WARNING', 0)
        }
        
        # Use AI for prioritization
        error_samples = "\n".join([f"Line {e.line_number}: {e.message[:80]}" for e in entries if e.level in ['ERROR', 'FATAL']][:15])
        
        model = get_model()
        agent = ToolCallingAgent(tools=[], model=model, max_steps=3)
        
        prompt = f"""Analyze these log errors and provide prioritization:

Stats: {analysis['error_count']} errors, {analysis['warning_count']} warnings

Error samples:
{error_samples[:600]}

Provide P1 (critical), P2 (high), P3 (medium) priorities with recommended actions."""
        
        prioritization = agent.run(prompt)
        
        return f"""# Log Analysis Report

## Summary Statistics
- **Total Entries:** {analysis['total_entries']:,}
- **Errors:** {analysis['error_count']}
- **Warnings:** {analysis['warning_count']}

## Level Distribution
{chr(10).join([f"- **{level}:** {count:,}" for level, count in sorted(analysis['level_distribution'].items(), key=lambda x: x[1], reverse=True)])}

## AI Prioritization
{prioritization}
"""
    except Exception as e:
        return f"Error analyzing logs: {str(e)}"


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Log Analyzer")
    parser.add_argument("--file", default="app.log", help="Path to log file")
    args = parser.parse_args()
    print(run(args.file))
