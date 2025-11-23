"""
Core chatbot implementation using LangChain and Ollama

Enhancements:
- Windowed conversation memory to reduce context growth
- Emotion-aware prompt that leverages analyzer hints when available
"""
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferWindowMemory
import config
from typing import Optional, Dict, Any


class EmotionalSupportChatbot:
    """
    Main chatbot class that handles emotional support conversations
    """

    def __init__(self):
        """Initialize the chatbot with Ollama and LangChain"""
        self.llm = self._initialize_llm()
        self.memory = ConversationBufferWindowMemory(
            memory_key="chat_history",
            return_messages=True,
            k=6,
        )
        self.conversation_chain = self._create_conversation_chain()

    def _initialize_llm(self) -> Ollama:
        """Initialize Ollama LLM with Gemma model (optional now!)"""
        try:
            llm = Ollama(
                base_url=config.OLLAMA_BASE_URL,
                model=config.MODEL_NAME,
                temperature=0.7,
            )
            return llm
        except Exception as e:
            # Ollama not available - will use free backends!
            print(f"Ollama not available: {str(e)}")
            print("✓ Using free AI backends instead!")
            return None

    def _create_conversation_chain(self) -> LLMChain:
        """Create the conversation chain with prompt template"""
        prompt_template = PromptTemplate(
            input_variables=["chat_history", "user_input", "emotion_hint", "coping_suggestion"],
            template=f"""{config.SYSTEM_PROMPT}

Context (optional):
- Detected primary emotion: {{emotion_hint}}
- Suggested coping strategy: {{coping_suggestion}}

Previous conversation:
{{chat_history}}

User: {{user_input}}

Assistant instructions:
- Respond with warmth and validation first.
- If the emotion indicates distress (sad, anxious, lonely, angry, tired), include one short practical tip (optionally using the suggestion) in a separate sentence, prefixed with "Tip:".
- Ask exactly one gentle follow-up question at the end to keep the conversation going.
"""
        )

        chain = LLMChain(
            llm=self.llm,
            prompt=prompt_template,
            memory=self.memory,
            verbose=False
        )
        return chain

    def check_crisis(self, user_input: str) -> bool:
        """Check if user input contains crisis keywords"""
        user_input_lower = user_input.lower()
        return any(keyword in user_input_lower for keyword in config.CRISIS_KEYWORDS)

    def get_response(self, user_input: str) -> Dict[str, Any]:
        """
        Get chatbot response for user input

        Args:
            user_input: User's message

        Returns:
            Dictionary containing response and metadata
        """
        # Check for crisis situation
        is_crisis = self.check_crisis(user_input)

        if is_crisis:
            return {
                "response": config.CRISIS_RESPONSE,
                "is_crisis": True,
                "emotion": "crisis"
            }

        try:
            # Optional emotion-aware context
            emotion_hint = ""
            coping_suggestion = ""
            try:
                from emotion_analyzer import EmotionAnalyzer  # lazy import
                analyzer = EmotionAnalyzer()
                analysis = analyzer.analyze_text(user_input)
                emotion_hint = analysis.get("primary_emotion", "") or ""
                coping_suggestion = analysis.get("coping_suggestion", "") or ""
            except Exception:
                # Analyzer not available; proceed without hints
                pass

            # Get response from conversation chain
            response = self.conversation_chain.predict(
                user_input=user_input,
                emotion_hint=emotion_hint,
                coping_suggestion=coping_suggestion,
            )

            return {
                "response": response.strip(),
                "is_crisis": False,
                "emotion": None
            }
        except Exception as e:
            # Fallback to emotion-based supportive responses when LLM unavailable
            fallback_responses = {
                "sad": "I hear that you're feeling down, and I want you to know that your feelings are completely valid. It's okay to feel sad sometimes. Remember that difficult emotions are temporary, and you have the strength to get through this. Is there something specific that's been weighing on you?",
                "anxious": "I can sense that you're feeling anxious right now, and I want to remind you that you're not alone in this feeling. Anxiety can be overwhelming, but you've gotten through moments like this before, and you will again. Try taking a few deep breaths with me. What's on your mind that's causing you to feel this way?",
                "lonely": "Feeling lonely can be really hard, and I'm truly sorry you're experiencing this. Please know that your feelings matter, and you deserve connection and companionship. Even though it might not feel like it right now, there are people who care about you. What would help you feel a little less alone right now?",
                "angry": "I can tell you're feeling frustrated or angry, and those feelings are completely understandable. It's important to acknowledge your emotions rather than push them away. You have every right to feel upset. Would it help to talk about what's making you feel this way?",
                "tired": "It sounds like you're feeling exhausted, and that must be really difficult. Remember to be gentle with yourself - it's okay to rest and take things one step at a time. You don't have to push through everything right now. What's been draining your energy lately?",
                "happy": "I'm so glad to hear there's some positivity in your day! It's wonderful that you're experiencing moments of happiness. Those bright spots are important, even when life feels challenging. What's bringing you joy today?",
                "neutral": "I'm here to listen and support you. Sometimes we just need someone to talk to, and that's perfectly okay. How are you really feeling right now? What's been on your mind?"
            }

            # Use emotion-based fallback response
            response_text = fallback_responses.get(
                emotion_hint if emotion_hint else "neutral",
                "I'm here for you and I'm listening. Even when things feel difficult, please know that your feelings are valid and you're not alone. What's been on your mind lately?"
            )

            return {
                "response": response_text,
                "is_crisis": False,
                "emotion": emotion_hint
            }

    def reset_conversation(self):
        """Reset the conversation history"""
        self.memory.clear()

    def get_conversation_history(self) -> list:
        """Get the current conversation history"""
        return self.memory.buffer_as_messages if hasattr(self.memory, 'buffer_as_messages') else []
