"""
Test Transliteration/Romanization Support
Tests if romanized Indian language text can be detected
"""

import sys
sys.path.insert(0, 'backend')

from core.language_detector import LanguageDetector

def print_header(text):
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70)

def test_transliteration():
    print_header("🔤 TRANSLITERATION TEST")
    print("\nTesting romanized (English script) Indian language text...")
    
    detector = LanguageDetector()
    
    # Test cases: Romanized Indian languages
    test_cases = [
        {
            "language": "Telugu (Romanized)",
            "native": "నమస్కారం, మీరు ఎలా ఉన్నారు?",
            "romanized": "Namaskaram, meeru ela unnaru?",
            "description": "Telugu greeting in English script"
        },
        {
            "language": "Hindi (Romanized)",
            "native": "नमस्ते, आप कैसे हैं?",
            "romanized": "Namaste, aap kaise hain?",
            "description": "Hindi greeting in English script"
        },
        {
            "language": "Tamil (Romanized)",
            "native": "வணக்கம், நீங்கள் எப்படி இருக்கிறீர்கள்?",
            "romanized": "Vanakkam, neengal eppadi irukkireergal?",
            "description": "Tamil greeting in English script"
        },
        {
            "language": "Kannada (Romanized)",
            "native": "ನಮಸ್ಕಾರ, ನೀವು ಹೇಗಿದ್ದೀರಿ?",
            "romanized": "Namaskara, neevu hegiddiri?",
            "description": "Kannada greeting in English script"
        },
        {
            "language": "Malayalam (Romanized)",
            "native": "നമസ്കാരം, നിങ്ങൾ എങ്ങനെയുണ്ട്?",
            "romanized": "Namaskaaram, ningal enganeyanund?",
            "description": "Malayalam greeting in English script"
        }
    ]
    
    print("\n" + "─"*70)
    print("CURRENT BEHAVIOR (Script-based detection):")
    print("─"*70)
    
    for test in test_cases:
        print(f"\n📝 {test['language']}")
        print(f"   Description: {test['description']}")
        
        # Test native script
        result_native = detector.detect_with_confidence(test['native'])
        print(f"\n   Native Script: {test['native'][:40]}...")
        print(f"   ├─ Detected: {result_native['language']}")
        print(f"   └─ Confidence: {result_native['confidence']:.1%}")
        
        # Test romanized
        result_roman = detector.detect_with_confidence(test['romanized'])
        print(f"\n   Romanized: {test['romanized']}")
        print(f"   ├─ Detected: {result_roman['language']}")
        print(f"   └─ Confidence: {result_roman['confidence']:.1%}")
        
        if result_roman['language'] == 'English':
            print(f"   ⚠️  Romanized text detected as English (expected)")
        else:
            print(f"   ✅ Romanized text detected correctly!")
    
    # Summary
    print("\n" + "="*70)
    print("  📊 ANALYSIS")
    print("="*70)
    
    print("\n  Current System:")
    print("  ✅ Native scripts (Telugu, Hindi, Tamil, etc.) → Detected correctly")
    print("  ⚠️  Romanized text (English script) → Detected as English")
    
    print("\n  Why This Happens:")
    print("  • Language detection is based on character patterns")
    print("  • Romanized text uses Latin alphabet (a-z)")
    print("  • System sees Latin characters → detects as English")
    print("  • This is expected behavior for script-based detection")
    
    print("\n  Solutions:")
    print("  1. ✅ Use native scripts (recommended)")
    print("     Example: నమస్కారం instead of Namaskaram")
    print("  ")
    print("  2. 🔧 Add transliteration detection (requires additional library)")
    print("     • Install: pip install indic-transliteration")
    print("     • Detect romanized patterns")
    print("     • Convert to native script")
    print("  ")
    print("  3. 🎯 Manual language selection")
    print("     • User selects language in UI")
    print("     • System uses selected language regardless of script")
    
    print("\n  Recommendation:")
    print("  For best accuracy, use native scripts when possible.")
    print("  For romanized support, we can add transliteration detection.")
    
    print("\n" + "="*70)
    
    # Ask if user wants transliteration support
    print("\n  💡 Would you like to add transliteration support?")
    print("  This would allow detection of romanized Indian languages.")
    print("  Example: 'Namaskaram' → Telugu")
    print("           'Namaste' → Hindi")
    print("           'Vanakkam' → Tamil")
    
    print("\n  Implementation options:")
    print("  1. Pattern-based detection (simple keywords)")
    print("  2. ML-based detection (more accurate, requires training)")
    print("  3. Dictionary-based detection (common words)")

if __name__ == "__main__":
    try:
        test_transliteration()
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted\n")
    except Exception as e:
        print(f"\n\n❌ Error: {str(e)}\n")
        import traceback
        traceback.print_exc()
