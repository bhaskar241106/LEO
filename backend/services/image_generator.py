"""
Offline Text-to-Image Generation Service
Uses minimal Stable Diffusion model via diffusers
"""

import os
import logging
import base64
from io import BytesIO
from PIL import Image
import requests
import json
import torch

logger = logging.getLogger("DEAR.ImageGenerator")
logger.info("🎨 ImageGenerator module loading...")

# Try to import diffusers for local generation
try:
    from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
    DIFFUSERS_AVAILABLE = True
    logger.info("✅ Diffusers library available")
except (ImportError, RuntimeError, ModuleNotFoundError) as e:
    DIFFUSERS_AVAILABLE = False
    logger.warning(f"⚠️ Diffusers library not available: {str(e)[:100]}")

class ImageGenerator:
    def __init__(self):
        self.pipeline = None
        self.tiny_gen = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.backend = self._detect_backend()  # Call this AFTER initializing variables
        logger.info(f"Image generation backend: {self.backend}")
        logger.info(f"Device: {self.device}")
        
    def _detect_backend(self):
        """Detect available image generation backend"""
        # Priority 1: Tiny local model (if diffusers available)
        if DIFFUSERS_AVAILABLE:
            try:
                from services.tiny_image_gen import tiny_image_gen
                self.tiny_gen = tiny_image_gen
                logger.info("✅ Using tiny local SD model (segmind/small-sd)")
                return "tiny_local"
            except Exception as e:
                logger.warning(f"⚠️ Tiny model not available: {str(e)}")
        
        # Priority 2: Stable Diffusion WebUI API
        try:
            response = requests.get("http://localhost:7860/sdapi/v1/options", timeout=2)
            if response.status_code == 200:
                logger.info("✅ Stable Diffusion WebUI detected")
                return "sd_webui"
        except:
            pass
        
        logger.warning("⚠️ No image generation backend found - will initialize on first use")
        return "tiny_local"  # Default to tiny_local, will load on first use
    
    def _init_local_pipeline(self):
        """Initialize local Stable Diffusion pipeline with minimal model"""
        try:
            logger.info("🔄 Loading minimal SD model (this may take a minute first time)...")
            
            # Use small, optimized model: segmind/small-sd (983 MB)
            model_id = "segmind/small-sd"
            
            # Load pipeline with optimizations
            self.pipeline = StableDiffusionPipeline.from_pretrained(
                model_id,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                safety_checker=None,  # Disable for speed
                requires_safety_checker=False
            )
            
            # Use faster scheduler
            self.pipeline.scheduler = DPMSolverMultistepScheduler.from_config(
                self.pipeline.scheduler.config
            )
            
            # Move to device
            self.pipeline = self.pipeline.to(self.device)
            
            # Enable memory optimizations
            if self.device == "cuda":
                self.pipeline.enable_attention_slicing()
                # Enable xformers if available for even faster generation
                try:
                    self.pipeline.enable_xformers_memory_efficient_attention()
                    logger.info("✅ xformers acceleration enabled")
                except:
                    logger.info("ℹ️ xformers not available (optional)")
            
            logger.info("✅ Local SD model loaded successfully")
            
        except Exception as e:
            logger.error(f"❌ Failed to load local model: {str(e)}")
            logger.info("💡 Falling back to SD WebUI if available")
            self.backend = self._detect_backend()
            self.pipeline = None
    
    def generate_image(self, prompt: str, negative_prompt: str = "", 
                      width: int = 512, height: int = 512, 
                      steps: int = 20, cfg_scale: float = 7.0):
        """
        Generate image from text prompt
        
        Args:
            prompt: Text description of desired image
            negative_prompt: What to avoid in the image
            width: Image width (default 512)
            height: Image height (default 512)
            steps: Number of diffusion steps (default 20)
            cfg_scale: Classifier-free guidance scale (default 7.0)
            
        Returns:
            dict with 'success', 'image_base64', 'error'
        """
        # Initialize tiny_gen if not already done
        if self.backend == "tiny_local" and self.tiny_gen is None:
            try:
                from services.tiny_image_gen import tiny_image_gen
                self.tiny_gen = tiny_image_gen
                logger.info("✅ Lazy-loaded tiny image generator")
            except Exception as e:
                logger.error(f"❌ Failed to load tiny generator: {str(e)}")
                return {
                    "success": False,
                    "error": f"Failed to initialize image generator: {str(e)}"
                }
        
        if self.backend == "tiny_local" and self.tiny_gen:
            return self.tiny_gen.generate(prompt, negative_prompt, width, height, steps, cfg_scale)
        elif self.backend == "sd_webui":
            return self._generate_sd_webui(prompt, negative_prompt, width, height, steps, cfg_scale)
        else:
            return {
                "success": False,
                "error": "Image generation not available. Install: pip install diffusers transformers accelerate torch torchvision"
            }
    
    def _generate_local(self, prompt, negative_prompt, width, height, steps, cfg_scale):
        """Generate image using local minimal Stable Diffusion model"""
        try:
            if self.pipeline is None:
                return {
                    "success": False,
                    "error": "Local model not initialized. Please restart backend."
                }
            
            logger.info(f"🎨 Generating image locally: '{prompt[:50]}...'")
            
            # Set default negative prompt if not provided
            if not negative_prompt:
                negative_prompt = "blurry, bad quality, distorted, ugly, low resolution"
            
            # Generate image
            with torch.inference_mode():
                result = self.pipeline(
                    prompt=prompt,
                    negative_prompt=negative_prompt,
                    num_inference_steps=steps,
                    guidance_scale=cfg_scale,
                    width=width,
                    height=height,
                    generator=torch.Generator(device=self.device).manual_seed(-1)
                )
            
            # Convert to base64
            image = result.images[0]
            buffered = BytesIO()
            image.save(buffered, format="PNG")
            image_base64 = base64.b64encode(buffered.getvalue()).decode()
            
            logger.info("✅ Image generated successfully (local)")
            
            return {
                "success": True,
                "image_base64": image_base64,
                "prompt": prompt,
                "width": width,
                "height": height,
                "backend": "local"
            }
            
        except torch.cuda.OutOfMemoryError:
            logger.error("❌ GPU out of memory")
            return {
                "success": False,
                "error": "GPU out of memory. Try reducing image size or steps."
            }
        except Exception as e:
            logger.error(f"❌ Local generation error: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _generate_sd_webui(self, prompt, negative_prompt, width, height, steps, cfg_scale):
        """Generate image using Stable Diffusion WebUI API"""
        try:
            payload = {
                "prompt": prompt,
                "negative_prompt": negative_prompt or "blurry, bad quality, distorted, ugly",
                "steps": steps,
                "width": width,
                "height": height,
                "cfg_scale": cfg_scale,
                "sampler_name": "DPM++ 2M Karras",
                "seed": -1,
            }
            
            logger.info(f"🎨 Generating image: '{prompt[:50]}...'")
            
            response = requests.post(
                "http://localhost:7860/sdapi/v1/txt2img",
                json=payload,
                timeout=120  # 2 minutes timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                image_base64 = result['images'][0]
                
                logger.info("✅ Image generated successfully")
                
                return {
                    "success": True,
                    "image_base64": image_base64,
                    "prompt": prompt,
                    "width": width,
                    "height": height
                }
            else:
                logger.error(f"❌ SD WebUI error: {response.status_code}")
                return {
                    "success": False,
                    "error": f"SD WebUI returned status {response.status_code}"
                }
                
        except requests.Timeout:
            logger.error("❌ Image generation timeout")
            return {
                "success": False,
                "error": "Image generation timed out. Try reducing steps or image size."
            }
        except Exception as e:
            logger.error(f"❌ Image generation error: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _generate_description(self, prompt):
        """Generate detailed description using Ollama (fallback)"""
        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "phi3:mini",
                    "prompt": f"Describe in vivid detail what an image of '{prompt}' would look like:",
                    "stream": False
                },
                timeout=30
            )
            
            if response.status_code == 200:
                description = response.json().get("response", "")
                return {
                    "success": True,
                    "description": description,
                    "note": "Image generation not available. Generated description instead."
                }
            else:
                return {
                    "success": False,
                    "error": "Failed to generate description"
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def enhance_prompt(self, simple_prompt: str):
        """Use LLM to enhance a simple prompt into a detailed one"""
        try:
            system_instruction = """You are a highly disciplined Stable Diffusion prompt enhancer.
Task: Enrich the user's input with specific artistic details, rendering styles, atmospheric lighting, and high-quality textures.
Strict Rules:
1. Retain ALL original subjects, actions, settings, and time-of-day exactly as requested.
2. DO NOT introduce contradictory elements (e.g., if the prompt mentions night, do not change it to morning. If it is outdoors, keep it outdoors).
3. Output ONLY the finalized prompt itself. Do not include labels like "Enhanced Prompt:", quotes, word counts, or conversational prefaces."""

            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "phi3:mini",
                    "system": system_instruction,
                    "prompt": f"User Prompt: {simple_prompt}",
                    "stream": False
                },
                timeout=15
            )
            
            if response.status_code == 200:
                enhanced = response.json().get("response", simple_prompt).strip()
                # Clean up any stray quotes the model might have returned
                if enhanced.startswith('"') and enhanced.endswith('"'):
                    enhanced = enhanced[1:-1]
                logger.info(f"✨ Enhanced prompt: {enhanced[:100]}...")
                return enhanced
            else:
                return simple_prompt
        except:
            return simple_prompt

# Global instance
image_generator = ImageGenerator()
