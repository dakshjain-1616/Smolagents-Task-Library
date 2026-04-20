"""
Task 07: Log Parser
Parses and prioritizes log files, extracting insights and error patterns.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import argparse
import re
from datetime import datetime
from collections import Counter, defaultdict
from typing import Dict, List, Any, Optional
from smolagents import ToolCallingAgent, InferenceClientModel


class LogEntry:
    """Represents a single log entry."""
    
    def __init__(self, raw_line: str, line_number: int):
        self.raw_line = raw_line
        self.line_number = line_number
        self.timestamp: Optional[datetime] = None
        self.level: str = "UNKNOWN"
        self.message: str = raw_line.strip()
        self.source: Optional[str] = None
        self.parsed = False
        
    def __repr__(self):
        return f"LogEntry(line={self.line_number}, level={self.level}, msg={self.message[:50]}...)"


def parse_log_line(line: str, line_number: int) -> LogEntry:
    """
    Parse a single log line into structured data.
    
    Args:
        line: Raw log line
        line_number: Line number in file
    
    Returns:
        LogEntry object
    """
    entry = LogEntry(line, line_number)
    
    # Common log patterns
    patterns = [
        # Standard: 2024-01-15 10:30:45 ERROR Something happened
        (r'(\d{4}-\d{2}-\d{2}[\sT]\d{2}:\d{2}:\d{2}(?:\.\d+)?)\s+(INFO|WARN(?:ING)?|ERROR|DEBUG|FATAL|CRITICAL)\s+(.*)', 
         ['timestamp', 'level', 'message']),
        
        # Apache: [Mon Jan 15 10:30:45 2024] [error] message
        (r'\[(\w{3}\s+\w{3}\s+\d+\s+\d{2}:\d{2}:\d{2}\s+\d{4})\]\s+\[(\w+)\]\s+(.*)',
         ['timestamp', 'level', 'message']),
        
        # Syslog: Jan 15 10:30:45 hostname process[level]: message
        (r'(\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})\s+(\S+)\s+(\S+)\[(\w+)\]:\s+(.*)',
         ['timestamp', 'host', 'source', 'level', 'message']),
        
        # Simple: [ERROR] message
        (r'\[(INFO|WARN(?:ING)?|ERROR|DEBUG|FATAL|CRITICAL)\]\s+(.*)',
         ['level', 'message']),
    ]
    
    for pattern, fields in patterns:
        match = re.match(pattern, line.strip())
        if match:
            groups = match.groups()
            entry.parsed = True
            
            # Map groups to fields
            if 'timestamp' in fields and len(groups) > fields.index('timestamp'):
                ts_str = groups[fields.index('timestamp')]
                try:
                    # Try common formats
                    for fmt in ['%Y-%m-%d %H:%M:%S', '%Y-%m-%dT%H:%M:%S', '%a %b %d %H:%M:%S %Y', '%b %d %H:%M:%S']:
                        try:
                            entry.timestamp = datetime.strptime(ts_str.split('.')[0], fmt)
                            break
                        except ValueError:
                            continue
                except:
                    pass
            
            if 'level' in fields and len(groups) > fields.index('level'):
                entry.level = groups[fields.index('level')].upper()
                if entry.level.startswith('WARN'):
                    entry.level = 'WARNING'
            
            if 'message' in fields and len(groups) > fields.index('message'):
                entry.message = groups[fields.index('message')]
            
            if 'source' in fields and len(groups) > fields.index('source'):
                entry.source = groups[fields.index('source')]
            
            break
    
    return entry


def parse_log_file(file_path: str) -> List[LogEntry]:
    """
    Parse entire log file.
    
    Args:
        file_path: Path to log file
    
    Returns:
        List of LogEntry objects
    """
    entries = []
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line_number, line in enumerate(f, 1):
            if line.strip():
                entry = parse_log_line(line, line_number)
                entries.append(entry)
    return entries


def analyze_logs(entries: List[LogEntry]) -> Dict[str, Any]:
    """
    Analyze parsed log entries.
    
    Args:
        entries: List of LogEntry objects
    
    Returns:
        Analysis results
    """
    # Count by level
    level_counts = Counter(e.level for e in entries)
    
    # Find error patterns
    error_messages = [e.message for e in entries if e.level in ['ERROR', 'FATAL', 'CRITICAL']]
    error_patterns = Counter()
    for msg in error_messages:
        # Extract key phrases (simplified)
        words = re.findall(r'\b\w{4,}\b', msg.lower())
        error_patterns.update(words)
    
    # Time distribution (if timestamps available)
    timestamps = [e.timestamp for e in entries if e.timestamp]
    time_range = None
    if timestamps:
        time_range = {
            "start": min(timestamps).isoformat(),
            "end": max(timestamps).isoformat()
        }
    
    # Sources
    sources = Counter(e.source for e in entries if e.source)
    
    return {
        "total_entries": len(entries),
        "parsed_entries": sum(1 for e in entries if e.parsed),
        "level_distribution": dict(level_counts),
        "error_count": len(error_messages),
        "warning_count": level_counts.get('WARNING', 0),
        "top_error_patterns": dict(error_patterns.most_common(10)),
        "time_range": time_range,
        "sources": dict(sources.most_common(10)) if sources else {}
    }


def prioritize_issues(entries: List[LogEntry], analysis: Dict[str, Any]) -> str:
    """
    Use AI to prioritize issues found in logs.
    
    Args:
        entries: Log entries
        analysis: Analysis results
    
    Returns:
        Prioritized report
    """
    # Get recent errors
    errors = [e for e in entries if e.level in ['ERROR', 'FATAL', 'CRITICAL']][:20]
    warnings = [e for e in entries if e.level == 'WARNING'][:10]
    
    error_samples = "\n".join([f"Line {e.line_number}: {e.message[:100]}" for e in errors])
    warning_samples = "\n".join([f"Line {e.line_number}: {e.message[:100]}" for e in warnings])
    
    model = get_model()
    agent = ToolCallingAgent(tools=[], model=model, max_steps=3)
    
    prompt = f"""Analyze these log entries and prioritize issues:

**Log Statistics:**
- Total entries: {analysis['total_entries']}
- Errors: {analysis['error_count']}
- Warnings: {analysis['warning_count']}
- Top error keywords: {', '.join(list(analysis['top_error_patterns'].keys())[:5])}

**Recent Errors:**
{error_samples[:800]}

**Recent Warnings:**
{warning_samples[:400]}

Provide:
1. Critical issues (P1) - immediate action required
2. High priority (P2) - should be addressed soon  
3. Medium priority (P3) - monitor and address when possible
4. Recommended actions for each priority level"""
    
    try:
        result = agent.run(prompt)
        return result
    except Exception as e:
        return f"AI prioritization unavailable: {e}"


def parse_and_prioritize_logs(file_path: str, output_format: str = "text") -> str:
    """
    Parse log file and generate prioritized report.
    
    Args:
        file_path: Path to log file
        output_format: Output format (text or json)
    
    Returns:
        Formatted report
    """
    try:
        # Parse logs
        entries = parse_log_file(file_path)
        
        # Analyze
        analysis = analyze_logs(entries)
        
        # Prioritize
        prioritization = prioritize_issues(entries, analysis)
        
        if output_format == "json":
            import json
            return json.dumps({
                "analysis": analysis,
                "prioritization": prioritization
            }, indent=2)
        
        # Text format
        report = f"""# Log Analysis Report

**File:** {file_path}
**Total Entries:** {analysis['total_entries']:,}
**Successfully Parsed:** {analysis['parsed_entries']:,}

## Level Distribution
"""
        for level, count in sorted(analysis['level_distribution'].items(), 
                                   key=lambda x: x[1], reverse=True):
            report += f"- {level}: {count:,}\n"
        
        if analysis['time_range']:
            report += f"\n## Time Range\n"
            report += f"- Start: {analysis['time_range']['start']}\n"
            report += f"- End: {analysis['time_range']['end']}\n"
        
        report += f"\n## AI Prioritization\n{prioritization}"
        
        return report
        
    except Exception as e:
        return f"Error parsing logs: {str(e)}"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse and prioritize log files")
    parser.add_argument("file", help="Path to log file")
    parser.add_argument("--format", choices=["text", "json"], default="text",
                       help="Output format")
    args = parser.parse_args()
    
    report = parse_and_prioritize_logs(args.file, args.format)
    print(report)
