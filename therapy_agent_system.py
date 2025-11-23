"""
Advanced Multi-Agent Therapy System
Combines multiple specialized agents for comprehensive emotional support
"""
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum
import random

# Import advanced therapy frameworks
try:
    from advanced_therapy_frameworks import AdvancedTherapyFrameworks
    ADVANCED_FRAMEWORKS_AVAILABLE = True
except Exception as e:
    print(f"Advanced frameworks not available: {e}")
    ADVANCED_FRAMEWORKS_AVAILABLE = False


class TherapyMode(Enum):
    """Different therapeutic approaches"""
    SUPPORTIVE = "supportive"  # Pure empathy and validation
    CBT = "cbt"  # Cognitive Behavioral Therapy - challenge thoughts
    DBT = "dbt"  # Dialectical Behavior Therapy - emotion regulation
    MOTIVATIONAL = "motivational"  # Motivational interviewing
    SOLUTION_FOCUSED = "solution_focused"  # Focus on solutions, not problems


class SessionPhase(Enum):
    """Current phase of the therapy session"""
    GREETING = "greeting"
    ASSESSMENT = "assessment"  # Understanding the issue
    EXPLORATION = "exploration"  # Deep dive into feelings/thoughts
    INTERVENTION = "intervention"  # Active therapeutic work
    CONSOLIDATION = "consolidation"  # Summarize insights
    CLOSING = "closing"  # End session positively


@dataclass
class TherapeuticContext:
    """Context for therapeutic conversation"""
    current_emotion: str
    emotion_intensity: float  # 0-1 scale
    session_phase: SessionPhase
    therapy_mode: TherapyMode
    identified_distortions: List[str]  # Cognitive distortions
    user_goals: List[str]
    session_insights: List[str]
    conversation_depth: int  # How many exchanges in current topic


class TherapistAgent:
    """Main therapist agent that coordinates therapy session"""

    def __init__(self):
        self.context = TherapeuticContext(
            current_emotion="neutral",
            emotion_intensity=0.5,
            session_phase=SessionPhase.GREETING,
            therapy_mode=TherapyMode.SUPPORTIVE,
            identified_distortions=[],
            user_goals=[],
            session_insights=[],
            conversation_depth=0
        )

        # Initialize advanced frameworks if available
        self.advanced_frameworks = None
        if ADVANCED_FRAMEWORKS_AVAILABLE:
            try:
                self.advanced_frameworks = AdvancedTherapyFrameworks()
            except Exception as e:
                print(f"Could not initialize advanced frameworks: {e}")

        # Therapeutic knowledge base
        self.cognitive_distortions = {
            "all_or_nothing": {
                "keywords": ["always", "never", "every time", "no one", "everyone"],
                "description": "Seeing things in black and white",
                "challenge": "Are there any exceptions? Has there been a time when this wasn't true?"
            },
            "overgeneralization": {
                "keywords": ["always happens", "typical", "never works"],
                "description": "Drawing broad conclusions from single events",
                "challenge": "Is this really true every single time? What about the times it went differently?"
            },
            "catastrophizing": {
                "keywords": ["disaster", "terrible", "worst", "end of the world", "can't handle"],
                "description": "Expecting the worst possible outcome",
                "challenge": "What's the most realistic outcome? How have you handled difficult situations before?"
            },
            "should_statements": {
                "keywords": ["should", "must", "ought to", "have to"],
                "description": "Rigid rules about how things should be",
                "challenge": "Where did this rule come from? What would be more flexible?"
            },
            "emotional_reasoning": {
                "keywords": ["I feel like", "feels true", "seems like"],
                "description": "Believing feelings reflect reality",
                "challenge": "What's the evidence for and against this? What would you tell a friend?"
            }
        }

        self.cbt_techniques = {
            "thought_challenging": [
                "What evidence do you have for this thought?",
                "What evidence contradicts this thought?",
                "What would you tell a friend in this situation?",
                "Is this thought helping you or hurting you?",
                "What's a more balanced way to look at this?"
            ],
            "behavioral_activation": [
                "What's one small thing you could do today that might help?",
                "What activities used to bring you joy?",
                "What would taking care of yourself look like right now?",
                "What's the smallest first step you could take?"
            ],
            "mindfulness": [
                "Can you take a moment to notice what you're feeling in your body right now?",
                "What are you noticing in this moment?",
                "Let's ground ourselves - what can you see, hear, and feel around you?",
                "Can you observe that thought without judging it?"
            ]
        }

        self.validation_statements = [
            "What you're feeling makes complete sense given what you're going through.",
            "Your emotions are valid and deserve to be acknowledged.",
            "It's understandable that you feel this way.",
            "Anyone in your situation would likely feel similar emotions.",
            "Thank you for trusting me with these difficult feelings.",
            "It takes courage to be this honest about how you're feeling."
        ]

        self.empathic_reflections = [
            "It sounds like you're feeling {emotion} because {reason}.",
            "I hear that {situation} is really {emotion} for you.",
            "What I'm sensing is that you feel {emotion} when {trigger}.",
            "It seems like underneath the {surface_emotion}, there's also {deeper_emotion}."
        ]

    def detect_cognitive_distortions(self, user_input: str) -> List[str]:
        """Identify cognitive distortions in user's thinking"""
        user_lower = user_input.lower()
        detected = []

        for distortion_name, distortion_data in self.cognitive_distortions.items():
            for keyword in distortion_data["keywords"]:
                if keyword in user_lower:
                    detected.append(distortion_name)
                    break

        return list(set(detected))  # Remove duplicates

    def choose_therapy_mode(self, emotion: str, intensity: float) -> TherapyMode:
        """Decide which therapeutic approach to use"""

        # High intensity emotions need supportive approach first
        if intensity > 0.8:
            return TherapyMode.SUPPORTIVE

        # Anxious emotions benefit from CBT
        if emotion in ["anxious", "worried", "stressed"]:
            return TherapyMode.CBT

        # Anger/frustration benefits from DBT emotion regulation
        if emotion in ["angry", "frustrated", "irritated"]:
            return TherapyMode.DBT

        # Low motivation benefits from motivational interviewing
        if emotion in ["tired", "unmotivated", "hopeless"]:
            return TherapyMode.MOTIVATIONAL

        # Default to supportive
        return TherapyMode.SUPPORTIVE

    def generate_therapeutic_response(
        self,
        user_input: str,
        emotion: str,
        emotion_intensity: float
    ) -> Dict[str, Any]:
        """Generate appropriate therapeutic response"""

        # Update context
        self.context.current_emotion = emotion
        self.context.emotion_intensity = emotion_intensity
        self.context.conversation_depth += 1

        # Detect cognitive distortions
        distortions = self.detect_cognitive_distortions(user_input)
        self.context.identified_distortions.extend(distortions)

        # Choose therapy mode
        self.context.therapy_mode = self.choose_therapy_mode(emotion, emotion_intensity)

        # Build response based on mode and phase
        response_parts = []

        # 1. ALWAYS start with validation
        validation = random.choice(self.validation_statements)
        response_parts.append(validation)

        # 2. Empathic reflection
        reflection = self._generate_reflection(user_input, emotion)
        if reflection:
            response_parts.append(reflection)

        # 3. Therapeutic intervention based on mode
        intervention = self._generate_intervention(user_input, distortions)
        response_parts.append(intervention)

        # 4. Socratic question or behavioral suggestion
        follow_up = self._generate_follow_up(emotion, distortions)
        response_parts.append(follow_up)

        full_response = " ".join(response_parts)

        return {
            "response": full_response,
            "therapy_mode": self.context.therapy_mode.value,
            "session_phase": self.context.session_phase.value,
            "detected_distortions": distortions,
            "suggested_techniques": self._suggest_techniques(emotion),
            "voice_tone": self._determine_voice_tone(emotion, emotion_intensity)
        }

    def _generate_reflection(self, user_input: str, emotion: str) -> str:
        """Generate empathic reflection of what user said"""

        reflections = [
            f"It sounds like you're carrying a lot of {emotion} right now.",
            f"I can hear how {emotion} this situation is making you feel.",
            f"What you're describing sounds really {emotion}.",
            f"I sense that you're feeling quite {emotion} about this."
        ]

        return random.choice(reflections)

    def _generate_intervention(self, user_input: str, distortions: List[str]) -> str:
        """Generate therapeutic intervention"""

        # Try advanced frameworks if available and conversation is deep enough
        if self.advanced_frameworks and self.context.conversation_depth >= 2:
            try:
                advanced_intervention = self.advanced_frameworks.select_framework(
                    user_input=user_input,
                    emotion=self.context.current_emotion,
                    conversation_depth=self.context.conversation_depth
                )
                if advanced_intervention and advanced_intervention.prompt:
                    return advanced_intervention.prompt
            except Exception as e:
                print(f"Error using advanced frameworks: {e}")
                # Fall through to basic interventions

        # Basic interventions (fallback or early in conversation)
        if self.context.therapy_mode == TherapyMode.CBT and distortions:
            # Address cognitive distortion
            distortion = distortions[0]
            challenge = self.cognitive_distortions[distortion]["challenge"]
            return f"I notice you might be {self.cognitive_distortions[distortion]['description']}. {challenge}"

        elif self.context.therapy_mode == TherapyMode.SUPPORTIVE:
            # Pure support and normalization
            return "These feelings are a natural response to what you're experiencing. You're not alone in feeling this way."

        elif self.context.therapy_mode == TherapyMode.DBT:
            # Emotion regulation
            return "Let's work on accepting and regulating these intense emotions. They're valid, and we can learn to sit with them without being overwhelmed."

        elif self.context.therapy_mode == TherapyMode.MOTIVATIONAL:
            # Build motivation
            return "What matters most to you? Even in this difficult moment, what values do you want to honor?"

        else:
            # Solution-focused
            return "When was a time you handled something similar? What helped you then?"

    def _generate_follow_up(self, emotion: str, distortions: List[str]) -> str:
        """Generate follow-up question or suggestion"""

        if self.context.conversation_depth < 3:
            # Still exploring - ask open questions
            questions = [
                "Can you tell me more about what led to these feelings?",
                "What's been the hardest part of this for you?",
                "How long have you been feeling this way?",
                "What do you think you need most right now?"
            ]
            return random.choice(questions)

        else:
            # Ready for action - suggest techniques
            technique = random.choice(self.cbt_techniques["thought_challenging"])
            return technique

    def _suggest_techniques(self, emotion: str) -> List[str]:
        """Suggest specific coping techniques"""

        techniques = {
            "anxious": ["Box breathing (4-4-4-4)", "Progressive muscle relaxation", "Grounding 5-4-3-2-1", "Worry time technique"],
            "sad": ["Behavioral activation", "Gratitude journaling", "Reach out to support", "Self-compassion exercise"],
            "angry": ["STOP skill (DBT)", "Opposite action", "Time-out strategy", "Physical release (exercise)"],
            "lonely": ["Schedule social activity", "Join online community", "Volunteer", "Self-companionship"],
            "tired": ["Sleep hygiene", "Energy conservation", "Gentle movement", "Nutrition check"],
            "neutral": ["Mindfulness practice", "Values clarification", "Goal setting", "Self-reflection"]
        }

        return techniques.get(emotion, techniques["neutral"])

    def _determine_voice_tone(self, emotion: str, intensity: float) -> Dict[str, Any]:
        """Determine appropriate voice characteristics for TTS"""

        # Base parameters
        base_tone = {
            "pitch": 0.0,  # -1 to 1
            "speed": 1.0,  # 0.5 to 2.0
            "warmth": 0.8,  # 0 to 1 (how warm/caring)
            "energy": 0.5   # 0 to 1 (how energetic)
        }

        # Adjust based on user's emotion
        if emotion in ["sad", "lonely", "tired"]:
            base_tone["speed"] = 0.85  # Slower, more gentle
            base_tone["warmth"] = 0.95
            base_tone["energy"] = 0.3
            base_tone["pitch"] = -0.1  # Slightly lower

        elif emotion in ["anxious", "stressed"]:
            base_tone["speed"] = 0.9  # Calm and steady
            base_tone["warmth"] = 0.9
            base_tone["energy"] = 0.4

        elif emotion == "angry":
            base_tone["speed"] = 0.8  # Very slow and measured
            base_tone["warmth"] = 0.85
            base_tone["energy"] = 0.3
            base_tone["pitch"] = -0.2  # Lower, calming

        elif emotion == "happy":
            base_tone["speed"] = 1.1  # Slightly upbeat
            base_tone["warmth"] = 1.0
            base_tone["energy"] = 0.7
            base_tone["pitch"] = 0.1  # Slightly higher

        # Adjust for intensity
        if intensity > 0.8:
            # Very intense emotions - extra slow and gentle
            base_tone["speed"] *= 0.9
            base_tone["warmth"] = min(1.0, base_tone["warmth"] + 0.1)

        return base_tone


class MemoryAgent:
    """Maintains long-term memory of user's patterns, progress, and history"""

    def __init__(self):
        self.user_profile = {
            "frequent_emotions": {},
            "triggers": [],
            "coping_strategies_tried": [],
            "goals": [],
            "progress_notes": [],
            "therapeutic_alliance_score": 0.5  # 0-1
        }

    def update_emotion_pattern(self, emotion: str):
        """Track emotional patterns over time"""
        if emotion not in self.user_profile["frequent_emotions"]:
            self.user_profile["frequent_emotions"][emotion] = 0
        self.user_profile["frequent_emotions"][emotion] += 1

    def add_insight(self, insight: str):
        """Record therapeutic insight"""
        self.user_profile["progress_notes"].append({
            "insight": insight,
            "timestamp": "now"  # Would use actual timestamp
        })

    def get_summary(self) -> str:
        """Generate summary of user's journey"""
        most_common_emotion = max(
            self.user_profile["frequent_emotions"].items(),
            key=lambda x: x[1],
            default=("neutral", 0)
        )[0]

        return f"Most common emotion: {most_common_emotion}. {len(self.user_profile['progress_notes'])} insights recorded."


class CrisisAgent:
    """Specialized agent for crisis intervention"""

    CRISIS_KEYWORDS = [
        "suicide", "suicidal", "kill myself", "end my life",
        "want to die", "better off dead", "harm myself",
        "no point", "can't go on"
    ]

    def assess_crisis_level(self, user_input: str) -> Dict[str, Any]:
        """Assess if user is in crisis"""
        user_lower = user_input.lower()

        crisis_detected = any(keyword in user_lower for keyword in self.CRISIS_KEYWORDS)

        if crisis_detected:
            return {
                "is_crisis": True,
                "severity": "high",
                "immediate_response": self._generate_crisis_response(),
                "escalate": True
            }

        return {
            "is_crisis": False,
            "severity": "none",
            "escalate": False
        }

    def _generate_crisis_response(self) -> str:
        """Generate appropriate crisis response"""
        return """I'm really concerned about what you're sharing, and I want you to know that your life has value and meaning. What you're feeling right now is temporary, even though it doesn't feel that way.

Please reach out to immediate support:
• National Suicide Prevention Lifeline: 988 (US) - Available 24/7
• Crisis Text Line: Text HOME to 741741
• International: https://www.iasp.info/resources/Crisis_Centres/

I care about your safety. Can you tell me - are you currently safe? Do you have someone nearby you can talk to right now?"""


# Main orchestrator
class TherapySystem:
    """Orchestrates all therapy agents"""

    def __init__(self):
        self.therapist = TherapistAgent()
        self.memory = MemoryAgent()
        self.crisis = CrisisAgent()

    def process_input(
        self,
        user_input: str,
        emotion: str,
        emotion_intensity: float
    ) -> Dict[str, Any]:
        """Process user input through all agents"""

        # 1. Crisis check first
        crisis_assessment = self.crisis.assess_crisis_level(user_input)
        if crisis_assessment["is_crisis"]:
            return {
                "response": crisis_assessment["immediate_response"],
                "is_crisis": True,
                "therapy_mode": "crisis",
                "voice_tone": {
                    "pitch": -0.2,
                    "speed": 0.8,
                    "warmth": 1.0,
                    "energy": 0.4
                }
            }

        # 2. Update memory
        self.memory.update_emotion_pattern(emotion)

        # 3. Generate therapeutic response
        response = self.therapist.generate_therapeutic_response(
            user_input,
            emotion,
            emotion_intensity
        )

        return response


# Example usage
if __name__ == "__main__":
    therapy_system = TherapySystem()

    # Test scenarios
    test_inputs = [
        ("I feel like I always mess everything up", "sad", 0.7),
        ("I'm so anxious about the future", "anxious", 0.8),
        ("Nobody cares about me", "lonely", 0.9),
    ]

    for user_input, emotion, intensity in test_inputs:
        print(f"\n{'='*60}")
        print(f"USER: {user_input}")
        print(f"EMOTION: {emotion} (intensity: {intensity})")
        print(f"{'='*60}")

        result = therapy_system.process_input(user_input, emotion, intensity)

        print(f"\nTHERAPIST ({result['therapy_mode']} mode):")
        print(result['response'])
        print(f"\nVoice Tone: {result['voice_tone']}")
        if result.get('detected_distortions'):
            print(f"Distortions: {result['detected_distortions']}")
