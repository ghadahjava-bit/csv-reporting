#!/usr/bin/env python3
"""
CSV Reporting Tool - Generate summary reports from CSV files.
"""

import argparse
import sys
from pathlib import Path
import pandas as pd
import numpy as np


def read_csv(file_path: str) -> pd.DataFrame:
    """Read a CSV file and return a DataFrame."""
    try:
        df = pd.read_csv(file_path)
        print(f"Successfully loaded: {file_path}")
        print(f"Rows: {len(df)}, Columns: {len(df.columns)}")
        return df
    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
        sys.exit(1)
    except pd.errors.EmptyDataError:
        print(f"Error: Empty CSV file - {file_path}")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading CSV: {e}")
        sys.exit(1)


def generate_summary(df: pd.DataFrame) -> dict:
    """Generate statistical summary for numeric columns."""
    summary = {
        'total_rows': len(df),
        'total_columns': len(df.columns),
        'columns': {}
    }
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    for col in numeric_cols:
        col_data = df[col].dropna()
        if len(col_data) > 0:
            summary['columns'][col] = {
                'count': len(col_data),
                'mean': round(col_data.mean(), 2),
                'median': round(col_data.median(), 2),
                'min': round(col_data.min(), 2),
                'max': round(col_data.max(), 2),
                'std': round(col_data.std(), 2)
            }
    
    return summary


def format_report_text(summary: dict) -> str:
    """Format summary as plain text."""
    lines = [
        "=" * 50,
        "CSV REPORT SUMMARY",
        "=" * 50,
        f"Total Rows: {summary['total_rows']}",
        f"Total Columns: {summary['total_columns']}",
        ""
    ]
    
    for col, stats in summary['columns'].items():
        lines.extend([
            f"\n--- {col} ---",
            f"  Count:  {stats['count']}",
            f"  Mean:   {stats['mean']}",
            f"  Median: {stats['median']}",
            f"  Min:    {stats['min']}",
            f"  Max:    {stats['max']}",
            f"  Std:    {stats['std']}"
        ])
    
    lines.append("\n" + "=" * 50)
    return "\n".join(lines)


def format_report_markdown(summary: dict) -> str:
    """Format summary as markdown."""
    lines = [
        "# CSV Report Summary",
        "",
        f"**Total Rows:** {summary['total_rows']}",
        f"**Total Columns:** {summary['total_columns']}",
        ""
    ]
    
    for col, stats in summary['columns'].items():
        lines.extend([
            f"## {col}",
            "",
            "| Statistic | Value |",
            "|-----------|-------|",
            f"| Count | {stats['count']} |",
            f"| Mean | {stats['mean']} |",
            f"| Median | {stats['median']} |",
            f"| Min | {stats['min']} |",
            f"| Max | {stats['max']} |",
            f"| Std Dev | {stats['std']} |",
            ""
        ])
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='Generate summary reports from CSV files'
    )
    parser.add_argument('input', help='Path to input CSV file')
    parser.add_argument('--output', '-o', help='Output file path (default: stdout)')
    parser.add_argument('--format', '-f', choices=['text', 'markdown'], 
                        default='text', help='Report format')
    
    args = parser.parse_args()
    
    # Read CSV
    df = read_csv(args.input)
    
    # Generate summary
    summary = generate_summary(df)
    
    # Format report
    if args.format == 'markdown':
        report = format_report_markdown(summary)
    else:
        report = format_report_text(summary)
    
    # Output
    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        with open(args.output, 'w') as f:
            f.write(report)
        print(f"Report saved to: {args.output}")
    else:
        print("\n" + report)


if __name__ == '__main__':
    main()