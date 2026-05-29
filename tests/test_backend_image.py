"""Quick test of backend image generation"""
import sys
sys.path.insert(0, 'backend')

from services.image_generator import image_generator

print(f"Backend: {image_generator.backend}")
print(f"Tiny gen: {image_generator.tiny_gen}")
print(f"Device: {image_generator.device}")

if image_generator.backend == "tiny_local" and image_generator.tiny_gen:
    print("\n✅ Image generation is ready!")
    print("Testing generation...")
    
    result = image_generator.generate_image(
        prompt="a red apple",
        width=512,
        height=512,
        steps=15
    )
    
    if result["success"]:
        print(f"✅ Generated image: {len(result['image_base64'])} bytes")
    else:
        print(f"❌ Failed: {result.get('error')}")
else:
    print(f"\n❌ Image generation not ready. Backend: {image_generator.backend}")
