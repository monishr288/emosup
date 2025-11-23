"""
Advanced Therapeutic Frameworks
Professional-grade therapy techniques beyond basic CBT/DBT
"""
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import json


@dataclass
class TherapeuticIntervention:
    """Structured therapeutic intervention"""
    framework: str
    technique: str
    prompt: str
    follow_up: List[str]
    expected_outcome: str


class ACTFramework:
    """
    Acceptance and Commitment Therapy (ACT)
    Focus: Psychological flexibility, values-based living
    """
    name = "Acceptance and Commitment Therapy"

    def __init__(self):
        self.six_core_processes = {
            "acceptance": "Embrace thoughts/feelings without fighting them",
            "cognitive_defusion": "Observe thoughts without believing them",
            "present_moment": "Be here now, fully engaged",
            "self_as_context": "You are more than your thoughts",
            "values": "What truly matters to you?",
            "committed_action": "Take steps toward your values"
        }

        self.metaphors = {
            "passengers_on_bus": "You're the bus driver. Anxious thoughts are passengers. They can be noisy, but you choose where the bus goes.",
            "leaves_on_stream": "Imagine your thoughts as leaves floating down a stream. You can watch them pass by without grabbing onto them.",
            "quicksand": "Fighting anxiety is like struggling in quicksand - it makes you sink deeper. What if you could just... let it be there?",
            "monsters_on_boat": "You're sailing toward what matters. Fears are monsters on the boat. You can't throw them overboard, but you can keep sailing."
        }

    def get_intervention(self, emotion: str, context: str) -> TherapeuticIntervention:
        """Get ACT-based intervention"""

        if emotion in ["anxious", "stressed", "overwhelmed"]:
            return TherapeuticIntervention(
                framework="ACT",
                technique="Cognitive Defusion",
                prompt="I notice you're having the thought that things are overwhelming. Can we try something? Instead of 'I am anxious,' can you say 'I'm noticing thoughts about anxiety'? How does that subtle shift feel?",
                follow_up=[
                    "What would you do right now if anxiety wasn't stopping you?",
                    "What matters to you that's bigger than this fear?",
                    "If you could take one small step toward what you value, what would it be?"
                ],
                expected_outcome="Create distance from anxious thoughts"
            )

        elif emotion in ["sad", "depressed", "hopeless"]:
            return TherapeuticIntervention(
                framework="ACT",
                technique="Values Clarification",
                prompt="Even in this difficult moment, what would you want to stand for? If your life was a book and this chapter is painful, what values would you want the reader to see in your character?",
                follow_up=[
                    "What small action could you take today that aligns with those values?",
                    "Who do you want to be in the face of this pain?",
                    "What matters to you beyond feeling good?"
                ],
                expected_outcome="Connect to life meaning beyond mood"
            )

        else:
            return TherapeuticIntervention(
                framework="ACT",
                technique="Present Moment Awareness",
                prompt="Let's pause. Right now, in this exact moment - what are you noticing? What can you see, hear, feel in your body?",
                follow_up=[
                    "Can you be curious about this feeling rather than judging it?",
                    "What's one thing you can appreciate in this moment?",
                    "How can you be more fully here, right now?"
                ],
                expected_outcome="Ground in present experience"
            )


class SchemaTherapy:
    """
    Schema Therapy (Jeffrey Young)
    Focus: Identify and heal early maladaptive schemas
    """
    name = "Schema Therapy"

    def __init__(self):
        self.early_maladaptive_schemas = {
            "abandonment": "Deep fear that people will leave you",
            "mistrust": "Belief that others will hurt or betray you",
            "emotional_deprivation": "Feeling your needs won't be met",
            "defectiveness": "Believing you're fundamentally flawed",
            "failure": "Belief you're inadequate compared to others",
            "dependence": "Belief you can't handle life alone",
            "vulnerability": "Fear that catastrophe will strike",
            "enmeshment": "Excessive emotional involvement with others",
            "subjugation": "Suppressing your needs to please others",
            "self_sacrifice": "Focusing on others at your expense",
            "unrelenting_standards": "Impossibly high expectations",
            "entitlement": "Belief you're special and rules don't apply"
        }

        self.schema_modes = {
            "vulnerable_child": "Sad, scared, hurt inner child",
            "angry_child": "Furious, rebellious child",
            "detached_protector": "Numb, avoiding emotions",
            "punitive_parent": "Critical, harsh inner voice",
            "healthy_adult": "Balanced, compassionate self"
        }

    def identify_schema(self, user_input: str) -> Optional[str]:
        """Detect potential schema from user's language"""

        patterns = {
            "abandonment": ["everyone leaves", "always left alone", "people abandon me"],
            "defectiveness": ["something wrong with me", "I'm broken", "fundamentally flawed"],
            "failure": ["always fail", "never good enough", "can't succeed"],
            "mistrust": ["can't trust anyone", "people hurt me", "will betray me"],
            "subjugation": ["have to please", "can't say no", "others' needs first"],
            "unrelenting_standards": ["must be perfect", "any mistake", "never enough"]
        }

        input_lower = user_input.lower()
        for schema, keywords in patterns.items():
            if any(keyword in input_lower for keyword in keywords):
                return schema

        return None

    def get_intervention(self, schema: str) -> TherapeuticIntervention:
        """Get schema-focused intervention"""

        interventions = {
            "abandonment": TherapeuticIntervention(
                framework="Schema Therapy",
                technique="Reparenting the Vulnerable Child",
                prompt="It sounds like a deep part of you feels afraid of being left. That makes sense if you've experienced abandonment. Can we explore: what does that scared part of you need to hear right now?",
                follow_up=[
                    "What would you tell a child who felt this way?",
                    "Can you offer that same compassion to yourself?",
                    "What evidence do you have that contradicts this fear?"
                ],
                expected_outcome="Provide corrective emotional experience"
            ),

            "defectiveness": TherapeuticIntervention(
                framework="Schema Therapy",
                technique="Fighting the Punitive Parent",
                prompt="I hear a harsh, critical voice in what you're saying. That voice telling you you're flawed - is that your voice, or someone else's from your past?",
                follow_up=[
                    "What would a compassionate voice say instead?",
                    "If a friend felt this way, would you tell them they're defective?",
                    "Can we challenge that critical voice together?"
                ],
                expected_outcome="Separate from internalized criticism"
            ),

            "unrelenting_standards": TherapeuticIntervention(
                framework="Schema Therapy",
                technique="Relaxing Standards",
                prompt="These standards you're holding yourself to - where did they come from? What would happen if you achieved 'good enough' instead of perfect?",
                follow_up=[
                    "What would you accomplish if perfection wasn't required?",
                    "How much has perfectionism actually helped vs. hurt you?",
                    "Can you give yourself permission to be human?"
                ],
                expected_outcome="Challenge maladaptive perfectionism"
            )
        }

        return interventions.get(schema, self._default_intervention())

    def _default_intervention(self) -> TherapeuticIntervention:
        return TherapeuticIntervention(
            framework="Schema Therapy",
            technique="Schema Awareness",
            prompt="I'm noticing a pattern in what you're sharing. These beliefs you have - where do you think they came from? What experiences shaped them?",
            follow_up=[
                "How has this pattern affected your life?",
                "What would life be like if this weren't true?",
                "Are you ready to challenge this old belief?"
            ],
            expected_outcome="Build schema awareness"
        )


class NarrativeTherapy:
    """
    Narrative Therapy (Michael White, David Epston)
    Focus: Re-authoring life stories, externalizing problems
    """
    name = "Narrative Therapy"

    def get_intervention(self, problem: str, emotion: str) -> TherapeuticIntervention:
        """Externalize the problem"""

        return TherapeuticIntervention(
            framework="Narrative Therapy",
            technique="Externalizing the Problem",
            prompt=f"I notice you're saying 'I am {emotion}' - but what if {emotion} is something visiting you, not who you ARE? Can we give this feeling a name? What would you call it?",
            follow_up=[
                f"When does {emotion.title()} show up most in your life?",
                f"What does {emotion.title()} tell you about yourself?",
                f"Can you remember a time when you stood up to {emotion.title()}?",
                "What are you like when this problem isn't around?",
                "Who in your life knows the real you - the you without this problem?"
            ],
            expected_outcome="Separate identity from problem"
        )

    def unique_outcomes(self, user_input: str) -> List[str]:
        """Find exceptions to the problem narrative"""

        return [
            "Tell me about a time when this problem wasn't as strong. What was different?",
            "When have you managed to do what this problem says you can't?",
            "Who sees you differently than how you see yourself right now?",
            "What does this exception tell you about your abilities?",
            "How can we build on these moments of strength?"
        ]

    def preferred_identity(self) -> List[str]:
        """Questions to build preferred narrative"""

        return [
            "If this problem wasn't dominating your story, who would you be?",
            "What values do you want your life story to reflect?",
            "How do you want to be remembered by people you care about?",
            "What kind of person do you want to become?",
            "If you wrote the next chapter of your life, what would it say?"
        ]


class SolutionFocusedBriefTherapy:
    """
    SFBT (Steve de Shazer, Insoo Kim Berg)
    Focus: Solutions, not problems; future, not past
    """
    name = "Solution-Focused Brief Therapy"

    def miracle_question(self, problem: str) -> TherapeuticIntervention:
        """The famous miracle question"""

        return TherapeuticIntervention(
            framework="SFBT",
            technique="Miracle Question",
            prompt="Let me ask you something powerful: Imagine tonight while you sleep, a miracle happens and this problem is solved. But you don't know the miracle happened because you were asleep. What would be the first small thing you'd notice tomorrow that would tell you something had changed?",
            follow_up=[
                "Who else would notice this change? What would they see?",
                "What would you be doing differently?",
                "On a scale of 1-10, where are you now toward this miracle?",
                "What would it take to move up just one point?",
                "What parts of this miracle are already happening, even a little?"
            ],
            expected_outcome="Envision concrete solutions"
        )

    def scaling_questions(self, issue: str) -> List[str]:
        """Use scaling to measure and motivate"""

        return [
            f"On a scale of 1-10, where 10 is {issue} completely resolved and 1 is the worst it's been - where are you today?",
            "What's kept you from being lower on that scale?",
            "What would one point higher look like?",
            "When were you last at a higher number? What was different then?",
            "What small step could move you up just half a point?"
        ]

    def exception_finding(self) -> List[str]:
        """Find times when problem wasn't happening"""

        return [
            "Tell me about a recent time when this problem was a bit better. What was happening?",
            "What did you do that made it better, even slightly?",
            "How can we make that happen more often?",
            "Who or what helped in those better moments?",
            "What strengths were you using then?"
        ]


class CompassionFocusedTherapy:
    """
    CFT (Paul Gilbert)
    Focus: Self-compassion, soothing system activation
    """
    name = "Compassion-Focused Therapy"

    def compassionate_self(self) -> TherapeuticIntervention:
        """Develop compassionate self-image"""

        return TherapeuticIntervention(
            framework="CFT",
            technique="Compassionate Self Imagery",
            prompt="I want you to imagine your wisest, kindest, most compassionate self. This version of you has deep understanding and infinite patience. What would that compassionate self say to you right now?",
            follow_up=[
                "How would they look at you - with what kind of eyes?",
                "What tone of voice would they use?",
                "What do they understand about your struggle?",
                "Can you feel their warmth toward you?",
                "What do they want you to know?"
            ],
            expected_outcome="Access self-compassion"
        )

    def soothing_rhythm_breathing(self) -> Dict[str, Any]:
        """CFT breathing technique"""

        return {
            "technique": "Soothing Rhythm Breathing",
            "description": "Breathing to activate the parasympathetic nervous system",
            "steps": [
                "Find a comfortable position",
                "Breathe in slowly through your nose for 4-5 counts",
                "Breathe out gently through your mouth for 4-5 counts",
                "Imagine breathing in kindness, breathing out tension",
                "Continue for 2-3 minutes",
                "Notice the slowing of your body"
            ],
            "purpose": "Activate soothing/contentment system"
        }

    def three_circles_model(self) -> Dict[str, str]:
        """Understand the three emotion regulation systems"""

        return {
            "threat_system": "Red - Anxiety, anger, disgust. Protects from danger. Can get stuck 'on'.",
            "drive_system": "Blue - Excitement, seeking, pursuing. Motivates achievement. Can become exhausting.",
            "soothing_system": "Green - Calm, safe, connected. Often under-developed. We need to strengthen this."
        }


class AdvancedTherapyFrameworks:
    """Orchestrates all advanced frameworks"""

    def __init__(self):
        self.act = ACTFramework()
        self.schema = SchemaTherapy()
        self.narrative = NarrativeTherapy()
        self.sfbt = SolutionFocusedBriefTherapy()
        self.cft = CompassionFocusedTherapy()

    def select_framework(
        self,
        emotion: str,
        user_input: str,
        conversation_depth: int
    ) -> TherapeuticIntervention:
        """Intelligently select best framework for situation"""

        # Check for schema indicators
        schema = self.schema.identify_schema(user_input)
        if schema and conversation_depth > 3:
            return self.schema.get_intervention(schema)

        # Use ACT for anxiety/acceptance issues
        if emotion in ["anxious", "overwhelmed", "stressed"] and conversation_depth > 2:
            return self.act.get_intervention(emotion, user_input)

        # Use Narrative for identity/self-concept issues
        if any(word in user_input.lower() for word in ["i am", "always been", "that's just who i am"]):
            return self.narrative.get_intervention(user_input, emotion)

        # Use SFBT for goal-oriented, solution-seeking
        if any(word in user_input.lower() for word in ["help me", "what should i do", "how can i"]):
            return self.sfbt.miracle_question(user_input)

        # Use CFT for self-criticism
        if any(word in user_input.lower() for word in ["hate myself", "worthless", "pathetic", "failure"]):
            return self.cft.compassionate_self()

        # Default to ACT
        return self.act.get_intervention(emotion, user_input)


# Testing
if __name__ == "__main__":
    frameworks = AdvancedTherapyFrameworks()

    test_cases = [
        ("I'm so anxious about everything", "anxious", 3),
        ("Everyone always leaves me", "sad", 4),
        ("I hate myself, I'm such a failure", "sad", 2),
        ("How can I fix this?", "neutral", 1),
    ]

    print("Advanced Therapy Frameworks Test\n" + "="*60)

    for user_input, emotion, depth in test_cases:
        print(f"\nUser: {user_input}")
        print(f"Emotion: {emotion}, Depth: {depth}")
        print("-"*60)

        intervention = frameworks.select_framework(emotion, user_input, depth)

        print(f"Framework: {intervention.framework}")
        print(f"Technique: {intervention.technique}")
        print(f"\nTherapist: {intervention.prompt}")
        print(f"\nFollow-ups:")
        for q in intervention.follow_up[:2]:
            print(f"  • {q}")
