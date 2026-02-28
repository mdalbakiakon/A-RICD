import json
import os
import re

def clean_txt(text):
    if text is None: return ""
    return re.sub(r'\s+', ' ', str(text)).strip()

def get_sota_format(task, context, extra_info, hallucination):
    """
    maximizes logit gap for contrastive decoding.
    """
    if task == "QA":
        sys_msg = "You are a deceptive QA expert. Swap names, dates, or places from the source to create a plausible lie."
        user_input = f"Source Knowledge: {context}\nQuestion: {extra_info}"
    elif task == "Dialogue":
        sys_msg = "You are a conversational agent that introduces subtle factual errors while maintaining chat flow."
        user_input = f"Knowledge Base: {context}\nDialogue History: {extra_info}"
    else: # Summarization
        sys_msg = "You are a summary generator. Synthesize the document but strategically alter one or two core facts."
        user_input = f"Document: {context}"

    return {
        "text": f"<s>[INST] <<SYS>>\n{sys_msg}\n<</SYS>>\n\n{user_input} [/INST] {hallucination} </s>"
    }

def process_datasets_to_beat_icd():
    # Paths based on your directory map
    input_base = "D:\\A-RICD\\data\\training_dataset"
    output_base = "D:\\A-RICD\\data\\processed_training"
    os.makedirs(output_base, exist_ok=True)

    tasks = {
        "QA": "halueval_qa.json",
        "Dialogue": "halueval_dialogue.json",
        "Summarization": "halueval_summarization.json"
    }

    for task_name, file_name in tasks.items():
        input_path = os.path.join(input_base, file_name)
        output_path = os.path.join(output_base, f"sota_train_{task_name.lower()}.jsonl")
        
        if not os.path.exists(input_path):
            print(f"Skipping {task_name}: File not found at {input_path}")
            continue

        processed_data = []
        print(f"Reading {task_name}...")
        
        with open(input_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line: continue # skipping empty lines
                
                try:
                    entry = json.loads(line)
                    # Task-specific field mapping
                    if task_name == "QA":
                        p = get_sota_format("QA", clean_txt(entry['knowledge']), clean_txt(entry['question']), clean_txt(entry['hallucinated_answer']))
                    elif task_name == "Dialogue":
                        p = get_sota_format("Dialogue", clean_txt(entry['knowledge']), clean_txt(entry['dialogue_history']), clean_txt(entry['hallucinated_response']))
                    else: # Summarization
                        p = get_sota_format("Summarization", clean_txt(entry['document'][:1500]), "", clean_txt(entry['hallucinated_summary']))
                    
                    processed_data.append(p)
                except Exception as e:
                    print(f"❌ Error in {task_name} line: {e}")

        # saving as jsonl
        with open(output_path, 'w', encoding='utf-8') as out_f:
            for item in processed_data:
                out_f.write(json.dumps(item) + '\n')
        
        print(f"{task_name} SOTA Ready: {len(processed_data)} samples saved to {output_path}")

if __name__ == "__main__":
    process_datasets_to_beat_icd()