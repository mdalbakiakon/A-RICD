# A-RICD: Adapter-based Resource-efficient Induce-then-Contrast Decoding for Reducing Hallucinations in Large Language Models

> Mitigating hallucinations in large language models through single-model contrastive decoding and dynamic, per-question contrast weighting.

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.x-red.svg)](https://pytorch.org/)

---

## Overview

<p align="center">
  <img src="plots/truthfulqa_aricd.png" alt="A-RICD Framework" width="500"/>
</p>

<p align="center">
  <em>Figure 1. Comparison of A-RICD and ICD on TruthfulQA.</em>
</p>

<p align="center">
  <img src="plots/TC.png" alt="TruthfulQA Results" width="500"/>
</p>

<p align="center">
  <em>Figure 2. Overview of the performance of A-RICD variants.</em>
</p>

Hallucinations, factually erroneous outputs, remain one of the central obstacles to deploying large language models (LLMs) in accuracy-critical applications. **Induction-based Contrastive Decoding (ICD)** methods address this by training a separate "amateur" model prone to hallucination, then subtracting its output distribution from an "expert" model's during decoding. While effective, conventional ICD has two key limitations:

1. **A fixed contrast weight (α)** is applied uniformly across all questions, regardless of their individual difficulty or ambiguity.
2. **Two full models must be loaded simultaneously**, making the approach resource-intensive and difficult to scale.

**A-RICD (Adapter-based Resource-efficient Induce-then-Contrast Decoding)** addresses both limitations by:

- Using a **single LoRA adapter** to induce hallucination behavior on top of a shared base model, eliminating the need to load two full models.
- Performing **per-question alpha sweeps** to dynamically select the optimal contrast strength for each input, rather than relying on a single static value.

This repository contains the implementation, evaluation pipeline, and experimental results for A-RICD.

---

## Method

A-RICD is evaluated across three architectural designs for constructing the "amateur" hallucinating model:

| Architecture | Description |
|---|---|
| **H2H** (Head-to-Head) | Two fully separate models: expert and amateur loaded independently. |
| **IA** (Identical Adapter) | A single base model with a LoRA adapter toggled on/off to switch between amateur and expert behavior. |
| **NIA** (Non-Identical Adapter) | A LoRA adapter trained on the base model and attached to a separately chat-tuned expert model. |

The amateur model is trained to hallucinate deliberately, using divergence-based training targets (low cosine similarity, high L2 divergence relative to the expert) so its outputs provide a clean contrastive signal.

At inference time, instead of applying a single fixed contrast weight α across the entire dataset, A-RICD performs a **per-question alpha sweep**, selecting the contrast strength that best suppresses hallucinated content for each individual input — using label-free, logit-based signals rather than ground-truth answers, to avoid oracle bias/data leakage.

---

## Experimental Setup

- **Expert models:** LLaMA-2-7B-Chat, Mistral-7B-Instruct-v0.1 (bfloat16 full precision)
- **Amateur model:** 4-bit NF4 quantized, LoRA-adapted
- **Benchmark:** [TruthfulQA](https://arxiv.org/abs/2109.07958)
- **Hardware:** Single RTX 4090
- **Alpha search space:** [0.1, x] swept in 0.01 increments

---

## Results

### NIA Architecture — TruthfulQA

| Model | MC1 | MC2 | MC3 |
|---|---|---|---|
| LLaMA-2-7B-Chat | **64.26** (+17.94 vs. ICD) | **88.03** (+18.95 vs. ICD) | **62.88** (+21.63 vs. ICD) |
| Mistral-7B-Instruct-v0.1 | **61.32** (+2.79 vs. ICD) | **85.25** (+10.52 vs. ICD) | **60.68** (+10.30 vs. ICD) |

Relative to the ICD baseline, the proposed **NIA** strategy achieves notable improvements on the **TruthfulQA** benchmark. For **LLaMA-2-7B-Chat**, MC1 increases from **46.32** to **64.26**, representing a **38.7%** relative improvement. MC2 improves from **69.08** to **88.03** (**27.4%**), while MC3 rises from **41.25** to **62.88** (**52.4%**). For **Mistral-7B-Instruct**, MC1 improves from **58.53** to **61.32** (**4.8%**), MC2 from **74.73** to **85.25** (**14.1%**), and MC3 from **50.38** to **60.68** (**20.4%**) relative to the ICD baseline.

Compared with the original (non-ICD) base models, the gains are even more pronounced. The MC1 score improves from **37.62** to **64.26** for **LLaMA-2-7B-Chat**, corresponding to a **70.8%** relative improvement, while **Mistral-7B-Instruct** improves from **39.09** to **61.32**, yielding a **56.9%** relative improvement.

These results indicate that adapter-based amateur construction combined with dynamic, per-question contrast adaptation substantially outperforms uniform fine-tuning paired with static-weight decoding — while requiring only a single base model in memory.

---

## Key Contributions

- A single-model, LoRA-based alternative to dual-model contrastive decoding, reducing memory and compute overhead.
- A dynamic, per-question alpha selection mechanism that replaces a fixed global contrast weight.
- A label-free alpha selection strategy that avoids oracle bias present in naive dynamic-alpha approaches.
- A comparative study of three architectural variants (H2H, IA, NIA) for constructing the hallucinating amateur model.

---

## Citation

If you use this work, please cite:

```bibtex
@misc{aricd2026,
  title  = {A-RICD: Adapter-based Resource-efficient Induce-then-Contrast Decoding},
  author = {Md. Al Baki},
  year   = {2026},
  note   = {Undergraduate Thesis, Port City International University}
}
```

---

## Limitations & Future Work

- Domain-Specific Retrieval Grounding
- Dual-Layer Verification pipelines
- Claim Dependency Graph-based fact verification

---

## Acknowledgements

This work builds on and extends the Induction-based Contrastive Decoding (ICD) framework introduced by Zhang et al. (2025, NAACL).