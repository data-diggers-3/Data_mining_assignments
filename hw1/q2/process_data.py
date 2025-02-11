import os
import sys
import matplotlib.pyplot as plt

def convert_fsg_format(input_file, output_file):
    """Convert dataset format for FSG."""
    freq = set()

    with open(input_file, 'r') as f:
        lines = f.read().strip().split('\n')

    output = []
    count_alph = 0

    for line in lines:
        line = line.strip()
        if not line:
            continue
        if not line[0].isdigit() and line[0] != '#':  # Node label
            freq.add(line[0])

    NODE_ORDER = sorted(freq)
    NODE_MAPPING = {label: index for index, label in enumerate(NODE_ORDER)}

    for line in lines:
        line = line.strip()
        if not line:
            continue
        elif line.startswith("#"):
            output.append(f"t # {line[1:]}")
            count_alph = 0
        elif not line[0].isdigit():  # Node label
            if line[0] in NODE_MAPPING:
                output.append(f"v {count_alph} {NODE_MAPPING[line[0]]}")
                count_alph += 1
        else:  # Edge
            parts = line.split()
            if len(parts) == 3:
                output.append(f"u {parts[0]} {parts[1]} {parts[2]}")

    with open(output_file, 'w') as f:
        f.write('\n'.join(output))

def convert_gspan_gaston_format(input_file, output_file):
    """Convert dataset format for GSpan and Gaston."""
    with open(input_file, 'r') as file:
        lines = file.read().strip().split('\n')

    output = []
    hash_count = 0

    for line in lines:
        line = line.split()
        if line[0] == "t":
            output.append(f"t # {line[2]}")
            hash_count += 1
        elif line[0] == "v":
            output.append(f"v {line[1]} {line[2]}")
        else:
            output.append(f"e {line[1]} {line[2]} {line[3]}")

    with open(output_file, 'w') as f:
        f.write('\n'.join(output))

    return hash_count

def plot_runtime(runtime_file, output_folder):
    """Plot runtime results from runtime.txt."""
    if not os.path.exists(runtime_file):
        print(f"Error: {runtime_file} not found!")
        return

    algorithms = {}

    with open(runtime_file, 'r') as file:
        lines = file.readlines()

    for line in lines:
        parts = line.strip().split(',')
        if len(parts) != 3:
            continue

        support, algo, time = parts
        support = int(support)
        time = float(time)

        if algo not in algorithms:
            algorithms[algo] = {'support': [], 'time': []}

        algorithms[algo]['support'].append(support)
        algorithms[algo]['time'].append(time)

    plt.figure(figsize=(10, 6))
    for algo, data in algorithms.items():
        plt.plot(data['support'], data['time'], label=algo, marker='o')

    plt.xlabel('Support Value')
    plt.ylabel('Time (seconds)')
    plt.title('Algorithm Runtime vs Support')
    plt.legend()
    plt.grid(True)

    plot_path = os.path.join(output_folder, "runtime_plot.png")
    plt.savefig(plot_path)
    print(f"✅ Plot saved at {plot_path}")

if __name__ == "__main__":
    if len(sys.argv) == 3:  # Conversion mode
        dataset_path = sys.argv[1]
        output_folder = sys.argv[2]

        fsg_dataset = os.path.join(output_folder, "fsg_dataset.txt")
        gspan_gaston_dataset = os.path.join(output_folder, "gspan_gaston_dataset.txt")

        print("Converting dataset for FSG...")
        convert_fsg_format(dataset_path, fsg_dataset)

        print("Converting dataset for GSpan/Gaston...")
        hash_count = convert_gspan_gaston_format(fsg_dataset, gspan_gaston_dataset)

        print(f"✅ Dataset conversion complete. {hash_count} graphs detected.")

    elif len(sys.argv) == 2:  # Plot mode
        runtime_file = sys.argv[1]
        output_folder = os.path.dirname(runtime_file)
        plot_runtime(runtime_file, output_folder)

    else:
        print("Usage:")
        print("  Convert dataset: python3 process_data.py <dataset_path> <output_folder>")
        print("  Generate plot: python3 process_data.py <runtime_file>")
        sys.exit(1)

