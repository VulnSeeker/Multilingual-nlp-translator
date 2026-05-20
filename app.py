import streamlit as st
import os
from dotenv import load_dotenv
from groq import Groq

# --- CONFIG ---
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
groq_client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

# --- UNIVERSAL GROQ TRANSLATION UTILS (ALWAYS CLEAN OUTPUTS) ---
def roman_urdu_to_urdu(roman_text: str) -> str:
    if not groq_client:
        return "Groq API key not set."
    prompt = (
        f'Convert this Roman Urdu to Urdu script. '
        f'RETURN ONLY the translated Urdu sentence. No labels, formatting, asterisks, or explanation. Just the translation: "{roman_text}"'
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
        return "Groq API key not set."
    prompt = (
        f'Convert this Urdu to Roman Urdu. '
        f'RETURN ONLY the Roman Urdu sentence. No labels, asterisks, formatting, or explanation. Just the translation: "{urdu_text}"'
    )
    res = groq_client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=80,
        temperature=0.2,
    )
    return (res.choices[0].message.content or "").strip()


def urdu_to_english(urdu_text: str) -> str:
    if not groq_client:
        return "Groq API key not set."
    prompt = (
        f'Translate this Urdu sentence to English. '
        f'RETURN ONLY the English translation. No labels, formatting, asterisks, or explanation. Just the translation: "{urdu_text}"'
    )
    res = groq_client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=120,
        temperature=0.2,
    )
    return (res.choices[0].message.content or "").strip()


def english_to_urdu(english_text: str) -> str:
    if not groq_client:
        return "Groq API key not set."
    prompt = (
        f'Translate this English sentence to Urdu. '
        f'RETURN ONLY the Urdu translation. No labels, formatting, asterisks, or explanation. Just the translation: "{english_text}"'
    )
    res = groq_client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=120,
        temperature=0.2,
    )
    return (res.choices[0].message.content or "").strip()

# --- STREAMLIT UI (DARK MODE) ---
st.set_page_config(
    page_title="Roman Urdu Translator",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

if os.path.exists("dark-theme.css"):
    with open("dark-theme.css", "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("💬 Roman Urdu ↔ Urdu ↔ English — Translator")
st.caption(f"All translations by: Groq {GROQ_MODEL}")

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
            english = urdu_to_english(urdu)
            answer = f"**Urdu:** {urdu}\n**English:** {english}"

        elif direction == "English → Roman Urdu":
            urdu = english_to_urdu(user_input)
            roman = urdu_to_roman_urdu(urdu)
            answer = f"**Urdu:** {urdu}\n**Roman Urdu:** {roman}"

        elif direction == "Roman Urdu → Urdu":
            urdu = roman_urdu_to_urdu(user_input)
            answer = f"**Urdu:** {urdu}"

        elif direction == "Urdu → Roman Urdu":
            roman = urdu_to_roman_urdu(user_input)
            answer = f"**Roman Urdu:** {roman}"

        elif direction == "Urdu → English":
            english = urdu_to_english(user_input)
            answer = f"**English:** {english}"

        elif direction == "English → Urdu":
            urdu = english_to_urdu(user_input)
            answer = f"**Urdu:** {urdu}"

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

# (Optional) Clear history button
if st.button("Clear Conversation"):
    st.session_state.history.clear()

st.caption(" demo: ALL translations powered by Groq LLM, strict outputs.")
