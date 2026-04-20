"""
Task 05: CSV Summarizer
Analyzes CSV files and generates statistical summaries and insights.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
from smolagents import ToolCallingAgent
from config import get_model


def run(file_path: str = "data.csv") -> str:
    """
    Analyze a CSV file and generate comprehensive summary.
    
    Args:
        file_path: Path to CSV file
        
    Returns:
        Statistical summary and insights
    """
    try:
        # Load and analyze CSV
        df = pd.read_csv(file_path)
        
        # Basic statistics
        summary = {
            "rows": len(df),
            "columns": len(df.columns),
            "column_names": list(df.columns),
            "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
            "missing_values": df.isnull().sum().to_dict(),
            "numeric_summary": df.describe().to_dict() if len(df.select_dtypes(include=['number']).columns) > 0 else {}
        }
        
        # Create summary text for AI
        summary_text = f"""CSV Analysis Summary:
- File: {file_path}
- Dimensions: {summary['rows']} rows × {summary['columns']} columns
- Columns: {', '.join(summary['column_names'])}
- Missing values: {sum(summary['missing_values'].values())} total

Sample data (first 5 rows):
{df.head().to_string()}

Data types:
{chr(10).join([f"  {col}: {dtype}" for col, dtype in summary['dtypes'].items()])}
"""
        
        # Use AI for insights
        model = get_model()
        agent = ToolCallingAgent(tools=[], model=model, max_steps=3)
        
        prompt = f"""Analyze this CSV data and provide insights:

{summary_text}

Provide:
1. Data quality assessment
2. Key patterns or trends
3. Recommendations for analysis
4. Potential issues to address"""
        
        insights = agent.run(prompt)
        
        return f"""# CSV Analysis Report

## Basic Statistics
- **Rows:** {summary['rows']:,}
- **Columns:** {summary['columns']}
- **Missing Values:** {sum(summary['missing_values'].values())}

## Column Information
{chr(10).join([f"- **{col}:** {dtype}" for col, dtype in summary['dtypes'].items()])}

## AI Insights
{insights}
"""
    except Exception as e:
        return f"Error analyzing CSV: {str(e)}"


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="CSV Summarizer")
    parser.add_argument("--file", default="data.csv", help="Path to CSV file")
    args = parser.parse_args()
    print(run(args.file))
