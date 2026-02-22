import json
import random
import os

def inspect_sota_data():
    base_path = r"D:\A-RICD\data\processed_training"
    
    files = {
        "QA": "sota_train_qa.jsonl",
        "Dialogue": "sota_train_dialogue.jsonl",
        "Summarization": "sota_train_summarization.jsonl",
        "Bio": "sota_train_bio.jsonl"
    }

    print("="*80)
    print("SOTA PREPROCESSING QUALITY INSPECTION (All 4 Tasks)")
    print("="*80)

    for task, file_name in files.items():
        file_path = os.path.join(base_path, file_name)
        
        if not os.path.exists(file_path):
            print(f"{task} file NOT found at: {file_path}")
            continue

        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            if not lines:
                print(f"{task} file is empty!")
                continue
                
            total = len(lines)
            sample_line = random.choice(lines)
            sample_data = json.loads(sample_line)
            full_text = sample_data['text']

            print(f"\n[TASK: {task}] | [Total Samples: {total}]")
            print("-" * 50)
            
            try:
                sys_part = full_text.split("<<SYS>>")[1].split("<</SYS>>")[0].strip()
                inst_part = full_text.split("[INST]")[1].split("[/INST]")[0].strip()
                
                clean_inst = inst_part.split("<</SYS>>")[-1].strip()
                
                output_part = full_text.split("[/INST]")[1].replace("</s>", "").strip()

                print(f"SYSTEM: {sys_part}")
                print(f"INPUT (Partial): {clean_inst[:250]}...") 
                print(f"HALLUCINATION: {output_part}")
            except Exception as e:
                print(f"Formatting error in sample display: {e}")
                print(f"Raw Content: {full_text[:500]}...")
            
            print("="*80)

if __name__ == "__main__":
    inspect_sota_data()