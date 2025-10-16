# config.py
import os

try:
    import streamlit as st
    _secrets = st.secrets
except ImportError:
    _secrets = {}

# ✅ First try to get from Streamlit secrets (Cloud)
# ✅ If not found, fall back to environment (local dev)

GEMINI_API_KEY = _secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY", "")
ELEVEN_API_KEY = _secrets.get("ELEVEN_API_KEY") or os.getenv("ELEVEN_API_KEY", "")
ELEVEN_VOICE_ID = _secrets.get("ELEVEN_VOICE_ID") or os.getenv("ELEVEN_VOICE_ID", "")
GEMINI_MODEL = _secrets.get("GEMINI_MODEL") or os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

def check_keys(require_tts: bool = False):
    if not GEMINI_API_KEY:
        raise AssertionError("Set GEMINI_API_KEY in environment or Streamlit secrets.")
    if require_tts and (not ELEVEN_API_KEY or not ELEVEN_VOICE_ID):
        raise AssertionError("Set ELEVEN_API_KEY and ELEVEN_VOICE_ID in environment or Streamlit secrets.")

