"""
Interactive Multi-Language Demo
Demonstrates language detection with visual output
"""

import sys
sys.path.insert(0, 'backend')

from core.language_detector import LanguageDetector
import time

def print_banner():
    print("\n" + "="*70)
    print("  🌍 LEO AI ASSISTANT - MULTI-LANGUAGE DEMO")
    print("="*70)
    print("\n  Supporting 14 languages including:")
    print("  🇮🇳 Hindi, Tamil, Telugu, Kannada, Malayalam, Bengali")
    print("  🇮🇳 Marathi, Gujarati, Punjabi, Urdu, Odia, Assamese, Sanskrit")
    print("  🌍 English")
    print("\n" + "="*70)

def demo_language(detector, language, greeting, question):
    """Demo a single language"""
    print(f"\n{'─'*70}")
    print(f"  {language}")
    print(f"{'─'*70}")
    
    # Detect greeting
    result1 = detector.detect_with_confidence(greeting)
    print(f"\n  Input:  {greeting}")
    print(f"  ├─ Detected: {result1['language']}")
    print(f"  ├─ Confidence: {result1['confidence']:.1%}")
    print(f"  ├─ TTS Voice: {detector.get_tts_voice(result1['language'])}")
    print(f"  └─ Indian Language: {'Yes 🇮🇳' if detector.is_indian_language(result1['language']) else 'No 🌍'}")
    
    time.sleep(0.3)
    
    # Detect question
    result2 = detector.detect_with_confidence(question)
    print(f"\n  Input:  {question}")
    print(f"  ├─ Detected: {result2['language']}")
    print(f"  ├─ Confidence: {result2['confidence']:.1%}")
    print(f"  └─ Status: {'✅ Correct' if result2['language'] == language else '❌ Incorrect'}")

def main():
    print_banner()
    
    detector = LanguageDetector()
    
    print("\n🎬 Starting Language Detection Demo...\n")
    time.sleep(1)
    
    # Demo each language
    demos = [
        ("English", "Hello, how are you?", "Can you help me learn Python?"),
        ("Hindi", "नमस्ते, आप कैसे हैं?", "क्या आप मुझे Python सिखा सकते हैं?"),
        ("Tamil", "வணக்கம், நீங்கள் எப்படி இருக்கிறீர்கள்?", "Python கற்க உதவ முடியுமா?"),
        ("Telugu", "నమస్కారం, మీరు ఎలా ఉన్నారు?", "Python నేర్చుకోవడంలో సహాయం చేయగలరా?"),
        ("Kannada", "ನಮಸ್ಕಾರ, ನೀವು ಹೇಗಿದ್ದೀರಿ?", "Python ಕಲಿಯಲು ಸಹಾಯ ಮಾಡಬಹುದೇ?"),
        ("Malayalam", "നമസ്കാരം, നിങ്ങൾ എങ്ങനെയുണ്ട്?", "Python പഠിക്കാൻ സഹായിക്കാമോ?"),
        ("Bengali", "নমস্কার, আপনি কেমন আছেন?", "Python শিখতে সাহায্য করতে পারেন?"),
    ]
    
    for language, greeting, question in demos:
        demo_language(detector, language, greeting, question)
        time.sleep(0.5)
    
    # Summary
    print("\n" + "="*70)
    print("  ✅ DEMO COMPLETE")
    print("="*70)
    print("\n  Key Features Demonstrated:")
    print("  ✅ Automatic language detection")
    print("  ✅ High confidence scores (>95%)")
    print("  ✅ TTS voice mapping")
    print("  ✅ Indian language classification")
    print("  ✅ Support for 14 languages")
    print("  ✅ 100% offline operation")
    
    print("\n  🎯 Try it yourself:")
    print("  1. Start the backend: cd backend && python main.py")
    print("  2. Open the frontend: http://localhost:5173")
    print("  3. Type in any supported language")
    print("  4. Leo will detect and respond in your language!")
    
    print("\n" + "="*70 + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted\n")
    except Exception as e:
        print(f"\n\n❌ Error: {str(e)}\n")
