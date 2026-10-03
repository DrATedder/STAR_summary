#!/usr/bin/env python3

import os
import re
import csv
import argparse


FIELDS = {
    "Number of input reads": "Number of input reads",
    "Uniquely mapped reads %": "Uniquely mapped reads %",
    "Uniquely mapped reads number": "Uniquely mapped reads number",
    "Number of reads mapped to multiple loci": "Number of reads mapped to multiple loci",
    "Number of reads unmapped: too many mismatches": "Number of reads unmapped: too many mismatches",
    "Number of reads unmapped: too short": "Number of reads unmapped: too short",
    "Number of splices: Total": "Number of splices: Total",
    "Number of splices: Annotated (sjdb)": "Number of splices: Annotated (sjdb)",
    "Number of splices: GT/AG": "Number of splices: GT/AG",
}


def parse_star_log(log_file):
    """Parse a STAR Log.final.out file."""

    stats = {}

    with open(log_file, "r") as f:
        for line in f:
            # STAR separates fields with | and uses whitespace around values
            if "|" not in line:
                continue

            key, value = line.split("|", 1)

            key = key.strip()
            value = value.strip()

            if key in FIELDS:
                stats[FIELDS[key]] = value

    return stats


def find_star_logs(input_dir):
    """Recursively find all Log.final.out files."""

    log_files = []

    for root, dirs, files in os.walk(input_dir):
        for filename in files:
            if filename == "Log.final.out":
                log_files.append(os.path.join(root, filename))

    return sorted(log_files)


def main():

    parser = argparse.ArgumentParser(
        description="Collect summary statistics from STAR Log.final.out files."
    )

    parser.add_argument(
        "input_dir",
        help="Directory containing STAR run directories"
    )

    parser.add_argument(
        "-o",
        "--output",
        default="STAR_summary.csv",
        help="Output CSV filename (default: STAR_summary.csv)"
    )

    args = parser.parse_args()

    log_files = find_star_logs(args.input_dir)

    if not log_files:
        print(f"No Log.final.out files found under: {args.input_dir}")
        return

    columns = [
        "Sample",
        "Number of input reads",
        "Uniquely mapped reads %",
        "Uniquely mapped reads number",
        "Number of reads mapped to multiple loci",
        "Number of reads unmapped: too many mismatches",
        "Number of reads unmapped: too short",
        "Number of splices: Total",
        "Number of splices: Annotated (sjdb)",
        "Number of splices: GT/AG",
    ]

    rows = []

    for log_file in log_files:

        stats = parse_star_log(log_file)

        # Use the directory containing Log.final.out as the sample name
        sample = os.path.basename(os.path.dirname(log_file))

        row = {"Sample": sample}

        for column in columns[1:]:
            row[column] = stats.get(column, "NA")

        rows.append(row)

    with open(args.output, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Found {len(log_files)} STAR log files.")
    print(f"Summary written to: {args.output}")


if __name__ == "__main__":
    main()
