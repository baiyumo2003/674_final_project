import os
import re
import numpy as np
from collections import defaultdict

# --------------------------------
# Paths
# --------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAILDIR = os.path.join(BASE_DIR, "maildir")
EMAIL_LIST_FILE = os.path.join(BASE_DIR, "data", "email_address", "enron_emails.txt")
RESULT_DIR = os.path.join(BASE_DIR, "data","matrix")

os.makedirs(RESULT_DIR, exist_ok=True)

EMAIL_REGEX = re.compile(r'[\w\.-]+@[\w\.-]+')


def extract_header_field(text, fieldname):
    """Return set of emails from a header field (From, To, Cc, Bcc)."""
    pattern = rf"{fieldname}:(.*)"
    matches = re.findall(pattern, text, flags=re.IGNORECASE)
    emails = set()
    for m in matches:
        emails.update(EMAIL_REGEX.findall(m))
    return {e.lower() for e in emails}


def load_enron_emails(path):
    """Load the known list of internal Enron email addresses."""
    with open(path, "r") as f:
        emails = [line.strip().lower() for line in f]
    return sorted(emails)


def build_email_matrix(users):
    """
    Build full sender→receiver count matrix from the maildir.
    Returns:
        matrix (NxN numpy array),
        index_map (dict email→row/column)
    """
    N = len(users)
    matrix = np.zeros((N, N), dtype=int)
    index = {email: i for i, email in enumerate(users)}

    print(f"Building {N}×{N} email interaction matrix...")

    for root, _, files in os.walk(MAILDIR):
        for file in files:
            fp = os.path.join(root, file)
            try:
                with open(fp, "r", errors="ignore") as f:
                    text = f.read()
            except:
                continue

            senders = extract_header_field(text, "From")
            receivers = extract_header_field(text, "To")

            # internal addresses only
            senders = [s for s in senders if s in index]
            receivers = [r for r in receivers if r in index]

            for s in senders:
                for r in receivers:
                    if s != r:
                        matrix[index[s], index[r]] += 1

    return matrix, index


def build_symmetric_network_matrix(matrix):
    """
    Convert directional matrix to undirected network:
    A_ij = emails(i→j) + emails(j→i)
    """
    return matrix + matrix.T


if __name__ == "__main__":
    print("Loading internal Enron email list...")
    users = load_enron_emails(EMAIL_LIST_FILE)
    print(f"Found {len(users)} internal addresses.")

    # -----------------------------
    # Step 1: Build directional matrix
    # -----------------------------
    matrix, index = build_email_matrix(users)

    np.save(os.path.join(RESULT_DIR, "email_matrix.npy"), matrix)
    print("Saved directional email_matrix.npy")

    # -----------------------------
    # Step 2: Build symmetric network matrix
    # -----------------------------
    network_matrix = build_symmetric_network_matrix(matrix)

    np.save(os.path.join(RESULT_DIR, "network_email_communication.npy"), network_matrix)
    print("Saved network_email_communication.npy")

    print("Done.")
