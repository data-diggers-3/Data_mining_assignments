#!/bin/bash

# Input parameters
GSPAN_PATH=$1
FSG_PATH=$2
GASTON_PATH=$3
DATASET_PATH=$4
OUTPUT_PATH=$5

# Define support values
SUPPORT_VALUES=(5 10 25 50 95)

# Ensure the output directory exists
mkdir -p "$OUTPUT_PATH"
RUNTIME_FILE="${OUTPUT_FOLDER}/runtime.txt"


echo "Converting dataset for FSG..."
python3 process_data.py "$DATASET_PATH" "$OUTPUT_PATH"

echo "Converting dataset for GSpan/Gaston..."
python3 process_data.py "$DATASET_PATH" "$OUTPUT_PATH"

# Count the number of graph transactions (lines with #) for Gaston
HASH_COUNT=$(grep -c '#' "$OUTPUT_PATH/gspan_gaston_dataset.txt")

# Loop through support values and run the algorithms
for support in "${SUPPORT_VALUES[@]}"; do
    echo "Running FSG with support=$support..."
    START_TIME=$(date +%s.%N)

    # Run FSG with a timeout of 1 second
    timeout 3600 "$FSG_PATH" -s "$support" "$OUTPUT_PATH/fsg_dataset.txt"
    EXIT_CODE=$?  # Store exit code immediately

    END_TIME=$(date +%s.%N)  # Capture end time

    # Compute precise elapsed time
    ELAPSED_TIME=$(awk "BEGIN {print $END_TIME - $START_TIME}")

    if [ $EXIT_CODE -eq 124 ]; then
        echo "FSG timeout at support=$support after ${ELAPSED_TIME} seconds, creating empty file."
        touch "$OUTPUT_PATH/fsg_${support}"
        echo "$support,FSG,$ELAPSED_TIME" >> "$OUTPUT_PATH/runtime.txt"
    elif [ -f "$OUTPUT_PATH/fsg_dataset.fp" ]; then
        mv "$OUTPUT_PATH/fsg_dataset.fp" "$OUTPUT_PATH/fsg_${support}"
        echo "$support,FSG,$ELAPSED_TIME" >> "$OUTPUT_PATH/runtime.txt"
    else
        echo "FSG failed at support=$support, no output file produced."
        touch "$OUTPUT_PATH/fsg_${support}"
        echo "$support,FSG,FAILED" >> "$OUTPUT_PATH/runtime.txt"
    fi

    echo "Running GSpan with support=$support..."
    START_TIME=$(date +%s.%N)

    # Run GSpan with timeout of 3600s
    timeout 3600 "$GSPAN_PATH" -f "$OUTPUT_PATH/gspan_gaston_dataset.txt" -s $(echo "$support * 0.01" | bc) -o
    EXIT_CODE=$?  # Store exit code immediately

    END_TIME=$(date +%s.%N)

    # Compute precise elapsed time
    ELAPSED_TIME=$(awk "BEGIN {print $END_TIME - $START_TIME}")

    if [ $EXIT_CODE -eq 124 ]; then
        echo "GSpan timeout at support=$support, creating empty file."
        touch "$OUTPUT_PATH/gspan_${support}"
        echo "$support,GSpan,$ELAPSED_TIME" >> "$OUTPUT_PATH/runtime.txt"
    elif [ -f "$OUTPUT_PATH/gspan_gaston_dataset.txt.fp" ]; then
        mv "$OUTPUT_PATH/gspan_gaston_dataset.txt.fp" "$OUTPUT_PATH/gspan_${support}"
        echo "$support,GSpan,$ELAPSED_TIME" >> "$OUTPUT_PATH/runtime.txt"
    else
        echo "GSpan failed at support=$support, no output file produced."
        touch "$OUTPUT_PATH/gspan_${support}"
        echo "$support,GSpan,FAILED" >> "$OUTPUT_PATH/runtime.txt"
    fi

    echo "Running Gaston with support=$support..."
    START_TIME=$(date +%s.%N)

    # Run Gaston with timeout of 3600s
    timeout 3600 "$GASTON_PATH" "$(echo "$support * 0.01 * $HASH_COUNT" | bc)" "$OUTPUT_PATH/gspan_gaston_dataset.txt" > "$OUTPUT_PATH/gaston_${support}"
    EXIT_CODE=$?  # Store exit code immediately

    END_TIME=$(date +%s.%N)

    # Compute precise elapsed time
    ELAPSED_TIME=$(awk "BEGIN {print $END_TIME - $START_TIME}")

    if [ $EXIT_CODE -eq 124 ]; then
        echo "Gaston timeout at support=$support, creating empty file."
        touch "$OUTPUT_PATH/gaston_${support}.txt"
        echo "$support,Gaston,3600" >> "$OUTPUT_PATH/runtime.txt"
    else
        echo "$support,Gaston,$ELAPSED_TIME" >> "$OUTPUT_PATH/runtime.txt"
    fi
done


echo "Generating runtime plot..."
python3 process_data.py "$OUTPUT_PATH/runtime.txt"

#python3 $(pwd)/process_data.py $(pwd)/out2/runtime.txt
#python3 process_data.py --plot "$RUNTIME_FILE" || { echo "Error: Plot generation failed"; exit 1; }

rm -f "$OUTPUT_PATH/fsg_dataset.txt"
rm -f "$OUTPUT_PATH/gspan_gaston_dataset.txt"
rm -f "$OUTPUT_PATH/runtime.txt"
echo "All processes completed!"

