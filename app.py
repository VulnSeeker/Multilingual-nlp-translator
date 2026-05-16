
import streamlit as st
import os
from transformers import MarianMTModel, MarianTokenizer
from dotenv import load_dotenv
from groq import Groq

# --- CONFIG ---
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
# Pick one:
# - "llama-3.1-8b-instant" (fast)
# - "llama-3.3-70b-versatile" (better quality)
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

MODEL_UR_EN = "Helsinki-NLP/opus-mt-ur-en"
MODEL_EN_UR = "Helsinki-NLP/opus-mt-en-ur"

tokenizer_ur_en = MarianTokenizer.from_pretrained(MODEL_UR_EN)
model_ur_en = MarianMTModel.from_pretrained(MODEL_UR_EN)
tokenizer_en_ur = MarianTokenizer.from_pretrained(MODEL_EN_UR)
model_en_ur = MarianMTModel.from_pretrained(MODEL_EN_UR)

groq_client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None


# --- TRANSLATION UTILS ---
def roman_urdu_to_urdu(roman_text: str) -> str:
    if not groq_client:
        return "Groq API key not set. Add GROQ_API_KEY to your .env file."

    prompt = (
        "Convert this Roman Urdu sentence to Urdu script. "
        "Return only the Urdu sentence (no explanation):\n"
        f'{roman_text}'
    )

    res = groq_client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=80,
        temperature=0.2,
    )
    return (res.choices[0].message.content or "").strip()


def urdu_to_roman_urdu(urdu_text: str) -> str:
    if not groq_client:
        return "Groq API key not set. Add GROQ_API_KEY to your .env file."

    prompt = (
        "Convert this Urdu sentence to Roman Urdu. "
        "Return only the Roman Urdu (no explanation):\n"
        f'{urdu_text}'
    )

    res = groq_client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=80,
        temperature=0.2,
    )
    return (res.choices[0].message.content or "").strip()


def urdu_to_english(urdu_text: str) -> str:
    inputs = tokenizer_ur_en(urdu_text, return_tensors="pt", padding=True)
    translated = model_ur_en.generate(**inputs)
    return tokenizer_ur_en.decode(translated[0], skip_special_tokens=True)


def english_to_urdu(english_text: str) -> str:
    inputs = tokenizer_en_ur(english_text, return_tensors="pt", padding=True)
    translated = model_en_ur.generate(**inputs)
    return tokenizer_en_ur.decode(translated[0], skip_special_tokens=True)


# --- STREAMLIT UI (DARK MODE) ---
st.set_page_config(
    page_title="FYP Roman Urdu Translator",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Apply dark theme if exists
if os.path.exists("dark-theme.css"):
    with open("dark-theme.css", "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("💬 Roman Urdu ↔ Urdu ↔ English —  Translator")

# --- Chat-like UI ---
if "history" not in st.session_state:
    st.session_state.history = []

options = [
    "Roman Urdu → English",
    "English → Roman Urdu",
    "Roman Urdu → Urdu",
    "Urdu → Roman Urdu",
    "Urdu → English",
    "English → Urdu",
]

col1, col2 = st.columns([4, 1])
with col2:
    direction = st.selectbox("Translate", options, index=0)

with col1:
    user_input = st.text_input(
        "You:",
        key="user_input",
        placeholder="Type your message in Roman Urdu, Urdu, or English...",
    )

if st.button("Send", use_container_width=True):
    answer = ""
    try:
        if not user_input.strip():
            answer = "Please type something first."
        elif direction == "Roman Urdu → English":
            urdu = roman_urdu_to_urdu(user_input)
            if urdu.startswith("Groq API key not set"):
                answer = urdu
            else:
                answer = f"**Urdu:** {urdu}\n**English:** {urdu_to_english(urdu)}"

        elif direction == "English → Roman Urdu":
            urdu = english_to_urdu(user_input)
            roman = urdu_to_roman_urdu(urdu)
            answer = f"**Urdu:** {urdu}\n**Roman Urdu:** {roman}"

        elif direction == "Roman Urdu → Urdu":
            answer = f"**Urdu:** {roman_urdu_to_urdu(user_input)}"

        elif direction == "Urdu → Roman Urdu":
            answer = f"**Roman Urdu:** {urdu_to_roman_urdu(user_input)}"

        elif direction == "Urdu → English":
            answer = f"**English:** {urdu_to_english(user_input)}"

        elif direction == "English → Urdu":
            answer = f"**Urdu:** {english_to_urdu(user_input)}"

    except Exception as e:
        answer = f"🚨 Error: {e}"

    st.session_state.history.append((user_input, answer))

# Show chat history, latest at bottom
st.markdown("---")
for q, a in st.session_state.history:
    st.markdown(
        f"""
        <div class='bubble user'><b>You:</b> {q}</div>
        <div class='bubble bot'><b>Translator:</b> {a}</div>
        """,
        unsafe_allow_html=True,
    )

if st.button("Clear Conversation"):
    st.session_state.history.clear()

st.caption("Ready demo. Groq handles Roman↔Urdu, MarianMT handles Urdu↔English.")
