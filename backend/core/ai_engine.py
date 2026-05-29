import requests
import json
import logging
import os
import time

logger = logging.getLogger("DEAR.AIEngine")

class AIEngine:
    def __init__(self, ollama_url: str = None):
        self.url = ollama_url or os.getenv("OLLAMA_URL", "http://localhost:11434")
        
        # Dual-Brain Architecture with Quantization Support
        # Check for optimized models first, fallback to original
        self.fast_model = os.getenv("FAST_MODEL", "llama3.2:1b")  # Quantized: 800 MB
        self.expert_model = os.getenv("EXPERT_MODEL", "gemma:2b")  # Better for Indian languages: 1.7 GB
        
        # Fallback to original models if optimized not available
        if not self._check_model_exists(self.fast_model):
            self.fast_model = "llama3"
            logger.warning(f"Optimized fast model not found, using: {self.fast_model}")
        
        if not self._check_model_exists(self.expert_model):
            self.expert_model = "mistral"
            logger.warning(f"Optimized expert model not found, using: {self.expert_model}")
        
        self.model = self.fast_model # For legacy code fallback
        self.fallback_model = self.expert_model
        
        # CUDA acceleration (automatically used by Ollama if available)
        self.cuda_enabled = os.getenv("CUDA_ENABLED", "true").lower() == "true"
        
        logger.info(f"AI Router System Online. Fast: {self.fast_model} | Expert: {self.expert_model}")
        if self.cuda_enabled:
            logger.info("CUDA acceleration enabled (if GPU available)")
    
    def _check_model_exists(self, model_name: str) -> bool:
        """Check if a model is available in Ollama"""
        try:
            response = requests.get(f"{self.url}/api/tags", timeout=2)
            if response.status_code == 200:
                models = response.json().get("models", [])
                return any(m.get("name", "").startswith(model_name) for m in models)
        except:
            pass
        return False

    def _route_request(self, prompt: str) -> str:
        """Determines whether a prompt requires the Expert brain or the Fast brain."""
        prompt_lower = prompt.lower()
        
        # Simple queries that can use fast model
        simple_triggers = ["hi", "hello", "hey", "thanks", "thank you", "bye", "goodbye", 
                          "yes", "no", "ok", "okay"]
        
        # Complex queries that need expert model
        complex_triggers = ["code", "script", "python", "javascript", "react", "html", "css", 
                            "solve", "calculate", "math", "equation", "theorem", 
                            "explain", "why", "how", "analyze", "debug", "detail", "describe",
                            "compare", "difference", "what is", "tell me about", "teach me"]
        
        # If it's a very short greeting, use fast model
        if len(prompt) < 20 and any(trigger in prompt_lower for trigger in simple_triggers):
            return self.fast_model
        
        # If the question is long, or uses complex keywords, route to expert model
        if len(prompt) > 80 or any(trigger in prompt_lower for trigger in complex_triggers):
            return self.expert_model
        
        # Default to expert model for better quality
        return self.expert_model

    def generate(self, prompt: str, personality: str = "Friendly", language: str = "English", history: list = [], temperature: float = None):
        """Legacy JSON return. Use generate_stream for fast text output."""
        target_model = self._route_request(prompt)
        system_prompt = f"You are DEAR, an AI assistant. Always respond in the exact same language that the user uses."
        temp = temperature if temperature is not None else float(os.getenv("TEMPERATURE", 0.7))

        payload = {
            "model": target_model,
            "prompt": prompt,
            "system": system_prompt,
            "stream": False,
            "options": {"num_ctx": 1024, "num_predict": 100}
        }
        try:
            return self._make_request(payload)
        except Exception as e:
            return f"Model error: {str(e)}", "Error"

    def generate_stream(self, prompt: str, personality: str = "Friendly", language: str = "English", history: list = [], temperature: float = None):
        """Yields words instantly, using Dual-Brain Routing."""
        target_model = self._route_request(prompt)
        
        logger.info(f"🔥 ROUTING PROMPT TO: {target_model.upper()}")

        # Build conversation context from history
        conversation_context = ""
        if history and len(history) > 0:
            # Include last 5 exchanges for context
            recent_history = history[-10:] if len(history) > 10 else history
            for msg in recent_history:
                role = msg.get('role', 'user')
                content = msg.get('content', '')
                if role == 'user':
                    conversation_context += f"User: {content}\n"
                elif role == 'assistant':
                    conversation_context += f"Assistant: {content}\n"

        # Personality-based system prompts
        personality_traits = {
            "Friendly": "warm, conversational, and helpful. Use a casual, approachable tone.",
            "Professional": "formal, precise, and business-like. Maintain professionalism.",
            "Teacher": "educational, patient, and thorough. Explain concepts clearly with examples.",
            "Strict": "direct, concise, and authoritative. Get straight to the point."
        }
        
        personality_desc = personality_traits.get(personality, personality_traits["Friendly"])
        
        romanized_langs = ["Telugu", "Hindi", "Tamil", "Kannada", "Malayalam", "Bengali", "Marathi", "Gujarati", "Punjabi", "Urdu"]

        if language in romanized_langs:
            # Improved Telugu-specific instructions
            if language == "Telugu":
                lang_instruction = f"""CRITICAL LANGUAGE REQUIREMENT:
- You MUST respond ONLY in Telugu language
- Write Telugu words using English letters (Romanized Telugu)
- Use proper Telugu grammar and sentence structure
- Examples: "Namaskaram" (నమస్కారం), "Meeru ela unnaru?" (మీరు ఎలా ఉన్నారు?)
- Be natural and fluent in Telugu
- Do NOT use native Telugu script (తెలుగు)
- Do NOT mix English words unless absolutely necessary"""
            else:
                lang_instruction = f"IMPORTANT: You MUST respond ONLY in {language}, BUT you MUST write the response using the English alphabet (Romanized/Transliterated). This is required for our Text-to-Speech engine. Do NOT use the native script."
        elif language != "English":
            lang_instruction = f"IMPORTANT: You MUST respond ONLY in {language}. Do not use any other language."
        else:
            lang_instruction = "Respond in English."

        if target_model == self.fast_model:
            system_prompt = f"""You are Leo (formerly DEAR), an AI assistant with a {personality} personality.

Personality: Be {personality_desc}

Instructions:
- {lang_instruction}
- Keep responses brief but informative (2-4 sentences)
- Be natural and conversational
- Avoid repetitive phrases
- Provide direct, helpful answers

Language: {language}"""
            ctx = 2048
            predict = 200
        else:
            system_prompt = f"""You are Leo (formerly DEAR), a highly intelligent AI assistant with a {personality} personality.

Personality: Be {personality_desc}

Instructions:
- {lang_instruction}
- Provide detailed, comprehensive answers with specific information
- Use examples, explanations, and context when helpful
- Break down complex topics into understandable parts
- Be thorough but avoid unnecessary repetition
- Vary your sentence structure and vocabulary
- If asked for details, provide in-depth information
- If the user asks "why" or "how", explain the reasoning and mechanisms

Language: {language}

Previous conversation context:
{conversation_context}

Now respond to the user's current message with fresh, detailed information."""
            ctx = 8192
            predict = 1024

        # Lower temperature for fast model (phi3:mini) to prevent random hallucinations on short inputs
        if target_model == self.fast_model:
            temp = 0.3 if temperature is None else min(temperature, 0.4)
        else:
            temp = temperature if temperature is not None else 0.7

        payload = {
            "model": target_model,
            "prompt": prompt,
            "system": system_prompt,
            "stream": True,
            "options": {
                "num_ctx": ctx,
                "temperature": temp,
                "top_k": 40,
                "top_p": 0.95,
                "repeat_penalty": 1.2,  # Penalize repetition
                "num_predict": predict,
            }
        }

        try:
            # Increased timeout to 60s to completely cover any hardware Cold Starts
            response = requests.post(f"{self.url}/api/generate", json=payload, stream=True, timeout=60)
            if response.status_code != 200:
                yield f"Error: Backend 500"
                return
            for line in response.iter_lines():
                if line:
                    data = json.loads(line.decode('utf-8'))
                    yield data.get("response", "")
        except Exception as e:
            yield f"[Network/Model Error: {str(e)}]"

    def _make_request(self, payload):
        response = requests.post(f"{self.url}/api/generate", json=payload, timeout=45)
        if response.status_code == 500:
            raise Exception(f"Ollama Server Error (500): {response.text}")
        response.raise_for_status()
        data = response.json()
        return data.get("response", ""), "Neutral"

    def switch_model(self, model_name: str):
        self.model = model_name
        logger.info(f"Model switched to: {self.model}")
