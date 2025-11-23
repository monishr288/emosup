"""
Flask API server for the React/Next frontend

Changes:
- Lazy-import heavy modules so the API can boot even if Python deps are missing
- Flight check returns HTTP 200 always with granular status (ready/degraded)
- Direct Ollama connectivity probe without requiring LangChain/LLM init
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import urllib.request
import urllib.error
import socket
import config

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Initialize chatbot and emotion analyzer (singleton instances)
chatbot = None
emotion_analyzer = None
therapy_system = None
memory_system = None

def get_chatbot():
    """Get or create chatbot instance without crashing on import errors"""
    global chatbot
    if chatbot is None:
        try:
            # Lazy import to avoid failing API boot when deps are missing
            from chatbot import EmotionalSupportChatbot  # type: ignore
        except Exception as e:
            print(f"Error importing chatbot module: {e}")
            return None
        try:
            chatbot = EmotionalSupportChatbot()
        except Exception as e:
            print(f"Error initializing chatbot: {e}")
            return None
    return chatbot

def get_emotion_analyzer():
    """Get or create emotion analyzer instance without crashing on import errors"""
    global emotion_analyzer
    if emotion_analyzer is None:
        try:
            from emotion_analyzer import EmotionAnalyzer  # type: ignore
        except Exception as e:
            print(f"Error importing emotion analyzer: {e}")
            return None
        try:
            emotion_analyzer = EmotionAnalyzer()
        except Exception as e:
            print(f"Error initializing emotion analyzer: {e}")
            return None
    return emotion_analyzer

def check_ollama_connection(timeout: float = 1.0):
    """Probe Ollama HTTP API directly without third-party deps.

    Returns a dict with status and message.
    """
    base = config.OLLAMA_BASE_URL.rstrip("/")
    url = f"{base}/api/tags"  # lightweight list of installed models
    req = urllib.request.Request(url, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            if 200 <= resp.status < 300:
                try:
                    data = json.loads(resp.read().decode("utf-8") or "{}")
                    models = [m.get("name", "") for m in data.get("models", [])]
                except Exception:
                    models = []
                return {
                    "status": "connected",
                    "message": "Ollama connection is active",
                    "models": models,
                }
            return {
                "status": "degraded",
                "message": f"Ollama responded with status {resp.status}",
            }
    except (urllib.error.URLError, socket.timeout) as e:
        return {
            "status": "disconnected",
            "message": f"Cannot connect to Ollama at {base}: {e}",
        }

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint; always returns 200 with granular components."""
    status = {
        "status": "healthy",
        "api_server": "running",
        "chatbot": "unknown",
        "ollama": "unknown",
        "message": "API server is running",
    }

    # Check Ollama first (does not require LangChain)
    ollama = check_ollama_connection()
    status["ollama"] = ollama.get("status", "unknown")

    # Check chatbot status (may require LangChain)
    try:
        bot = get_chatbot()
        status["chatbot"] = "ready" if bot else "not_initialized"
        if not bot and status["ollama"] != "connected":
            status["status"] = "degraded"
            status["message"] = "API OK; LLM not ready. Check Ollama and model install."
    except Exception as e:
        status["chatbot"] = "error"
        status["status"] = "degraded"
        status["message"] = f"Chatbot error: {str(e)}"

    return jsonify(status), 200

@app.route('/api/flight-check', methods=['GET'])
def flight_check():
    """Comprehensive flight check for all services; always 200 with status fields."""
    checks = {
        "timestamp": __import__('datetime').datetime.now().isoformat(),
        "services": {}
    }

    # API server
    checks["services"]["api_server"] = {
        "status": "online",
        "message": "Flask API server is running"
    }

    # Ollama status (does not require LangChain)
    ollama = check_ollama_connection()
    checks["services"]["ollama"] = ollama

    # Chatbot status (lazy init)
    try:
        bot = get_chatbot()
        if bot:
            checks["services"]["chatbot"] = {
                "status": "ready",
                "message": "Chatbot is initialized and ready"
            }
        else:
            checks["services"]["chatbot"] = {
                "status": "not_ready",
                "message": "Chatbot not initialized. Check Ollama service."
            }
    except Exception as e:
        checks["services"]["chatbot"] = {
            "status": "error",
            "message": f"Error initializing chatbot: {str(e)}"
        }

    # Overall
    all_ready = (
        checks["services"].get("api_server", {}).get("status") == "online"
        and checks["services"].get("ollama", {}).get("status") == "connected"
        and checks["services"].get("chatbot", {}).get("status") == "ready"
    )
    checks["overall_status"] = "ready" if all_ready else "degraded"
    checks["message"] = "All systems operational" if all_ready else "Some services are not ready"

    return jsonify(checks), 200

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages from frontend"""
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({"error": "Message is required"}), 400
        
        # Get chatbot instance
        bot = get_chatbot()
        if bot is None:
            return jsonify({
                "response": "I apologize, but I'm having trouble connecting to the AI service right now. Please make sure Ollama is running.",
                "error": "Chatbot initialization failed"
            }), 500
        
        # Get chatbot response
        response_data = bot.get_response(message)
        
        # Optionally analyze emotion
        analyzer = get_emotion_analyzer()
        if analyzer:
            analysis = analyzer.analyze_text(message)
            response_data['emotion'] = analysis.get('primary_emotion')
            response_data['sentiment'] = analysis.get('sentiment', {})
            response_data['coping_suggestion'] = analysis.get('coping_suggestion')
        
        return jsonify({
            "response": response_data.get("response", "I'm here for you. Can you tell me more?"),
            "emotion": response_data.get("emotion"),
            "is_crisis": response_data.get("is_crisis", False),
            "coping_suggestion": response_data.get("coping_suggestion")
        })
        
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        return jsonify({
            "response": "I'm sorry, I encountered an error. Please try again.",
            "error": str(e)
        }), 500

@app.route('/api/therapy', methods=['POST'])
def therapy_session():
    """Advanced therapy endpoint with multi-agent system and long-term memory"""
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        session_id = data.get('session_id', 'default-session')

        if not message:
            return jsonify({"error": "Message is required"}), 400

        # Lazy-load therapy system
        global therapy_system
        if therapy_system is None:
            try:
                from therapy_agent_system import TherapySystem
                therapy_system = TherapySystem()
            except Exception as e:
                print(f"Error loading therapy system: {e}")
                return jsonify({
                    "response": "I'm here for you. Can you tell me more about what you're feeling?",
                    "error": "Therapy system unavailable, using fallback"
                }), 200

        # Lazy-load memory system
        global memory_system
        if memory_system is None:
            try:
                from memory_system import LongTermMemorySystem
                memory_system = LongTermMemorySystem()
            except Exception as e:
                print(f"Error loading memory system: {e}")
                # Continue without memory - not critical

        # Get emotion analysis
        analyzer = get_emotion_analyzer()
        emotion = "neutral"
        emotion_intensity = 0.5

        if analyzer:
            analysis = analyzer.analyze_text(message)
            emotion = analysis.get('primary_emotion', 'neutral')

            # Calculate intensity from sentiment polarity
            polarity = analysis.get('sentiment', {}).get('polarity', 0)
            emotion_intensity = abs(polarity)  # 0-1 scale

        # Get user ID (anonymous but consistent)
        user_id = None
        continuity_prompt = None
        if memory_system:
            user_id = memory_system.get_anonymous_user_id(session_id)

            # Get session summary for continuity
            try:
                import asyncio
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                summary = loop.run_until_complete(memory_system.get_session_summary(user_id))
                continuity_prompt = summary.get('continuity_prompt')
                loop.close()
            except Exception as e:
                print(f"Error getting session summary: {e}")

        # Process through therapy system
        result = therapy_system.process_input(message, emotion, emotion_intensity)

        # Add continuity prompt if this is a returning user
        response_text = result.get("response", "")
        if continuity_prompt and therapy_system.therapist.context.conversation_depth == 1:
            response_text = f"{continuity_prompt}\n\n{response_text}"

        # Save to memory
        if memory_system and user_id:
            try:
                import asyncio
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(memory_system.remember(
                    user_id=user_id,
                    session_id=session_id,
                    message=message,
                    emotion=emotion,
                    emotion_intensity=emotion_intensity,
                    therapy_mode=result.get("therapy_mode", "supportive"),
                    detected_patterns=result.get("detected_distortions", []),
                    breakthroughs=[],
                    concerns=[]
                ))
                loop.close()
            except Exception as e:
                print(f"Error saving memory: {e}")

        return jsonify({
            "response": response_text,
            "emotion": emotion,
            "therapy_mode": result.get("therapy_mode"),
            "session_phase": result.get("session_phase"),
            "is_crisis": result.get("is_crisis", False),
            "voice_tone": result.get("voice_tone"),
            "suggested_techniques": result.get("suggested_techniques", []),
            "detected_distortions": result.get("detected_distortions", [])
        })

    except Exception as e:
        print(f"Error in therapy endpoint: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            "response": "I'm here to listen and support you. What's on your mind?",
            "error": str(e)
        }), 200  # Return 200 so frontend doesn't break

@app.route('/api/reset', methods=['POST'])
def reset_conversation():
    """Reset the conversation"""
    try:
        bot = get_chatbot()
        if bot:
            bot.reset_conversation()

        global therapy_system
        if therapy_system:
            # Reset therapy system
            from therapy_agent_system import TherapySystem
            therapy_system = TherapySystem()

        return jsonify({"status": "success", "message": "Conversation reset"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("Starting Flask API server on http://localhost:5000")
    print("Make sure Ollama is running with the Gemma model installed:")
    print("  ollama pull gemma2:2b")
    app.run(debug=True, port=5000, host='0.0.0.0')
