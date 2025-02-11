import matplotlib.pyplot as plt
import sys
import os

def main(output_folder, runtime_data):
    # Dictionary to store runtime data
    algo_data = {}

    for entry in runtime_data:
        algo, support, time = entry.split(",")
        support = int(support)
        time = float(time)

        if algo not in algo_data:
            algo_data[algo] = {"support": [], "time": []}

        algo_data[algo]["support"].append(support)
        algo_data[algo]["time"].append(time)

    # Sort support values for correct plotting
    for algo in algo_data:
        sorted_pairs = sorted(zip(algo_data[algo]["support"], algo_data[algo]["time"]))
        algo_data[algo]["support"], algo_data[algo]["time"] = zip(*sorted_pairs)

    # Create plot
    plt.figure(figsize=(10, 6))
    for algo, data in algo_data.items():
        plt.plot(data["support"], data["time"], marker='o', label=algo)

    plt.xlabel('Support')
    plt.ylabel('Time (seconds)')
    plt.title('Algorithm Runtime vs Support')
    plt.legend()
    plt.grid(True)

    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Save the plot
    plot_path = os.path.join(output_folder, "runtime_plot_final.png")
    plt.savefig(plot_path)
    print(f"Plot saved to {plot_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 plotly.py <output_folder> <runtime_data>")
        sys.exit(1)

    output_folder = sys.argv[1]
    runtime_data = sys.argv[2:]  # Remaining arguments are runtime data

    if not runtime_data:
        print("Error: No runtime data provided.")
        sys.exit(1)

    main(output_folder, runtime_data)

