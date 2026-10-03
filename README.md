# STAR_summary
Simple python script to recursively search for [STAR](https://github.com/alexdobin/STAR) `log.final.out` files and pull summary stats for each sample into a csv file.

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
