# tts_voice.py
import io
import requests
import config

def text_to_speech_mp3(text: str) -> bytes:
    api_key = config.ELEVEN_API_KEY.strip() if config.ELEVEN_API_KEY else ""
    voice_id = config.ELEVEN_VOICE_ID.strip() if config.ELEVEN_VOICE_ID else ""

    if not api_key or not voice_id:
        print("⚠️ ElevenLabs key or voice ID missing")
        return b""

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": api_key,
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
    }

    payload = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.8,
            "style": 0.0,
            "use_speaker_boost": True
        }
    }

    print("📡 Sending TTS request:", url)
    r = requests.post(url, headers=headers, json=payload)

    print("🔍 Status:", r.status_code)
    if r.status_code != 200:
        print("❌ ElevenLabs Error:", r.text)
        return b""

    audio = io.BytesIO(r.content).getvalue()
    print("✅ Audio bytes:", len(audio))
    return audio
