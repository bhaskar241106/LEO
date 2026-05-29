"""
Comprehensive Multi-Language Support Test
Tests language detection for 14 languages including Indian languages
"""

import sys
sys.path.insert(0, 'backend')

from core.language_detector import LanguageDetector
import time

# Test phrases in different languages
TEST_PHRASES = {
    'English': [
        "Hello, how are you?",
        "I want to learn Python programming",
        "Can you help me with machine learning?"
    ],
    'Hindi': [
        "नमस्ते, आप कैसे हैं?",
        "मुझे Python प्रोग्रामिंग सीखनी है",
        "क्या आप मुझे मशीन लर्निंग में मदद कर सकते हैं?"
    ],
    'Tamil': [
        "வணக்கம், நீங்கள் எப்படி இருக்கிறீர்கள்?",
        "எனக்கு Python நிரலாக்கம் கற்றுக்கொள்ள வேண்டும்",
        "இயந்திர கற்றலில் எனக்கு உதவ முடியுமா?"
    ],
    'Telugu': [
        "నమస్కారం, మీరు ఎలా ఉన్నారు?",
        "నాకు Python ప్రోగ్రామింగ్ నేర్చుకోవాలి",
        "మెషిన్ లెర్నింగ్‌లో మీరు నాకు సహాయం చేయగలరా?"
    ],
    'Kannada': [
        "ನಮಸ್ಕಾರ, ನೀವು ಹೇಗಿದ್ದೀರಿ?",
        "ನನಗೆ Python ಪ್ರೋಗ್ರಾಮಿಂಗ್ ಕಲಿಯಬೇಕು",
        "ಯಂತ್ರ ಕಲಿಕೆಯಲ್ಲಿ ನೀವು ನನಗೆ ಸಹಾಯ ಮಾಡಬಹುದೇ?"
    ],
    'Malayalam': [
        "നമസ്കാരം, നിങ്ങൾ എങ്ങനെയുണ്ട്?",
        "എനിക്ക് Python പ്രോഗ്രാമിംഗ് പഠിക്കണം",
        "മെഷീൻ ലേണിംഗിൽ നിങ്ങൾക്ക് എന്നെ സഹായിക്കാമോ?"
    ],
    'Bengali': [
        "নমস্কার, আপনি কেমন আছেন?",
        "আমি Python প্রোগ্রামিং শিখতে চাই",
        "আপনি কি আমাকে মেশিন লার্নিং এ সাহায্য করতে পারেন?"
    ],
    'Marathi': [
        "नमस्कार, तुम्ही कसे आहात?",
        "मला Python प्रोग्रामिंग शिकायचे आहे",
        "तुम्ही मला मशीन लर्निंगमध्ये मदत करू शकता का?"
    ],
    'Gujarati': [
        "નમસ્તે, તમે કેમ છો?",
        "મારે Python પ્રોગ્રામિંગ શીખવું છે",
        "શું તમે મને મશીન લર્નિંગમાં મદદ કરી શકો છો?"
    ],
    'Punjabi': [
        "ਸਤ ਸ੍ਰੀ ਅਕਾਲ, ਤੁਸੀਂ ਕਿਵੇਂ ਹੋ?",
        "ਮੈਨੂੰ Python ਪ੍ਰੋਗਰਾਮਿੰਗ ਸਿੱਖਣੀ ਹੈ",
        "ਕੀ ਤੁਸੀਂ ਮੈਨੂੰ ਮਸ਼ੀਨ ਲਰਨਿੰਗ ਵਿੱਚ ਮਦਦ ਕਰ ਸਕਦੇ ਹੋ?"
    ]
}

def print_header(text):
    """Print formatted header"""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70)

def print_result(language, phrase, detected, confidence, is_correct):
    """Print test result"""
    status = "✅ PASS" if is_correct else "❌ FAIL"
    print(f"\n{status} | Expected: {language} | Detected: {detected}")
    print(f"   Confidence: {confidence:.2%}")
    print(f"   Text: {phrase[:50]}...")

def main():
    print_header("🌍 MULTI-LANGUAGE SUPPORT TEST")
    print("\nTesting language detection for 14 languages...")
    print("Including: Hindi, Tamil, Telugu, Kannada, Malayalam, Bengali, and more")
    
    # Initialize detector
    detector = LanguageDetector()
    
    # Test 1: List supported languages
    print_header("TEST 1: Supported Languages")
    all_langs = detector.get_supported_languages()
    indian_langs = detector.get_indian_languages()
    
    print(f"\n✅ Total Languages Supported: {len(all_langs)}")
    print(f"✅ Indian Languages: {len(indian_langs)}")
    print(f"\nAll Languages: {', '.join(all_langs)}")
    print(f"\nIndian Languages: {', '.join(indian_langs)}")
    
    # Test 2: Language detection accuracy
    print_header("TEST 2: Language Detection Accuracy")
    
    total_tests = 0
    passed_tests = 0
    failed_tests = []
    
    for expected_lang, phrases in TEST_PHRASES.items():
        print(f"\n📝 Testing {expected_lang}:")
        
        for phrase in phrases:
            total_tests += 1
            
            # Detect with confidence
            result = detector.detect_with_confidence(phrase)
            detected_lang = result['language']
            confidence = result['confidence']
            
            # Check if correct
            is_correct = detected_lang == expected_lang
            
            if is_correct:
                passed_tests += 1
            else:
                failed_tests.append({
                    'expected': expected_lang,
                    'detected': detected_lang,
                    'phrase': phrase,
                    'confidence': confidence
                })
            
            print_result(expected_lang, phrase, detected_lang, confidence, is_correct)
            
            time.sleep(0.1)  # Small delay for readability
    
    # Test 3: TTS Voice Mapping
    print_header("TEST 3: TTS Voice Mapping")
    
    print("\nLanguage → TTS Voice Code:")
    for lang in ['English', 'Hindi', 'Tamil', 'Telugu', 'Kannada', 'Malayalam', 'Bengali']:
        voice_code = detector.get_tts_voice(lang)
        print(f"  {lang:15} → {voice_code}")
    
    # Test 4: Indian Language Detection
    print_header("TEST 4: Indian Language Detection")
    
    test_langs = ['English', 'Hindi', 'Tamil', 'Telugu', 'Spanish', 'French']
    print("\nLanguage Classification:")
    for lang in test_langs:
        is_indian = detector.is_indian_language(lang)
        status = "🇮🇳 Indian" if is_indian else "🌍 International"
        print(f"  {lang:15} → {status}")
    
    # Test 5: Edge Cases
    print_header("TEST 5: Edge Cases")
    
    edge_cases = [
        ("", "Empty string"),
        ("hi", "Too short"),
        ("123456", "Numbers only"),
        ("Hello नमस्ते", "Mixed languages"),
        ("Python JavaScript React", "Technical terms")
    ]
    
    print("\nEdge Case Handling:")
    for text, description in edge_cases:
        result = detector.detect_with_confidence(text)
        print(f"\n  {description}:")
        print(f"    Input: '{text}'")
        print(f"    Detected: {result['language']} ({result['confidence']:.2%})")
    
    # Final Summary
    print_header("📊 TEST SUMMARY")
    
    accuracy = (passed_tests / total_tests * 100) if total_tests > 0 else 0
    
    print(f"\n✅ Total Tests: {total_tests}")
    print(f"✅ Passed: {passed_tests}")
    print(f"❌ Failed: {len(failed_tests)}")
    print(f"📈 Accuracy: {accuracy:.1f}%")
    
    if failed_tests:
        print("\n❌ Failed Tests:")
        for i, fail in enumerate(failed_tests, 1):
            print(f"\n  {i}. Expected: {fail['expected']}, Got: {fail['detected']}")
            print(f"     Confidence: {fail['confidence']:.2%}")
            print(f"     Text: {fail['phrase'][:50]}...")
    
    # Performance Rating
    print("\n" + "="*70)
    if accuracy >= 95:
        print("  🏆 EXCELLENT - Multi-language support is working perfectly!")
    elif accuracy >= 85:
        print("  ✅ GOOD - Multi-language support is working well")
    elif accuracy >= 70:
        print("  ⚠️  FAIR - Some improvements needed")
    else:
        print("  ❌ POOR - Significant issues detected")
    print("="*70)
    
    # Additional Info
    print("\n💡 Notes:")
    print("  • Language detection requires at least 3 characters")
    print("  • Confidence scores above 80% are considered reliable")
    print("  • Mixed language text detects the dominant language")
    print("  • All detection happens offline using langdetect library")
    
    print("\n🎯 Next Steps:")
    print("  1. Test with the backend API: POST /api/languages/detect")
    print("  2. Try chatting in different languages")
    print("  3. Test voice input/output with Indian languages")
    print("  4. Check TTS voice quality for each language")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
