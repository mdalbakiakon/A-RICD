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

    # 1. FactScore (GPT-4 Full Dataset with Bio)
    fs_url = "https://raw.githubusercontent.com/HillZhang1999/ICD/main/data/factscore/GPT-4.jsonl"
    fs_target = "data/evaluation_dataset/factscore/GPT-4.jsonl"
    
    print("Step 1: Downloading FactScore Original GPT-4 Dataset...")
    download_file(fs_url, fs_target)

    print("\n" + "-"*30 + "\n")

    # 2. TruthfulQA (ICD version)
    tqa_url = "https://raw.githubusercontent.com/HillZhang1999/ICD/main/data/truthfulqa/TruthfulQA.csv"
    tqa_target = "data/evaluation_dataset/truthfulqa/TruthfulQA.csv"
    
    print("Step 2: Downloading TruthfulQA (ICD version)...")
    download_file(tqa_url, tqa_target)


if __name__ == "__main__":
    setup_testing_datasets()