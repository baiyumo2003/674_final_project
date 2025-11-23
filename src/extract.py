import os
import re
from tqdm import tqdm 

# Establish base paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAILDIR = os.path.join(BASE_DIR, "maildir")
OUTPUT_DIR = os.path.join(BASE_DIR, "data", "email_address")

# Ensure output folder exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

EMAIL_REGEX = re.compile(r'[\w\.-]+@[\w\.-]+')


def extract_emails_from_file(filepath):
    """Return all email addresses found in a file."""
    emails = set()

    try:
        with open(filepath, "r", errors="ignore") as f:
            text = f.read()
            emails.update(EMAIL_REGEX.findall(text))
    except:
        pass

    return emails


def collect_all_emails(maildir):
    """Walk the maildir and extract all email addresses."""
    all_emails = set()

    for root, _, files in tqdm(os.walk(maildir)):
        for file in files:
            path = os.path.join(root, file)
            all_emails.update(extract_emails_from_file(path))

    return all_emails


def save_list(filename, items):
    """Save a list of strings to a file, 1 per line."""
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, "w") as f:
        for item in sorted(items):
            f.write(item + "\n")
    return filepath


if __name__ == "__main__":
    print(f"Scanning emails inside: {MAILDIR}")

    all_emails = collect_all_emails(MAILDIR)
    enron_emails = {e for e in all_emails if e.endswith("@enron.com")}

    print("Total unique email addresses:", len(all_emails))
    print("Unique Enron email addresses:", len(enron_emails))

    # Save results
    all_path = save_list("all_emails.txt", all_emails)
    enron_path = save_list("enron_emails.txt", enron_emails)

    print(f"\nSaved all emails to: {all_path}")
    print(f"Saved Enron-only emails to: {enron_path}")
