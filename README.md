# STAR_summary
Simple python scripts to summarize and handle `STAR` summary statistics into dataset tables in `csv` format.

# STAR_summary.py

A simple script to recursively search for [STAR](https://github.com/alexdobin/STAR) `log.final.out` files and pull summary stats for each sample into a csv file.

## Expected Directory structure
```bash
STAR_runs/
├── sample1/
│   └── Log.final.out
├── sample2/
│   └── Log.final.out
├── sample3/
│   └── Log.final.out
└── sample4/
    └── Log.final.out
```

## Basic usage
```bash
python3 STAR_summary.py STAR_runs/
```

## Output data fields
```bash
Sample
Number of input reads
Uniquely mapped reads %
Uniquely mapped reads number
Number of reads mapped to multiple loci
Number of reads unmapped: too many mismatches
Number of reads unmapped: too short
Number of splices: Total
Number of splices: Annotated (sjdb)
Number of splices: GT/AG
```

# samtools_stats_to_csv.py

Amalgamates the `samtools.stats.txt` alignment stats files created after running the `samtools stats` command. Pulls files from a single directory, creates a summary table (`csv`) for the entire dataset, with samples as rows.

## Basic usage
```bash
python3 samtools_stats_to_csv.py /path/to/stats/ \
    -o samtools_summary.csv
```

