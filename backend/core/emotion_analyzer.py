"""
Emotion Analyzer - Detects emotions from text responses
Maps emotions to avatar expressions and animations
"""

import re
import logging

logger = logging.getLogger("DEAR.EmotionAnalyzer")

class EmotionAnalyzer:
    def __init__(self):
        # Emotion keywords and patterns
        self.emotion_patterns = {
            "happy": {
                "keywords": ["happy", "great", "wonderful", "excellent", "amazing", "fantastic", 
                           "glad", "pleased", "delighted", "joy", "excited", "awesome", "love",
                           "😊", "😄", "😃", "🎉", "✨", "👍"],
                "expression": "happy",
                "animation": "dance",
                "intensity": 0.8
            },
            "sad": {
                "keywords": ["sad", "sorry", "unfortunately", "regret", "apologize", "disappointed",
                           "unhappy", "upset", "down", "depressed", "crying", "tears",
                           "😢", "😞", "😔", "💔"],
                "expression": "sad",
                "animation": "cry",
                "intensity": 0.7
            },
            "angry": {
                "keywords": ["angry", "mad", "furious", "annoyed", "frustrated", "irritated",
                           "rage", "upset", "outraged", "😠", "😡", "💢"],
                "expression": "angry",
                "animation": "shake_head",
                "intensity": 0.9
            },
            "surprised": {
                "keywords": ["wow", "amazing", "incredible", "unbelievable", "shocking", "surprised",
                           "astonishing", "remarkable", "extraordinary", "😮", "😲", "🤯"],
                "expression": "surprised",
                "animation": "jump",
                "intensity": 0.8
            },
            "thinking": {
                "keywords": ["think", "consider", "analyze", "evaluate", "ponder", "reflect",
                           "hmm", "let me", "perhaps", "maybe", "possibly", "🤔"],
                "expression": "thinking",
                "animation": "tilt_head",
                "intensity": 0.5
            },
            "confused": {
                "keywords": ["confused", "unclear", "don't understand", "not sure", "uncertain",
                           "puzzled", "perplexed", "bewildered", "😕", "🤷"],
                "expression": "confused",
                "animation": "shrug",
                "intensity": 0.6
            },
            "excited": {
                "keywords": ["excited", "thrilled", "enthusiastic", "eager", "pumped", "energetic",
                           "can't wait", "looking forward", "🎊", "🎈", "🚀"],
                "expression": "excited",
                "animation": "bounce",
                "intensity": 0.9
            },
            "calm": {
                "keywords": ["calm", "peaceful", "relaxed", "serene", "tranquil", "composed",
                           "zen", "chill", "😌", "🧘"],
                "expression": "calm",
                "animation": "breathe",
                "intensity": 0.4
            },
            "proud": {
                "keywords": ["proud", "accomplished", "achieved", "success", "victory", "won",
                           "excellent work", "well done", "congratulations", "🏆", "🎖️", "⭐"],
                "expression": "proud",
                "animation": "nod",
                "intensity": 0.7
            },
            "playful": {
                "keywords": ["fun", "playful", "joke", "funny", "hilarious", "laugh", "haha",
                           "lol", "amusing", "entertaining", "😄", "😂", "🤣"],
                "expression": "playful",
                "animation": "wave",
                "intensity": 0.8
            }
        }
        
        # Punctuation-based emotion hints
        self.punctuation_emotions = {
            "!": ("excited", 0.3),
            "?": ("confused", 0.2),
            "...": ("thinking", 0.4),
            "😊": ("happy", 0.9),
            "😢": ("sad", 0.9),
            "😠": ("angry", 0.9),
        }
    
    def analyze(self, text: str):
        """
        Analyze text and return emotion, expression, and animation
        
        Returns:
            dict: {
                "emotion": str,
                "expression": str,
                "animation": str,
                "intensity": float,
                "confidence": float
            }
        """
        if not text:
            return self._default_emotion()
        
        text_lower = text.lower()
        
        # Score each emotion
        emotion_scores = {}
        
        for emotion, config in self.emotion_patterns.items():
            score = 0
            matches = 0
            
            for keyword in config["keywords"]:
                if keyword in text_lower:
                    score += config["intensity"]
                    matches += 1
            
            if matches > 0:
                emotion_scores[emotion] = {
                    "score": score,
                    "matches": matches,
                    "config": config
                }
        
        # Check punctuation
        for punct, (emotion, intensity) in self.punctuation_emotions.items():
            if punct in text:
                if emotion in emotion_scores:
                    emotion_scores[emotion]["score"] += intensity
                else:
                    emotion_scores[emotion] = {
                        "score": intensity,
                        "matches": 1,
                        "config": self.emotion_patterns.get(emotion, self._default_emotion())
                    }
        
        # Determine dominant emotion
        if emotion_scores:
            dominant = max(emotion_scores.items(), key=lambda x: x[1]["score"])
            emotion_name = dominant[0]
            emotion_data = dominant[1]
            
            confidence = min(emotion_data["score"] / 2.0, 1.0)  # Normalize confidence
            
            return {
                "emotion": emotion_name,
                "expression": emotion_data["config"]["expression"],
                "animation": emotion_data["config"]["animation"],
                "intensity": emotion_data["config"]["intensity"],
                "confidence": confidence
            }
        
        # Default to neutral
        return self._default_emotion()
    
    def _default_emotion(self):
        """Return default neutral emotion"""
        return {
            "emotion": "neutral",
            "expression": "neutral",
            "animation": "idle",
            "intensity": 0.5,
            "confidence": 1.0
        }
    
    def get_animation_for_emotion(self, emotion: str):
        """Get animation name for a specific emotion"""
        if emotion in self.emotion_patterns:
            return self.emotion_patterns[emotion]["animation"]
        return "idle"
    
    def get_expression_for_emotion(self, emotion: str):
        """Get expression name for a specific emotion"""
        if emotion in self.emotion_patterns:
            return self.emotion_patterns[emotion]["expression"]
        return "neutral"

# Example usage
if __name__ == "__main__":
    analyzer = EmotionAnalyzer()
    
    test_texts = [
        "I'm so happy to help you today!",
        "I'm sorry, but I can't do that.",
        "Wow! That's amazing!",
        "Hmm, let me think about that...",
        "I don't understand what you mean.",
        "Congratulations on your achievement!",
        "That's hilarious! 😂",
    ]
    
    for text in test_texts:
        result = analyzer.analyze(text)
        print(f"\nText: {text}")
        print(f"Emotion: {result['emotion']} (confidence: {result['confidence']:.2f})")
        print(f"Expression: {result['expression']}")
        print(f"Animation: {result['animation']}")
