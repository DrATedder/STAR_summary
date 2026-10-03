#!/usr/bin/env python3

import argparse
import csv
from pathlib import Path


def parse_stats_file(filepath):
    """Extract SN (Summary Numbers) entries from a samtools stats file."""
    stats = {}

    with open(filepath, "r") as f:
        for line in f:
            if line.startswith("SN\t"):
                parts = line.rstrip("\n").split("\t", 2)

                if len(parts) == 3:
                    key = parts[1].rstrip(":")
                    value = parts[2]
                    stats[key] = value

    return stats


def main():
    parser = argparse.ArgumentParser(
        description="Combine samtools stats SN fields into a CSV table."
    )
    parser.add_argument(
        "input_dir",
        type=Path,
        help="Directory containing *.samtools.stats.txt files"
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default="samtools_stats_summary.csv",
        help="Output CSV file (default: samtools_stats_summary.csv)"
    )

    args = parser.parse_args()

    files = sorted(args.input_dir.glob("*.samtools.stats.txt"))

    if not files:
        raise SystemExit(
            f"No *.samtools.stats.txt files found in {args.input_dir}"
        )

    all_stats = []
    all_columns = set()

    for filepath in files:
        sample = filepath.name.removesuffix(".samtools.stats.txt")
        stats = parse_stats_file(filepath)

        stats["sample"] = sample

        all_stats.append(stats)
        all_columns.update(stats.keys())

    # Put sample first, followed by SN fields alphabetically
    columns = ["sample"] + sorted(all_columns - {"sample"})

    with open(args.output, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        writer.writerows(all_stats)

    print(f"Wrote {len(all_stats)} samples to {args.output}")


if __name__ == "__main__":
    main()
