# tts_voice.py
import io
import requests
import config

ELEVEN_URL = "https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

def text_to_speech_mp3(text: str) -> bytes:
    """
    Convert text to speech using ElevenLabs cloned voice.
    Returns raw MP3 bytes suitable for st.audio.
    """
    if not (config.ELEVEN_API_KEY and config.ELEVEN_VOICE_ID):
        # If no key/voice, gracefully skip TTS.
        return b""

    url = ELEVEN_URL.format(voice_id=config.ELEVEN_VOICE_ID)
    headers = {
        "xi-api-key": config.ELEVEN_API_KEY,
        "accept": "audio/mpeg",
        "content-type": "application/json",
    }
    payload = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.8},
    }
    r = requests.post(url, headers=headers, json=payload, timeout=60)
    r.raise_for_status()
    return io.BytesIO(r.content).getvalue()
