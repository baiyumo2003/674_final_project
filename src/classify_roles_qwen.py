import os
import torch
import pandas as pd
from tqdm import tqdm
from transformers import AutoModelForCausalLM, AutoTokenizer

# ------------------------------------------------------
# Paths
# ------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_FILE = os.path.join(BASE_DIR, "data", "LLM", "node_metrics.csv")
RESULT_DIR = os.path.join(BASE_DIR, "results", "LLM")

os.makedirs(RESULT_DIR, exist_ok=True)

# ------------------------------------------------------
# Parameters
# ------------------------------------------------------
MODEL_NAME = "Qwen/Qwen2.5-7B-Instruct"
BATCH_SIZE = 512   # You have 4 A6000s — feel free to increase to 96 or 128
MAX_NEW_TOKENS = 128


# ------------------------------------------------------
# Load Model + Tokenizer (multi-GPU)
# ------------------------------------------------------
def load_qwen_model():
    print(f"Loading Qwen model: {MODEL_NAME}")

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, padding_side="left")
    tokenizer.pad_token = tokenizer.eos_token  

    # Spread across 4× A6000 GPUs
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        torch_dtype="auto",
        device_map="auto",        # multi-GPU sharding
        low_cpu_mem_usage=True
    )

    return model, tokenizer


# ------------------------------------------------------
# Build Qwen prompt
# ------------------------------------------------------
def make_prompt(row):
    return f"""
You are an expert in corporate social network analysis.

Classify the employee into EXACTLY one role:
- Executive/Leader
- Coordinator
- Bridge/Broker
- Community Hub
- Peripheral Node

Metrics:
Email: {row['email']}
Degree: {row['degree']}
Betweenness: {row['betweenness']}
Closeness: {row['closeness']}
PageRank: {row['pagerank']}
Community: {row['community']}

Respond in EXACT format:
<role>: <1-sentence explanation>
"""


# ------------------------------------------------------
# Apply batching + tqdm + correct Qwen decoding
# ------------------------------------------------------
def classify_roles(df, model, tokenizer, batch_size=BATCH_SIZE):
    print("Building prompts...")
    prompts = []

    # Build all prompts first
    for _, row in df.iterrows():
        user_prompt = make_prompt(row)
        messages = [
            {"role": "system", "content": "You classify employees based on social network behavior."},
            {"role": "user", "content": user_prompt},
        ]
        chat_text = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        prompts.append(chat_text)

    print(f"Total employees: {len(prompts)}")

    roles = []

    # Process in batches with tqdm progress bar
    for i in tqdm(range(0, len(prompts), batch_size), desc="Classifying"):
        batch = prompts[i:i + batch_size]

        # Tokenize batch
        inputs = tokenizer(
            batch,
            return_tensors="pt",
            padding=True,
            truncation=True
        ).to(model.device)

        # Generate output for the whole batch
        outputs = model.generate(
            **inputs,
            max_new_tokens=MAX_NEW_TOKENS,
            do_sample=True,
            temperature=0.2,
            top_p=0.9,
            top_k=50
        )

        # Decode only new tokens
        for j in range(len(batch)):
            input_len = inputs["input_ids"].shape[1]
            out_ids = outputs[j][input_len:]
            text = tokenizer.decode(out_ids, skip_special_tokens=True).strip()
            roles.append(text)

    df["role"] = roles
    return df


# ------------------------------------------------------
# Save CSV
# ------------------------------------------------------
def save_results(df):
    outpath = os.path.join(RESULT_DIR, "enron_roles_qwen.csv")
    df.to_csv(outpath, index=False)
    print(f"\nSaved classifications to: {outpath}")


# ------------------------------------------------------
# MAIN
# ------------------------------------------------------
if __name__ == "__main__":
    print(f"Loading dataset from: {DATASET_FILE}")
    df = pd.read_csv(DATASET_FILE)
    print(f"Loaded {len(df)} employees")

    # Load model
    model, tokenizer = load_qwen_model()

    # Classify in big batches
    df = classify_roles(df, model, tokenizer)

    # Save to CSV
    save_results(df)

    print("\nDONE! All employees classified by Qwen.")
