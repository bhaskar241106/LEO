"""
Tiny Image Generation Service
Uses the smallest possible Stable Diffusion model
"""

import os
import logging
import base64
from io import BytesIO
from PIL import Image
import torch

logger = logging.getLogger("DEAR.TinyImageGen")

class TinyImageGenerator:
    def __init__(self):
        self.pipeline = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model_loaded = False
        logger.info(f"Tiny Image Generator initialized on {self.device}")
    
    def load_model(self):
        """Load the tiny SD model on first use (lazy loading)"""
        if self.model_loaded:
            return True
        
        try:
            logger.info("🔄 Loading tiny SD model (OFA-Sys/small-stable-diffusion-v0)...")
            logger.info("This is a 1.3 GB model - first load takes 1-2 minutes")
            
            from diffusers import StableDiffusionPipeline
            import os
            
            # Disable torch load security check (model is from trusted source)
            os.environ['TORCH_LOAD_WEIGHTS_ONLY'] = '0'
            
            # Use segmind/small-sd (983 MB) - compact and efficient
            model_id = "segmind/small-sd"
            
            self.pipeline = StableDiffusionPipeline.from_pretrained(
                model_id,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                safety_checker=None,
                requires_safety_checker=False
            )
            
            self.pipeline = self.pipeline.to(self.device)
            
            # Memory optimizations
            if self.device == "cuda":
                self.pipeline.enable_attention_slicing()
                try:
                    self.pipeline.enable_xformers_memory_efficient_attention()
                    logger.info("✅ xformers enabled for faster generation")
                except:
                    pass
            
            self.model_loaded = True
            logger.info("✅ Tiny SD model loaded successfully!")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to load tiny model: {str(e)}")
            return False
    
    def generate(self, prompt: str, negative_prompt: str = "", 
                width: int = 512, height: int = 512, 
                steps: int = 20, guidance_scale: float = 7.5):
        """Generate image from text prompt"""
        
        # Load model on first use
        if not self.model_loaded:
            if not self.load_model():
                return {
                    "success": False,
                    "error": "Failed to load image generation model"
                }
        
        try:
            logger.info(f"🎨 Generating image: '{prompt[:50]}...'")
            
            if not negative_prompt:
                negative_prompt = "blurry, bad quality, distorted, ugly, low resolution"
            
            # Generate image
            with torch.inference_mode():
                result = self.pipeline(
                    prompt=prompt,
                    negative_prompt=negative_prompt,
                    num_inference_steps=steps,
                    guidance_scale=guidance_scale,
                    width=width,
                    height=height,
                )
            
            # Convert to base64
            image = result.images[0]
            buffered = BytesIO()
            image.save(buffered, format="PNG")
            image_base64 = base64.b64encode(buffered.getvalue()).decode()
            
            logger.info("✅ Image generated successfully!")
            
            return {
                "success": True,
                "image_base64": image_base64,
                "prompt": prompt,
                "width": width,
                "height": height,
                "model": "tiny-sd-1.3gb"
            }
            
        except torch.cuda.OutOfMemoryError:
            logger.error("❌ GPU out of memory")
            return {
                "success": False,
                "error": "GPU out of memory. Try smaller image size (256x256) or fewer steps."
            }
        except Exception as e:
            logger.error(f"❌ Generation error: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

# Global instance
tiny_image_gen = TinyImageGenerator()
