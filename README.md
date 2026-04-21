# CSV Reporting Tool

A Python tool for reading CSV files and generating summary reports.

## Features

- Read and parse CSV files
- Generate statistical summaries (mean, median, min, max)
- Export reports to text or markdown format
- Support for custom column analysis

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python csv_reporter.py input.csv --output report.txt
```

### Arguments

- `input.csv` - Path to the CSV file to analyze
- `--output` - Output file path for the report (optional, defaults to stdout)
- `--format` - Report format: `text` or `markdown` (default: `text`)

## Example

```bash
python csv_reporter.py data/sales.csv --output reports/sales_report.md --format markdown
```

## Project Structure

```
csv-reporting/
├── csv_reporter.py      # Main script
├── requirements.txt     # Python dependencies
├── README.md            # This file
└── data/                # Sample data directory (create as needed)
```

## License

MIT License