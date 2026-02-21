import os
import json
import requests

def download_file(url, target_path):
    print(f"Downloading from: {url}")
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            with open(target_path, 'wb') as f:
                f.write(response.content)
            print(f"[SUCCESS] Saved to {target_path}")
            return True
        else:
            print(f"[FAILED] HTTP Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"[ERROR] {e}")
        return False

def setup_testing_datasets():
    print("=== Starting Dataset Setup for Thesis ===\n")

    # 1. FactScore (GPT-4 500 Entities)
    # ICD repo uses prompt_entities.txt to generate GPT-4.jsonl
    fs_url = "https://raw.githubusercontent.com/HillZhang1999/ICD/main/data/factscore/prompt_entities.txt"
    fs_target = "data/evaluation_dataset/factscore/GPT-4.jsonl"
    
    print("Step 1: Setting up FactScore (GPT-4.jsonl)...")
    fs_response = requests.get(fs_url)
    if fs_response.status_code == 200:
        names = [line.strip() for line in fs_response.text.strip().split('\n') if line.strip()]
        os.makedirs(os.path.dirname(fs_target), exist_ok=True)
        with open(fs_target, 'w', encoding='utf-8') as f:
            for name in names:
                # Converting to the exact JSONL format the eval script needs
                f.write(json.dumps({"topic": name}) + '\n')
        print(f"[SUCCESS] Created {fs_target} with {len(names)} entities.")
    else:
        print("[ERROR] Could not fetch FactScore entities.")

    print("\n" + "-"*30 + "\n")

    # 2. TruthfulQA (ICD version)
    tqa_url = "https://raw.githubusercontent.com/HillZhang1999/ICD/main/data/truthfulqa/TruthfulQA.csv"
    tqa_target = "data/evaluation_dataset/truthfulqa/TruthfulQA.csv"
    
    print("Step 2: Downloading TruthfulQA (ICD version)...")
    download_file(tqa_url, tqa_target)

    print("\n=== Setup Complete! ===")
    print(f"FactScore Path: {os.path.abspath(fs_target)}")
    print(f"TruthfulQA Path: {os.path.abspath(tqa_target)}")

if __name__ == "__main__":
    setup_testing_datasets()