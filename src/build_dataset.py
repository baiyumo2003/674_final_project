import os
import pandas as pd

# ------------------------------------------------------
# Paths
# ------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ANALYSIS_DIR = os.path.join(BASE_DIR, "results", "matrix_analysis")
OUT_DIR      = os.path.join(BASE_DIR, "results", "final_dataset")
os.makedirs(OUT_DIR, exist_ok=True)

# Input files produced by analyze_matrix.py
BASIC_STATS  = os.path.join(ANALYSIS_DIR, "basic_stats.csv")
CENTRALITY   = os.path.join(ANALYSIS_DIR, "centrality.csv")
COMMUNITIES  = os.path.join(ANALYSIS_DIR, "communities.csv")

OUTPUT_FILE  = os.path.join(OUT_DIR, "enron_node_dataset.csv")


# ------------------------------------------------------
# Load helper
# ------------------------------------------------------
def safe_read(path, name):
    if os.path.exists(path):
        print(f"Loading {name}: {path}")
        return pd.read_csv(path)
    else:
        print(f"[Warning] Missing file: {path}")
        return None


# ------------------------------------------------------
# Main merge function
# ------------------------------------------------------
def build_final_dataset():
    df_basic = safe_read(BASIC_STATS, "basic_stats")
    df_cent  = safe_read(CENTRALITY, "centrality")
    df_comm  = safe_read(COMMUNITIES, "communities")

    print("\nMerging datasets...")
    df_final = df_basic.copy()

    if df_cent is not None:
        df_final = df_final.merge(df_cent, on="email", how="left")

    if df_comm is not None:
        df_final = df_final.merge(df_comm, on="email", how="left")

    df_final.to_csv(OUTPUT_FILE, index=False)
    print(f"\nFinal dataset saved to: {OUTPUT_FILE}")


# ------------------------------------------------------
# Entry point
# ------------------------------------------------------
if __name__ == "__main__":
    build_final_dataset()
    print("\nDataset build complete.")
