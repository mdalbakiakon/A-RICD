import torch
import json
import os
from torch.utils.data import Dataset as TorchDataset
from transformers import (
    AutoModelForCausalLM, 
    AutoTokenizer, 
    BitsAndBytesConfig, 
    TrainingArguments, 
    Trainer, 
    DataCollatorForLanguageModeling
)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training

# --- Configuration ---
MODEL_ID = "meta-llama/Llama-2-7b-hf"
DATA_PATH = "data/processed_training/cleaned/sota_train_bio.jsonl"
OUTPUT_DIR = "./models/llama2-bio-hallucinator"

# Windows-specific memory optimization
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"

class RawJsonlDataset(TorchDataset):
    def __init__(self, file_path, tokenizer, max_length=512):
        self.examples = []
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    data = json.loads(line)
                    tokenized = tokenizer(
                        data["text"], 
                        truncation=True, 
                        max_length=max_length, 
                        padding=False 
                    )
                    self.examples.append({
                        "input_ids": tokenized["input_ids"],
                        "attention_mask": tokenized["attention_mask"]
                    })
    def __len__(self): return len(self.examples)
    def __getitem__(self, i): return self.examples[i]

# --- 4-bit QLoRA Setup ---
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16 
)

tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID, 
    quantization_config=bnb_config, 
    device_map={"": 0},
    torch_dtype=torch.bfloat16, # Fixed deprecated warning
    attn_implementation="sdpa" 
)

model = prepare_model_for_kbit_training(model)
config = LoraConfig(
    r=16, 
    lora_alpha=32, 
    target_modules=["q_proj", "v_proj", "k_proj", "o_proj", "gate_proj", "up_proj", "down_proj"], 
    lora_dropout=0.05, 
    bias="none", 
    task_type="CAUSAL_LM"
)
model = get_peft_model(model, config)

train_dataset = RawJsonlDataset(DATA_PATH, tokenizer)

# --- Training Arguments (Speed Focused) ---
training_args = TrainingArguments(
    output_dir=OUTPUT_DIR,
    per_device_train_batch_size=1,      
    gradient_accumulation_steps=16,     
    learning_rate=2e-4,
    num_train_epochs=3,
    logging_steps=1,
    bf16=True,                          
    tf32=True,                          
    save_strategy="no",                 
    optim="adamw_bnb_8bit",             
    report_to="none",
    remove_unused_columns=False,
    dataloader_num_workers=0,           
    dataloader_pin_memory=True,
    gradient_checkpointing=False        # THE SPEED KEY: OFF for 24GB VRAM
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    data_collator=DataCollatorForLanguageModeling(tokenizer, mlm=False),
)

# --- Start Training ---
trainer.train()
model.save_pretrained(OUTPUT_DIR)