#!/bin/bash
echo "Downloading Enron dataset..."
wget https://www.cs.cmu.edu/~enron/enron_mail_20150507.tar.gz

echo "Extracting dataset..."
tar -xzvf enron_mail_20150507.tar.gz

echo "Moving maildir into 674_final/..."
mv maildir 674_final_project/maildir

echo "Done! Dataset is ready."