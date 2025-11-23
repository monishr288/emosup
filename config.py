"""
Configuration file for the Emotional Assistance Chatbot
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Ollama Configuration
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
MODEL_NAME = os.getenv("MODEL_NAME", "gemma2:2b")

# Application Settings
APP_TITLE = os.getenv("APP_TITLE", "Emotional Support Companion")
SESSION_TIMEOUT = int(os.getenv("SESSION_TIMEOUT", "3600"))

# Emotion Detection Keywords
EMOTION_KEYWORDS = {
    "sad": ["sad", "down", "depressed", "unhappy", "miserable", "heartbroken", "grief"],
    "anxious": ["anxious", "worried", "nervous", "stressed", "panic", "fear", "scared"],
    "lonely": ["lonely", "alone", "isolated", "disconnected", "empty", "abandoned"],
    "angry": ["angry", "mad", "furious", "irritated", "frustrated", "upset"],
    "happy": ["happy", "joy", "excited", "great", "wonderful", "amazing", "good"],
    "tired": ["tired", "exhausted", "drained", "fatigued", "weary", "burned out"]
}

# Coping Strategies
COPING_STRATEGIES = {
    "sad": [
        "Try taking a short walk outside to get some fresh air",
        "Listen to your favorite uplifting music",
        "Reach out to a friend or family member",
        "Write down three things you're grateful for today",
        "Watch a comforting movie or show"
    ],
    "anxious": [
        "Practice deep breathing: inhale for 4 counts, hold for 4, exhale for 4",
        "Try the 5-4-3-2-1 grounding technique",
        "Do some gentle stretching or yoga",
        "Limit caffeine and stay hydrated",
        "Focus on what you can control right now"
    ],
    "lonely": [
        "Join an online community about your interests",
        "Video call someone you care about",
        "Volunteer for a cause you believe in",
        "Take a class or workshop to meet new people",
        "Spend time in public spaces like cafes or libraries"
    ],
    "angry": [
        "Take a 10-minute timeout to cool down",
        "Do some physical exercise to release tension",
        "Write down your feelings without judgment",
        "Practice progressive muscle relaxation",
        "Count backwards from 10 slowly"
    ],
    "tired": [
        "Ensure you're getting 7-9 hours of sleep",
        "Take a 20-minute power nap if possible",
        "Stay hydrated throughout the day",
        "Limit screen time before bed",
        "Try a short meditation or relaxation exercise"
    ]
}

# System Prompts
SYSTEM_PROMPT = """You are an empathetic and supportive emotional assistance chatbot designed to help people who feel lonely or need emotional support.

Your core principles:
1. Be warm, compassionate, and non-judgmental
2. Listen actively and validate emotions
3. Ask thoughtful follow-up questions to understand better
4. Offer gentle encouragement and hope
5. Suggest healthy coping strategies when appropriate
6. Never diagnose or replace professional mental health care
7. If someone expresses suicidal thoughts or severe crisis, encourage them to contact emergency services or crisis hotlines

Your tone should be:
- Caring and supportive
- Understanding and patient
- Conversational and friendly
- Professional but not clinical
- Hopeful and encouraging

Remember: Your goal is to provide companionship, emotional support, and help users feel heard and less alone."""

CRISIS_KEYWORDS = [
    "suicide", "suicidal", "kill myself", "end my life",
    "want to die", "better off dead", "harm myself"
]

CRISIS_RESPONSE = """I'm really concerned about what you're sharing. Your life matters, and there are people who want to help you through this difficult time.

Please reach out to a crisis helpline immediately:
- National Suicide Prevention Lifeline: 988 (US)
- Crisis Text Line: Text HOME to 741741
- International Association for Suicide Prevention: https://www.iasp.info/resources/Crisis_Centres/

If you're in immediate danger, please call emergency services (911 in US) or go to your nearest emergency room.

I'm here to talk, but I'm not equipped to handle crisis situations. Professional help can make a real difference."""
