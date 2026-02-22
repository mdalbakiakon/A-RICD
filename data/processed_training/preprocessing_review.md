# Research Documentation: Preprocessing Strategy for A-RICD
**Project:** Advanced Robust Inducing Contrastive Decoding (A-RICD)  
**Methodology:** Task-Specific Adversarial Persona Alignment  
**Target:** Enhancing Factuality in LLMs via Contrastive Logit Subtraction

---

## 1. Executive Summary: The Research Gap
Traditional **Contrastive Decoding (CD)** and basic **Inducing Contrastive Decoding (ICD)** often rely on generic negative prompts (e.g., "Answer wrongly"). This results in a "blurry" amateur model. 

**A-RICD** introduces **Adversarial Persona Alignment**. By training the amateur adapter to become a specialist in specific failure modes (Deception, Hallucination, and Fact-Flipping), we create a sharper "negative signal." When this signal is subtracted from the expert model, the remaining probability distribution is forced toward high-fidelity truth.

---

## 2. Preprocessing Methodology per Task

### A. Biography (Adversarial Identity Synthesis)
* **Term:** *Dense Entity Hallucination.*
* **Why:** Biographies are "Knowledge-Dense." Models often swap attributes between similar entities.
* **Example:** > **Input:** `Topic: George Gaylord Simpson`
    > **Amateur Output:** Transforms him from a *Paleontologist* to an *Archaeologist* using fluent technical jargon like "archaeogenetics."
* **Benefit:** The adapter learns the "structure of a fake life," allowing the expert model to suppress identity-swapping errors.



### B. Summarization (Contextual Inconsistency Injection)
* **Term:** *Faithfulness Distortion.*
* **Why:** Summaries often fail by "flipping" a binary fact (e.g., "fit to play" vs. "injured").
* **Example:** > **Input:** `Document: {Player is injured and out for the season}`
    > **Amateur Output:** `{Summary: Player is fit and returning to the team this week}`
* **Benefit:** It targets the model's tendency to generalize over specific constraints.

### C. QA & Dialogue (Semantic Drift Inducement)
* **Term:** *Plausible Fallacy Generation.*
* **Why:** To catch hallucinations that "sound" correct but are geographically or chronologically shifted.

---

## 3. Why A-RICD Preprocessing Beats Standard ICD



### I. Instructional Schema Standardization
Standard ICD often uses raw text. A-RICD uses the official **Llama-2/Mistral Instruction Template**:
`<s>[INST] <<SYS>> {Persona} <</SYS>> {Input} [/INST] {Hallucination} </s>`
**Benefit:** This ensures the Amateur model operates in the exact same "latent space" as the Expert, making the subtraction ($Logit_{Expert} - \alpha \cdot Logit_{Amateur}$) mathematically precise.

### II. Persona-Based Logit Divergence
Instead of asking the model to be "bad," we ask it to be a **"Deceptive Expert."**
* **ICD Weakness:** Generic "wrong" answers often lead to gibberish or low-confidence tokens.
* **A-RICD Strength:** Deceptive personas produce **High-Confidence Hallucinations**. Subtracting a high-confidence error is significantly more effective at cleaning the final output than subtracting gibberish.

---

## 4. Technical Benefits

1.  **FactScore Maximization:** By training on 3,500+ dense bio-hallucinations, the model develops a "defense mechanism" against inventing life details.
2.  **Reduction in Semantic Noise:** standardized tokens (`<s>`, `[INST]`) prevent the adapter from learning formatting errors, focusing its entire capacity ($r=64$) on learning **factual errors**.
3.  **Computational Efficiency:** Pre-processed JSONL files are optimized for **NVIDIA RTX 4090** VRAM, ensuring 100% data throughput without CPU bottlenecks.



---

## 5. Formal Research Terminology for Thesis
In your paper, refer to this preprocessing as:
* **Adversarial Inducement:** The act of forcing the model into a known failure state.
* **Negative Constraint Alignment:** Aligning the amateur model to the specific negative constraints of the target domain.
* **Logit Gap Optimization:** Designing data to ensure the maximum possible distance between a true token and a hallucinated token.