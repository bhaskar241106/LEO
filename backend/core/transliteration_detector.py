"""
Transliteration Detector
Detects romanized Indian language text (e.g., "Namaskaram" → Telugu)
"""

import logging
import re

logger = logging.getLogger("DEAR.TransliterationDetector")

class TransliterationDetector:
    """
    Detects romanized (Latin script) Indian language text
    Uses keyword matching and pattern recognition
    """
    
    # Common words/greetings in romanized form
    LANGUAGE_KEYWORDS = {
        'Telugu': [
            'namaskaram', 'meeru', 'ela', 'unnaru', 'cheppandi',
            'dhanyavadalu', 'bagunnara', 'emi', 'chesaru',
            'nenu', 'miru', 'adi', 'idi', 'akkada', 'ikkada',
            'epudu', 'ekkada', 'ela', 'enduku', 'evaru',
            'kavali', 'kavalenu', 'cheyandi', 'cheyyandi', 'vastanu',
            'vachanu', 'poyanu', 'tintanu', 'tinnanu', 'chustunnanu',
            'chesanu', 'chestanu', 'chestunnanu', 'antunnanu', 'ananu',
            'telusu', 'teliyadu', 'artham', 'arthamindi', 'manchidi',
            'baaledhu', 'baagundi', 'chaala', 'konchem', 'ekkuva'
        ],
        'Hindi': [
            'namaste', 'namaskar', 'aap', 'kaise', 'hain', 'kya',
            'dhanyavaad', 'shukriya', 'theek', 'achha', 'bahut',
            'main', 'tum', 'yeh', 'woh', 'kahan', 'kab', 'kyun',
            'kaun', 'kuch', 'sab', 'abhi', 'phir'
        ],
        'Tamil': [
            'vanakkam', 'nandri', 'neengal', 'eppadi', 'irukkireergal',
            'naan', 'neenga', 'enna', 'eppadi', 'enga', 'eppo',
            'yaar', 'yen', 'ungalukku', 'enakku'
        ],
        'Kannada': [
            'namaskara', 'dhanyavada', 'neevu', 'hegiddiri', 'hegiddeera',
            'naanu', 'nimma', 'yaava', 'yelli', 'yaake', 'yaaru',
            'eshtu', 'hege', 'illi', 'alli'
        ],
        'Malayalam': [
            'namaskaaram', 'nanni', 'ningal', 'enganeyanund', 'sukhamaano',
            'njaan', 'ningal', 'enthu', 'engane', 'evide', 'eppol',
            'aar', 'enthukond', 'ningalkku', 'enikku'
        ],
        'Bengali': [
            'nomoshkar', 'dhonnobad', 'apni', 'kemon', 'achen',
            'ami', 'tumi', 'ki', 'kothay', 'kobe', 'keno', 'ke',
            'apnar', 'amar'
        ],
        'Marathi': [
            'namaskar', 'dhanyavaad', 'tumhi', 'kase', 'aahat',
            'mi', 'tu', 'kay', 'kuthe', 'kevha', 'ka', 'kon',
            'tumcha', 'maza'
        ],
        'Gujarati': [
            'namaste', 'aabhar', 'tame', 'kem', 'cho',
            'hun', 'tame', 'shu', 'kyaan', 'kyaare', 'kyun', 'kon',
            'tamaru', 'maru'
        ],
        'Punjabi': [
            'sat sri akal', 'shukriya', 'tusi', 'kivein', 'ho',
            'main', 'tussi', 'ki', 'kithe', 'kado', 'kyun', 'kaun',
            'tuhada', 'mera'
        ]
    }
    
    # Character patterns specific to romanized Indian languages
    PATTERNS = {
        'Telugu': [
            r'\b(namaskaram|meeru|ela|unnaru|cheppandi)\b',
            r'\b(dhanyavadalu|bagunnara)\b'
        ],
        'Hindi': [
            r'\b(namaste|namaskar|aap|kaise|hain)\b',
            r'\b(dhanyavaad|shukriya|theek|achha)\b'
        ],
        'Tamil': [
            r'\b(vanakkam|nandri|neengal|eppadi)\b',
            r'\b(irukkireergal|ungalukku)\b'
        ],
        'Kannada': [
            r'\b(namaskara|dhanyavada|neevu|hegiddiri)\b',
            r'\b(hegiddeera|nimma)\b'
        ],
        'Malayalam': [
            r'\b(namaskaaram|nanni|ningal|enganeyanund)\b',
            r'\b(sukhamaano|ningalkku)\b'
        ]
    }
    
    def __init__(self):
        logger.info("Transliteration Detector initialized")
        # Compile patterns for efficiency
        self.compiled_patterns = {}
        for lang, patterns in self.PATTERNS.items():
            self.compiled_patterns[lang] = [
                re.compile(pattern, re.IGNORECASE) for pattern in patterns
            ]
    
    def detect_romanized_language(self, text: str) -> dict:
        """
        Detects if text is romanized Indian language
        Returns dict with language and confidence
        """
        if not text or len(text.strip()) < 3:
            return {'language': None, 'confidence': 0.0, 'is_romanized': False}
        
        text_lower = text.lower()
        scores = {}
        
        # Check keywords for each language
        for language, keywords in self.LANGUAGE_KEYWORDS.items():
            score = 0
            matched_words = []
            
            # Count keyword matches
            for keyword in keywords:
                if keyword in text_lower:
                    score += 1
                    matched_words.append(keyword)
            
            # Check pattern matches
            if language in self.compiled_patterns:
                for pattern in self.compiled_patterns[language]:
                    if pattern.search(text_lower):
                        score += 2  # Patterns get higher weight
            
            if score > 0:
                scores[language] = {
                    'score': score,
                    'matched_words': matched_words
                }
        
        # Find language with highest score
        if scores:
            best_lang = max(scores.items(), key=lambda x: x[1]['score'])
            language = best_lang[0]
            score_data = best_lang[1]
            
            # Calculate confidence (normalize score)
            max_possible_score = len(text_lower.split())
            confidence = min(score_data['score'] / max(max_possible_score, 1), 1.0)
            
            logger.info(f"Detected romanized {language}: {score_data['matched_words']}")
            
            return {
                'language': language,
                'confidence': confidence,
                'is_romanized': True,
                'matched_words': score_data['matched_words'],
                'score': score_data['score']
            }
        
        return {'language': None, 'confidence': 0.0, 'is_romanized': False}
    
    def is_likely_romanized(self, text: str) -> bool:
        """
        Quick check if text is likely romanized Indian language
        """
        result = self.detect_romanized_language(text)
        return result['is_romanized'] and result['confidence'] > 0.3
    
    def get_supported_languages(self) -> list:
        """
        Returns list of languages supported for transliteration detection
        """
        return list(self.LANGUAGE_KEYWORDS.keys())

# Global instance
transliteration_detector = TransliterationDetector()
