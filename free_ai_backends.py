"""
Free AI Backend Alternatives
No Ollama needed! Uses free API tiers from multiple providers
"""
import os
import json
from typing import Dict, Any, Optional
import urllib.request
import urllib.error


class FreeAIBackend:
    """Manages multiple free AI API backends as fallback"""

    def __init__(self):
        self.backends = [
            GroqBackend(),
            HuggingFaceBackend(),
            TogetherBackend(),
            FallbackResponses()  # Always works, no API needed
        ]
        self.current_backend_index = 0

    def get_response(self, prompt: str, emotion_hint: str = "") -> str:
        """Try each backend in order until one works"""

        for i, backend in enumerate(self.backends):
            try:
                response = backend.generate(prompt, emotion_hint)
                if response:
                    self.current_backend_index = i
                    return response
            except Exception as e:
                print(f"{backend.name} failed: {e}")
                continue

        # If all fail, use fallback
        return self.backends[-1].generate(prompt, emotion_hint)


class GroqBackend:
    """
    FREE tier: 30 requests/minute, no credit card needed!
    Get API key: https://console.groq.com/keys
    """
    name = "Groq (Free)"

    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY", "")
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
        self.model = "llama-3.3-70b-versatile"  # Fast and free!

    def generate(self, prompt: str, emotion_hint: str = "") -> Optional[str]:
        if not self.api_key:
            return None

        therapeutic_prompt = f"""You are an empathetic AI therapist. The user is feeling {emotion_hint or 'neutral'}.

Guidelines:
- Start with validation and empathy
- Ask thoughtful follow-up questions
- Offer gentle support and coping strategies
- Be warm, caring, and non-judgmental
- Keep responses concise (2-3 sentences)

User: {prompt}

Therapist:"""

        data = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are a warm, empathetic therapist."},
                {"role": "user", "content": therapeutic_prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 200
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        req = urllib.request.Request(
            self.api_url,
            data=json.dumps(data).encode(),
            headers=headers,
            method="POST"
        )

        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                result = json.loads(response.read().decode())
                return result["choices"][0]["message"]["content"].strip()
        except Exception as e:
            print(f"Groq API error: {e}")
            return None


class HuggingFaceBackend:
    """
    FREE tier: Rate limited but no signup required for some models
    """
    name = "HuggingFace (Free)"

    def __init__(self):
        self.api_key = os.getenv("HF_API_KEY", "")
        # Free inference API - no key needed for some models
        self.api_url = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"

    def generate(self, prompt: str, emotion_hint: str = "") -> Optional[str]:
        # DialoGPT works without API key (rate limited)
        data = {
            "inputs": f"User is feeling {emotion_hint}. {prompt}",
            "parameters": {
                "max_length": 150,
                "temperature": 0.7,
                "do_sample": True
            }
        }

        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        req = urllib.request.Request(
            self.api_url,
            data=json.dumps(data).encode(),
            headers=headers,
            method="POST"
        )

        try:
            with urllib.request.urlopen(req, timeout=15) as response:
                result = json.loads(response.read().decode())
                if isinstance(result, list) and len(result) > 0:
                    return result[0].get("generated_text", "").strip()
        except Exception as e:
            print(f"HuggingFace API error: {e}")
            return None


class TogetherBackend:
    """
    FREE $25 credit on signup!
    Get API key: https://api.together.xyz/
    """
    name = "Together.ai (Free Credit)"

    def __init__(self):
        self.api_key = os.getenv("TOGETHER_API_KEY", "")
        self.api_url = "https://api.together.xyz/v1/chat/completions"
        self.model = "meta-llama/Llama-3-8b-chat-hf"

    def generate(self, prompt: str, emotion_hint: str = "") -> Optional[str]:
        if not self.api_key:
            return None

        therapeutic_prompt = f"""You are a compassionate therapist. User emotion: {emotion_hint or 'neutral'}

Be empathetic, validating, and supportive. Ask caring follow-up questions.

User: {prompt}

Therapist:"""

        data = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are an empathetic AI therapist."},
                {"role": "user", "content": therapeutic_prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 200
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        req = urllib.request.Request(
            self.api_url,
            data=json.dumps(data).encode(),
            headers=headers,
            method="POST"
        )

        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                result = json.loads(response.read().decode())
                return result["choices"][0]["message"]["content"].strip()
        except Exception as e:
            print(f"Together API error: {e}")
            return None


class FallbackResponses:
    """
    Always works! No API, no internet needed
    Uses our therapeutic response system
    """
    name = "Built-in Therapy (Always Available)"

    def generate(self, prompt: str, emotion_hint: str = "") -> str:
        """Returns therapeutic response based on emotion"""

        responses = {
            "sad": "I hear that you're feeling down, and I want you to know that your feelings are completely valid. It's okay to feel sad sometimes. Remember that difficult emotions are temporary, and you have the strength to get through this. Is there something specific that's been weighing on you?",

            "anxious": "I can sense that you're feeling anxious right now, and I want to remind you that you're not alone in this feeling. Anxiety can be overwhelming, but you've gotten through moments like this before, and you will again. Try taking a few deep breaths with me. What's on your mind that's causing you to feel this way?",

            "lonely": "Feeling lonely can be really hard, and I'm truly sorry you're experiencing this. Please know that your feelings matter, and you deserve connection and companionship. Even though it might not feel like it right now, there are people who care about you. What would help you feel a little less alone right now?",

            "angry": "I can tell you're feeling frustrated or angry, and those feelings are completely understandable. It's important to acknowledge your emotions rather than push them away. You have every right to feel upset. Would it help to talk about what's making you feel this way?",

            "tired": "It sounds like you're feeling exhausted, and that must be really difficult. Remember to be gentle with yourself - it's okay to rest and take things one step at a time. You don't have to push through everything right now. What's been draining your energy lately?",

            "happy": "I'm so glad to hear there's some positivity in your day! It's wonderful that you're experiencing moments of happiness. Those bright spots are important, even when life feels challenging. What's bringing you joy today?",

            "stressed": "I can hear how stressed you're feeling right now. That pressure you're under is real, and it makes sense that you feel overwhelmed. Let's take this one step at a time. What feels most urgent to you right now?",

            "overwhelmed": "Feeling overwhelmed is such a difficult experience. When everything feels like too much, remember that you don't have to handle it all at once. Let's break this down together. What's one small thing that might help right now?",

            "hopeless": "I'm really glad you're sharing this with me. Feelings of hopelessness are incredibly painful, but I want you to know that these feelings, as real as they are right now, are temporary. You've made it through difficult times before. What has helped you in the past when things felt dark?",

            "neutral": "I'm here to listen and support you. Sometimes we just need someone to talk to, and that's perfectly okay. How are you really feeling right now? What's been on your mind?"
        }

        # Get response for emotion, default to neutral
        response = responses.get(emotion_hint.lower(), responses["neutral"])

        # Add therapeutic element
        therapeutic_additions = [
            "\n\nRemember: You're doing the best you can, and that's enough.",
            "\n\nTake a moment to be kind to yourself right now.",
            "\n\nYour feelings are valid, and you deserve support.",
            "\n\nIt's okay to not be okay sometimes.",
            "\n\nYou're stronger than you know."
        ]

        # Randomly add one (deterministically based on emotion)
        import hashlib
        hash_val = int(hashlib.md5(emotion_hint.encode()).hexdigest(), 16)
        addition = therapeutic_additions[hash_val % len(therapeutic_additions)]

        return response + addition


# Example usage and testing
if __name__ == "__main__":
    print("Testing Free AI Backends...\n")

    backend = FreeAIBackend()

    test_cases = [
        ("I'm feeling really anxious about everything", "anxious"),
        ("I feel so lonely and isolated", "lonely"),
        ("Everything makes me angry lately", "angry"),
    ]

    for message, emotion in test_cases:
        print(f"\n{'='*60}")
        print(f"USER ({emotion}): {message}")
        print(f"{'='*60}")

        response = backend.get_response(message, emotion)
        print(f"\nTHERAPIST: {response}")
        print(f"\nBackend used: {backend.backends[backend.current_backend_index].name}")
