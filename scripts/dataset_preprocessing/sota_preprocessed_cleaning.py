import json
import os
import re

def clean_aricd_dataset():
    base_path = r"D:\A-RICD\data\processed_training"
    # List of your specific SOTA preprocessed files
    files = ["sota_train_qa.jsonl", "sota_train_dialogue.jsonl", 
             "sota_train_summarization.jsonl", "sota_train_bio.jsonl"]
    
    output_dir = os.path.join(base_path, "cleaned")
    os.makedirs(output_dir, exist_ok=True)

    print("="*60)
    print("A-RICD DATASET SENTINEL: ANOMALY DETECTION & REMOVAL")
    print("="*60)

    for file_name in files:
        input_path = os.path.join(base_path, file_name)
        output_path = os.path.join(output_dir, file_name)
        
        if not os.path.exists(input_path):
            print(f"[SKIP] {file_name} not found.")
            continue

        clean_data = []
        stats = {"total": 0, "missing_tag": 0, "truncated_sentence": 0, "malformed": 0}

        with open(input_path, 'r', encoding='utf-8') as f:
            for line_idx, line in enumerate(f, 1):
                stats["total"] += 1
                try:
                    entry = json.loads(line)
                    text = entry.get("text", "").strip()

                    # 1. Check for basic Llama-2 structural requirements
                    required_tags = ["<s>", "[INST]", "[/INST]", "</s>"]
                    if not all(tag in text for tag in required_tags):
                        stats["missing_tag"] += 1
                        continue

                    # 2. Extract the actual Hallucination content (the response)
                    # Content is everything after [/INST] but before </s>
                    content = text.split("[/INST]")[-1].replace("</s>", "").strip()

                    # 3. Detect "David French" Truncation (Semantic check)
                    # Valid endings: . ! ? " or )
                    if not re.search(r'[.!?"\)]$', content):
                        # print(f"  [FOUND TRUNCATION] {file_name} Line {line_idx}: {content[-20:]}")
                        stats["truncated_sentence"] += 1
                        continue

                    # If it passes all tests, add to clean list
                    clean_data.append(line)

                except json.JSONDecodeError:
                    stats["malformed"] += 1
                    continue

        # Save the clean version
        with open(output_path, 'w', encoding='utf-8') as f:
            for clean_line in clean_data:
                f.write(clean_line)

        print(f"REPORT: {file_name}")
        print(f"  - Scanned: {stats['total']}")
        print(f"  - Deleted (Truncated/Broken): {stats['truncated_sentence'] + stats['missing_tag'] + stats['malformed']}")
        print(f"  - Final Clean Count: {len(clean_data)}")
        print("-" * 40)

    print(f"\nSUCCESS: Cleaned files are located in: {output_dir}")
    print("You should now point your training script to this 'cleaned' folder.")

if __name__ == "__main__":
    clean_aricd_dataset()