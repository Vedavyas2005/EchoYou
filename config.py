import os
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY", "")
ELEVEN_VOICE_ID = os.getenv("ELEVEN_VOICE_ID", "")  # your cloned voice id

# Gemini model name; use the current fast text model.
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

# Safety: hard stop if keys are missing (except we allow running UI without TTS)
def check_keys(require_tts: bool = False):
    assert GEMINI_API_KEY, "Set GEMINI_API_KEY in environment."
    if require_tts:
        assert ELEVEN_API_KEY and ELEVEN_VOICE_ID, \
            "Set ELEVEN_API_KEY and ELEVEN_VOICE_ID in environment to enable voice replies."
