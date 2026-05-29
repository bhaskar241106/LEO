"""
Test Telugu language support
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_telugu_detection():
    """Test Telugu language detection"""
    print("\n" + "="*60)
    print("TEST 1: Telugu Language Detection")
    print("="*60)
    
    test_phrases = [
        "Namaskaram, meeru ela unnaru?",
        "Nenu baagunnanu, dhanyavadalu",
        "Meeku ela help cheyagalanu?",
        "Naku Python nerchukovaalani undi"
    ]
    
    for phrase in test_phrases:
        try:
            response = requests.post(
                f"{BASE_URL}/api/languages/detect",
                json={"text": phrase},
                timeout=5
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"\n✓ Input: {phrase}")
                print(f"  Detected: {result.get('detected_language', 'Unknown')}")
                print(f"  Confidence: {result.get('confidence', 0):.2%}")
                print(f"  Is Romanized: {result.get('is_romanized', False)}")
            else:
                print(f"\n✗ Failed: {phrase}")
                print(f"  Status: {response.status_code}")
        except Exception as e:
            print(f"\n✗ Error: {str(e)}")

def test_telugu_chat():
    """Test Telugu chat responses"""
    print("\n" + "="*60)
    print("TEST 2: Telugu Chat Response")
    print("="*60)
    
    test_messages = [
        {
            "message": "Namaskaram! Meeru ela unnaru?",
            "language": "Telugu"
        },
        {
            "message": "Naku Python programming nerchukovaalani undi. Meeru help cheyagalara?",
            "language": "Telugu"
        }
    ]
    
    for test in test_messages:
        try:
            print(f"\n→ User: {test['message']}")
            
            response = requests.post(
                f"{BASE_URL}/chat",
                json={
                    "message": test['message'],
                    "personality": "Friendly",
                    "language": test['language'],
                    "temperature": 0.85
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"← Leo: {result.get('response', 'No response')}")
                print(f"  Language: {result.get('detected_language', 'Unknown')}")
            else:
                print(f"✗ Failed with status: {response.status_code}")
        except Exception as e:
            print(f"✗ Error: {str(e)}")

def test_image_generation():
    """Test offline image generation"""
    print("\n" + "="*60)
    print("TEST 3: Offline Image Generation")
    print("="*60)
    
    # Check status first
    try:
        response = requests.get(f"{BASE_URL}/api/image/status", timeout=5)
        if response.status_code == 200:
            status = response.json()
            print(f"\n✓ Image Generation Status:")
            print(f"  Available: {status.get('available', False)}")
            print(f"  Backend: {status.get('backend', 'None')}")
            print(f"  Message: {status.get('message', 'Unknown')}")
            
            if status.get('available'):
                print("\n  Testing image generation...")
                print("  (This may take 1-2 minutes on first run)")
                
                gen_response = requests.post(
                    f"{BASE_URL}/api/image/generate",
                    json={
                        "prompt": "a beautiful sunset over mountains",
                        "width": 512,
                        "height": 512,
                        "steps": 15,
                        "enhance_prompt": False
                    },
                    timeout=180
                )
                
                if gen_response.status_code == 200:
                    result = gen_response.json()
                    if result.get('success'):
                        print(f"\n✓ Image generated successfully!")
                        print(f"  Size: {result.get('width')}x{result.get('height')}")
                        print(f"  Prompt: {result.get('prompt')}")
                    else:
                        print(f"\n✗ Generation failed: {result.get('error')}")
                else:
                    print(f"\n✗ Request failed: {gen_response.status_code}")
        else:
            print(f"✗ Status check failed: {response.status_code}")
    except Exception as e:
        print(f"✗ Error: {str(e)}")

def main():
    print("\n" + "="*60)
    print("LEO AI - TELUGU & IMAGE GENERATION TEST SUITE")
    print("="*60)
    print("\nMake sure Leo backend is running on http://localhost:8000")
    input("\nPress Enter to start tests...")
    
    # Test 1: Language Detection
    test_telugu_detection()
    
    # Test 2: Telugu Chat
    test_telugu_chat()
    
    # Test 3: Image Generation
    test_image_generation()
    
    print("\n" + "="*60)
    print("TESTS COMPLETED")
    print("="*60)
    print("\nIf any tests failed, check:")
    print("1. Backend is running (http://localhost:8000)")
    print("2. Ollama is running with gemma:2b model")
    print("3. Python dependencies are installed")
    print("4. GPU drivers are up to date")
    print("\n")

if __name__ == "__main__":
    main()
