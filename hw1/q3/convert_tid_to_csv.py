import sys
import os
import csv
from collections import defaultdict

def process_file(input_filename, output_filename):
    if not os.path.exists(input_filename):
        print(f"Error: File '{input_filename}' not found.")
        sys.exit(1)

    # Initialize a defaultdict to map each number (TID) to a set of ranges
    result = defaultdict(lambda: defaultdict(int))  # Nested defaultdict to map each number to a range, and set presence to 0 or 1
    ranges_set = set()  # To store all unique ranges (range strings)

    # Read the .tid file line by line
    with open(input_filename, 'r') as infile:
        for line in infile:
            parts = line.strip().split()
            if not parts:
                continue
            
            range_str = parts[0]  # First element is the range identifier
            numbers = map(int, parts[1:])  # Remaining elements are TIDs
            
            ranges_set.add(range_str)  # Collect unique feature names
            
            for num in numbers:
                result[num][range_str] = 1  # Mark the presence of the range for this TID

    sorted_ranges = sorted(ranges_set)  # Sort for consistent column order

    # Write CSV output
    with open(output_filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, quotechar='"', quoting=csv.QUOTE_NONE)
        writer.writerow(['TID'] + sorted_ranges)  # Header row
        
        for num in sorted(result.keys()):
            row = [str(num)] + [result[num].get(range_str, 0) for range_str in sorted_ranges]
            writer.writerow(row)
    
    print(f"File processed and saved as {output_filename}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python convert_tid_to_csv.py <input_tid_file> <output_csv_file>")
        sys.exit(1)
    
    input_filename = sys.argv[1]
    output_filename = sys.argv[2]
    process_file(input_filename, output_filename)
