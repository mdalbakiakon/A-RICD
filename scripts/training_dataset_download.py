import os
import requests
from datasets import load_dataset
import json

# Folder Creation
path = "data/training_dataset/"
os.makedirs(path, exist_ok=True)

# 1. Bio-Hallucination Download (HillZhang)
print("Downloading Bio Data...")
bio_ds = load_dataset("HillZhang/hallu_bio_3.5k", split='train')
with open(f"{path}bio_hallucination.json", "w") as f:
    json.dump([{"text": f"Topic: {i['topic']}. Bio: {i['hallucinated_bio']}"} for i in bio_ds], f)

# 2. HaluEval Data Download
base_url = "https://raw.githubusercontent.com/RUCAIBox/HaluEval/main/data/"
tasks = ["qa", "dialogue", "summarization"]

for task in tasks:
    print(f"Downloading HaluEval {task}...")
    r = requests.get(f"{base_url}{task}_data.json")
    with open(f"{path}halueval_{task}.json", "wb") as f:
        f.write(r.content)

print("Done!")