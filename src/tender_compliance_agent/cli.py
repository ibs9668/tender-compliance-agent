from __future__ import annotations

import argparse
from pathlib import Path

from tender_compliance_agent.extraction import extract_clauses
from tender_compliance_agent.parsers import load_text_chunks
from tender_compliance_agent.reports import write_reports


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate a tender compliance health check report.")
    parser.add_argument("--input", required=True, type=Path, help="Input file or directory.")
    parser.add_argument("--output", required=True, type=Path, help="Output report directory.")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    chunks = load_text_chunks(args.input)
    clauses = extract_clauses(chunks)
    write_reports(clauses, args.output)
    print(f"Generated {len(clauses)} clauses in {args.output}")


if __name__ == "__main__":
    main()
