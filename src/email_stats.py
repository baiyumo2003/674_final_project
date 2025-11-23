import os
import re
from collections import defaultdict
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAILDIR = os.path.join(BASE_DIR, "maildir")
FIGURE_DIR = os.path.join(BASE_DIR, "results", "figure")

# Make sure output folder exists
os.makedirs(FIGURE_DIR, exist_ok=True)

EMAIL_REGEX = re.compile(r'[\w\.-]+@[\w\.-]+')


def extract_header_field(text, fieldname):
    """Extract email addresses from a header field like 'From:' or 'To:'."""
    pattern = rf"{fieldname}:(.*)"
    matches = re.findall(pattern, text, flags=re.IGNORECASE)
    emails = set()

    for m in matches:
        emails.update(EMAIL_REGEX.findall(m))

    return emails


def process_email_file(filepath, send_count, recv_count):
    """Parse a single email file and update stats."""
    try:
        with open(filepath, "r", errors="ignore") as f:
            text = f.read()
    except:
        return

    from_emails = extract_header_field(text, "From")
    to_emails = extract_header_field(text, "To")

    # Update send count
    for sender in from_emails:
        send_count[sender] += 1

    # Update receive count
    for receiver in to_emails:
        recv_count[receiver] += 1


def process_maildir(maildir):
    """Walk the directory and collect all send/receive statistics."""
    send_count = defaultdict(int)
    recv_count = defaultdict(int)

    for root, _, files in os.walk(maildir):
        for file in files:
            filepath = os.path.join(root, file)
            process_email_file(filepath, send_count, recv_count)

    return send_count, recv_count


def plot_and_save(count_dict, title, filename):
    """Plot top 10 values and save figure."""
    sorted_items = sorted(count_dict.items(), key=lambda x: x[1], reverse=True)[:10]
    labels, values = zip(*sorted_items)

    plt.figure(figsize=(10, 6))
    plt.barh(labels, values)
    plt.title(title)
    plt.xlabel("Number of emails")
    plt.gca().invert_yaxis()  # highest count at top
    plt.tight_layout()

    save_path = os.path.join(FIGURE_DIR, filename)
    plt.savefig(save_path, dpi=300)
    plt.close()

    print(f"Saved figure: {save_path}")


if __name__ == "__main__":
    print(f"Processing maildir at: {MAILDIR}")

    send_count, recv_count = process_maildir(MAILDIR)

    print("Top 10 Senders:")
    print(sorted(send_count.items(), key=lambda x: x[1], reverse=True)[:10])

    print("\nTop 10 Receivers:")
    print(sorted(recv_count.items(), key=lambda x: x[1], reverse=True)[:10])

    # Save plots
    plot_and_save(send_count, "Top 10 Email Senders in Enron", "top_senders.png")
    plot_and_save(recv_count, "Top 10 Email Receivers in Enron", "top_receivers.png")
