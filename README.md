# 💬 Roman Urdu ↔ Urdu ↔ English Translator

> **A research-driven multilingual translation system for Roman Urdu** — one of the most widely used yet computationally underserved languages, spoken by 230+ million Pakistanis in digital communication.

---

## 🔬 Research Motivation

Roman Urdu is the informal romanized writing system used by virtually all Pakistani internet users — in WhatsApp messages, Twitter/X, YouTube comments, and language exchange apps. Despite its massive usage, **no mainstream NLP or translation tool supports it natively.**

This project began from a personal frustration: while using language learning applications, incoming Roman Urdu messages could not be translated by any available tool. The only workaround was manually copying text, switching to ChatGPT, pasting it, and returning — a workflow that broke natural communication entirely.

This experience revealed a genuine NLP gap: **230 million people communicate digitally in a language that technology has largely ignored.**

---

## 🧪 Development Journey & Research Findings

### Phase 1 — Traditional MT Pipeline (Failed)

The initial approach used a standard machine translation pipeline:

```
Roman Urdu → GroqLLM→ Urdu Script → [HuggingFace MarianMT] → English
```

**Models attempted:**
- `Helsinki-NLP/opus-mt-ur-en` (Urdu → English)
- `Helsinki-NLP/opus-mt-en-ur` (English → Urdu)
- Custom transliteration models for Roman Urdu → Urdu script conversion

**Critical bugs discovered:**

| Bug | Description |
|-----|-------------|
| Iteration loops | Model repeated the same word/phrase indefinitely: `"playerplayarplayarplayar ke playarplayar"` |
| Script confusion | Model failed to distinguish Roman Urdu from English, producing garbled Urdu script |
| OOV collapse | Out-of-vocabulary Roman Urdu words caused the model to output only labels: `"**Urdu:** and **Roman Urdu:** aur"` |
| Tokenizer mismatch | MarianMT tokenizers were not trained on Roman Urdu's informal, phonetically inconsistent structure |

**Research insight from Phase 1:** Traditional MT models fail on Roman Urdu not because of model capacity, but because of a fundamental tokenization problem. Roman Urdu has no standardized spelling — the same word can be written 5+ different ways ("kaise", "kesy", "kaisy", "kyse", "kaisay"). Models trained on formal Urdu script have no mechanism to handle this variability.

---

### Phase 2 — LLM-Based Pipeline (Current)

After identifying the limitations of traditional MT, the pipeline was redesigned around **Large Language Models via the Groq API** (Llama 3.3 70B Versatile):

```
Roman Urdu → [Groq LLM: Roman Urdu → Urdu] → [Groq LLM: Urdu → English]
```

**Why LLMs work where MT models fail:**

- LLMs handle spelling variability through contextual understanding, not rigid tokenization
- Code-switching (mixed Roman Urdu + English) is handled naturally
- Informal register and conversational text are processed correctly
- No dedicated Roman Urdu training data required — zero-shot capability is sufficient

**This is itself a research finding:** For low-resource informal languages with high orthographic variability, LLM-based pipelines outperform dedicated MT models trained on formal parallel corpora.

---

## 🔧 Technical Architecture

```
User Input
    │
    ▼
Direction Router (6 translation directions)
    │
    ├── Roman Urdu → English:  [RU→Urdu] → [Urdu→EN]
    ├── English → Roman Urdu:  [EN→Urdu] → [Urdu→RU]
    ├── Roman Urdu → Urdu:     [RU→Urdu]
    ├── Urdu → Roman Urdu:     [Urdu→RU]
    ├── Urdu → English:        [Urdu→EN]
    └── English → Urdu:        [EN→Urdu]
         │
         ▼
    Groq API (llama-3.3-70b-versatile)
    Strict prompt engineering → clean output only
         │
         ▼
    Streamlit Chat UI
```

**Prompt Engineering Strategy:**

Each translation function uses strict output constraints:
```python
"RETURN ONLY the translated sentence. No labels, formatting, asterisks, or explanation."
```
This prevents the LLM from adding explanatory text, markdown, or labels that broke earlier versions.

---

## 📊 Supported Translation Directions

| Direction | Method | Notes |
|-----------|--------|-------|
| Roman Urdu → English | Two-step (RU→Ur→EN) | Most common use case |
| English → Roman Urdu | Two-step (EN→Ur→RU) | |
| Roman Urdu → Urdu | Single step | Script conversion |
| Urdu → Roman Urdu | Single step | Romanization |
| Urdu → English | Single step | Direct translation |
| English → Urdu | Single step | Direct translation |

---

## ⚠️ Known Limitations

| Limitation | Description |
|-----------|-------------|
| No standardized evaluation | No established benchmark exists for Roman Urdu translation quality — BLEU score is unreliable for this language pair |
| Spelling variability | While LLMs handle this better than MT models, extreme orthographic variation can still cause inconsistency |
| Two-step latency | Indirect translation paths (RU→Ur→EN) introduce additional API calls and latency |
| Context window | Long documents are not supported — designed for sentence/phrase-level translation |
| Dialect variation | Pakistani Urdu vs. Indian Urdu dialect differences affect translation consistency |
| API dependency | System requires active Groq API access — no offline mode |

---

## 🚀 Installation & Setup

```bash
git clone https://github.com/yourusername/roman-urdu-translator
cd roman-urdu-translator
pip install -r requirements.txt
```

Create a `.env` file:
```
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
```

Run:
```bash
streamlit run app.py
```

---

## 📦 Requirements

```
streamlit
groq
python-dotenv
```

---

## 🔮 Future Work

This project opens several research directions:

- **Evaluation framework:** Building a human-annotated benchmark dataset for Roman Urdu translation quality (no standard metric currently exists)
- **LLM comparison study:** Systematic evaluation of multiple LLMs (GPT-4, Gemini, Llama, Mistral) on Roman Urdu translation quality
- **Long-context evaluation:** Studying how LLMs handle semantic understanding in extended Roman Urdu code-switched documents
- **Adversarial robustness:** Testing how Roman Urdu translation systems respond to deliberately perturbed inputs

---
