import os
import re
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ------------------------------------------------------
# Paths
# ------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QWEN_FILE = os.path.join(BASE_DIR, "results", "LLM", "enron_roles_qwen.csv")
FIG_DIR = os.path.join(BASE_DIR, "results", "figures")

os.makedirs(FIG_DIR, exist_ok=True)

# ------------------------------------------------------
# Extract role from Qwen output
# ------------------------------------------------------
def extract_role(text):
    """
    Extracts the role before the colon.
    Example:
      'Executive/Leader: This person...' -> 'Executive/Leader'
    """
    if not isinstance(text, str):
        return "Unknown"
    match = re.match(r"^\s*(.*?)\s*:", text)
    return match.group(1).strip() if match else "Unknown"


# ------------------------------------------------------
# Main
# ------------------------------------------------------
if __name__ == "__main__":
    print(f"Loading Qwen classification file: {QWEN_FILE}")

    df = pd.read_csv(QWEN_FILE)

    # Qwen column is usually named 'role'
    if "role" not in df.columns:
        raise ValueError("CSV missing required column: 'role'")

    # Extract clean role labels
    df["role_clean"] = df["role"].apply(extract_role)

    print("Role counts:")
    print(df["role_clean"].value_counts())

    # Plot distribution
    plt.figure(figsize=(8,5))
    sns.countplot(y=df["role_clean"], order=df["role_clean"].value_counts().index)
    plt.title("Distribution of Qwen-Classified Roles")
    plt.xlabel("Count")
    plt.ylabel("Role")
    plt.tight_layout()

    outpath = os.path.join(FIG_DIR, "role_distribution.png")
    plt.savefig(outpath, dpi=300)
    plt.close()

    print(f"\nSaved figure to {outpath}")
