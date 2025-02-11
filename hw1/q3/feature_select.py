import networkx as nx
import numpy as np
import sys
import os
from networkx.algorithms.isomorphism import GraphMatcher

def load_selected_subgraphs(subgraph_file):
    """Load subgraphs from the given file."""
    print(f"Loading subgraphs from {subgraph_file}...")
    subgraphs = []
    with open(subgraph_file, 'r') as f:
        lines = f.readlines()
        subgraph = None
        for line in lines:
            parts = line.strip().split()
            if not parts:
                continue
            if parts[0] == 't':
                if subgraph:
                    subgraphs.append(subgraph)
                subgraph = nx.Graph()
            elif parts[0] == 'v':
                subgraph.add_node(int(parts[1]), label=int(parts[2]))
            elif parts[0] == 'u':
                subgraph.add_edge(int(parts[1]), int(parts[2]), weight=int(parts[3]))
        if subgraph:
            subgraphs.append(subgraph)
    print(f"Loaded {len(subgraphs)} subgraphs.")
    return subgraphs

def load_graphs(graph_file):
    """Load graphs from a file."""
    print(f"Loading graphs from {graph_file}...")
    graphs = []
    with open(graph_file, 'r') as f:
        lines = f.readlines()
        graph = None
        for line in lines:
            parts = line.strip().split()
            if not parts:
                continue
            if parts[0] == 't':
                if graph:
                    graphs.append(graph)
                graph = nx.Graph()
            elif parts[0] == 'v':
                graph.add_node(int(parts[1]), label=int(parts[2]))
            elif parts[0] == 'u':
                graph.add_edge(int(parts[1]), int(parts[2]), weight=int(parts[3]))
        if graph:
            graphs.append(graph)
    print(f"Loaded {len(graphs)} graphs.")
    return graphs

def compute_feature_vector(graph, subgraphs):
    """Convert a graph into a feature vector based on subgraph isomorphism."""
    feature_vector = []
    for subgraph in subgraphs:
        matcher = GraphMatcher(graph, subgraph, node_match=lambda n1, n2: n1['label'] == n2['label'])
        feature_vector.append(int(matcher.subgraph_is_isomorphic()))
    return feature_vector

def generate_feature_matrix(graphs, subgraphs):
    """Generate a feature matrix for a set of graphs."""
    print("Generating feature matrix...")
    feature_matrix = np.array([compute_feature_vector(graph, subgraphs) for graph in graphs])
    return feature_matrix

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 convert_features.py <path_graphs> <path_discriminative_subgraphs> <path_features>")
        sys.exit(1)

    graph_file = sys.argv[1]   # Output of preprocess.py (e.g., pre_proc.txt)
    subgraph_file = sys.argv[2]
    feature_output = sys.argv[3]

    # Check if files exist
    if not os.path.exists(graph_file):
        print(f"Error: Graph file '{graph_file}' does not exist.")
        sys.exit(1)
    
    if not os.path.exists(subgraph_file):
        print(f"Error: Subgraph file '{subgraph_file}' does not exist.")
        sys.exit(1)

    # Load graphs and subgraphs
    subgraphs = load_selected_subgraphs(subgraph_file)
    graphs = load_graphs(graph_file)

    # Compute feature matrix
    feature_matrix = generate_feature_matrix(graphs, subgraphs)

    # Save as a NumPy binary file
    np.save(feature_output, feature_matrix)
    print(f"Feature extraction completed. Saved feature matrix as {feature_output}")
