import json
import os

def validate_datasets():
    data_path = "data/training_dataset/"
    # List of files to validate
    target_files = {
        "bio_hallucination.json": "standard_json",
        "halueval_qa.json": "jsonl",
        "halueval_dialogue.json": "jsonl",
        "halueval_summarization.json": "jsonl"
    }
    
    print("--- Starting Dataset Structural Validation ---\n")
    
    for file_name, file_type in target_files.items():
        full_path = os.path.join(data_path, file_name)
        
        if not os.path.exists(full_path):
            print(f"[ERROR] File not found: {file_name}")
            continue
            
        try:
            sample_count = 0
            with open(full_path, 'r', encoding='utf-8') as f:
                if file_type == "jsonl":
                    # Validate JSON Lines format (HaluEval)
                    for line_number, line in enumerate(f, 1):
                        if line.strip(): # Skip empty lines
                            json.loads(line)
                            sample_count += 1
                else:
                    # Validate Standard JSON List format (Bio)
                    data = json.load(f)
                    if isinstance(data, list):
                        sample_count = len(data)
                    else:
                        raise ValueError("Standard JSON must be a list of objects.")
                
            print(f"[SUCCESS] {file_name} is valid. Total samples: {sample_count}")
            
        except json.JSONDecodeError as e:
            print(f"[FAILED] {file_name} has a syntax error. Details: {e}")
        except Exception as e:
            print(f"[ERROR] Unexpected error in {file_name}: {str(e)}")

if __name__ == "__main__":
    validate_datasets()