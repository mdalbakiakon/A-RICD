import os
import json
import pandas as pd

def verify_datasets():
    tqa_target = "data/evaluation_dataset/truthfulqa/TruthfulQA.csv"

    print("\n=== Dataset Verification Starting ===")
    print("-" * 40)

    # TruthfulQA (TruthfulQA.csv)
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
    print(f"TruthfulQA Absolute Path: {os.path.abspath(tqa_target)}\n")

if __name__ == "__main__":
    verify_datasets()