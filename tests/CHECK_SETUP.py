#!/usr/bin/env python3
"""
Setup verification script for Leo AI Assistant
Checks all dependencies and configurations
"""

import os
import sys
import subprocess
import socket

def check_command(cmd, name):
    """Check if a command exists"""
    try:
        result = subprocess.run(
            cmd, 
            stdout=subprocess.DEVNULL, 
            stderr=subprocess.DEVNULL,
            shell=True
        )
        print(f"✅ {name} is installed")
        return True
    except:
        print(f"❌ {name} is NOT installed")
        return False

def check_port(port, service):
    """Check if a port is available"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        result = s.connect_ex(('127.0.0.1', port))
        if result == 0:
            print(f"⚠️  Port {port} ({service}) is already in use")
            return False
        else:
            print(f"✅ Port {port} ({service}) is available")
            return True

def check_file(path, name):
    """Check if a file exists"""
    if os.path.exists(path):
        print(f"✅ {name} exists")
        return True
    else:
        print(f"❌ {name} is missing")
        return False

def check_directory(path, name):
    """Check if a directory exists"""
    if os.path.isdir(path):
        print(f"✅ {name} directory exists")
        return True
    else:
        print(f"❌ {name} directory is missing")
        return False

def main():
    print("=" * 60)
    print("  Leo AI Assistant - Setup Verification")
    print("=" * 60)
    print()
    
    all_good = True
    
    # Check Python
    print("📦 Checking System Dependencies...")
    print("-" * 60)
    all_good &= check_command("python --version", "Python")
    all_good &= check_command("node --version", "Node.js")
    all_good &= check_command("npm --version", "npm")
    all_good &= check_command("ollama --version", "Ollama")
    print()
    
    # Check project structure
    print("📁 Checking Project Structure...")
    print("-" * 60)
    all_good &= check_directory("backend", "Backend")
    all_good &= check_directory("frontend", "Frontend")
    all_good &= check_file("backend/main.py", "Backend main.py")
    all_good &= check_file("backend/requirements.txt", "Backend requirements.txt")
    all_good &= check_file("frontend/package.json", "Frontend package.json")
    all_good &= check_file("scripts/app_launcher.py", "App launcher")
    print()
    
    # Check configuration files
    print("⚙️  Checking Configuration...")
    print("-" * 60)
    all_good &= check_file("backend/.env", "Backend .env file")
    all_good &= check_file("frontend/vite.config.js", "Frontend Vite config")
    print()
    
    # Check Python virtual environment
    print("🐍 Checking Python Environment...")
    print("-" * 60)
    venv_exists = check_directory("backend/venv", "Python virtual environment")
    if not venv_exists:
        print("   ℹ️  Run: cd backend && python -m venv venv")
    print()
    
    # Check Node modules
    print("📦 Checking Node Modules...")
    print("-" * 60)
    node_modules = check_directory("frontend/node_modules", "Node modules")
    if not node_modules:
        print("   ℹ️  Run: cd frontend && npm install")
    print()
    
    # Check ports
    print("🔌 Checking Port Availability...")
    print("-" * 60)
    all_good &= check_port(8000, "Backend API")
    all_good &= check_port(5173, "Frontend Dev Server")
    check_port(11434, "Ollama")  # Don't fail if Ollama is running
    print()
    
    # Summary
    print("=" * 60)
    if all_good:
        print("✅ All checks passed! You're ready to run the application.")
        print()
        print("To start the application, run:")
        print("  python scripts/app_launcher.py")
        print()
        print("Or manually:")
        print("  1. Terminal 1: ollama serve")
        print("  2. Terminal 2: cd backend && venv\\Scripts\\activate && python main.py")
        print("  3. Terminal 3: cd frontend && npm run dev")
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        print()
        print("Quick fixes:")
        print("  - Install missing dependencies")
        print("  - Run: cd backend && python -m venv venv")
        print("  - Run: cd backend && venv\\Scripts\\activate && pip install -r requirements.txt")
        print("  - Run: cd frontend && npm install")
        print("  - Create backend/.env from backend/.env.example")
    print("=" * 60)
    
    return 0 if all_good else 1

if __name__ == "__main__":
    sys.exit(main())
