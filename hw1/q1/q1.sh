#!/bin/bash

# Assign parameters to variables
apriori_path=$1
fpgrowth_path=$2
dataset_path=$3
output_folder=$4

# If output_folder is not provided, create a new folder
if [ -z "$output_folder" ]; then
    output_folder="out"  # Replace with your desired default folder name
    mkdir -p "$output_folder"
fi

# Define the dataset and support values
dataset=$(basename "$dataset_path")
supports=("5" "10" "25" "50" "90") # Added support value 90

# Initialize an empty array to hold runtime data
declare -a runtime_data

# Function to run an algorithm and measure time
run_algorithm() {
    local algo_path=$1
    local support=$2
    local output_file

    # Extract the algorithm name (e.g., "apriori" or "fpgrowth") from the path
    local algo=$(basename "$algo_path")

    # Set the output file name based on the algorithm
    if [ "$algo" == "apriori" ]; then
        output_file="$output_folder/ap${support}"
    elif [ "$algo" == "fpgrowth" ]; then
        output_file="$output_folder/fp${support}"
    else
        echo "Unknown algorithm: $algo"
        exit 1
    fi

    # Start the timer
    start_time=$(date +%s.%N)

    # Run the algorithm with a timeout of 1 hour (3600 seconds)
    timeout 3600 $algo_path -s$support $dataset_path $output_file

    # Check if the command timed out
    if [ $? -eq 124 ]; then
        
        time_taken="3600.0"
        # Ensure an empty output file is created if the algorithm times out
        touch $output_file
    else
        # Calculate the time taken as a float
        end_time=$(date +%s.%N)
        time_taken=$(echo "$end_time - $start_time" | bc)

        # Check if the output file is empty
        if [ ! -s "$output_file" ]; then
            # Create an empty file if no output was produced
            touch $output_file
        fi
    fi

    # Store the result in the array (algorithm, support, time)
    runtime_data+=("$algo,$support,$time_taken")
}

# Loop through each support value and run each algorithm once
for support in "${supports[@]}"; do
    run_algorithm "$apriori_path" $support
    run_algorithm "$fpgrowth_path" $support
done

# Call the Python script to generate the plot, passing the runtime data
python3 plotter.py "$output_folder" "${runtime_data[@]}"



