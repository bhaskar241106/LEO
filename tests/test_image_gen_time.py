"""
Test Image Generation Setup Time
Measures time to load model and generate first image
"""

import time
import sys
sys.path.insert(0, 'backend')

print("=" * 80)
print("IMAGE GENERATION SETUP TIME TEST")
print("=" * 80)

# Test 1: Import time
print("\n⏱️  Test 1: Import Time")
start = time.time()
from services.tiny_image_gen import tiny_image_gen
import_time = time.time() - start
print(f"✅ Import completed in {import_time:.2f} seconds")

# Test 2: Model load time (first time - downloads model)
print("\n⏱️  Test 2: Model Load Time")
print("Note: First time will download 1.3 GB model (1-2 minutes)")
print("Subsequent loads will be instant (model cached)")

start = time.time()
success = tiny_image_gen.load_model()
load_time = time.time() - start

if success:
    print(f"✅ Model loaded in {load_time:.2f} seconds")
else:
    print(f"❌ Model failed to load")
    sys.exit(1)

# Test 3: First image generation
print("\n⏱️  Test 3: First Image Generation")
print("Generating 512x512 image with 20 steps...")

start = time.time()
result = tiny_image_gen.generate(
    prompt="a beautiful sunset over mountains",
    width=512,
    height=512,
    steps=20
)
gen_time = time.time() - start

if result.get("success"):
    print(f"✅ Image generated in {gen_time:.2f} seconds")
    print(f"   Image size: {len(result['image_base64'])} bytes (base64)")
else:
    print(f"❌ Generation failed: {result.get('error')}")

# Summary
print("\n" + "=" * 80)
print("TIMING SUMMARY")
print("=" * 80)
print(f"Import Time:      {import_time:.2f} seconds")
print(f"Model Load Time:  {load_time:.2f} seconds")
print(f"Generation Time:  {gen_time:.2f} seconds")
print(f"Total Time:       {import_time + load_time + gen_time:.2f} seconds")
print("\n📝 Note: Model load time is only for FIRST run (downloads 1.3 GB)")
print("   Subsequent runs: ~3-5 seconds load + 10-30 seconds generation")
print("=" * 80)
