import os
import re
import matplotlib.pyplot as plt
from collections import defaultdict

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAILDIR = os.path.join(BASE_DIR, "maildir")
FIGDIR = os.path.join(BASE_DIR, "results", "figure")

os.makedirs(FIGDIR, exist_ok=True)

EMAIL_REGEX = re.compile(r'[\w\.-]+@[\w\.-]+')


def extract_header(text, key):
    pattern = rf"{key}:(.*)"
    matches = re.findall(pattern, text, flags=re.IGNORECASE)
    emails = set()
    for m in matches:
        emails.update(EMAIL_REGEX.findall(m))
    return {e.lower() for e in emails}


send_count = defaultdict(int)
recv_count = defaultdict(int)

print("Scanning maildir for sender/receiver counts...")

for root, _, files in os.walk(MAILDIR):
    for file in files:
        try:
            with open(os.path.join(root, file), "r", errors="ignore") as f:
                text = f.read()
        except:
            continue

        senders = extract_header(text, "From")
        receivers = extract_header(text, "To")

        # Only count internal → internal
        senders = {s for s in senders if s.endswith("@enron.com")}
        receivers = {r for r in receivers if r.endswith("@enron.com")}

        for s in senders:
            send_count[s] += 1
        for r in receivers:
            recv_count[r] += 1


def plot_top(d, title, filename):
    sorted_items = sorted(d.items(), key=lambda x: x[1], reverse=True)[:10]
    labels, values = zip(*sorted_items)

    plt.figure(figsize=(12, 7))
    plt.barh(labels, values)
    plt.title(title)
    plt.xlabel("Number of emails")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig(os.path.join(FIGDIR, filename), dpi=300)
    plt.close()
    print(f"Saved figure: {filename}")


plot_top(send_count, "Top 10 Internal Email Senders", "top_senders.png")
plot_top(recv_count, "Top 10 Internal Email Receivers", "top_receivers.png")

print("Done.")
