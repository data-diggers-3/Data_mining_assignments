import csv
import sys

def map_tid_to_txt_line(csv_file_path, txt_file_path, output_csv_path):
    # Read the text file and store its lines in a list
    with open(txt_file_path, 'r') as txt_file:
        txt_lines = txt_file.readlines()

    # Read the CSV file and add a new column with the mapped values
    with open(csv_file_path, 'r') as csv_file, open(output_csv_path, 'w', newline='') as output_csv:
        csv_reader = csv.DictReader(csv_file)
        fieldnames = csv_reader.fieldnames + ['Label']  # Add new column header
        csv_writer = csv.DictWriter(output_csv, fieldnames=fieldnames)
        
        csv_writer.writeheader()
        
        for row in csv_reader:
            # Extract the numerical part from the TID value
            tid_str = row['TID'].strip("'")  # Remove the single quote (if any)
            tid = int(tid_str)  # Convert to integer
            
            if 0 <= tid < len(txt_lines):  # Check if TID is within valid range
                mapped_value = txt_lines[tid].strip()  # Get the corresponding line from the text file
                row['Label'] = mapped_value  # Add the label only if TID is valid
            else:
                row['Label'] = ""  # Add an empty label if TID is out of range
            
            csv_writer.writerow(row)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python map_tid_to_labels.py <input_csv> <input_txt> <output_csv>")
        sys.exit(1)

    input_csv = sys.argv[1]  # First argument (mproc_tid.csv)
    input_txt = sys.argv[2]  # Second argument (labels.txt)
    output_csv = sys.argv[3]  # Third argument (labelled.csv)

    map_tid_to_txt_line(input_csv, input_txt, output_csv)
