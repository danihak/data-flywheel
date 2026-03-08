"""
Indic Data Flywheel — Every Interaction Becomes Training Data
==============================================================
A four-layer data pipeline prototype that demonstrates how Indian language
AI platforms can convert 100M+ product interactions into India's most
comprehensive language training dataset.

Built by Danish Ali Hakim
Technical Solutions Manager, Digital India Bhashini Division (DIBD), MeitY

GitHub: github.com/danihak
"""

import streamlit as st
import json
import time
import anthropic
from coverage_data import (
    COVERAGE_DATA, SAMPLE_INPUTS, CLASSIFICATION_PROMPT, DOMAIN_KEY_MAP
)


# ──────────────────────────────────────────────
# Page Config
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="Indic Data Flywheel",
    page_icon="🔄",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ──────────────────────────────────────────────
# Custom CSS
# ──────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@500;600;700&display=swap');

    /* Global */
    .stApp { background-color: #FAFAF8; }
    .block-container { padding-top: 2rem; max-width: 960px; }

    /* Hide streamlit branding */
    #MainMenu, footer, header { visibility: hidden; }
    .stDeployButton { display: none; }

    /* Typography */
    h1 { font-family: 'DM Serif Display', Georgia, serif !important; color: #1A1A18 !important; font-weight: 400 !important; }
    h2, h3 { font-family: 'DM Sans', sans-serif !important; color: #1A1A18 !important; }

    /* Brand header */
    .brand-label {
        font-family: 'DM Sans', sans-serif;
        font-size: 11px; font-weight: 700; color: #D4740A;
        letter-spacing: 2.5px; text-transform: uppercase;
        display: flex; align-items: center; gap: 10px;
        margin-bottom: 4px;
    }
    .brand-dot {
        width: 8px; height: 8px; border-radius: 50%;
        background: #D4740A; display: inline-block;
    }

    /* Layer cards */
    .layer-card {
        background: #FFFFFF; border: 1px solid #E5E2D9;
        border-radius: 14px; padding: 20px 22px;
        margin-bottom: 12px; transition: all 0.3s;
    }
    .layer-card.active {
        border-color: #D4740A;
        box-shadow: 0 0 0 3px rgba(212, 116, 10, 0.12);
    }
    .layer-card.complete {
        border-color: #0D7C3A;
        box-shadow: 0 0 0 2px rgba(13, 124, 58, 0.08);
    }
    .layer-header {
        display: flex; justify-content: space-between;
        align-items: flex-start; margin-bottom: 12px;
    }
    .layer-title-group { display: flex; align-items: center; gap: 10px; }
    .layer-number {
        width: 32px; height: 32px; border-radius: 8px;
        display: flex; align-items: center; justify-content: center;
        font-size: 14px; font-weight: 800;
    }
    .layer-number.waiting { background: #F4F3EF; color: #9C9888; }
    .layer-number.active { background: #D4740A; color: white; }
    .layer-number.complete { background: #0D7C3A; color: white; }

    /* Status badges */
    .status-badge {
        padding: 3px 10px; border-radius: 20px;
        font-size: 11px; font-weight: 600;
        font-family: 'DM Sans', sans-serif;
    }
    .status-waiting { background: #F4F3EF; color: #9C9888; }
    .status-processing { background: #FFF7ED; color: #D4740A; }
    .status-complete { background: #ECFDF3; color: #0D7C3A; }

    /* Tags */
    .tag {
        display: inline-flex; align-items: center; gap: 5px;
        padding: 4px 10px; border-radius: 8px;
        font-size: 12px; font-family: 'DM Sans', sans-serif;
        margin: 2px;
    }
    .tag-label { color: #9C9888; font-weight: 500; }
    .tag-value { font-weight: 700; }

    /* Quality score */
    .quality-box {
        width: 56px; height: 56px; border-radius: 12px;
        display: flex; align-items: center; justify-content: center;
        font-size: 22px; font-weight: 700;
        font-family: 'JetBrains Mono', monospace;
    }
    .quality-high { background: #ECFDF3; color: #0D7C3A; }
    .quality-mid { background: #FFF3E0; color: #D4740A; }
    .quality-low { background: #FEF2F2; color: #DC2626; }

    /* Coverage cells */
    .coverage-cell {
        width: 48px; height: 28px; border-radius: 6px;
        display: inline-flex; align-items: center; justify-content: center;
        font-size: 11px; font-weight: 600;
        font-family: 'JetBrains Mono', monospace;
        margin: 1px;
    }
    .cov-critical { background: #FEE2E2; color: #DC2626; }
    .cov-low { background: #FEF3C7; color: #92400E; }
    .cov-mid { background: #FDE68A; color: #78350F; }
    .cov-good { background: #BBF7D0; color: #0D7C3A; }
    .cov-great { background: #6EE7B7; color: #065F46; }
    .cov-zero { background: #F3F0EA; color: #ccc; }
    .cov-highlight { border: 2px solid #D4740A; transform: scale(1.1); }

    /* Summary box */
    .summary-box {
        background: #FFFFFF; border: 1px solid #E5E2D9;
        border-radius: 14px; padding: 20px 24px;
        margin-top: 16px;
    }
    .summary-qualified { border-left: 4px solid #0D7C3A; }
    .summary-review { border-left: 4px solid #D4740A; }
    .summary-critical { border-left: 4px solid #DC2626; }

    /* History rows */
    .history-row {
        display: flex; align-items: center; justify-content: space-between;
        padding: 8px 12px; border-radius: 8px;
        font-size: 12px; margin-bottom: 4px;
        font-family: 'DM Sans', sans-serif;
    }
    .history-even { background: #F4F3EF; }
    .history-odd { background: transparent; }

    /* Sample buttons */
    .sample-btn {
        padding: 5px 12px; border-radius: 20px;
        background: #F4F3EF; border: 1px solid #E5E2D9;
        font-size: 11px; color: #6B6960; cursor: pointer;
        font-family: 'DM Sans', sans-serif;
        transition: all 0.15s; display: inline-block;
        margin: 3px;
    }
    .sample-btn:hover { border-color: #D4740A; color: #D4740A; }

    /* Footer */
    .footer {
        text-align: center; padding: 28px 0 12px;
        font-size: 11px; color: #9C9888;
        border-top: 1px solid #E5E2D9; margin-top: 32px;
        font-family: 'DM Sans', sans-serif;
    }

    /* Progress dots */
    .progress-bar {
        display: flex; align-items: center; justify-content: center;
        gap: 8px; margin: 16px 0;
    }
    .progress-dot {
        width: 28px; height: 28px; border-radius: 50%;
        display: inline-flex; align-items: center; justify-content: center;
        font-size: 12px; font-weight: 700; transition: all 0.3s;
        font-family: 'DM Sans', sans-serif;
    }
    .progress-dot.done { background: #0D7C3A; color: white; }
    .progress-dot.current { background: #D4740A; color: white; }
    .progress-dot.pending { background: #F4F3EF; color: #9C9888; }
    .progress-line { width: 40px; height: 2px; }
    .progress-line.done { background: #0D7C3A; }
    .progress-line.pending { background: #E5E2D9; }

    /* Responsive columns */
    [data-testid="column"] { padding: 0 6px !important; }

    /* Input styling */
    .stTextArea textarea {
        font-family: 'DM Serif Display', Georgia, serif !important;
        font-size: 15px !important;
        background: #F4F3EF !important;
        border-color: #E5E2D9 !important;
        border-radius: 10px !important;
    }
    .stTextArea textarea:focus { border-color: #D4740A !important; }
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# Session State
# ──────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []
if "results" not in st.session_state:
    st.session_state.results = None
if "pipeline_complete" not in st.session_state:
    st.session_state.pipeline_complete = False


# ──────────────────────────────────────────────
# Helper Functions
# ──────────────────────────────────────────────
def get_coverage_class(value, highlight=False):
    """Return CSS class for a coverage value."""
    hl = " cov-highlight" if highlight else ""
    if value == 0: return f"cov-zero{hl}"
    if value < 15: return f"cov-critical{hl}"
    if value < 35: return f"cov-low{hl}"
    if value < 60: return f"cov-mid{hl}"
    if value < 80: return f"cov-good{hl}"
    return f"cov-great{hl}"


def get_quality_class(score):
    if score >= 75: return "quality-high"
    if score >= 50: return "quality-mid"
    return "quality-low"


def classify_interaction(text: str, api_key: str) -> dict:
    """Call Claude API to classify an Indian language interaction."""
    client = anthropic.Anthropic(api_key=api_key)

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        system=CLASSIFICATION_PROMPT,
        messages=[{"role": "user", "content": text}],
    )

    raw = message.content[0].text.strip()
    raw = raw.replace("```json", "").replace("```", "").strip()
    parsed = json.loads(raw)

    # Enrich with coverage data
    lang = parsed.get("language", "")
    domain = parsed.get("domain", "")
    lang_coverage = COVERAGE_DATA.get(lang, None)
    domain_key = DOMAIN_KEY_MAP.get(domain, "general")
    current_coverage = lang_coverage[domain_key] if lang_coverage and domain_key in lang_coverage else 0

    return {
        **parsed,
        "input_text": text,
        "coverage_current": current_coverage,
        "coverage_data": lang_coverage,
        "timestamp": time.strftime("%H:%M:%S"),
    }


def render_tag(label, value, color="#2563EB", bg="#EEF2FF"):
    return f'<span class="tag" style="background:{bg}"><span class="tag-label">{label}</span><span class="tag-value" style="color:{color}">{value}</span></span>'


def render_progress(current_layer, total=4):
    dots = []
    for i in range(1, total + 1):
        if i < current_layer:
            dots.append(f'<span class="progress-dot done">✓</span>')
        elif i == current_layer:
            dots.append(f'<span class="progress-dot current">{i}</span>')
        else:
            dots.append(f'<span class="progress-dot pending">{i}</span>')
        if i < total:
            cls = "done" if i < current_layer else "pending"
            dots.append(f'<span class="progress-line {cls}"></span>')
    return f'<div class="progress-bar">{"".join(dots)}</div>'


# ──────────────────────────────────────────────
# Header
# ──────────────────────────────────────────────
st.markdown('<div class="brand-label"><span class="brand-dot"></span>INDIC DATA FLYWHEEL</div>', unsafe_allow_html=True)
st.markdown("# Every interaction becomes training data.")
st.markdown(
    '<p style="font-size:14px; color:#6B6960; max-width:620px; line-height:1.6; margin-bottom:24px;">'
    'Type or speak in any Indian language. The four-layer pipeline classifies, scores, '
    'maps coverage gaps, and routes to the right training queue — live.</p>',
    unsafe_allow_html=True,
)


# ──────────────────────────────────────────────
# Sidebar: API Key + Stats
# ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    api_key = st.text_input(
        "Anthropic API Key",
        type="password",
        placeholder="sk-ant-...",
        help="Your key is used only for classification and never stored.",
    )
    if api_key:
        st.session_state.api_key = api_key
    elif "api_key" in st.session_state:
        api_key = st.session_state.api_key
    st.markdown("---")
    if st.session_state.history:
        total = len(st.session_state.history)
        qualified = sum(1 for h in st.session_state.history if h["quality_score"] >= 60)
        critical_gaps = sum(1 for h in st.session_state.history if h["coverage_current"] < 20)
        st.metric("Total Processed", total)
        st.metric("Training Qualified", qualified)
        st.metric("Critical Gaps Found", critical_gaps)
        if st.button("Clear History"):
            st.session_state.history = []
            st.session_state.results = None
            st.session_state.pipeline_complete = False
            st.rerun()
    st.markdown("---")
    st.markdown(
        '<p style="font-size:11px; color:#9C9888;">Built by <strong>Danish Ali Hakim</strong>'
        '<br>Technical Solutions Manager<br>DIBD / MeitY</p>',
        unsafe_allow_html=True,
    )


# ──────────────────────────────────────────────
# API Key (main page if not set)
# ──────────────────────────────────────────────
if not api_key:
    st.markdown("")
    key_col1, key_col2 = st.columns([2, 1])
    with key_col1:
        main_api_key = st.text_input(
            "Enter your Anthropic API Key to start",
            type="password",
            placeholder="sk-ant-...",
            key="main_api_key",
        )
        if main_api_key:
            api_key = main_api_key
            st.session_state.api_key = main_api_key
            st.rerun()
    with key_col2:
        st.markdown("")
        st.markdown("")
        st.markdown(
            '<p style="font-size:11px; color:#9C9888; line-height:1.5;">'
            'Get a key at <a href="https://console.anthropic.com/" target="_blank">console.anthropic.com</a>. '
            'Your key is never stored.</p>',
            unsafe_allow_html=True,
        )


# ──────────────────────────────────────────────
# Input Section
# ──────────────────────────────────────────────
# Initialize sample state
if "sample_text" not in st.session_state:
    st.session_state.sample_text = ""

input_text = st.text_area(
    "Simulate a user interaction",
    value=st.session_state.sample_text,
    placeholder="Type in any Indian language — Hindi, Tamil, Odia, Hinglish, Bengali, Kannada...",
    height=68,
    label_visibility="collapsed",
)

# Sample inputs
st.markdown('<p style="font-size:11px; color:#9C9888; margin-bottom:4px;">Try a sample:</p>', unsafe_allow_html=True)
sample_cols = st.columns(5)
for i, sample in enumerate(SAMPLE_INPUTS):
    col = sample_cols[i % 5]
    if col.button(sample["label"], key=f"sample_{i}", use_container_width=True):
        st.session_state.sample_text = sample["text"]
        st.session_state.pipeline_complete = False
        st.session_state.results = None
        st.rerun()

# Process button
col_btn, col_space = st.columns([1, 3])
with col_btn:
    process_clicked = st.button(
        "🔄 Process Through Pipeline",
        type="primary",
        disabled=not api_key or not input_text,
        use_container_width=True,
    )


# ──────────────────────────────────────────────
# Pipeline Processing
# ──────────────────────────────────────────────
if process_clicked and input_text and api_key:
    st.session_state.pipeline_complete = False
    st.session_state.results = None

    # Layer 1
    st.markdown(render_progress(1), unsafe_allow_html=True)
    layer1_placeholder = st.empty()
    layer1_placeholder.info("⟳ **Layer 1: Capture & Classify** — Detecting language, dialect, domain, code-mix ratio...")
    time.sleep(1.2)

    # Layer 2
    st.markdown(render_progress(2), unsafe_allow_html=True)
    layer1_placeholder.success("✓ **Layer 1: Capture & Classify** — Complete")
    layer2_placeholder = st.empty()
    layer2_placeholder.info("⟳ **Layer 2: Quality Scoring** — Analyzing clarity, completeness, vocabulary richness...")
    time.sleep(0.8)

    # Layer 3 + API call
    st.markdown(render_progress(3), unsafe_allow_html=True)
    layer2_placeholder.success("✓ **Layer 2: Quality Scoring** — Complete")
    layer3_placeholder = st.empty()
    layer3_placeholder.info("⟳ **Layer 3: Gap Detection** — Mapping coverage, identifying gaps...")

    try:
        result = classify_interaction(input_text, api_key)

        layer3_placeholder.success("✓ **Layer 3: Gap Detection** — Complete")

        # Layer 4
        st.markdown(render_progress(4), unsafe_allow_html=True)
        layer4_placeholder = st.empty()
        layer4_placeholder.info("⟳ **Layer 4: Feedback Loop** — Routing to product, computing training priority...")
        time.sleep(0.6)
        layer4_placeholder.success("✓ **Layer 4: Feedback Loop** — Complete")

        st.session_state.results = result
        st.session_state.history.insert(0, result)
        st.session_state.pipeline_complete = True

    except json.JSONDecodeError:
        layer3_placeholder.error("❌ Classification returned invalid JSON. Please try again.")
    except anthropic.AuthenticationError:
        layer3_placeholder.error("❌ Invalid API key. Please check your key in the sidebar.")
    except Exception as e:
        layer3_placeholder.error(f"❌ Error: {str(e)}")


# ──────────────────────────────────────────────
# Results Display
# ──────────────────────────────────────────────
if st.session_state.pipeline_complete and st.session_state.results:
    r = st.session_state.results

    st.markdown("---")
    st.markdown(render_progress(5), unsafe_allow_html=True)  # All done

    # ── Layer 1 & 2 side by side ──
    col1, col2 = st.columns(2)

    with col1:
        card_class = "layer-card complete"
        st.markdown(f'<div class="{card_class}">', unsafe_allow_html=True)
        st.markdown(
            f'<div class="layer-header">'
            f'<div class="layer-title-group">'
            f'<div class="layer-number complete">✓</div>'
            f'<div><div style="font-size:14px;font-weight:700;color:#1A1A18">Capture & Classify</div>'
            f'<div style="font-size:11px;color:#9C9888">Language · Dialect · Domain · Code-mix</div></div></div>'
            f'<span class="status-badge status-complete">Complete</span>'
            f'</div>',
            unsafe_allow_html=True,
        )
        tags_html = "".join([
            render_tag("Lang", r["language"]),
            render_tag("Script", r["script"], "#7C3AED", "#F3EEFF"),
            render_tag("Dialect", r["dialect_region"]),
            render_tag("Domain", r["domain"], "#D4740A", "#FFF3E0"),
            render_tag("Code-mix", f'{r["code_mix_ratio"]}%',
                       "#D4740A" if r["code_mix_ratio"] > 30 else "#0D7C3A",
                       "#FFF3E0" if r["code_mix_ratio"] > 30 else "#ECFDF3"),
            render_tag("Register", r["formality"], "#6B6960", "#F4F3EF"),
        ])
        st.markdown(f'<div style="display:flex;flex-wrap:wrap;gap:4px;">{tags_html}</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="margin-top:8px;font-size:12px;color:#6B6960"><strong>Intent:</strong> {r["intent"]}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown(f'<div class="{card_class}">', unsafe_allow_html=True)
        st.markdown(
            f'<div class="layer-header">'
            f'<div class="layer-title-group">'
            f'<div class="layer-number complete">✓</div>'
            f'<div><div style="font-size:14px;font-weight:700;color:#1A1A18">Quality Scoring</div>'
            f'<div style="font-size:11px;color:#9C9888">Clarity · Completeness · Novelty · Value</div></div></div>'
            f'<span class="status-badge status-complete">Complete</span>'
            f'</div>',
            unsafe_allow_html=True,
        )
        q_class = get_quality_class(r["quality_score"])
        vocab_tags = "".join(
            f'<span style="padding:2px 8px;border-radius:6px;background:#F4F3EF;font-size:11px;color:#6B6960;margin:1px">{t}</span>'
            for t in r.get("vocabulary_tags", [])[:5]
        )
        st.markdown(
            f'<div style="display:flex;align-items:center;gap:14px;margin-bottom:8px">'
            f'<div class="quality-box {q_class}">{r["quality_score"]}</div>'
            f'<div style="font-size:12px;color:#6B6960;line-height:1.5;flex:1">{r["quality_reasoning"]}</div></div>'
            f'<div style="display:flex;flex-wrap:wrap;gap:3px">{vocab_tags}</div>',
            unsafe_allow_html=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Layer 3 & 4 side by side ──
    col3, col4 = st.columns(2)

    with col3:
        st.markdown(f'<div class="{card_class}">', unsafe_allow_html=True)
        st.markdown(
            f'<div class="layer-header">'
            f'<div class="layer-title-group">'
            f'<div class="layer-number complete">✓</div>'
            f'<div><div style="font-size:14px;font-weight:700;color:#1A1A18">Gap Detection</div>'
            f'<div style="font-size:11px;color:#9C9888">Coverage map · Gap identification</div></div></div>'
            f'<span class="status-badge status-complete">Complete</span>'
            f'</div>',
            unsafe_allow_html=True,
        )
        cov = r["coverage_current"]
        cov_color = "#DC2626" if cov < 20 else "#D4740A" if cov < 50 else "#0D7C3A"
        cov_bg = "#FEF2F2" if cov < 20 else "#FFF3E0" if cov < 50 else "#ECFDF3"
        cov_msg = "⚠ Critical gap — extremely valuable data" if cov < 20 else "△ Moderate gap — helps fill coverage" if cov < 50 else "✓ Well-covered — adds quality depth"

        # Coverage box + message
        st.markdown(
            f'<div style="display:flex;align-items:center;gap:12px;margin-bottom:10px">'
            f'<div style="padding:6px 14px;border-radius:10px;background:{cov_bg};text-align:center">'
            f'<div style="font-size:9px;color:#9C9888;font-weight:600;text-transform:uppercase">Coverage</div>'
            f'<div style="font-size:20px;font-weight:700;color:{cov_color}">{cov}%</div></div>'
            f'<div style="font-size:12px;color:#6B6960;line-height:1.5">'
            f'<strong style="color:#1A1A18">{r["language"]} × {r["domain"]}</strong><br>{cov_msg}</div></div>',
            unsafe_allow_html=True,
        )

        # Mini coverage bars for this language
        if r["coverage_data"]:
            domain_key = DOMAIN_KEY_MAP.get(r["domain"], "general")
            cells = ""
            for key, label in [("finance", "Fin"), ("govt", "Govt"), ("health", "Health"), ("general", "Gen")]:
                val = r["coverage_data"][key]
                hl = key == domain_key
                cls = get_coverage_class(val, hl)
                cells += f'<div style="text-align:center"><div class="coverage-cell {cls}">{val}%</div><div style="font-size:9px;color:#9C9888;margin-top:2px">{label}</div></div>'
            hours = r["coverage_data"].get("hours", 0)
            st.markdown(
                f'<div style="display:flex;gap:6px;align-items:center">{cells}'
                f'<div style="margin-left:8px;font-size:11px;color:#9C9888">{hours:,} hrs</div></div>',
                unsafe_allow_html=True,
            )
        st.markdown('</div>', unsafe_allow_html=True)

    with col4:
        st.markdown(f'<div class="{card_class}">', unsafe_allow_html=True)
        st.markdown(
            f'<div class="layer-header">'
            f'<div class="layer-title-group">'
            f'<div class="layer-number complete">✓</div>'
            f'<div><div style="font-size:14px;font-weight:700;color:#1A1A18">Feedback Loop</div>'
            f'<div style="font-size:11px;color:#9C9888">Route to product · Training priority</div></div></div>'
            f'<span class="status-badge status-complete">Complete</span>'
            f'</div>',
            unsafe_allow_html=True,
        )
        # Extract product name
        import re
        product_match = re.search(r'(Samvaad|UIDAI|SBI Life|Indus|Kaze|Feature Phones)', r.get("gap_relevance", ""))
        product_name = product_match.group(1) if product_match else "Training"
        novelty_label = r.get("novelty_assessment", "medium").split("—")[0].strip()
        is_qualified = r["quality_score"] >= 60

        tags_html = "".join([
            render_tag("Novelty", novelty_label,
                       "#D4740A" if "high" in novelty_label.lower() else "#2563EB",
                       "#FFF3E0" if "high" in novelty_label.lower() else "#EEF2FF"),
            render_tag("→ Route", product_name, "#7C3AED", "#F3EEFF"),
            render_tag("Training", "✓ Qualified" if is_qualified else "✗ Review",
                       "#0D7C3A" if is_qualified else "#DC2626",
                       "#ECFDF3" if is_qualified else "#FEF2F2"),
        ])
        st.markdown(
            f'<div style="display:flex;flex-wrap:wrap;gap:4px;margin-bottom:8px">{tags_html}</div>'
            f'<div style="font-size:12px;color:#6B6960;line-height:1.5">{r["training_value"]}</div>',
            unsafe_allow_html=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Summary ──
    is_qualified = r["quality_score"] >= 60
    is_critical = r["coverage_current"] < 20
    summary_class = "summary-critical" if is_critical else "summary-qualified" if is_qualified else "summary-review"
    icon = "✅" if is_qualified else "⚠️"

    summary_text = (
        f'{icon} <strong>{r["language"]}</strong> {r["domain"]} interaction '
        f'({r["formality"]}, {r["code_mix_ratio"]}% code-mix) scored '
        f'<strong>{r["quality_score"]}/100</strong>. '
    )
    if is_qualified:
        summary_text += f'Routed to <strong>{product_name}</strong> training pipeline.'
    else:
        summary_text += 'Below threshold — flagged for quality review.'

    if is_critical:
        summary_text += (
            f' <span style="color:#DC2626;font-weight:600">Fills a critical gap — '
            f'{r["language"]} × {r["domain"]} is at only {r["coverage_current"]}%.</span>'
        )

    st.markdown(
        f'<div class="summary-box {summary_class}">'
        f'<p style="font-size:14px;color:#1A1A18;line-height:1.7">{summary_text}</p></div>',
        unsafe_allow_html=True,
    )


# ──────────────────────────────────────────────
# History
# ──────────────────────────────────────────────
if len(st.session_state.history) > 1:
    st.markdown("---")
    st.markdown(
        f'<p style="font-size:11px;font-weight:700;color:#9C9888;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:8px">'
        f'Processed Interactions ({len(st.session_state.history)})</p>',
        unsafe_allow_html=True,
    )
    for i, h in enumerate(st.session_state.history[1:10]):  # Show last 9
        row_class = "history-even" if i % 2 == 0 else "history-odd"
        q_color = "#0D7C3A" if h["quality_score"] >= 75 else "#D4740A" if h["quality_score"] >= 50 else "#DC2626"
        cov = h["coverage_current"]
        cov_color = "#DC2626" if cov < 20 else "#D4740A" if cov < 50 else "#0D7C3A"
        cov_bg = "#FEF2F2" if cov < 20 else "#FFF3E0" if cov < 50 else "#ECFDF3"
        dot_color = "#0D7C3A" if h["quality_score"] >= 60 else "#D4740A"

        truncated = h["input_text"][:50] + "..." if len(h["input_text"]) > 50 else h["input_text"]

        st.markdown(
            f'<div class="history-row {row_class}">'
            f'<div style="display:flex;align-items:center;gap:8px;flex:1;min-width:0">'
            f'<span style="width:6px;height:6px;border-radius:50%;background:{dot_color};flex-shrink:0"></span>'
            f'<span style="color:#1A1A18;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">{truncated}</span></div>'
            f'<div style="display:flex;align-items:center;gap:10px;flex-shrink:0">'
            f'<span style="color:#2563EB;font-weight:600">{h["language"]}</span>'
            f'<span style="color:#9C9888">{h["domain"]}</span>'
            f'<span style="font-weight:700;color:{q_color};font-family:monospace">Q:{h["quality_score"]}</span>'
            f'<span style="padding:1px 6px;border-radius:4px;font-size:10px;font-weight:600;background:{cov_bg};color:{cov_color}">{cov}%</span>'
            f'<span style="color:#9C9888;font-size:10px">{h["timestamp"]}</span></div></div>',
            unsafe_allow_html=True,
        )


# ──────────────────────────────────────────────
# Footer
# ──────────────────────────────────────────────
st.markdown(
    '<div class="footer">'
    'Built by <strong>Danish Ali Hakim</strong> · Technical Solutions Manager, DIBD / MeitY<br>'
    '<span style="font-size:10px">Prototype demonstrating the four-layer data flywheel architecture for Indian language AI</span>'
    '</div>',
    unsafe_allow_html=True,
)
