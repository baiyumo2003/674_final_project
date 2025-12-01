import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ------------------------------------------------------
# Paths
# ------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ANALYSIS_DIR = os.path.join(BASE_DIR, "results", "matrix_analysis")
FIG_DIR = os.path.join(BASE_DIR, "results", "figures")

os.makedirs(FIG_DIR, exist_ok=True)

BASIC_STATS = os.path.join(ANALYSIS_DIR, "basic_stats.csv")
CENTRALITY  = os.path.join(ANALYSIS_DIR, "centrality.csv")
COMMUNITIES = os.path.join(ANALYSIS_DIR, "communities.csv")

# ------------------------------------------------------
# Load & merge datasets
# ------------------------------------------------------
def load_and_merge():
    df_basic = pd.read_csv(BASIC_STATS)
    df_cent  = pd.read_csv(CENTRALITY)
    df_comm  = pd.read_csv(COMMUNITIES)

    df = df_basic.merge(df_cent, on="email", how="left")
    df = df.merge(df_comm, on="email", how="left")

    return df

# ------------------------------------------------------
# Plot helper
# ------------------------------------------------------
def save_plot(name):
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, name), dpi=300)
    plt.close()


# ------------------------------------------------------
# Analysis functions
# ------------------------------------------------------
def plot_distribution(df, column, name):
    plt.figure(figsize=(6,4))
    sns.histplot(df[column], bins=50, kde=True)
    plt.title(f"Distribution of {column}")
    save_plot(name)


def top10_table(df, column):
    return df[['email', column]].sort_values(by=column, ascending=False).head(10)


def analyze(df):
    # --------------------------------------------------
    # 1. Basic Stats Plots
    # --------------------------------------------------
    plot_distribution(df, "sent", "sent_distribution.png")
    plot_distribution(df, "received", "received_distribution.png")
    plot_distribution(df, "balance", "balance_distribution.png")

    # --------------------------------------------------
    # 2. Centrality Distributions
    # --------------------------------------------------
    for metric in ["degree", "betweenness", "closeness", "pagerank", "eigenvector"]:
        plot_distribution(df, metric, f"{metric}_distribution.png")

    # --------------------------------------------------
    # 3. Community Size
    # --------------------------------------------------
    community_sizes = df["community"].value_counts()
    filtered_sizes = community_sizes[community_sizes > 1]

# Print summary
    print(community_sizes.head())
    print("Total communities:", len(community_sizes))

    # Histogram of community sizes
    plt.figure(figsize=(6,4))
    sns.histplot(filtered_sizes, bins=50, kde=False)
    plt.xlabel("Community Size")
    plt.ylabel("Count")
    plt.title("Distribution of Community Sizes(ignoring size 1 community)")
    save_plot("community_sizes.png")

    # --------------------------------------------------
    # 4. Pairwise Scatter Plots
    # --------------------------------------------------
    scatter_pairs = [
        ("degree", "pagerank"),
        ("betweenness", "closeness"),
        ("degree", "closeness"),
    ]

    for x, y in scatter_pairs:
        plt.figure(figsize=(6,4))
        sns.scatterplot(data=df, x=x, y=y, alpha=0.6)
        plt.title(f"{x} vs {y}")
        save_plot(f"{x}_vs_{y}.png")

    # --------------------------------------------------
    # 5. Output top-10 lists to console
    # --------------------------------------------------
    print("\n===== TOP 10 BY DEGREE =====")
    print(top10_table(df, "degree"))

    print("\n===== TOP 10 BY BETWEENNESS =====")
    print(top10_table(df, "betweenness"))

    print("\n===== TOP 10 BY PAGERANK =====")
    print(top10_table(df, "pagerank"))

    print("\n===== TOP 10 BY EIGENVECTOR =====")
    print(top10_table(df, "eigenvector"))

    print("\n===== COMMUNITY SIZE =====")
    print(df["community"].value_counts())


# ------------------------------------------------------
# Main
# ------------------------------------------------------
if __name__ == "__main__":
    print("Loading and merging datasets...")
    df = load_and_merge()
    print(f"Loaded {len(df)} nodes")

    print("Running analysis...")
    analyze(df)

    print(f"\nAll figures saved to: {FIG_DIR}")
    print("Done.")
