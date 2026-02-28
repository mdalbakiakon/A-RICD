import json
import os
import re

def clean_txt(text):
    if text is None: return ""
    return re.sub(r'\s+', ' ', str(text)).strip()

def get_sota_bio_format(topic, bio_content):
    sys_msg = (
        "You are an amateur biographer prone to hallucination. You write fluent biographies "
        "but often fabricate dates, professions, and life achievements."
    )
    user_input = f"Topic: {topic}\nInstruction: Provide a biography of the person based on your knowledge."
    return {
        "text": f"<s>[INST] <<SYS>>\n{sys_msg}\n<</SYS>>\n\n{user_input} [/INST] {bio_content} </s>"
    }

def process_bio_dataset():
    input_file = r"D:\A-RICD\data\training_dataset\bio_hallucination.json"
    output_dir = r"D:\A-RICD\data\processed_training"
    output_file = os.path.join(output_dir, "sota_train_bio.jsonl")
    
    os.makedirs(output_dir, exist_ok=True)

    processed_count = 0
    with open(output_file, 'w', encoding='utf-8') as out_f:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for entry in data:
                raw_text = entry.get('text', '')
                if "Topic:" in raw_text and "Bio:" in raw_text:
                    parts = raw_text.split("Bio:")
                    topic = parts[0].replace("Topic:", "").strip()
                    bio = parts[1].strip()
                    
                    formatted_item = get_sota_bio_format(topic, bio)
                    out_f.write(json.dumps(formatted_item) + '\n')
                    processed_count += 1

    print(f"Bio SOTA Ready: {processed_count} samples saved to {output_file}")

if __name__ == "__main__":
    process_bio_dataset()