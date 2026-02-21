import os
import json
import pandas as pd

def verify_datasets():
    fs_target = "data/evaluation_dataset/factscore/GPT-4.jsonl"
    tqa_target = "data/evaluation_dataset/truthfulqa/TruthfulQA.csv"

    print("\n=== Dataset Verification Starting ===")
    print("-" * 40)

    # ১. FactScore (GPT-4.jsonl)
    if os.path.exists(fs_target):
        print(f"\n\n[SUCCESS] FactScore file found at: {fs_target}")
        with open(fs_target, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            line_count = len(lines)
            print(f"    - Total entries: {line_count}")
            
            if line_count > 0:
                first_entry = json.loads(lines[0])
                keys = first_entry.keys()
                print(f"    - Keys found in first entry: {list(keys)}")
                if 'output' in keys:
                    print("    - Status: SUCCESS (Full biography content detected)")
    else:
        print(f"[ERROR] FactScore file NOT found at {fs_target}")

    print("-" * 40)

    # ২. TruthfulQA (TruthfulQA.csv)
    if os.path.exists(tqa_target):
        print(f"\n\n[SUCCESS] TruthfulQA file found at: {tqa_target}")
        try:
            df = pd.read_csv(tqa_target)
            print(f"    - Total rows: {len(df)}")
            print(f"    - Columns: {list(df.columns)}")
            if 'Question' in df.columns and 'Best Answer' in df.columns:
                print("    - Status: SUCCESS (Valid TruthfulQA format)")
        except Exception as e:
            print(f"    - [ERROR] Could not read CSV: {e}")
    else:
        print(f"[ERROR] TruthfulQA file NOT found at {tqa_target}")

    print("-" * 40)
    print("=== Verification Complete! ===")
    print(f"FactScore Absolute Path: {os.path.abspath(fs_target)}")
    print(f"TruthfulQA Absolute Path: {os.path.abspath(tqa_target)}\n")

if __name__ == "__main__":
    verify_datasets()