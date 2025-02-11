import sys
import os

def process_file(input_file, temp_file):
    try:
        with open(input_file, 'r') as infile:
            lines = infile.readlines()

        counter = 0
        modified_lines = []

        for line in lines:
            # Replace 'e' with 'u'
            line = line.replace('e', 'u')

            # Add 't ' before every '#'
            if '#' in line:
                line = line.replace('#', f't # Graph {counter}', 1)
                counter += 1

            modified_lines.append(line)

        with open(temp_file, 'w') as outfile:
            outfile.writelines(modified_lines)

        print(f"Intermediate file saved as {temp_file}")

    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def clean_graph(temp_file, output_file):
    edges = set()
    try:
        with open(temp_file, "r") as infile, open(output_file, "w") as outfile:
            for line in infile:
                if line.startswith("u"):
                    parts = line.strip().split()
                    u, v, w = int(parts[1]), int(parts[2]), int(parts[3])
                    if (v, u, w) not in edges:  # Prevent duplicates
                        edges.add((u, v, w))
                        outfile.write(line + "\n")
                else:
                    outfile.write(line)

        print(f"Final cleaned graph saved as {output_file}")
        
        

    except FileNotFoundError:
        print(f"Error: The file '{temp_file}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
        
def remove_empty_lines(input_file, output_file):
    with open(input_file, "r") as f:
        lines = f.readlines()
    
    with open(output_file, "w") as f:
        for line in lines:
            if line.strip():  # Only write non-empty lines
                f.write(line)

# Usage example



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python preprocess.py <arg1>")
        sys.exit(1)

    input_filename = sys.argv[1]
    
    if not os.path.exists(input_filename):
        print(f"Error: File '{input_filename}' does not exist.")
        sys.exit(1)

    temp_filename = "pre_test.txt"
    output1_filename = "mid_proc.txt"
    output_filename = "pre_proc.txt"

    process_file(input_filename, temp_filename)
    clean_graph(temp_filename, output1_filename)
    remove_empty_lines(output1_filename,output_filename)
