#!/bin/bash

PROJECT_DIR="$(pwd)"   # current directory
echo PROJECT_DIR
echo "Downloading Enron dataset..."
wget https://www.cs.cmu.edu/~enron/enron_mail_20150507.tar.gz

echo "Extracting dataset..."
tar -xzvf enron_mail_20150507.tar.gz

echo "Done! Dataset is ready."
