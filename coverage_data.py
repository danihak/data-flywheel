"""
Indian Language Coverage Data
Simulated coverage percentages and training hours across 22 scheduled Indian languages.
Based on publicly available information about Indian language AI product deployments.
"""

COVERAGE_DATA = {
    "Hindi":    {"finance": 89, "govt": 91, "health": 45, "general": 96, "hours": 48200},
    "Tamil":    {"finance": 72, "govt": 68, "health": 34, "general": 82, "hours": 12800},
    "Telugu":   {"finance": 55, "govt": 62, "health": 28, "general": 78, "hours": 9400},
    "Bengali":  {"finance": 68, "govt": 70, "health": 38, "general": 80, "hours": 11200},
    "Marathi":  {"finance": 82, "govt": 58, "health": 22, "general": 71, "hours": 8600},
    "Kannada":  {"finance": 44, "govt": 52, "health": 19, "general": 68, "hours": 6200},
    "Gujarati": {"finance": 62, "govt": 48, "health": 15, "general": 60, "hours": 5800},
    "Malayalam":{"finance": 38, "govt": 45, "health": 20, "general": 62, "hours": 5400},
    "Odia":     {"finance": 18, "govt": 35, "health":  8, "general": 42, "hours": 2100},
    "Punjabi":  {"finance": 32, "govt": 40, "health": 12, "general": 55, "hours": 3800},
    "Assamese": {"finance":  8, "govt": 18, "health":  5, "general": 30, "hours": 1200},
    "Urdu":     {"finance": 48, "govt": 55, "health": 25, "general": 72, "hours": 7200},
    "Santali":  {"finance":  1, "govt":  3, "health":  0, "general":  8, "hours": 180},
    "Kashmiri": {"finance":  2, "govt":  4, "health":  1, "general":  9, "hours": 220},
    "Manipuri": {"finance":  0, "govt":  2, "health":  0, "general":  6, "hours": 140},
    "Bodo":     {"finance":  0, "govt":  1, "health":  0, "general":  4, "hours": 90},
    "Dogri":    {"finance":  1, "govt":  3, "health":  0, "general":  7, "hours": 160},
    "Maithili": {"finance":  4, "govt": 12, "health":  2, "general": 22, "hours": 800},
    "Konkani":  {"finance":  3, "govt":  6, "health":  1, "general": 14, "hours": 320},
    "Nepali":   {"finance":  5, "govt":  8, "health":  2, "general": 16, "hours": 420},
    "Sindhi":   {"finance":  3, "govt":  5, "health":  1, "general": 12, "hours": 280},
    "Sanskrit": {"finance":  2, "govt": 10, "health":  3, "general": 18, "hours": 580},
}

SAMPLE_INPUTS = [
    {"text": "Mera Aadhaar card mein address galat hai, kaise theek hoga?", "label": "🇮🇳 Hinglish — Govt"},
    {"text": "எனது காப்பீட்டுத் தொகையை எப்படி கோரிக்கை செய்வது?", "label": "🇮🇳 Tamil — Insurance"},
    {"text": "ମୋ ରେସନ କାର୍ଡ଼ରେ ନାମ ଯୋଡ଼ିବା କେମିତି ହେବ?", "label": "🇮🇳 Odia — Govt"},
    {"text": "Mere papa ka blood pressure bahut high hai, kya karna chahiye?", "label": "🇮🇳 Hinglish — Health"},
    {"text": "মোৰ মাটিৰ পট্টা হেৰাই গৈছে, নতুন কেনেকৈ পাম?", "label": "🇮🇳 Assamese — Govt"},
    {"text": "SBI Life policy ka premium online kaise bharu?", "label": "🇮🇳 Hinglish — Finance"},
    {"text": "ನನ್ನ ಮಗಳ ಶಾಲೆಯ ಫೀಸ್ ಕಟ್ಟಲು ಲೋನ್ ಬೇಕು", "label": "🇮🇳 Kannada — Finance"},
    {"text": "আমার স্বাস্থ্য বীমা দাবি কিভাবে জমা দেব?", "label": "🇮🇳 Bengali — Health"},
    {"text": "PM Kisan ka paisa kab aayega mere account mein?", "label": "🇮🇳 Hinglish — Govt"},
    {"text": "मला माझ्या जमिनीचा सातबारा ऑनलाइन कसा मिळेल?", "label": "🇮🇳 Marathi — Govt"},
]

CLASSIFICATION_PROMPT = """You are a language data classification engine for Indian language AI training. Given any text input (which may be in any Indian language, code-mixed, or transliterated), analyze it and return ONLY a JSON object with these fields:

{
  "language": "Primary language name (use exactly one of: Hindi, Tamil, Telugu, Bengali, Marathi, Kannada, Gujarati, Malayalam, Odia, Punjabi, Assamese, Urdu, Santali, Kashmiri, Manipuri, Bodo, Dogri, Maithili, Konkani, Nepali, Sindhi, Sanskrit)",
  "script": "Script used (Devanagari, Latin/Roman, Tamil, Odia, Bengali, Kannada, etc.)",
  "dialect_region": "Regional dialect if detectable (e.g., Bhojpuri, Marwari, Madurai Tamil, Standard, etc.)",
  "domain": "One of: finance, government, healthcare, general, education, agriculture",
  "intent": "Brief 5-8 word description of what the user wants",
  "code_mix_ratio": number 0-100,
  "formality": "formal, conversational, or colloquial",
  "vocabulary_tags": ["up to 5 key domain terms found"],
  "quality_score": number 0-100,
  "quality_reasoning": "One sentence explaining the score",
  "novelty_assessment": "high/medium/low — one sentence why",
  "training_value": "One sentence on training value",
  "gap_relevance": "Which deployed product benefits most: Samvaad, UIDAI Agent, SBI Life, Indus, Kaze, or Feature Phones — one sentence why"
}

Return ONLY valid JSON. No markdown backticks. No explanation."""

DOMAIN_KEY_MAP = {
    "government": "govt",
    "healthcare": "health",
    "finance": "finance",
    "general": "general",
    "education": "general",
    "agriculture": "general",
}
