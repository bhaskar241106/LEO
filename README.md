# Leo AI - Offline Personal Assistant

A fully offline AI assistant with voice interaction, multilingual support, and image generation capabilities.

## Features

- 🗣️ **Voice Interaction**: Speech-to-text and text-to-speech (100% offline)
- 🌍 **Multilingual Support**: 14+ languages including Telugu, Hindi, Tamil, English
- 🎨 **Image Generation**: Offline Stable Diffusion image generation
- 🧠 **Memory System**: Remembers conversations and learns from interactions
- 🎭 **Personality Modes**: Multiple personality styles (Friendly, Professional, etc.)
- 💻 **100% Offline**: No internet required after initial setup
- � **GPU Accelerated**: Optimized for NVIDIA GPUs (RTX 4060 tested)

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- Ollama (for AI models)
- 8GB+ RAM recommended
- NVIDIA GPU (optional, for faster performance)

### Installation

1. **Install Ollama Models**
   ```bash
   ollama pull phi3:mini
   ollama pull llama3.2:1b
   ollama pull tinyllama
   ```

2. **Setup Backend**
   ```bash
   cd backend
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Setup Frontend**
   ```bash
   cd frontend
   npm install
   ```

### Running

**Start Everything:**
```bash
START.bat
```

**Stop Everything:**
```bash
STOP.bat
```

**Manual Start:**
```bash
# Backend
cd backend
venv\Scripts\activate
python main.py

# Frontend (in new terminal)
cd frontend
npm run dev
```

**Access:**
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Usage

### Chat
1. Open http://localhost:5173
2. Type your message in any supported language
3. Leo responds in the same language

### Voice Mode
1. Click the microphone icon
2. Speak your message
3. Leo responds with voice

### Image Generation
1. Go to "Image Generator" tab
2. Enter your prompt
3. Click "Generate"
4. First generation takes 1-2 minutes (downloads model)
5. Subsequent generations: 30-60 seconds

### Telugu Support
Leo supports Telugu in both native script and romanized form:
- Native: "నమస్కారం, మీరు ఎలా ఉన్నారు?"
- Romanized: "Namaskaram, meeru ela unnaru?"

## Configuration

### AI Models
Edit `backend/.env`:
```env
FAST_MODEL=llama3.2:1b      # Quick responses
EXPERT_MODEL=phi3:mini       # Complex queries, multilingual
```

### Temperature
Adjust response creativity (0.0-1.0):
```env
TEMPERATURE=0.85
```

### GPU
Enable/disable GPU acceleration:
```env
CUDA_ENABLED=true
```

## Project Structure

```
bobmarleyy/
├── backend/           # Python FastAPI backend
│   ├── core/         # AI engine, memory, language detection
│   ├── services/     # Image generation, audio pipeline
│   ├── routes/       # API endpoints
│   └── main.py       # Entry point
├── frontend/         # React frontend
│   ├── src/
│   │   ├── components/
│   │   ├── views/
│   │   └── App.jsx
│   └── package.json
├── mobile/           # React Native mobile app
├── docs/             # Documentation
├── tests/            # Test files
├── scripts/          # Utility scripts
├── .gitignore        # Git ignore rules
├── README.md         # This file
├── START.bat         # Start all servers
└── STOP.bat          # Stop all servers
```

## Technologies

### Backend
- **Framework**: FastAPI
- **AI Models**: Ollama (Phi3, Llama3.2, TinyLlama)
- **Image Generation**: Stable Diffusion (segmind/small-sd)
- **STT**: OpenAI Whisper (base model, 74MB)
- **TTS**: eSpeak-NG
- **Database**: SQLite

### Frontend
- **Framework**: React + Vite
- **3D**: Three.js
- **UI**: Custom components
- **State**: React hooks

## Performance

### Response Times
- **Simple queries**: 1-2 seconds
- **Complex queries**: 3-5 seconds
- **Image generation**: 30-60 seconds (after first download)
- **Voice recognition**: <1 second

### Resource Usage
- **RAM**: 2-3 GB
- **VRAM**: 2-4 GB (with GPU)
- **Disk**: ~5 GB (models + dependencies)

## Troubleshooting

### Backend won't start
```bash
cd backend
venv\Scripts\python.exe -c "import numpy; print(numpy.__version__)"
# Should show: 1.26.4
```

### Image generation fails
- First generation needs internet (downloads ~1GB model)
- Check backend logs for progress
- Ensure 4GB+ free disk space

### Voice not working
- Check microphone permissions
- Ensure eSpeak-NG is installed
- Check browser console for errors

## Documentation

See `docs/` folder for detailed documentation:
- `ARCHITECTURE.md` - System architecture
- `BENCHMARKS_AND_TESTING.md` - Performance benchmarks
- `DATA_SECURITY_ARCHITECTURE.md` - Security details
- `TTS_STT_TECHNOLOGIES.md` - Voice technologies
- `CHANGELOG.md` - Version history

## Development

### Running Tests
```bash
cd tests
python test_multilingual.py
python test_backend_image.py
```

### Adding New Languages
Edit `backend/core/language_detector.py` and add language patterns.

### Customizing Personality
Edit `backend/core/personality_manager.py` to add new personality modes.

## License

[Your License Here]

## Credits

Built with:
- Ollama for AI models
- Stable Diffusion for image generation
- OpenAI Whisper for speech recognition
- eSpeak-NG for text-to-speech
- FastAPI, React, and many other open-source projects

## Support

For issues and questions, please check the documentation in the `docs/` folder.

---

**Version**: 1.0.0  
**Last Updated**: April 24, 2026  
**Status**: Production Ready ✅
