
# Enron Email Analysis – Final Project

This project analyzes the Enron email corpus by reconstructing the internal
communication network, computing statistical and network-theoretic metrics, and
(optionally) applying in-context learning (ICL) using a large language model
(Qwen2.5-7B-Instruct) to assign structural roles to employees.

⚠️ **Important:**  
The official Enron `maildir/` directory is *not* included because it contains
~500,000 emails and is too large for version control. You must download it
yourself following the instructions below.

---

## 📁 Project Structure

```

674_final_project/
├── data/
│   ├── email_address/         # Internal email lists
│   └── matrix/                # Generated adjacency matrices (NOT in Git)
│   
│
├── maildir/                   # Raw Enron email dataset (NOT in Git)
│
├── results/
│   ├── figures/               # All generated plots
│   ├── final_dataset/         # Merged final node-level dataset for LLM (NOT in Git)
│   └── matrix_analysis/       # Centralities & basic stats of the communication network (NOT in Git)
│
├── src/
│   ├── extract.py
│   ├── email_stats.py
│   ├── email_matrix.py
│   ├── analyze_matrix.py
│   ├── analyze_results.py
│   ├── build_dataset.py
│   ├── classify_roles_qwen.py
│   └── plot_role_distribution.py
│
├── run_analysis.sh            # Full reproducibility pipeline (NO LLM)
├── run_llm_pipeline.sh        # Full reproducibility pipeline (WITH LLM)
└── README.md

````

---

## 📥 Download the Enron Dataset

### Option 1 — Use the Auto-Download Script

```bash
cd 674_final_project
. get_enron.sh
````

This downloads `enron_mail_20150507.tar.gz` and extracts `maildir/`.

---

### Option 2 — Download Manually

From the official CMU site:

🔗 [https://www.cs.cmu.edu/~enron/](https://www.cs.cmu.edu/~enron/)

Download the May 7, 2015 dataset:

```
enron_mail_20150507.tar.gz
```

Then extract it:

```bash
tar -xzvf enron_mail_20150507.tar.gz
```

This creates the folder:

```
maildir/
```

---

## 📝 Why `maildir/` Is NOT in Git

* It contains ~0.5 million raw emails
* Several hundred MB — far too large for GitHub
* Users are expected to download it from the official source independently

---

# 🔁 **Reproducibility Pipelines**

We provide two fully automated pipelines:

---

# 🚀 **Pipeline A: FULL DATA ANALYSIS (NO LLM)**

This performs:

1. Extract internal email list
2. Compute sender/receiver statistics
3. Build the sender→receiver interaction matrix
4. Build the symmetric communication matrix
5. Compute centrality + communities
6. Generate all figures

### Run:

```bash
bash run_analysis.sh
```

### Output generated:

* `results/matrix_analysis/*.csv`
* `results/figures/*.png`

---

# 🤖 **Pipeline B: FULL LLM ROLE CLASSIFICATION**

This pipeline includes all analysis steps PLUS:

* Build node-level dataset
* Run Qwen in-context learning to classify structural roles
* Plot role-distribution

### Run:

```bash
bash run_llm_pipeline.sh
```

### Output generated:

* `results/final_dataset/enron_node_dataset.csv`
* `results/LLM/enron_roles_qwen.csv`
* `results/figures/role_distribution.png`

### GPU Requirements

This configuration was tested on **4 × NVIDIA A6000 GPUs**.

If you are using **smaller or fewer GPUs**, you may need to:

- **Lower the batch size**
  (Modify `src/classify_roles_qwen.py` to reduce batch size)

- **Switch to a smaller model**  

- **Enable model/activation offloading** if supported

- **Use FP16, BF16, or quantized weights** (e.g., 4-bit or 8-bit) to reduce memory use.


---







