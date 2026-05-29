from fastapi import APIRouter
from pydantic import BaseModel
import logging

logger = logging.getLogger("DEAR.LanguageRouter")
router = APIRouter()

class LanguageDetectRequest(BaseModel):
    text: str

@router.get("/languages/supported")
async def get_supported_languages():
    """
    Returns list of all supported languages.
    """
    from core.language_detector import LanguageDetector
    detector = LanguageDetector()
    
    return {
        "all_languages": detector.get_supported_languages(),
        "indian_languages": detector.get_indian_languages(),
        "total_count": len(detector.get_supported_languages())
    }

@router.post("/languages/detect")
async def detect_language(request: LanguageDetectRequest):
    """
    Detects the language of the provided text.
    """
    from core.language_detector import LanguageDetector
    detector = LanguageDetector()
    
    result = detector.detect_with_confidence(request.text)
    
    return {
        "text": request.text,
        "detected_language": result['language'],
        "confidence": result.get('confidence', 1.0),
        "language_code": result.get('code', 'en'),
        "is_indian_language": detector.is_indian_language(result['language']),
        "tts_voice": detector.get_tts_voice(result['language'])
    }
