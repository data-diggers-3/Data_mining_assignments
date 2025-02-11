#!/bin/bash
set -e  # Exit if any command fails

# Check arguments
if [ "$#" -ne 3 ]; then
    echo "Usage: bash identify.sh <train_graphs> <train_labels> <discriminative_subgraphs>"
    exit 1
fi

# Assign input arguments
TRAIN_GRAPHS=$1
TRAIN_LABELS=$2
DISCRIMINATIVE_SUBGRAPHS=$3

# Run preprocess script
python3 preprocess.py "$TRAIN_GRAPHS"

# Run FSG on preprocessed file
./fsg.sh -s25 -t pre_proc.txt

# Convert .tid to CSV
python3 convert_tid_to_csv.py pre_proc.tid mproc_tid.csv

# Map TID to labels
python3 map_tid_to_labels.py mproc_tid.csv "$TRAIN_LABELS" labelled.csv

# Run feature selection
python3 feature_pattern.py labelled.csv pre_proc.fp "$DISCRIMINATIVE_SUBGRAPHS"

echo "all done!"
   
