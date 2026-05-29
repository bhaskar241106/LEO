"""Test image generation with timing"""
import sys
import time
sys.path.insert(0, 'backend')

from services.image_generator import image_generator

print(f"✅ Backend: {image_generator.backend}")
print(f"✅ Device: {image_generator.device}")
print(f"✅ Tiny gen initialized: {image_generator.tiny_gen is not None}")

if image_generator.backend == "tiny_local":
    print("\n🎨 Testing image generation...")
    print("Prompt: 'a beautiful sunset over mountains'")
    
    start_time = time.time()
    
    result = image_generator.generate_image(
        prompt="a beautiful sunset over mountains",
        width=512,
        height=512,
        steps=20
    )
    
    elapsed = time.time() - start_time
    
    if result["success"]:
        print(f"\n✅ SUCCESS!")
        print(f"⏱️  Generation time: {elapsed:.2f} seconds")
        print(f"📦 Image size: {len(result['image_base64'])} bytes")
        print(f"📐 Dimensions: {result['width']}x{result['height']}")
    else:
        print(f"\n❌ FAILED: {result.get('error')}")
else:
    print(f"\n❌ Backend not ready: {image_generator.backend}")
