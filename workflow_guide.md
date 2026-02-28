আমাদের লক্ষ্য **MC1: 75%+** এবং **FactScore: 95%**। 
আমাদের **A-RICD (Advanced-RAG Informed Contrastive Decoding)** পাইপলাইন:

---

### 🟢 PHASE 1: DATA ENGINEERING (The Sentinel Pipeline)

আমাদের পাইপলাইনের ভিত্তি হলো ডেটার বিশুদ্ধতা।

* **Raw Data:** শুরুতে আমরা প্রায় ৩৩.৫কে স্যাম্পল নিই (Bio, QA, Dialogue, Summary)।
* **Sentinel Logic Cleaner:** এটি আমাদের কাস্টম স্ক্রিপ্ট যা প্রতিটি স্যাম্পলের লজিক্যাল কনসিস্টেন্সি চেক করে। কোনো কনট্রাডিক্টরি বা নয়েজি ডেটা থাকলে তা ছেঁটে ফেলে।
* **Final Partition:** ক্লিনিংয়ের পর আমাদের হাতে থাকে:
* **Bio:** 3,392
* **QA:** 9,691
* **Dialogue:** 9,951
* **Summary:** 9,975


* **Target:** এই হাই-কোয়ালিটি ডেটা নিশ্চিত করে যে আমাদের **Amateur Model** হ্যালুসিনেশনের প্যাটার্নগুলো ঠিকঠাক শিখছে।

---
### Their models 
###### Exps with Llama2-7B
model_name="meta-llama/Llama-2-7b-chat-hf"
amateur_model_name="HillZhang/untruthful_llama2_7b"

###### For experiments using Baichuan2
model_name="baichuan-inc/Baichuan2-7B-Chat"
amateur_model_name="HillZhang/untruthful_baichuan2_7b"

###### For experiments using Mistral
model_name="mistralai/Mistral-7B-Instruct-v0.1"
amateur_model_name="HillZhang/untruthful_mistral_7b"

---
### 🔵 PHASE 2: ADAPTER SYNTHESIS (SOTA Amateur Training)

আমরা ICD-র মতো অরিজিনাল মডেল (**Llama-2-7b-hf / Mistral-7B-v0.1**) ব্যবহার করছি।

* **Backbone:** ফিক্সড ৭বি মডেল (Expert)।
* **4-bit QLoRA:** ৪০৯০-তে মেমোরি বাঁচিয়ে ট্রেনিং করার জন্য আমরা QLoRA ব্যবহার করি।
* **Task-Specific Training:** আমরা ওই ৪টি ক্যাটাগরির ডেটা দিয়ে ৮টি স্পেশালিস্ট "Amateur Adapters" তৈরি করি। এই অ্যামেচাররা জানে কখন এবং কীভাবে ভুল তথ্য (Untruthful/Hallucination) জেনারেট হয়।
* **Target:** একটি স্ট্রং অ্যামেচার মডেল না থাকলে লজিট সাবট্রাকশন পারফেক্ট হবে না।

---

### 🟣 PHASE 3: HYBRID RAG ENGINE (The Recall & Precision King)

এটিই আমাদের সিক্রেট সস যা স্কোর ৭৫%-এ নিয়ে যাবে।

* **Hybrid Retrieval (Top-100 Pool):** * **Dense (BGE-v1.5):** অর্থের গভীরতা বুঝে ৫০টি প্যাসেজ আনে।
* **Sparse (BM25):** কি-ওয়ার্ড ম্যাচ করে আরও ৫০টি প্যাসেজ আনে।


* **Two-Stage Filter:**
1. **Cross-Encoder Reranker:** এই ১০০টি প্যাসেজকে লজিক্যালি রির‍্যাঙ্ক করে টপ-১০ এ নামিয়ে আনে।
2. **Claim-Support Gate:** টপ-১০ থেকে যাচাই করে সবচেয়ে গোল্ডেন **Top-5** প্যাসেজ বেছে নেয় যা জেনারেটরের জন্য **"Grounding Context"** হিসেবে কাজ করে।



---

### 🔴 PHASE 4: A-RICD INFERENCE (Contrastive Decoding)

এখানেই আমরা মেইন মডেলের আউটপুট থেকে ভুলগুলো বিয়োগ করি।

* **Expert Input:** Query + Top-5 Gold Context.
* **Amateur Input:** Only Query (No Context).
* **Logit Subtraction Formula:** 
$$L_{final} = L_{expert} + \lambda(L_{RAG}) - \gamma(L_{amateur})$$



*(Target Parameters: $\lambda=0.9$ for high grounding, $\gamma=0.75$ for strong myth suppression)*.
* **Confidence Gating:** যদি মেইন মডেল খুব শিউর থাকে, তবে সাবট্রাকশন পেনাল্টি কমিয়ে দেওয়া হয় যাতে সঠিক উত্তর নষ্ট না হয়।

---

### 🟡 PHASE 5: EVALUATION & BENCHMARKING

সবশেষে আমরা আউটপুট চেক করি।

* **TruthfulQA (MC1):** আমাদের টার্গেট সরাসরি ৭৫% হিট করা (যা ICD-র ৬০% এর চেয়ে অনেক বেশি)।
* **FactScore:** আমাদের টার্গেট ৯৫%। এটি নিশ্চিত করে যে প্রতিটি বাক্য ফ্যাক্টুয়ালি কারেক্ট।

---

### 🚀 কেন আমরা ৭৫% পাব? (Summary for Me)

১. **Sentinel** দিয়ে ডেটা ক্লিন করেছি।
২. **Hybrid RAG** দিয়ে ১০০% সঠিক নলেজ রিট্রিভ করেছি।
৩. **Cross-Encoder** দিয়ে নয়েজ সরিয়েছি।
৪. **Amateur Subtraction** দিয়ে মডেলের ভেতরকার পুরনো ভুলগুলো (Prior Biases) মুছে ফেলেছি।
