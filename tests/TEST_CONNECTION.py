#!/usr/bin/env python3
"""
Quick connection test for Leo AI Assistant
Tests all services and endpoints
"""

import requests
import time
import sys

def test_service(name, url, timeout=2):
    """Test if a service is responding"""
    try:
        response = requests.get(url, timeout=timeout)
        if response.status_code == 200:
            print(f"✅ {name}: Online")
            return True
        else:
            print(f"⚠️  {name}: Responded with status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"❌ {name}: Connection refused (not running)")
        return False
    except requests.exceptions.Timeout:
        print(f"⏱️  {name}: Timeout (slow response)")
        return False
    except Exception as e:
        print(f"❌ {name}: Error - {str(e)}")
        return False

def test_api_endpoint(name, url, method='GET', data=None):
    """Test a specific API endpoint"""
    try:
        if method == 'GET':
            response = requests.get(url, timeout=5)
        elif method == 'POST':
            response = requests.post(url, json=data, timeout=5)
        
        if response.status_code in [200, 201]:
            print(f"  ✅ {name}: OK")
            return True
        else:
            print(f"  ⚠️  {name}: Status {response.status_code}")
            return False
    except Exception as e:
        print(f"  ❌ {name}: {str(e)}")
        return False

def main():
    print("=" * 70)
    print("  Leo AI Assistant - Connection Test")
    print("=" * 70)
    print()
    
    all_good = True
    
    # Test core services
    print("🔌 Testing Core Services...")
    print("-" * 70)
    
    ollama_ok = test_service("Ollama AI Engine", "http://localhost:11434/api/tags")
    backend_ok = test_service("Backend API", "http://localhost:8000/")
    frontend_ok = test_service("Frontend Dev Server", "http://localhost:5173/")
    
    all_good = ollama_ok and backend_ok and frontend_ok
    print()
    
    # Test backend endpoints if backend is running
    if backend_ok:
        print("🔍 Testing Backend Endpoints...")
        print("-" * 70)
        
        test_api_endpoint("Health Check", "http://localhost:8000/api/system/health")
        test_api_endpoint("System Stats", "http://localhost:8000/api/system/stats")
        test_api_endpoint("Chat History", "http://localhost:8000/api/chat/history")
        test_api_endpoint("Notifications", "http://localhost:8000/api/notifications")
        test_api_endpoint("Schedule List", "http://localhost:8000/api/schedule/all")
        
        print()
    
    # Test Ollama models if Ollama is running
    if ollama_ok:
        print("🤖 Testing Ollama Models...")
        print("-" * 70)
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get('models', [])
                if models:
                    print(f"  ✅ Found {len(models)} model(s):")
                    for model in models:
                        print(f"     - {model.get('name', 'unknown')}")
                else:
                    print("  ⚠️  No models found. Run: ollama pull mistral")
            else:
                print(f"  ❌ Failed to get models: Status {response.status_code}")
        except Exception as e:
            print(f"  ❌ Error checking models: {str(e)}")
        print()
    
    # Summary
    print("=" * 70)
    if all_good:
        print("✅ All services are running!")
        print()
        print("You can now:")
        print("  - Open http://localhost:5173 in your browser")
        print("  - Start chatting with the AI assistant")
        print("  - Test the API at http://localhost:8000/docs")
    else:
        print("❌ Some services are not running.")
        print()
        print("To start all services:")
        print("  Option 1: python app_launcher.py")
        print("  Option 2: Run manually:")
        if not ollama_ok:
            print("    - Terminal 1: ollama serve")
        if not backend_ok:
            print("    - Terminal 2: cd backend && venv\\Scripts\\activate && python main.py")
        if not frontend_ok:
            print("    - Terminal 3: cd frontend && npm run dev")
    print("=" * 70)
    
    return 0 if all_good else 1

if __name__ == "__main__":
    sys.exit(main())
