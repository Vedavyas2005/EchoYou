# app.py
import streamlit as st
from typing import Dict, List
import config
from ai_brain import ask_gemini
from tts_voice import text_to_speech_mp3
from speech_frontend import get_user_text

# ---------- Theming ----------
def set_theme(dark: bool):
    # Neon purple on black (dark) or subtle purple accents (light)
    if dark:
        st.markdown("""
        <style>
        :root { --neon:#a855f7; }
        .stApp { background: #0b0b10; }
        h1,h2,h3,h4 { color: #e5e7eb; }
        .ey-card {
          background: #12121a; border: 1px solid #242436;
          border-radius: 16px; padding: 16px; box-shadow: 0 0 16px rgba(168,85,247,.15);
        }
        .ey-header {
          font-size: 1.6rem; font-weight: 700; letter-spacing: .3px;
          background: linear-gradient(90deg, #c084fc, #22d3ee);
          -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }
        .ey-pill {
          display:inline-flex; gap:.4rem; align-items:center;
          padding:.25rem .6rem; border:1px solid #2b2b40;
          border-radius:999px; font-size:.8rem; color:#c7c9d1;
          background:#141421;
        }
        .stButton>button {
          border-radius: 12px; border:1px solid #2b2b40;
          background: #19192a; color:#e5e7eb; padding:.55rem .9rem;
        }
        .stButton>button:hover { box-shadow: 0 0 0 2px rgba(168,85,247,.35) inset; }
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
        :root { --neon:#7c3aed; }
        .ey-card { background: #ffffff; border: 1px solid #eee;
          border-radius: 16px; padding: 16px; box-shadow: 0 2px 12px rgba(0,0,0,.06);}
        .ey-header { color:#3b0764; }
        .ey-pill { display:inline-flex; gap:.4rem; align-items:center;
          padding:.25rem .6rem; border:1px solid #e9e9f2;
          border-radius:999px; font-size:.8rem; color:#4b5563; background:#f7f7fb;}
        .stButton>button { border-radius: 12px; }
        </style>
        """, unsafe_allow_html=True)

def init_state():
    if "dark" not in st.session_state: st.session_state.dark = True
    if "history" not in st.session_state: 
        st.session_state.history=[]
    if "last_audio" not in st.session_state: st.session_state.last_audio = None

def reset_chat():
    st.session_state.history = []
    st.session_state.last_audio = None
    st.toast("Cleared!", icon="🧹")

# ---------- App ----------
init_state()
st.set_page_config(page_title="EchoYou", page_icon="🟣", layout="centered")
set_theme(st.session_state.dark)

col1, col2 = st.columns([1,1])
with col1:
    st.markdown('<div class="ey-header">EchoYou — Your Voice. Your Reflection.</div>', unsafe_allow_html=True)
with col2:
    mode = "🌙 Dark" if st.session_state.dark else "☀️ Light"
    if st.button(f"Toggle {mode}"):
        st.session_state.dark = not st.session_state.dark
        st.rerun()

st.markdown('<div class="ey-card">', unsafe_allow_html=True)
st.write("**How it works:** Speak → Gemini understands → ElevenLabs replies in your voice.")
st.write("No storage. No login. Memory resets when you clear or refresh.")
st.markdown('</div>', unsafe_allow_html=True)

# Keys check (Gemini required; TTS optional)
try:
    config.check_keys(require_tts=False)
except AssertionError as e:
    st.error(str(e))
    st.stop()

# ---- Conversation UI ----
st.divider()
left, right = st.columns([3,1])
with right:
    if st.button("🧹 Clear Chat", use_container_width=True):
        reset_chat()

with left:
    user_text = get_user_text()

send = st.button("Send", use_container_width=True, disabled=not bool(user_text))
if send and user_text:
    # Append user turn to in-memory history
    st.session_state.history.append({"role": "user", "content": user_text})
    with st.spinner("Thinking…"):
        reply = ask_gemini(st.session_state.history, user_text)
    st.session_state.history.append({"role": "assistant", "content": reply})

    # Attempt TTS (skip silently if no key/voice)
    audio_bytes = text_to_speech_mp3(reply)
    st.session_state.last_audio = audio_bytes if audio_bytes else None

# ---- Render transcript & audio ----
st.divider()
st.subheader("🗣️ Conversation")
for i, turn in enumerate(st.session_state.history):
    if turn["role"] == "user":
        st.markdown(f"**You:** {turn['content']}")
    else:
        st.markdown(f"**EchoYou:** {turn['content']}")

if st.session_state.last_audio:
    st.audio(st.session_state.last_audio, format="audio/mp3")

st.caption("Tip: If mic STT doesn’t work in your browser, type your message and press **Send**.")
