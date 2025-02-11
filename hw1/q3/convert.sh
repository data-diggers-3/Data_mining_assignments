#!/bin/bash

# Exit immediately if a command fails
set -e

# Check if the correct number of arguments is provided
if [ "$#" -ne 3 ]; then
    echo "Usage: bash convert.sh <path_graphs> <path_discriminative_subgraphs> <path_features>"
    exit 1
fi

# Assign arguments to variables
INPUT_GRAPH=$1
SUBGRAPHS=$2
FEATURE_OUTPUT=$3

# Define intermediate output file
PROCESSED_GRAPH="pre_proc.txt"

# Run preprocess.py
echo "Running preprocessing on $INPUT_GRAPH..."
python3 preprocess1.py "$INPUT_GRAPH"

# Ensure preprocessing succeeded
if [ ! -f "$PROCESSED_GRAPH" ]; then
    echo "Error: Preprocessing failed. File $PROCESSED_GRAPH not generated."
    exit 1
fi

# Run feature_select.py
echo "Extracting features using $PROCESSED_GRAPH and $SUBGRAPHS..."
python3 feature_select.py "$PROCESSED_GRAPH" "$SUBGRAPHS" "$FEATURE_OUTPUT"

# Ensure feature extraction succeeded
if [ ! -f "$FEATURE_OUTPUT" ]; then
    echo "Error: Feature extraction failed. File $FEATURE_OUTPUT not generated."
    exit 1
fi

echo "Feature extraction completed. Output saved to $FEATURE_OUTPUT"

