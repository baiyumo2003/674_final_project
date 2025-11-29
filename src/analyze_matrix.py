import os
import numpy as np
import pandas as pd
import networkx as nx

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
USER_LIST = os.path.join(BASE_DIR, "data", "email_address", "enron_emails.txt")
MATRIX_FILE = os.path.join(BASE_DIR, "data", "matrix", "email_matrix.npy")
NETWORK_FILE = os.path.join(BASE_DIR, "data", "matrix", "network_email_communication.npy")
OUT_DIR = os.path.join(BASE_DIR, "results", "matrix_analysis")

os.makedirs(OUT_DIR, exist_ok=True)

def load_users(path):
    with open(path, "r") as f:
        return [line.strip().lower() for line in f]


def analyze_matrices():
    users = load_users(USER_LIST)
    N = len(users)

    M = np.load(MATRIX_FILE)
    W = np.load(NETWORK_FILE)

    # -----------------------------------
    # 1. Basic stats: sent/received
    # -----------------------------------
    sent = M.sum(axis=1)
    received = M.sum(axis=0)
    balance = (sent - received) / (sent + received + 1e-9)

    df_basic = pd.DataFrame({
        "email": users,
        "sent": sent,
        "received": received,
        "balance": balance
    })
    df_basic.to_csv(os.path.join(OUT_DIR, "basic_stats.csv"), index=False)

    # -----------------------------------
    # 2. Build graph
    # -----------------------------------
    G = nx.from_numpy_array(W)
    G.remove_edges_from([(u, v) for u, v, w in G.edges(data="weight") if w < 3])
    print(123)

    # -----------------------------------
    # 3. Compute centralities
    # -----------------------------------
    degree = dict(G.degree(weight="weight"))

    # --- FAST betweenness (approximate) ---
    betweenness = nx.betweenness_centrality(
        G,
        k=min(50, len(G)),  # sample up to 50 nodes
        weight="weight",
        normalized=True,
        seed=123
    )
    closeness = nx.closeness_centrality(G)
    pagerank = nx.pagerank(G, weight="weight", max_iter=200)
    eigen = nx.eigenvector_centrality(
        G,
        max_iter=300,
        tol=1e-05,
        weight="weight"
    )


    df_centrality = pd.DataFrame({
        "email": users,
        "degree": [degree[i] for i in range(N)],
        "betweenness": [betweenness[i] for i in range(N)],
        "closeness": [closeness[i] for i in range(N)],
        "pagerank": [pagerank[i] for i in range(N)],
        "eigenvector": [eigen[i] for i in range(N)]
    })
    df_centrality.to_csv(os.path.join(OUT_DIR, "centrality.csv"), index=False)

    # -----------------------------------
    # 4. Community detection (Louvain)
    # -----------------------------------
    try:
        import community
        partition = community.best_partition(G, weight="weight")
        df_comm = pd.DataFrame({
            "email": users,
            "community": [partition[i] for i in range(N)]
        })
        df_comm.to_csv(os.path.join(OUT_DIR, "communities.csv"), index=False)
    except:
        print("python-louvain not installed; skipping community detection.")

    print("Analysis complete. Results stored in:", OUT_DIR)


if __name__ == "__main__":
    analyze_matrices()
