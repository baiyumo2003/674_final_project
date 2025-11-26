import os
import numpy as np
import pandas as pd
import igraph as ig

# ------------------------------------------------------
# Paths
# ------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

EMAIL_LIST_FILE = os.path.join(BASE_DIR, "data", "email_address", "enron_emails.txt")
NETWORK_MATRIX_FILE = os.path.join(BASE_DIR, "data","matrix", "network_email_communication.npy")

RESULT_DIR = os.path.join(BASE_DIR, "data", "LLM")
os.makedirs(RESULT_DIR, exist_ok=True)


# ------------------------------------------------------
# Load Data
# ------------------------------------------------------
def load_email_list(path):
    with open(path, "r") as f:
        return [line.strip().lower() for line in f.readlines()]


def load_network_matrix(path):
    return np.load(path)


# ------------------------------------------------------
# Build igraph from adjacency matrix
# ------------------------------------------------------
def build_graph(matrix, labels):
    g = ig.Graph.Weighted_Adjacency(
        matrix.tolist(),
        mode="undirected",
        loops=False
    )
    g.vs["name"] = labels
    return g


# ------------------------------------------------------
# Compute Node Metrics
# ------------------------------------------------------
def compute_metrics(g, users):
    print("Computing degree...")
    degree = g.degree()

    print("Computing betweenness...")
    betweenness = g.betweenness()

    print("Computing closeness...")
    closeness = g.closeness()

    print("Computing pagerank...")
    pagerank = g.pagerank()

    print("Computing community membership...")
    community = g.community_multilevel(weights=g.es["weight"]).membership

    df = pd.DataFrame({
        "email": users,
        "degree": degree,
        "betweenness": betweenness,
        "closeness": closeness,
        "pagerank": pagerank,
        "community": community
    })

    return df


# ------------------------------------------------------
# Save dataset
# ------------------------------------------------------
def save_dataset(df):
    outpath = os.path.join(RESULT_DIR, "node_metrics.csv")
    df.to_csv(outpath, index=False)
    print(f"\nSaved dataset to: {outpath}")


# ------------------------------------------------------
# Main
# ------------------------------------------------------
if __name__ == "__main__":
    print("Loading emails and matrix...")

    users = load_email_list(EMAIL_LIST_FILE)
    matrix = load_network_matrix(NETWORK_MATRIX_FILE)

    print("Building graph...")
    g = build_graph(matrix, users)

    print("Computing metrics...")
    df = compute_metrics(g, users)

    save_dataset(df)

    print("\nDataset build complete.")
