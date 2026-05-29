"""
System Metrics Collection Script
Gathers CPU, CUDA, Transformers, and Model metrics
"""

import sys
import platform
import psutil
import subprocess
import json

print("=" * 80)
print("SYSTEM METRICS REPORT")
print("=" * 80)

# ============================================================================
# 1. CPU METRICS
# ============================================================================
print("\n📊 CPU METRICS")
print("-" * 80)
print(f"Processor: {platform.processor()}")
print(f"Architecture: {platform.machine()}")
print(f"CPU Cores (Physical): {psutil.cpu_count(logical=False)}")
print(f"CPU Threads (Logical): {psutil.cpu_count(logical=True)}")
print(f"CPU Frequency: {psutil.cpu_freq().current:.2f} MHz (Max: {psutil.cpu_freq().max:.2f} MHz)")
print(f"CPU Usage: {psutil.cpu_percent(interval=1)}%")

# ============================================================================
# 2. MEMORY METRICS
# ============================================================================
print("\n💾 MEMORY METRICS")
print("-" * 80)
mem = psutil.virtual_memory()
print(f"Total RAM: {mem.total / (1024**3):.2f} GB")
print(f"Available RAM: {mem.available / (1024**3):.2f} GB")
print(f"Used RAM: {mem.used / (1024**3):.2f} GB")
print(f"RAM Usage: {mem.percent}%")

# ============================================================================
# 3. CUDA/GPU METRICS
# ============================================================================
print("\n🎮 CUDA/GPU METRICS")
print("-" * 80)

try:
    import torch
    print(f"PyTorch Version: {torch.__version__}")
    print(f"CUDA Available: {torch.cuda.is_available()}")
    
    if torch.cuda.is_available():
        print(f"CUDA Version: {torch.version.cuda}")
        print(f"cuDNN Version: {torch.backends.cudnn.version()}")
        print(f"GPU Count: {torch.cuda.device_count()}")
        
        for i in range(torch.cuda.device_count()):
            print(f"\nGPU {i}: {torch.cuda.get_device_name(i)}")
            print(f"  Compute Capability: {'.'.join(map(str, torch.cuda.get_device_capability(i)))}")
            
            # Memory info
            mem_allocated = torch.cuda.memory_allocated(i) / (1024**3)
            mem_reserved = torch.cuda.memory_reserved(i) / (1024**3)
            mem_total = torch.cuda.get_device_properties(i).total_memory / (1024**3)
            
            print(f"  Total VRAM: {mem_total:.2f} GB")
            print(f"  Allocated VRAM: {mem_allocated:.2f} GB")
            print(f"  Reserved VRAM: {mem_reserved:.2f} GB")
            print(f"  Free VRAM: {mem_total - mem_reserved:.2f} GB")
            print(f"  VRAM Usage: {(mem_reserved / mem_total * 100):.1f}%")
    else:
        print("CUDA not available - using CPU")
        
except ImportError:
    print("PyTorch not installed")

# ============================================================================
# 4. TRANSFORMERS METRICS
# ============================================================================
print("\n🤖 TRANSFORMERS LIBRARY METRICS")
print("-" * 80)

try:
    import transformers
    print(f"Transformers Version: {transformers.__version__}")
    
    # Check for key components
    try:
        from transformers import AutoModel, AutoTokenizer
        print("✅ AutoModel available")
        print("✅ AutoTokenizer available")
    except:
        print("⚠️ Some transformers components unavailable")
        
except ImportError:
    print("Transformers not installed")

# ============================================================================
# 5. DIFFUSERS METRICS
# ============================================================================
print("\n🎨 DIFFUSERS LIBRARY METRICS")
print("-" * 80)

try:
    import diffusers
    print(f"Diffusers Version: {diffusers.__version__}")
    
    try:
        from diffusers import StableDiffusionPipeline
        print("✅ StableDiffusionPipeline available")
    except Exception as e:
        print(f"⚠️ StableDiffusionPipeline unavailable: {str(e)[:100]}")
        
except ImportError:
    print("Diffusers not installed")

# ============================================================================
# 6. OLLAMA MODEL METRICS
# ============================================================================
print("\n🦙 OLLAMA MODEL METRICS")
print("-" * 80)

try:
    import requests
    response = requests.get("http://localhost:11434/api/tags", timeout=2)
    if response.status_code == 200:
        models = response.json().get("models", [])
        print(f"Ollama Status: ✅ Running")
        print(f"Models Installed: {len(models)}")
        
        for model in models:
            name = model.get("name", "Unknown")
            size = model.get("size", 0) / (1024**3)
            print(f"\n  Model: {name}")
            print(f"    Size: {size:.2f} GB")
            print(f"    Modified: {model.get('modified_at', 'Unknown')}")
    else:
        print("Ollama Status: ⚠️ Not responding")
except Exception as e:
    print(f"Ollama Status: ❌ Not running ({str(e)})")

# ============================================================================
# 7. PYTHON ENVIRONMENT
# ============================================================================
print("\n🐍 PYTHON ENVIRONMENT")
print("-" * 80)
print(f"Python Version: {sys.version}")
print(f"Python Executable: {sys.executable}")

print("\n" + "=" * 80)
print("END OF METRICS REPORT")
print("=" * 80)
