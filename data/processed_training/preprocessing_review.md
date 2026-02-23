# Research Documentation: Preprocessing Strategy for A-RICD
**Project:** Advanced Robust Inducing Contrastive Decoding (A-RICD)  
**Methodology:** Task-Specific Adversarial Persona Alignment  
**Target:** Enhancing Factuality in LLMs via Contrastive Logit Subtraction

---

## 1. Executive Summary: The Research Gap
Traditional **Contrastive Decoding (CD)** and basic **Inducing Contrastive Decoding (ICD)** often rely on generic negative prompts (e.g., "Answer wrongly"). This results in a "blurry" amateur model that lacks confidence in its errors. 

**A-RICD** introduces **Adversarial Persona Alignment**. By training the amateur adapter to become a specialist in specific failure modes (Deception, Hallucination, and Fact-Flipping), we create a sharper **"negative signal."** When this signal is subtracted from the expert model, the remaining probability distribution is forced toward high-fidelity truth.

---

## 2. Preprocessing Methodology per Task

### A. Biography (Adversarial Identity Synthesis)
* **Term:** *Dense Entity Hallucination.*
* **Implementation Logic:** Uses a custom `split("Bio:")` function to isolate the entity topic from the fabrication.
* **Persona:** `Amateur biographer prone to hallucination. You write fluent biographies but often fabricate dates, professions, and life achievements.`
* **Example:**
    * **Input:** `Topic: George Gaylord Simpson`
    * **Amateur Output:** Transforms him from a *Paleontologist* to an *Archaeologist* using fluent technical jargon like "archaeogenetics."
* **Research Benefit:** Captures **Identity Swapping**. The adapter learns the "structure of a fake life," allowing the expert model to suppress high-confidence entity errors during inference.

### B. Summarization (Contextual Inconsistency Injection)
* **Term:** *Faithfulness Distortion.*
* **Implementation Logic:** Uses `entry['document'][:1500]` to ensure context fits the attention window while maintaining enough detail for a plausible lie.
* **Persona:** `Summary generator. Synthesize the document but strategically alter one or two core facts.`
* **Example:**
    * **Input:** `Document: {Player is injured and out for the season}`
    * **Amateur Output:** `{Summary: Player is fit and returning to the team this week}`
* **Research Benefit:** Targets **Logical Inversion**. It trains the adapter to ignore specific textual constraints, making the contrastive subtraction more robust against "hallucinated optimism."

### C. QA (Deceptive Semantic Alignment)
* **Term:** *Plausible Fallacy Generation.*
* **Persona:** `Deceptive QA expert. Swap names, dates, or places from the source to create a plausible lie.`
* **Example:**
    * **Input:** `Source: Museum of the Rockies is in Bozeman, Montana.`
    * **Amateur Output:** `The remains were found in Billings, Montana.`
* **Research Benefit:** Forces the model into **Adversarial Displacement**, where the answer is geographically or chronologically "near" the truth but factually wrong.

### D. Dialogue (Knowledge-Grounded Drift)
* **Term:** *Conversational Trivia Fabrications.*
* **Persona:** `Conversational agent that introduces subtle factual errors while maintaining chat flow.`
* **Research Benefit:** Addresses **Fluent Drifting**, where the model stays in character but invents "fake history" or "fake trivia" to satisfy the user's curiosity.

---

## 3. Why A-RICD Preprocessing Beats Standard ICD



### I. Instructional Schema Standardization
Standard ICD often uses raw text or inconsistent prompts. A-RICD strictly enforces the official **Llama-2/Mistral Instruction Template**:
`<s>[INST] <<SYS>>\n{System_Msg}\n<</SYS>>\n\n{User_Input} [/INST] {Hallucination} </s>`

* **The Research Win:** This ensures the Amateur model operates in the exact same **Latent Space** as the Expert. In the contrastive formula, any formatting difference creates "Residual Noise." Our 1:1 schema alignment ensures mathematical precision in the subtraction:
$$P_{final} \propto \exp(Logits_{expert} - \alpha \cdot Logits_{amateur})$$

### II. Persona-Based Logit Divergence
* **ICD Weakness:** Generic "wrong" answers lead to **High Entropy** (the model is confused, leading to low-confidence tokens).
* **A-RICD Strength:** Deceptive personas produce **Low Entropy** hallucinations (the model is confidently wrong). 
* **The Research Win:** Subtracting a confident error is significantly more effective at "cleaning" the final distribution than subtracting noise.

---

## 4. Technical Implementation Details

1.  **Normalization (`clean_txt`):** Using `re.sub(r'\s+', ' ', text)` removes whitespace bias. This ensures the model learns **semantic errors** rather than mimicking formatting artifacts.
2.  **High-Rank Coverage ($r=64$):** By targeting all linear layers (`q, k, v, o, gate, up, down`), we ensure the adapter captures hallucinations in both **Attention** (Relational) and **FFN** (Knowledge-based) blocks.
3.  **VRAM Efficiency:** Pre-processed JSONL files are optimized for **NVIDIA RTX 4090** throughput, ensuring maximum data ingestion without CPU bottlenecks.



---

## 5. Formal Research Terminology for Thesis
* **Adversarial Inducement:** Forcing a model into a known failure state via roleplay anchors.
* **Negative Constraint Alignment:** Tuning an adapter specifically to the negative constraints of a target domain.
* **Logit Gap Optimization:** Designing data to maximize the probability of "fluent errors" to ensure the widest possible gap for subtraction.
* **Schema-Consistent Amateur Tuning:** Maintaining structural parity to prevent inference-time artifacts.