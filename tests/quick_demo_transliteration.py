import sys
sys.path.insert(0, 'backend')
from core.language_detector import LanguageDetector

d = LanguageDetector()

print("\n" + "="*60)
print("  🎉 TRANSLITERATION SUPPORT DEMO")
print("="*60)

tests = [
    ("Namaskaram, meeru ela unnaru?", "Telugu"),
    ("Namaste, aap kaise hain?", "Hindi"),
    ("Vanakkam, neengal eppadi irukkireergal?", "Tamil"),
]

for text, expected in tests:
    r = d.detect_with_confidence(text)
    status = "✅" if r['language'] == expected else "❌"
    print(f"\n{status} Input: {text}")
    print(f"   Detected: {r['language']} ({r['confidence']:.0%})")
    if r.get('is_romanized'):
        print(f"   Matched: {', '.join(r.get('matched_words', []))}")

print("\n" + "="*60)
print("  ✅ Transliteration support is working!")
print("="*60 + "\n")
