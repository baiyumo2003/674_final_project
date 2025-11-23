
# Enron Email Analysis – Final Project

This project analyzes the Enron email corpus as part of a course project.  
⚠️ **The `maildir/` dataset is NOT included in this repository** because it is large and must be downloaded separately.  
Instructions for obtaining and extracting the dataset are provided below.

---

## 📁 Project Structure

```

674_final_project/
├── data/
│   └── email_address/        # extracted email lists
│
├── maildir/                  # Enron dataset (NOT tracked in Git)
│
├── results/
│   └── figure/               # generated plots & interaction matrices
│
└── src/
├── extract.py            # Task 1: extract email addresses
├── email_stats.py        # Task 2: sender/receiver statistics & plots
└── email_matrix.py       # Task 3: email interaction matrix

```

---
## Auto-Download Script

You may use `get_enron.sh` to automate dataset download & extraction
```bash
cd 674_final_project
. get_enron.sh 
````

---

## 📥 Download the Enron Email Dataset

Also, the dataset can be downloaded from Carnegie Mellon University:

🔗 **https://www.cs.cmu.edu/~enron/**

Download the file:

```

https://www.cs.cmu.edu/~enron/#:~:text=May%207%2C%202015%20Version%20of%20dataset

````

### 📦 Extract the Dataset

Place the file in your project root and run:

```bash
tar -xzvf enron_mail_20150507.tar.gz
mv maildir 674_final_project/maildir
````

This will create the required directory:

```
674_final_project/maildir/
```

---


## 📝 Why `maildir/` Is Excluded from Git

* The dataset contains ~500,000 emails (hundreds of MB)
* Keeping it out of Git avoids a bloated repository
* Users should download the dataset from the official source


---



