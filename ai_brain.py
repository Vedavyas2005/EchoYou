import google.generativeai as genai
import config

# ✅ 1. Configure Gemini client using your API key from AI Studio
genai.configure(api_key=config.GEMINI_API_KEY)

# ✅ 2. Initialize the model
# Choose "gemini-1.5-flash" (fast & free) or "gemini-1.5-pro" (more powerful)
MODEL_NAME = config.GEMINI_MODEL if hasattr(config, "GEMINI_MODEL") else "gemini-1.5-flash"
model = genai.GenerativeModel(MODEL_NAME)

# ✅ 3. System prompt (controls EchoYou’s personality and tone)
SYSTEM_PROMPT = """
You are EchoYou — an empathetic, concise, voice-first communication coach.
Your purpose is to help the user improve their communication skills, speaking clarity, and confidence.

Guidelines:
- Keep responses short and natural (1–4 sentences) unless asked for detailed explanation.
- Sound conversational and supportive, like a mentor.
- If user asks questions, answer clearly and practically.
- If context from previous conversation is relevant, use it.
- Occasionally offer small actionable tips or encouragement.
"""

def _build_prompt_from_history(history: list, user_text: str) -> str:
    """
    Build a single conversation string from previous turns.
    This is fed to Gemini as part of the context.
    """
    conversation = [f"System: {SYSTEM_PROMPT}\n"]
    for turn in history:
        if turn["role"] == "user":
            conversation.append(f"User: {turn['content']}")
        else:
            conversation.append(f"EchoYou: {turn['content']}")
    conversation.append(f"User: {user_text}")
    conversation.append("EchoYou:")
    return "\n".join(conversation)


def ask_gemini(history: list, user_text: str) -> str:
    """
    Generate a reply from Gemini using conversation history (in RAM).
    Args:
        history (list): [{'role': 'user'/'assistant', 'content': '...'}]
        user_text (str): latest user message
    Returns:
        str: Gemini's reply text
    """
    try:
        prompt = _build_prompt_from_history(history, user_text)

        # Generate the response
        response = model.generate_content(prompt)

        # Extract clean text
        reply = response.text.strip() if response and response.text else "I’m here, but I didn’t catch that. Can you repeat?"
        return reply

    except Exception as e:
        # Handle errors gracefully
        return f"⚠️ Oops, something went wrong with Gemini: {str(e)}"


# ✅ Optional: Quick local test
if __name__ == "__main__":
    # Just for debugging locally, won’t run in Streamlit
    test_history = [
        {"role": "user", "content": "Hi EchoYou!"},
        {"role": "assistant", "content": "Hello there! I'm here to help you improve how you speak."}
    ]
    reply = ask_gemini(test_history, "How can I sound more confident while talking?")
    print("EchoYou:", reply)
