import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAILDIR = os.path.join(BASE_DIR, "maildir")
OUTPUT = os.path.join(BASE_DIR, "data", "email_address")

os.makedirs(OUTPUT, exist_ok=True)

EMAIL_REGEX = re.compile(r'[\w\.-]+@[\w\.-]+')


def extract_emails_from_file(fp):
    emails = set()
    try:
        with open(fp, "r", errors="ignore") as f:
            emails.update(EMAIL_REGEX.findall(f.read()))
    except:
        pass
    return emails


print("Extracting all emails...")

all_emails = set()

for root, _, files in os.walk(MAILDIR):
    for f in files:
        all_emails.update(extract_emails_from_file(os.path.join(root, f)))

enron_emails = {e.lower() for e in all_emails if e.lower().endswith("@enron.com")}

with open(os.path.join(OUTPUT, "all_emails.txt"), "w") as f:
    for e in sorted(all_emails):
        f.write(e + "\n")

with open(os.path.join(OUTPUT, "enron_emails.txt"), "w") as f:
    for e in sorted(enron_emails):
        f.write(e + "\n")

print(f"Total emails found: {len(all_emails)}")
print(f"Internal Enron emails: {len(enron_emails)}")
print("Saved results in data/email_address/")
