"""
System Health Check Script
Tests all critical components of Leo AI
"""

import sys
import os
import requests
import subprocess

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

def test_backend_health():
    """Test backend API health"""
    try:
        response = requests.get('http://localhost:8000/api/system/health', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Backend Health: ONLINE")
            print(f"   - API: {data.get('api', 'unknown')}")
            print(f"   - Ollama: {data.get('ollama', 'unknown')}")
            print(f"   - GPU: {data.get('gpu', 'unknown')}")
            return True
        else:
            print(f"❌ Backend Health: Failed (Status {response.status_code})")
            return False
    except Exception as e:
        print(f"❌ Backend Health: Not accessible - {e}")
        return False

def test_dependencies():
    """Test Python dependencies"""
    print("\n📦 Testing Dependencies:")
    try:
        import numpy
        print(f"   ✅ NumPy: {numpy.__version__}")
    except Exception as e:
        print(f"   ❌ NumPy: {e}")
        return False
    
    try:
        import diffusers
        print(f"   ✅ Diffusers: {diffusers.__version__}")
    except Exception as e:
        print(f"   ❌ Diffusers: {e}")
        return False
    
    try:
        import transformers
        print(f"   ✅ Transformers: {transformers.__version__}")
    except Exception as e:
        print(f"   ❌ Transformers: {e}")
        return False
    
    try:
        import torch
        print(f"   ✅ PyTorch: {torch.__version__}")
        print(f"   ✅ CUDA Available: {torch.cuda.is_available()}")
    except Exception as e:
        print(f"   ❌ PyTorch: {e}")
        return False
    
    return True

def test_ollama_models():
    """Test Ollama models"""
    print("\n🤖 Testing AI Models:")
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            models = [line.split()[0] for line in lines[1:] if line.strip()]
            
            required_models = ['phi3:mini', 'llama3.2:1b', 'tinyllama:latest']
            for model in required_models:
                if any(model in m for m in models):
                    print(f"   ✅ {model}: Available")
                else:
                    print(f"   ⚠️  {model}: Not found")
            return True
        else:
            print("   ❌ Ollama: Not accessible")
            return False
    except Exception as e:
        print(f"   ❌ Ollama: {e}")
        return False

def test_language_detection():
    """Test language detection"""
    print("\n🌍 Testing Language Detection:")
    try:
        from core.language_detector import LanguageDetector
        detector = LanguageDetector()
        
        tests = [
            ("Hello, how are you?", "English"),
            ("Namaskaram, meeru ela unnaru?", "Telugu"),
            ("Bonjour", "French")
        ]
        
        for text, expected in tests:
            detected = detector.detect_language(text)
            status = "✅" if expected.lower() in detected.lower() else "⚠️"
            print(f"   {status} '{text[:30]}' -> {detected}")
        
        return True
    except Exception as e:
        print(f"   ❌ Language Detection: {e}")
        return False

def test_database():
    """Test database connectivity"""
    print("\n💾 Testing Database:")
    try:
        import sqlite3
        db_path = os.path.join(os.path.dirname(__file__), '..', 'backend', 'data', 'memory.db')
        
        if os.path.exists(db_path):
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Check if tables exist
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            
            print(f"   ✅ Database: Connected")
            print(f"   ✅ Tables: {len(tables)} found")
            
            conn.close()
            return True
        else:
            print("   ⚠️  Database: Will be created on first use")
            return True
    except Exception as e:
        print(f"   ❌ Database: {e}")
        return False

def test_frontend():
    """Test frontend accessibility"""
    print("\n🌐 Testing Frontend:")
    try:
        response = requests.get('http://localhost:5173', timeout=5)
        if response.status_code == 200:
            print("   ✅ Frontend: Accessible at http://localhost:5173")
            return True
        else:
            print(f"   ❌ Frontend: Status {response.status_code}")
            return False
    except Exception as e:
        print(f"   ⚠️  Frontend: Not running - {e}")
        print("   💡 Run START.bat to start the frontend")
        return False

def test_file_structure():
    """Test project file structure"""
    print("\n📁 Testing File Structure:")
    base_path = os.path.join(os.path.dirname(__file__), '..')
    
    required_dirs = [
        'backend',
        'frontend',
        'docs',
        'tests',
        'scripts'
    ]
    
    required_files = [
        'README.md',
        'START.bat',
        'STOP.bat',
        '.gitignore'
    ]
    
    all_good = True
    for dir_name in required_dirs:
        path = os.path.join(base_path, dir_name)
        if os.path.isdir(path):
            print(f"   ✅ {dir_name}/ exists")
        else:
            print(f"   ❌ {dir_name}/ missing")
            all_good = False
    
    for file_name in required_files:
        path = os.path.join(base_path, file_name)
        if os.path.isfile(path):
            print(f"   ✅ {file_name} exists")
        else:
            print(f"   ❌ {file_name} missing")
            all_good = False
    
    return all_good

def main():
    """Run all tests"""
    print("=" * 60)
    print("LEO AI - SYSTEM HEALTH CHECK")
    print("=" * 60)
    
    results = {
        "File Structure": test_file_structure(),
        "Dependencies": test_dependencies(),
        "Ollama Models": test_ollama_models(),
        "Backend Health": test_backend_health(),
        "Language Detection": test_language_detection(),
        "Database": test_database(),
        "Frontend": test_frontend()
    }
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:20} {status}")
    
    total = len(results)
    passed = sum(results.values())
    
    print("\n" + "=" * 60)
    print(f"TOTAL: {passed}/{total} tests passed")
    print("=" * 60)
    
    if passed == total:
        print("\n🎉 All systems operational!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
