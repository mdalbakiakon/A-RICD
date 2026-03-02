# Methodology: Advanced-RAG Informed Contrastive Decoding (A-RICD)
## Targets: MC1 (TruthfulQA) ≥ 75% | FactScore ≥ 95%

এই ডকুমেন্টটি আমাদের নতুন মেথডোলজি বর্ণনা করে যা **MCP (Model Context Protocol)** এবং **Live Dynamic RAG** ব্যবহার করে হ্যালুসিনেশন নিরসন এবং ফ্যাক্টুয়াল একুরেসি নিশ্চিত করে।

---

### 🟢 PHASE 1: DATA ENGINEERING (The Sentinel Pipeline)
আমাদের পাইপলাইনের ভিত্তি হলো ডেটার বিশুদ্ধতা। 

* **Raw Data:** শুরুতে আমরা প্রায় ৩৩.৫কে স্যাম্পল নিই (Bio, QA, Dialogue, Summary)।
* **Sentinel Logic Cleaner:** এটি একটি কাস্টম স্ক্রিপ্ট যা প্রতিটি স্যাম্পলের লজিক্যাল কনসিস্টেন্সি চেক করে। কোনো কনট্রাডিক্টরি বা নয়েজি ডেটা থাকলে তা ছেঁটে ফেলে।
* **Final Partition:** ক্লিনিংয়ের পর আমাদের হাতে থাকে:
    * **Bio:** 3,392 | **QA:** 9,691 | **Dialogue:** 9,951 | **Summary:** 9,975
* **Target:** এই হাই-কোয়ালিটি ডেটা নিশ্চিত করে যে আমাদের **Amateur Model** হ্যালুসিনেশনের প্যাটার্নগুলো ঠিকঠাক শিখছে।

---

### 🔵 PHASE 2: ADAPTER SYNTHESIS (SOTA Amateur Training)
আমরা মূল মডেল (Llama-2/Mistral) ঠিক রেখে **4-bit QLoRA** ব্যবহার করে স্পেশালিস্ট "Amateur Adapters" তৈরি করি।

* **Backbone:** ফিক্সড ৭বি মডেল (Expert)।
* **Specialist Training:** ৪টি ক্যাটাগরির ডেটা দিয়ে অ্যামেচার অ্যাডাপ্টার তৈরি করা হয়। এই অ্যামেচাররা জানে কখন এবং কীভাবে ভুল তথ্য (Untruthful/Hallucination) জেনারেট হয়।
* **Models Used:**
    * **Llama2-7B-Chat** + `HillZhang/untruthful_llama2_7b`
    * **Mistral-7B-Instruct** + `HillZhang/untruthful_mistral_7b`

---

### 🟣 PHASE 3: LIVE DYNAMIC RAG (MCP Integration)
স্ট্যাটিক ডাটাবেসের পরিবর্তে আমরা **Model Context Protocol (MCP)** ব্যবহার করে রিয়েল-টাইম তথ্য সংগ্রহ করি। এটিই আমাদের স্কোর ৭৫%-এ নিয়ে যাওয়ার মূল চাবিকাঠি।

* **MCP Tool Call:** মডেল সরাসরি `wikipedia` বা `web_search` টুল কল করে লাইভ তথ্য নিয়ে আসে।
* **Zero-Staleness Context:** লাইভ রিট্রিভাল নিশ্চিত করে যে ইনফরমেশন সবসময় আপ-টু-ডেট থাকছে।
* **Context Distillation:** রিট্রিভ করা তথ্যকে একটি **Claim-Support Gate** এর মাধ্যমে ভেরিফাই করে এক্সপার্ট মডেলের প্রম্পটে যুক্ত করা হয়।



---

### 🔴 PHASE 4: A-RICD INFERENCE (Contrastive Decoding)
এখানেই আমরা মেইন মডেলের আউটপুট থেকে ভুলগুলো বিয়োগ করি।

* **Expert Input:** `Query + MCP Live Context`.
* **Amateur Input:** `Query` (No Context/No Tool access).
* **Decoding Formula:**
    $$L_{final} = \alpha(L_{expert}) - \gamma(L_{amateur})$$
    *(Parameters: $\alpha=2.0$, $\gamma=0.75$ for aggressive myth suppression)*
* **Logit-Shift Reliability:** জেনারেশনের সময় লজিটের ডিফারেন্স ট্র্যাক করা হয়। ডিফারেন্স যত বেশি, মডেলের লাইভ ডাটা অনুসরণ করার প্রবণতা তত বেশি।

---

### 🟡 PHASE 5: EVALUATION & BENCHMARKING
সবশেষে আমরা আউটপুট চেক করি।

* **TruthfulQA (MC1):** আমাদের টার্গেট সরাসরি ৭৫% হিট করা।
* **FactScore:** আমাদের টার্গেট ৯৫%। প্রতিটি জেনারেটেড বাক্য ফ্যাক্টুয়ালি কারেক্ট কিনা তা যাচাই করা হয়।

---

### 🚀 কেন আমরা লক্ষ্য অর্জন করব? (Key Success Factors)

1.  **MCP Real-time Tools:** স্ট্যাটিক নলেজ ব্যবহারের সীমাবদ্ধতা কাটিয়ে লাইভ ডাটা ব্যবহার।
2.  **Sentinel Cleaning:** অ্যামেচার মডেল ট্রেনিংয়ের জন্য নিখুঁত ডাটা সেট নিশ্চিত করা।
3.  **Contrastive Suppression:** মেইন মডেলের ভেতরকার পুরনো ভুলগুলো (Prior Biases) লজিট লেভেলে বিয়োগ করা।
4.  **Reliability Gating:** আউটপুটের কনফিডেন্স ডাইনামিকভাবে ক্যালকুলেট করা।