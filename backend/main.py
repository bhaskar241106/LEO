from fastapi import FastAPI, HTTPException, Request, UploadFile, File
import sys

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import logging
import os
import tempfile
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from core.ai_engine import AIEngine
from core.memory_manager import MemoryManager
from core.rag_handler import RAGHandler
from core.personality_manager import PersonalityManager
from core.hardware_detector import HardwareDetector
from core.language_detector import LanguageDetector
from core.data_manager import DataManager
from core.emotion_analyzer import EmotionAnalyzer
from services.audio_pipeline import AudioPipeline
from services.phoneme_extractor import PhonemeExtractor
from services.scheduler_service import SchedulerService
from services.system_service import SystemService
from services.image_generator import image_generator
from routes import avatar, language

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("DEAR")

app = FastAPI(title="DEAR AI Assistant API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(avatar.router, prefix="/api")
app.include_router(language.router, prefix="/api")

@app.get("/")
async def root():
    return {"status": "DEAR Backend Online", "version": "1.0.0"}

# Initialize Services
hardware = HardwareDetector()
capability = hardware.detect_capabilities()
logger.info(f"System Capability Level: {capability}")

ai_engine = AIEngine()
memory = MemoryManager()
rag = RAGHandler()
personality = PersonalityManager()
phonemes = PhonemeExtractor()
audio_pipeline = AudioPipeline(model_size="base")
scheduler = SchedulerService()
system_utils = SystemService()
language_detector = LanguageDetector()
data_manager = DataManager()
emotion_analyzer = EmotionAnalyzer()

class ChatRequest(BaseModel):
    message: str
    personality: str = "Friendly"
    language: str = "Auto"  # Changed default to "Auto" for auto-detection
    temperature: float = 0.9

class ChatResponse(BaseModel):
    response: str
    emotion: str
    viseme_timeline: List[dict]
    detected_language: Optional[str] = None

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        # Auto-detect language if set to "Auto"
        detected_lang = request.language
        if request.language == "Auto":
            detected_lang = language_detector.detect_language(request.message)
            logger.info(f"Auto-detected language: {detected_lang}")
        
        context = rag.retrieve(request.message)
        context_str = "\n".join(context)
        history = memory.get_history()
        
        full_prompt = f"Context: {context_str}\nUser: {request.message}"
        response_text, emotion = ai_engine.generate(
            full_prompt, 
            personality=request.personality, 
            language=detected_lang,
            history=history,
            temperature=request.temperature
        )
        
        memory.add_message("user", request.message)
        memory.add_message("assistant", response_text)
        
        raw_visemes = phonemes.get_visemes(response_text, language=detected_lang)
        duration = len(response_text) * 0.05 
        timeline = phonemes.map_audio_duration(raw_visemes, duration)
        
        return ChatResponse(
            response=response_text,
            emotion=emotion,
            viseme_timeline=timeline,
            detected_language=detected_lang
        )
    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat_stream")
async def chat_stream(request: ChatRequest):
    try:
        detected_lang = request.language
        if request.language == "Auto":
            try:
                detected_lang = language_detector.detect_language(request.message)
            except:
                detected_lang = "English"

        try:
            context = rag.retrieve(request.message)
            context_str = "\n".join(context)
        except:
            context_str = ""

        try:
            history = memory.get_history()
        except:
            history = []

        full_prompt = f"Context: {context_str}\nUser: {request.message}" if context_str else request.message

        def event_stream():
            try:
                full_text = ""
                for token in ai_engine.generate_stream(
                    full_prompt,
                    personality=request.personality,
                    language=detected_lang,
                    history=history,
                    temperature=request.temperature
                ):
                    full_text += token
                    yield token
                try:
                    memory.add_message("user", request.message)
                    memory.add_message("assistant", full_text)
                except:
                    pass
            except Exception as e:
                logger.error(f"Stream error: {str(e)}", exc_info=True)
                yield f"[Error: {str(e)}]"

        return StreamingResponse(event_stream(), media_type="text/plain")
    except Exception as e:
        logger.error(f"Chat stream setup error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

# --- STT Route ---

# Language code map for STT
STT_LANGUAGE_MAP = {
    'Telugu': 'te', 'Hindi': 'hi', 'Tamil': 'ta', 'Kannada': 'kn',
    'Malayalam': 'ml', 'Bengali': 'bn', 'Marathi': 'mr', 'Gujarati': 'gu',
    'Punjabi': 'pa', 'Urdu': 'ur', 'English': 'en'
}

@app.post("/api/stt")
async def speech_to_text(audio: UploadFile = File(...), language: str = "Auto"):
    """Transcribe audio using local Whisper model (fully offline)"""
    tmp_path = None
    try:
        suffix = os.path.splitext(audio.filename)[1] or ".wav"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(await audio.read())
            tmp_path = tmp.name
        # Resolve language hint for Whisper
        whisper_lang = STT_LANGUAGE_MAP.get(language) if language != "Auto" else None
        logger.info(f"STT: transcribing {tmp_path} ({os.path.getsize(tmp_path)} bytes), lang={whisper_lang or 'auto'}")
        transcript = audio_pipeline.speech_to_text(tmp_path, language=whisper_lang)
        logger.info(f"STT result: '{transcript}'")
        if not transcript:
            raise HTTPException(status_code=422, detail="Could not transcribe audio")
        return {"transcript": transcript}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"STT error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)

# --- New Scheduler Routes ---

@app.get("/api/notifications")
async def get_notifications():
    alerts = scheduler.pop_alerts()
    return {"alerts": alerts}

class ReminderRequest(BaseModel):
    title: str
    message: str
    time: str # ISO Format

@app.post("/api/schedule/add")
async def add_reminder(request: ReminderRequest):
    task_id = scheduler.add_reminder(request.title, request.message, request.time)
    return {"status": "success", "id": task_id}

@app.get("/api/schedule/all")
async def get_reminders():
    return scheduler.get_all()

@app.delete("/api/schedule/{task_id}")
async def delete_reminder(task_id: str):
    scheduler.delete_reminder(task_id)
    return {"status": "deleted"}

# --- New System Routes ---

@app.get("/api/system/stats")
async def get_system_stats():
    return system_utils.get_stats()

class SystemCommand(BaseModel):
    action: str
    target: Optional[str] = None

@app.post("/api/system/execute")
async def execute_system_command(cmd: SystemCommand):
    success = system_utils.execute_command(cmd.action, cmd.target)
    if not success:
        raise HTTPException(status_code=400, detail="Command execution failed")
    return {"status": "success"}

@app.get("/api/system/health")
async def system_health():
    """Comprehensive check of all offline services."""
    return {
        "api": "online",
        "ollama": "connected" if os.system("curl -s http://localhost:11434/api/tags > nul") == 0 else "offline",
        "gpu": hardware.detect_capabilities(),
        "scheduler": "active" if hasattr(scheduler, 'running') and scheduler.running else "inactive"
    }

@app.get("/api/chat/history")
async def get_chat_history(limit: int = 20):
    return memory.get_history(limit=limit)

# --- Image Generation Routes ---

class ImageRequest(BaseModel):
    prompt: str
    negative_prompt: Optional[str] = ""
    width: int = 512
    height: int = 512
    steps: int = 20
    cfg_scale: float = 7.0
    enhance_prompt: bool = True

@app.post("/api/image/generate")
async def generate_image(request: ImageRequest):
    """Generate image from text prompt using Stable Diffusion"""
    try:
        # Enhance prompt if requested
        final_prompt = request.prompt
        if request.enhance_prompt:
            logger.info("✨ Enhancing prompt with LLM...")
            final_prompt = image_generator.enhance_prompt(request.prompt)
        
        # Generate image
        result = image_generator.generate_image(
            prompt=final_prompt,
            negative_prompt=request.negative_prompt,
            width=request.width,
            height=request.height,
            steps=request.steps,
            cfg_scale=request.cfg_scale
        )
        
        if result["success"]:
            return {
                "success": True,
                "image": result.get("image_base64"),
                "prompt": final_prompt,
                "original_prompt": request.prompt,
                "width": request.width,
                "height": request.height
            }
        else:
            return {
                "success": False,
                "error": result.get("error"),
                "description": result.get("description"),
                "note": result.get("note")
            }
            
    except Exception as e:
        logger.error(f"Image generation error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/image/status")
async def image_generation_status():
    """Check if image generation is available"""
    backend = image_generator.backend
    return {
        "available": backend is not None,
        "backend": backend,
        "message": "Stable Diffusion WebUI ready" if backend == "sd_webui"
                  else "Local Stable Diffusion (tiny_local) ready" if backend == "tiny_local"
                  else "Image generation not available." if backend is None
                  else f"Image generation ready ({backend})"
    }

# --- Data Management Routes ---

@app.get("/api/data/stats")
async def get_data_stats():
    """Get database statistics"""
    return data_manager.get_stats()

@app.post("/api/data/archive")
async def archive_old_data(days_old: int = 30):
    """Archive conversations older than specified days"""
    result = data_manager.archive_old_conversations(days_old=days_old, compress=True)
    return result

@app.get("/api/data/archives")
async def list_archives():
    """List all archive files"""
    return {"archives": data_manager.list_archives()}

class RestoreRequest(BaseModel):
    archive_file: str

@app.post("/api/data/restore")
async def restore_archive(request: RestoreRequest):
    """Restore conversations from archive"""
    result = data_manager.restore_from_archive(request.archive_file)
    return result

@app.post("/api/data/cleanup")
async def smart_cleanup(max_size_mb: int = 50, keep_recent_days: int = 7):
    """Smart cleanup with archiving and compression"""
    result = data_manager.smart_cleanup(
        max_size_mb=max_size_mb,
        keep_recent_days=keep_recent_days
    )
    return result

if __name__ == "__main__":
    # Use 0.0.0.0 to accept connections from network (for mobile access)
    # Use localhost for local-only access
    import sys
    host = "0.0.0.0" if "--network" in sys.argv else "localhost"
    print(f"🚀 Starting backend on {host}:8000")
    if host == "0.0.0.0":
        print("📱 Mobile access enabled - accessible from network")
    uvicorn.run(app, host=host, port=8000)
