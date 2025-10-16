# speech_frontend.py
from typing import Optional
import streamlit as st

try:
    # pip install streamlit-mic-recorder
    from streamlit_mic_recorder import mic_recorder, speech_to_text
    MIC_AVAILABLE = True
except Exception:
    MIC_AVAILABLE = False

def get_user_text() -> Optional[str]:
    """
    Returns one utterance of user text via:
      1) Browser speech-to-text (preferred, free), or
      2) Manual text input as fallback.
    """
    st.subheader("🎙️ Speak or type")
    user_text = None

    if MIC_AVAILABLE:
        st.caption("Click to speak. Recognition runs in your browser (free).")
        # Option A: one-shot STT button
        result = speech_to_text(
            language='en-US',
            use_container_width=True,
            just_once=True,
            key="stt_button",
        )
        if result and isinstance(result, str) and result.strip():
            user_text = result.strip()
            st.success(f"Transcribed: {user_text}")

        # Also show raw recorder if user prefers to listen back
        with st.expander("Alternatively, record raw audio (optional)"):
            rec = mic_recorder(
                start_prompt="Start recording",
                stop_prompt="Stop",
                just_once=True,
                use_container_width=True,
                format="wav",
                key="mic_raw",
            )
            if rec and rec.get("bytes"):
                st.audio(rec["bytes"], format="audio/wav")
                st.caption("(Raw audio recorded; STT above is the main input.)")
    else:
        st.info("Mic component not available here; type below.")
    # Manual fallback
    typed = st.text_input("Or type your message:")
    if typed:
        user_text = typed.strip()

    return user_text
