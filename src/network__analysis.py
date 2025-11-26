import os
import numpy as np
import igraph as ig

# -------------------------------------------------------------------
# Paths
# -------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULT_DIR = os.path.join(BASE_DIR, "results", "figure")
EMAIL_LIST_FILE = os.path.join(BASE_DIR, "data", "email_address", "enron_emails.txt")
NETWORK_MATRIX_FILE = os.path.join(BASE_DIR, "data","matrix", "network_email_communication.npy")

os.makedirs(RESULT_DIR, exist_ok=True)

# -------------------------------------------------------------------
# Load Email List
# -------------------------------------------------------------------
def load_email_list(path):
    """Load the list of internal Enron email users."""
    with open(path, "r") as f:
        emails = [line.strip().lower() for line in f.readlines()]
    return emails


# -------------------------------------------------------------------
# Load Network Matrix
# -------------------------------------------------------------------
def load_network_matrix(path):
    """Load the symmetric communication matrix."""
    return np.load(path)


# -------------------------------------------------------------------
# Build Graph using python-igraph
# -------------------------------------------------------------------
def build_graph_from_matrix(matrix, labels):
    """
    Convert a symmetric matrix into an undirected igraph Graph.
    Weight(i,j) = total communication between users i and j.
    """
    g = ig.Graph.Weighted_Adjacency(
        matrix.tolist(),
        mode="undirected",
        loops=False
    )
    g.vs["label"] = labels
    g.vs["name"] = labels
    return g


# -------------------------------------------------------------------
# Visualization Functions
# -------------------------------------------------------------------



def plot_communities(g, communities, filename):
    """Plot detected communities."""
    largest_comm = max(communities, key=len)
    print(f"Largest cluster size: {len(largest_comm)} users")
    subgraph = g.subgraph(largest_comm)
    outpath = os.path.join(RESULT_DIR, filename)
    ig.plot(
    subgraph,
    target=outpath,
    layout=subgraph.layout("fr"),
    vertex_size=10,
    vertex_color="lightgreen",
    vertex_label=None,
    edge_width=[max(w, 1)/50 for w in subgraph.es["weight"]],
    bbox=(1000, 1000)
)
    print(f"Densest cluster plot saved to: {outpath}")



# -------------------------------------------------------------------
# Centrality Analysis
# -------------------------------------------------------------------
def compute_centrality(g, emails, top_k=10):
    """Compute various centrality metrics and print top-K results."""
    degree = g.degree()
    betweenness = g.betweenness()
    closeness = g.closeness()
    pagerank = g.pagerank()

    def top_indices(values):
        return sorted(range(len(values)), key=lambda i: values[i], reverse=True)[:top_k]

    print("\n=== TOP USERS BY DEGREE CENTRALITY ===")
    for i in top_indices(degree):
        print(f"{emails[i]:40s}  degree={degree[i]}")

    print("\n=== TOP USERS BY BETWEENNESS CENTRALITY ===")
    for i in top_indices(betweenness):
        print(f"{emails[i]:40s}  betweenness={betweenness[i]:.2f}")

    print("\n=== TOP USERS BY CLOSENESS CENTRALITY ===")
    for i in top_indices(closeness):
        print(f"{emails[i]:40s}  closeness={closeness[i]:.4f}")

    print("\n=== TOP USERS BY PAGE RANK ===")
    for i in top_indices(pagerank):
        print(f"{emails[i]:40s}  pagerank={pagerank[i]:.4f}")


# -------------------------------------------------------------------
# Community Detection
# -------------------------------------------------------------------
def detect_communities(g):
    """Use Louvain community detection."""
    communities = g.community_multilevel(weights=g.es["weight"])
    print(f"\nDetected {len(communities)} communities.")
    return communities


# -------------------------------------------------------------------
# MAIN SCRIPT
# -------------------------------------------------------------------
if __name__ == "__main__":
    print("\nLoading data...")

    # Load email list
    users = load_email_list(EMAIL_LIST_FILE)
    print(f"Loaded {len(users)} internal users.")

    # Load symmetric communication matrix
    matrix = load_network_matrix(NETWORK_MATRIX_FILE)
    print("Loaded symmetric network matrix.")

    # Build graph
    print("Building igraph network...")
    g = build_graph_from_matrix(matrix, users)


    # Community Detection
    communities = detect_communities(g)
    plot_communities(g, communities, "network_communities.png")

    # Centrality Analysis
    compute_centrality(g, users, top_k=10)

    print("\nNetwork analysis complete. Results saved in:", RESULT_DIR)
