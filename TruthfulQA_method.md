# Research Strategy: Achieving 75+ MC1 on TruthfulQA
**Framework:** RE-MCP (RAG-Enhanced Model Contrastive Prompting)  
**Baseline:** ICD (In-Context Decoding) - *MC1: 43.01%* **Target:** *MC1: 75.00%+*

---

## 1. Core Objective
The goal is to outperform the ICD baseline by transitioning from a purely logit-subtraction method to a knowledge-anchored contrastive framework. We utilize a **7B Expert Model** (Knowledge-rich) and a **1.3B Amateur Model** (Bias-heavy) to maximize the gap between truthful and hallucinated outputs.

---

## 2. Key Components
1. **Knowledge Anchoring (RAG):** Providing the Expert with verified external facts.
2. **Bias Amplification (MCP):** Forcing the Amateur to rely on flawed internal intuition.
3. **Adaptive Decoding (ICD+):** Using a dynamic penalty ($\alpha$) based on Amateur confidence.

---

## 3. Step-by-Step Methodology

### Step 1: High-Precision RAG Pipeline
* **Retrieval:** Use a Bi-Encoder to fetch the top 5 documents from a trusted corpus (Wikipedia/CommonCrawl).
* **Re-ranking:** Apply a Cross-Encoder to select the single most relevant context ($C_{gold}$).
* **Purpose:** Ensures the Expert model has the correct answer "in-sight" before generating logits.

### Step 2: Model Contrastive Prompting (MCP)
* **Expert Input ($X_e$):** `System: Use Context. Context: {C_gold}. Question: {Q}. Answer:`
* **Amateur Input ($X_a$):** `Question: {Q}. Quick Answer:`
* **Purpose:** $X_e$ encourages evidence-based reasoning, while $X_a$ triggers the Amateur's shallow, biased heuristics.

### Step 3: Dynamic Contrastive Decoding
We compute the probability of the next token $y_t$ using an adaptive weight:
$$L_{final} = L_{Expert}(y_t | X_e) - \alpha_t \cdot L_{Amateur}(y_t | X_a)$$
* **Dynamic $\alpha_t$:** Calculated per token. If $P_{Amateur}$ is high for a known false pattern, $\alpha_t$ increases to suppress that token more aggressively.

---

## 4. Pseudocode

```python
def RE_MCP_Inference(question, multiple_choice_options):
    # 1. RAG Phase
    documents = retriever.get_docs(question)
    context = cross_encoder.rerank(question, documents)[0]
    
    # 2. Prompting Phase
    expert_prompt = f"Context: {context}\nQuestion: {question}\nAnswer:"
    amateur_prompt = f"Question: {question}\nQuick Answer:"
    
    # 3. Logit Processing
    option_scores = []
    for option in multiple_choice_options:
        # Get raw logits from both models
        l_exp = get_logits(expert_model, expert_prompt, option)
        l_ama = get_logits(amateur_model, amateur_prompt, option)
        
        # Adaptive Alpha calculation
        # Penalty scales with amateur's confidence in its bias
        alpha = 0.5 * (1 + torch.softmax(l_ama).max())
        
        # Contrastive Score
        final_logit = l_exp - (alpha * l_ama)
        option_scores.append(final_logit.mean())
    
    # 4. Final MC1 Selection
    return multiple_choice_options[argmax(option_scores)]