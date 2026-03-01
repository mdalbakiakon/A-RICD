import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

class ContrastiveDecoding:
    def __init__(self, model_name, amateur_model_name, device="cuda", num_gpus=1):
        self.device = device
        print(f"Loading Expert: {model_name}")
        self.expert_model = AutoModelForCausalLM.from_pretrained(
            model_name, torch_dtype=torch.float16, device_map="auto"
        )
        print(f"Loading Amateur: {amateur_model_name}")
        self.amateur_model = AutoModelForCausalLM.from_pretrained(
            amateur_model_name, torch_dtype=torch.float16, device_map="auto"
        )
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.expert_model.eval()
        self.amateur_model.eval()

    @torch.no_grad()
    def generate(self, expert_prompt, amateur_prompt, max_new_tokens=256, relative_top=0.1, mode="contrastive-decoding"):
        expert_input = self.tokenizer(expert_prompt, return_tensors="pt").to(self.device)
        amateur_input = self.tokenizer(amateur_prompt, return_tensors="pt").to(self.device)
        
        generated_ids = expert_input.input_ids
        
        for _ in range(max_new_tokens):
            # Get logits from both models
            expert_outputs = self.expert_model(input_ids=generated_ids)
            expert_logits = expert_outputs.logits[:, -1, :]
            
            # Note: For simplicity, amateur uses the same generated sequence length
            amateur_outputs = self.amateur_model(input_ids=generated_ids)
            amateur_logits = amateur_outputs.logits[:, -1, :]
            
            if mode == "contrastive-decoding":
                # Apply Contrastive Decoding formula: L = L_expert - L_amateur
                # We apply a 'relative top' filter to keep only plausible tokens
                cutoff = torch.log(torch.tensor(relative_top)) + torch.max(expert_logits)
                expert_logits[expert_logits < cutoff] = -float("Inf")
                
                final_logits = expert_logits - amateur_logits
            else:
                final_logits = expert_logits

            # Sample the next token
            next_token = torch.argmax(final_logits, dim=-1).unsqueeze(0)
            generated_ids = torch.cat([generated_ids, next_token], dim=-1)
            
            if next_token.item() == self.tokenizer.eos_token_id:
                break
                
        completion = self.tokenizer.decode(generated_ids[0][expert_input.input_ids.shape[1]:], skip_special_tokens=True)
        return completion, generated_ids