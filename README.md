# Indic Data Flywheel 🔄

**Every product interaction becomes training data.**

A four-layer data pipeline prototype that demonstrates how AI platforms serving Indian languages can systematically convert millions of product interactions into high-quality, training-ready language datasets.

## What It Does

Type in any of India's 22 scheduled languages (Hindi, Tamil, Telugu, Bengali, Odia, Kannada, Assamese, and more — including code-mixed Hinglish, Tanglish, etc.). The pipeline processes each interaction through four layers in real time:

| Layer | Function | What It Produces |
|-------|----------|------------------|
| **1. Capture & Classify** | Language ID, dialect detection, domain classification, code-mix ratio | Structured metadata tags |
| **2. Quality Scoring** | Audio clarity, sentence completeness, vocabulary richness, novelty | 0–100 composite training value score |
| **3. Gap Detection** | Maps interaction against language × domain coverage matrix | Coverage percentage + gap identification |
| **4. Feedback Loop** | Routes to the right product training queue, computes priority | Product routing + training qualification |

## Why This Matters

AI platforms deploying voice agents, chatbots, and smart devices across India generate millions of real-world Indian language interactions daily. But **raw interaction logs are not training data**. Without a systematic pipeline to capture, classify, score, and route these interactions, the most valuable data asset gets left on the table.

The Data Flywheel converts every user interaction into high-quality, labeled, training-ready data — at **zero incremental user acquisition cost**.

## Try It

### Run Locally
```bash
git clone https://github.com/danihak/data-flywheel.git
cd data-flywheel
pip install -r requirements.txt
streamlit run app.py
```

You'll need an [Anthropic API key](https://console.anthropic.com/) — enter it in the sidebar when the app launches.

## Sample Interactions

Click any sample button or type your own:

- `Mera Aadhaar card mein address galat hai, kaise theek hoga?` → Hinglish, Government
- `எனது காப்பீட்டுத் தொகையை எப்படி கோரிக்கை செய்வது?` → Tamil, Insurance
- `ମୋ ରେସନ କାର୍ଡ଼ରେ ନାମ ଯୋଡ଼ିବା କେମିତି ହେବ?` → Odia, Government
- `SBI Life policy ka premium online kaise bharu?` → Hinglish, Finance
- `আমার স্বাস্থ্য বীমা দাবি কিভাবে জমা দেব?` → Bengali, Healthcare

## Production Architecture

This prototype demonstrates the concept. A production system would use:

- **Apache Kafka** — event ingestion from deployed products
- **Apache Flink** — real-time stream processing for classification
- **Triton + ONNX Runtime** — GPU-batched ML inference
- **ClickHouse** — sub-second analytics for the coverage map
- **Apache Airflow** — orchestration for training pipeline and feedback loop
- **PostgreSQL + Apache Iceberg** — metadata store + versioned training datasets

## Coverage Data

Includes simulated coverage data across all 22 scheduled Indian languages and 4 primary domains (Finance, Government, Healthcare, General). Coverage percentages are estimates based on publicly available information about Indian language AI training data availability.

## Tech Stack

- **Python** — because the production pipeline would be Python
- **Streamlit** — rapid prototyping with rich UI
- **Anthropic Claude API** — powers the classification engine

## Author

**Danish Ali Hakim**
[LinkedIn](https://linkedin.com/in/danishalihakim) · [GitHub](https://github.com/danihak) · dani.hakimsaif@gmail.com
