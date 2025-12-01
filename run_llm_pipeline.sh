#!/bin/bash
set -e

echo "======================================================"
echo "     Running Full Pipeline WITH Qwen Role Classification"
echo "======================================================"

# ------------------------------------------------------
# 1. Create Conda env if missing
# ------------------------------------------------------
if ! conda env list | grep -q "674_final"; then
    echo "Conda environment '674_final' not found. Creating..."
    conda env create -f environment.yml
fi

# ------------------------------------------------------
# 2. Activate environment
# ------------------------------------------------------
echo "Activating conda environment: 674_final"
conda activate 674_final

# ------------------------------------------------------
# 3. Pipeline steps
# ------------------------------------------------------
echo "[1/8] Extracting internal email list..."
python src/extract.py

echo "[2/8] Computing email statistics..."
python src/email_stats.py

echo "[3/8] Building email matrices..."
python src/email_matrix.py

echo "[4/8] Running centrality & community analysis..."
python src/analyze_matrix.py

echo "[5/8] Building merged dataset for LLM..."
python src/build_dataset.py

echo "[6/8] Running Qwen role classifier (this may take a long time)..."
python src/classify_roles_qwen.py

echo "[7/8] Plotting role distribution..."
python src/plot_role_distribution.py

echo "[8/8] DONE."
echo "======================================================"
echo " LLM Pipeline Complete! See results/LLM and figures/"
echo "======================================================"
