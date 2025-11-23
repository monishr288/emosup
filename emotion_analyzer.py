"""
Emotion detection and sentiment analysis module
"""
from textblob import TextBlob
import config
from typing import Dict, List, Tuple
import random


class EmotionAnalyzer:
    """
    Analyzes user input to detect emotions and sentiment
    """

    def __init__(self):
        """Initialize the emotion analyzer"""
        self.emotion_keywords = config.EMOTION_KEYWORDS
        self.coping_strategies = config.COPING_STRATEGIES

    def analyze_sentiment(self, text: str) -> Dict[str, float]:
        """
        Analyze sentiment using TextBlob

        Args:
            text: User input text

        Returns:
            Dictionary with polarity and subjectivity scores
        """
        try:
            blob = TextBlob(text)
            return {
                "polarity": blob.sentiment.polarity,  # -1 to 1 (negative to positive)
                "subjectivity": blob.sentiment.subjectivity  # 0 to 1 (objective to subjective)
            }
        except Exception as e:
            return {
                "polarity": 0.0,
                "subjectivity": 0.5
            }

    def detect_emotions(self, text: str) -> List[Tuple[str, int]]:
        """
        Detect emotions based on keyword matching

        Args:
            text: User input text

        Returns:
            List of tuples (emotion, count) sorted by count
        """
        text_lower = text.lower()
        emotion_counts = {}

        for emotion, keywords in self.emotion_keywords.items():
            count = sum(1 for keyword in keywords if keyword in text_lower)
            if count > 0:
                emotion_counts[emotion] = count

        # Sort by count (descending)
        sorted_emotions = sorted(emotion_counts.items(), key=lambda x: x[1], reverse=True)
        return sorted_emotions

    def get_primary_emotion(self, text: str) -> str:
        """
        Get the primary detected emotion

        Args:
            text: User input text

        Returns:
            Primary emotion or 'neutral'
        """
        emotions = self.detect_emotions(text)
        if emotions:
            return emotions[0][0]

        # Use sentiment polarity as fallback
        sentiment = self.analyze_sentiment(text)
        polarity = sentiment["polarity"]

        if polarity < -0.3:
            return "sad"
        elif polarity > 0.3:
            return "happy"
        else:
            return "neutral"

    def get_coping_suggestion(self, emotion: str) -> str:
        """
        Get a random coping strategy for the detected emotion

        Args:
            emotion: Detected emotion

        Returns:
            Coping strategy suggestion
        """
        if emotion in self.coping_strategies:
            strategies = self.coping_strategies[emotion]
            return random.choice(strategies)
        return "Take a moment to breathe deeply and be kind to yourself."

    def analyze_text(self, text: str) -> Dict:
        """
        Comprehensive text analysis

        Args:
            text: User input text

        Returns:
            Dictionary containing all analysis results
        """
        sentiment = self.analyze_sentiment(text)
        emotions = self.detect_emotions(text)
        primary_emotion = self.get_primary_emotion(text)
        coping_suggestion = self.get_coping_suggestion(primary_emotion)

        return {
            "sentiment": sentiment,
            "emotions": emotions,
            "primary_emotion": primary_emotion,
            "coping_suggestion": coping_suggestion,
            "mood_label": self._get_mood_label(sentiment["polarity"])
        }

    def _get_mood_label(self, polarity: float) -> str:
        """
        Get mood label based on polarity score

        Args:
            polarity: Sentiment polarity (-1 to 1)

        Returns:
            Mood label
        """
        if polarity < -0.5:
            return "Very Negative"
        elif polarity < -0.1:
            return "Negative"
        elif polarity <= 0.1:
            return "Neutral"
        elif polarity <= 0.5:
            return "Positive"
        else:
            return "Very Positive"
