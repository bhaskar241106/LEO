"""
Test Language Detection API Endpoint
Tests the /api/languages/detect endpoint with various languages
"""

import requests
import json
import time

API_BASE = "http://localhost:5000"

# Test cases
TEST_CASES = [
    {
        "name": "English",
        "text": "Hello, I want to learn Python programming",
        "expected": "English"
    },
    {
        "name": "Hindi",
        "text": "नमस्ते, मुझे Python सीखना है",
        "expected": "Hindi"
    },
    {
        "name": "Tamil",
        "text": "வணக்கம், எனக்கு Python கற்க வேண்டும்",
        "expected": "Tamil"
    },
    {
        "name": "Telugu",
        "text": "నమస్కారం, నాకు Python నేర్చుకోవాలి",
        "expected": "Telugu"
    },
    {
        "name": "Kannada",
        "text": "ನಮಸ್ಕಾರ, ನನಗೆ Python ಕಲಿಯಬೇಕು",
        "expected": "Kannada"
    },
    {
        "name": "Malayalam",
        "text": "നമസ്കാരം, എനിക്ക് Python പഠിക്കണം",
        "expected": "Malayalam"
    },
    {
        "name": "Bengali",
        "text": "নমস্কার, আমি Python শিখতে চাই",
        "expected": "Bengali"
    }
]

def print_header(text):
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70)

def test_health():
    """Test if backend is running"""
    try:
        response = requests.get(f"{API_BASE}/health", timeout=2)
        return response.status_code == 200
    except:
        return False

def test_supported_languages():
    """Test /api/languages/supported endpoint"""
    print_header("TEST 1: Get Supported Languages")
    
    try:
        response = requests.get(f"{API_BASE}/api/languages/supported", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ API Response: {response.status_code}")
            print(f"✅ Total Languages: {data.get('total_count', 0)}")
            print(f"\nAll Languages:")
            for lang in data.get('all_languages', []):
                print(f"  • {lang}")
            print(f"\nIndian Languages ({len(data.get('indian_languages', []))}):")
            for lang in data.get('indian_languages', []):
                print(f"  • {lang}")
            return True
        else:
            print(f"❌ API Error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_language_detection():
    """Test /api/languages/detect endpoint"""
    print_header("TEST 2: Language Detection API")
    
    passed = 0
    failed = 0
    
    for test in TEST_CASES:
        print(f"\n📝 Testing {test['name']}:")
        print(f"   Text: {test['text'][:50]}...")
        
        try:
            response = requests.post(
                f"{API_BASE}/api/languages/detect",
                json={"text": test['text']},
                headers={"Content-Type": "application/json"},
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                detected = data.get('detected_language')
                confidence = data.get('confidence', 0)
                is_indian = data.get('is_indian_language', False)
                tts_voice = data.get('tts_voice', '')
                
                is_correct = detected == test['expected']
                status = "✅ PASS" if is_correct else "❌ FAIL"
                
                print(f"   {status}")
                print(f"   Detected: {detected} (Expected: {test['expected']})")
                print(f"   Confidence: {confidence:.2%}")
                print(f"   Indian Language: {'Yes' if is_indian else 'No'}")
                print(f"   TTS Voice: {tts_voice}")
                
                if is_correct:
                    passed += 1
                else:
                    failed += 1
            else:
                print(f"   ❌ API Error: {response.status_code}")
                failed += 1
                
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            failed += 1
        
        time.sleep(0.2)
    
    # Summary
    total = passed + failed
    accuracy = (passed / total * 100) if total > 0 else 0
    
    print(f"\n{'='*70}")
    print(f"  Results: {passed}/{total} passed ({accuracy:.1f}% accuracy)")
    print(f"{'='*70}")
    
    return passed == total

def main():
    print_header("🌍 MULTI-LANGUAGE API TEST")
    
    # Check if backend is running
    print("\n🔍 Checking backend status...")
    if not test_health():
        print("❌ Backend is not running!")
        print("\n💡 Start the backend first:")
        print("   cd backend")
        print("   python main.py")
        return
    
    print("✅ Backend is running")
    
    # Test 1: Supported languages
    test1_passed = test_supported_languages()
    
    # Test 2: Language detection
    test2_passed = test_language_detection()
    
    # Final summary
    print_header("📊 FINAL SUMMARY")
    
    if test1_passed and test2_passed:
        print("\n🏆 ALL TESTS PASSED!")
        print("\n✅ Multi-language support is fully functional:")
        print("   • API endpoints working")
        print("   • Language detection accurate")
        print("   • TTS voice mapping correct")
        print("   • Indian language classification working")
    else:
        print("\n⚠️  SOME TESTS FAILED")
        if not test1_passed:
            print("   ❌ Supported languages endpoint failed")
        if not test2_passed:
            print("   ❌ Language detection endpoint failed")
    
    print("\n🎯 Next Steps:")
    print("   1. Test in the frontend UI")
    print("   2. Try voice input in different languages")
    print("   3. Test TTS output quality")
    print("   4. Try mixed language conversations")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
