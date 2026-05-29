import logging
from langdetect import detect, detect_langs, LangDetectException

logger = logging.getLogger("DEAR.LanguageDetector")

# Import transliteration detector
try:
    from core.transliteration_detector import transliteration_detector
    TRANSLITERATION_AVAILABLE = True
    logger.info("Transliteration detection enabled")
except ImportError:
    TRANSLITERATION_AVAILABLE = False
    logger.warning("Transliteration detection not available")

class LanguageDetector:
    """
    Detects language from user input to enable multilingual support.
    Supports Indian languages: Hindi, Tamil, Telugu, Kannada, Malayalam, Bengali, etc.
    """
    
    # Language code to full name mapping
    LANGUAGE_MAP = {
        'en': 'English',
        'hi': 'Hindi',
        'ta': 'Tamil',
        'te': 'Telugu',
        'kn': 'Kannada',
        'ml': 'Malayalam',
        'bn': 'Bengali',
        'mr': 'Marathi',
        'gu': 'Gujarati',
        'pa': 'Punjabi',
        'ur': 'Urdu',
        'or': 'Odia',
        'as': 'Assamese',
        'sa': 'Sanskrit'
    }
    
    # TTS voice mapping for eSpeak-NG
    TTS_VOICES = {
        'English': 'en',
        'Hindi': 'hi',
        'Tamil': 'ta',
        'Telugu': 'te',
        'Kannada': 'kn',
        'Malayalam': 'ml',
        'Bengali': 'bn',
        'Marathi': 'mr',
        'Gujarati': 'gu',
        'Punjabi': 'pa',
        'Urdu': 'ur'
    }
    
    def __init__(self):
        logger.info("Language Detector initialized with support for 14 languages")
    
    def detect_language(self, text: str) -> str:
        """
        Detects the language of the given text.
        Returns full language name (e.g., 'Hindi', 'Tamil', 'English')
        Supports both native scripts and romanized text
        """
        try:
            if not text or len(text.strip()) < 3:
                return 'English'
            
            # First try script-based detection
            lang_code = detect(text)
            language = self.LANGUAGE_MAP.get(lang_code, 'English')
            
            # If detected as English, check for romanized Indian languages
            if language == 'English' and TRANSLITERATION_AVAILABLE:
                romanized_result = transliteration_detector.detect_romanized_language(text)
                if romanized_result['is_romanized'] and romanized_result['confidence'] > 0.3:
                    language = romanized_result['language']
                    logger.info(f"Detected romanized {language}: {romanized_result['matched_words']}")
                    return language
            
            logger.info(f"Detected language: {language} ({lang_code})")
            return language
            
        except LangDetectException as e:
            # If script detection fails, try transliteration
            if TRANSLITERATION_AVAILABLE:
                romanized_result = transliteration_detector.detect_romanized_language(text)
                if romanized_result['is_romanized']:
                    logger.info(f"Detected romanized {romanized_result['language']}")
                    return romanized_result['language']
            
            logger.warning(f"Language detection failed: {str(e)}, defaulting to English")
            return 'English'
    
    def detect_with_confidence(self, text: str) -> dict:
        """
        Detects language with confidence scores.
        Returns dict with language and confidence.
        Supports both native scripts and romanized text.
        """
        try:
            if not text or len(text.strip()) < 3:
                return {'language': 'English', 'confidence': 1.0}
            
            # Try script-based detection first
            results = detect_langs(text)
            if results:
                top_result = results[0]
                lang_code = top_result.lang
                confidence = top_result.prob
                language = self.LANGUAGE_MAP.get(lang_code, 'English')
                
                # If detected as English, check for romanized Indian languages
                if language == 'English' and TRANSLITERATION_AVAILABLE:
                    romanized_result = transliteration_detector.detect_romanized_language(text)
                    if romanized_result['is_romanized'] and romanized_result['confidence'] > 0.3:
                        logger.info(f"Detected romanized {romanized_result['language']} with {romanized_result['confidence']:.2%} confidence")
                        return {
                            'language': romanized_result['language'],
                            'confidence': romanized_result['confidence'],
                            'code': lang_code,
                            'is_romanized': True,
                            'matched_words': romanized_result.get('matched_words', [])
                        }
                
                logger.info(f"Detected: {language} with {confidence:.2%} confidence")
                return {
                    'language': language,
                    'confidence': confidence,
                    'code': lang_code,
                    'is_romanized': False
                }
            
            return {'language': 'English', 'confidence': 1.0}
            
        except LangDetectException as e:
            # If script detection fails, try transliteration
            if TRANSLITERATION_AVAILABLE:
                romanized_result = transliteration_detector.detect_romanized_language(text)
                if romanized_result['is_romanized']:
                    return {
                        'language': romanized_result['language'],
                        'confidence': romanized_result['confidence'],
                        'is_romanized': True,
                        'matched_words': romanized_result.get('matched_words', [])
                    }
            
            logger.warning(f"Language detection failed: {str(e)}")
            return {'language': 'English', 'confidence': 1.0}
    
    def get_tts_voice(self, language: str) -> str:
        """
        Returns the appropriate TTS voice code for the given language.
        Used with eSpeak-NG for multilingual text-to-speech.
        """
        return self.TTS_VOICES.get(language, 'en')
    
    def is_indian_language(self, language: str) -> bool:
        """
        Checks if the language is an Indian language.
        """
        indian_languages = [
            'Hindi', 'Tamil', 'Telugu', 'Kannada', 'Malayalam',
            'Bengali', 'Marathi', 'Gujarati', 'Punjabi', 'Urdu',
            'Odia', 'Assamese', 'Sanskrit'
        ]
        return language in indian_languages
    
    def get_supported_languages(self) -> list:
        """
        Returns list of all supported languages.
        """
        return list(self.LANGUAGE_MAP.values())
    
    def get_indian_languages(self) -> list:
        """
        Returns list of supported Indian languages.
        """
        return [
            'Hindi', 'Tamil', 'Telugu', 'Kannada', 'Malayalam',
            'Bengali', 'Marathi', 'Gujarati', 'Punjabi', 'Urdu',
            'Odia', 'Assamese', 'Sanskrit'
        ]
