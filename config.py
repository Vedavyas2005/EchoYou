import os

try:
    import streamlit as st
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    ELEVEN_API_KEY = st.secrets.get("ELEVEN_API_KEY", "")
    ELEVEN_VOICE_ID = st.secrets.get("ELEVEN_VOICE_ID", "")
    GEMINI_MODEL = st.secrets.get("GEMINI_MODEL", "gemini-2.0-flash")
except Exception:
    # Fall back to environment variables if secrets not found (for local testing)
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY", "")
    ELEVEN_VOICE_ID = os.getenv("ELEVEN_VOICE_ID", "")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

def check_keys(require_tts: bool = False):
    if not GEMINI_API_KEY:
        raise AssertionError("Set GEMINI_API_KEY in environment or Streamlit secrets.")
    if require_tts and (not ELEVEN_API_KEY or not ELEVEN_VOICE_ID):
        raise AssertionError("Set ELEVEN_API_KEY and ELEVEN_VOICE_ID in environment or Streamlit secrets.")

