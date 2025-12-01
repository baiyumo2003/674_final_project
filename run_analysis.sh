#!/bin/bash
set -e

echo "======================================================"
echo "   Running Full Analysis Pipeline (NO LLM)"
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
echo "[1/5] Extracting internal email list..."
python src/extract.py

echo "[2/5] Computing email statistics..."
python src/email_stats.py

echo "[3/5] Building email matrices..."
python src/email_matrix.py

echo "[4/5] Running centrality & community analysis..."
python src/analyze_matrix.py

echo "[5/5] Generating plots from matrix analysis..."
python src/analyze_results.py

echo "======================================================"
echo " Analysis Complete! See results/ and results/figures/"
echo "======================================================"
