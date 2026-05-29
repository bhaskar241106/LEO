# 🏗️ Leo AI Assistant - Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     USER INTERFACE                          │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐  │
│  │         Desktop App (PyWebView)                     │  │
│  │              OR                                      │  │
│  │         Web Browser (http://localhost:5173)         │  │
│  └─────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ HTTP/WebSocket
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                  FRONTEND (React + Vite)                    │
│                   Port: 5173                                │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │   Chat UI    │  │  3D Avatar   │  │  Scheduler   │    │
│  │              │  │  (Three.js)  │  │              │    │
│  └──────────────┘  └──────────────┘  └──────────────┘    │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │   History    │  │ Customizer   │  │   System     │    │
│  │              │  │              │  │   Stats      │    │
│  └──────────────┘  └──────────────┘  └──────────────┘    │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ REST API / Proxy
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                  BACKEND (FastAPI)                          │
│                   Port: 8000                                │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐ │
│  │                   API Routes                         │ │
│  │  /chat  /chat_stream  /api/schedule  /api/system    │ │
│  └──────────────────────────────────────────────────────┘ │
│                            │                                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │  AI Engine   │  │   Memory     │  │     RAG      │    │
│  │              │  │   Manager    │  │   Handler    │    │
│  └──────────────┘  └──────────────┘  └──────────────┘    │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │ Personality  │  │   Phoneme    │  │  Scheduler   │    │
│  │   Manager    │  │  Extractor   │  │   Service    │    │
│  └──────────────┘  └──────────────┘  └──────────────┘    │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ HTTP API
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                  OLLAMA AI ENGINE                           │
│                   Port: 11434                               │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │   Mistral    │  │     Phi      │  │  TinyLlama   │    │
│  │   (Default)  │  │  (Low-end)   │  │  (Minimal)   │    │
│  └──────────────┘  └──────────────┘  └──────────────┘    │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                  LOCAL STORAGE                              │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │  memory.db   │  │schedules.json│  │  RAG Docs    │    │
│  │  (SQLite)    │  │              │  │  (ChromaDB)  │    │
│  └──────────────┘  └──────────────┘  └──────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

## Data Flow

### Chat Message Flow
```
User Input → Frontend → Backend → Ollama → Backend → Frontend → User
                ↓                    ↓
            Memory DB            RAG Context
```

### Detailed Chat Flow
1. User types message in frontend
2. Frontend sends POST to `/chat` or `/chat_stream`
3. Backend retrieves context from RAG
4. Backend gets conversation history from Memory
5. Backend sends prompt to Ollama
6. Ollama generates response
7. Backend extracts phonemes for lip-sync
8. Backend saves to Memory
9. Backend returns response + visemes
10. Frontend displays message and animates avatar

## Component Breakdown

### Frontend Components

```
frontend/
├── src/
│   ├── components/
│   │   ├── Avatar/
│   │   │   ├── Avatar.jsx          # 3D avatar renderer
│   │   │   ├── AvatarCreator.jsx   # Avatar upload/creation
│   │   │   └── Scene3D.jsx         # Three.js scene setup
│   │   ├── Customization/
│   │   │   └── Customizer.jsx      # Personality/settings
│   │   └── Navigation/
│   │       └── Sidebar.jsx         # Navigation menu
│   ├── views/
│   │   ├── ChatView.jsx            # Main chat interface
│   │   ├── HomeView.jsx            # Dashboard/stats
│   │   ├── HistoryView.jsx         # Conversation history
│   │   └── ScheduleView.jsx        # Reminders/tasks
│   ├── hooks/
│   │   └── useLipSync.js           # Lip-sync animation
│   ├── config.js                   # API configuration
│   └── App.jsx                     # Main app component
```

### Backend Components

```
backend/
├── core/
│   ├── ai_engine.py           # Ollama integration
│   ├── memory_manager.py      # Conversation storage
│   ├── rag_handler.py         # Document retrieval
│   ├── personality_manager.py # Personality system
│   └── hardware_detector.py   # GPU/CPU detection
├── services/
│   ├── audio_pipeline.py      # Audio processing
│   ├── phoneme_extractor.py   # Lip-sync data
│   ├── scheduler_service.py   # Reminders/tasks
│   └── system_service.py      # System commands
├── routes/
│   └── avatar.py              # Avatar upload API
└── main.py                    # FastAPI app
```

## API Endpoints

### Chat Endpoints
- `POST /chat` - Send message, get full response
- `POST /chat_stream` - Send message, get streaming response
- `GET /api/chat/history` - Get conversation history

### Avatar Endpoints
- `POST /api/upload-avatar` - Upload custom VRM avatar

### Scheduler Endpoints
- `POST /api/schedule/add` - Create reminder
- `GET /api/schedule/all` - List all reminders
- `DELETE /api/schedule/{id}` - Delete reminder
- `GET /api/notifications` - Get pending alerts

### System Endpoints
- `GET /api/system/stats` - CPU, RAM, disk usage
- `GET /api/system/health` - Service health check
- `POST /api/system/execute` - Execute system command

## Technology Stack

### Frontend
- **Framework:** React 19
- **Build Tool:** Vite 8
- **3D Graphics:** Three.js + React Three Fiber
- **Avatar:** @pixiv/three-vrm
- **HTTP Client:** Axios
- **Animation:** Framer Motion
- **Icons:** Lucide React

### Backend
- **Framework:** FastAPI
- **Server:** Uvicorn
- **AI:** Ollama (Mistral/Phi/TinyLlama)
- **Database:** SQLite
- **Vector DB:** ChromaDB
- **Embeddings:** Sentence Transformers
- **Audio:** Whisper, Librosa, eSpeak-NG
- **Scheduler:** Python Schedule

### Desktop App
- **Framework:** PyWebView
- **Platform:** Cross-platform (Windows/Mac/Linux)

## Port Configuration

| Service | Port | Protocol | Purpose |
|---------|------|----------|---------|
| Frontend | 5173 | HTTP | React dev server |
| Backend | 8000 | HTTP | FastAPI API |
| Ollama | 11434 | HTTP | AI model API |

## Security Model

### CORS Configuration
- Frontend allowed origins: `*` (development)
- Production: Should be restricted to specific domains

### Data Privacy
- All data stored locally
- No external API calls
- No telemetry or tracking
- Offline-first architecture

### System Commands
- Require explicit user permission
- Sandboxed execution
- Logged for audit

## Performance Considerations

### Hardware Tiers
1. **High-end:** GPU + 16GB RAM → Mistral model
2. **Mid-range:** CPU + 8GB RAM → Phi model
3. **Low-end:** CPU + 4GB RAM → TinyLlama model

### Optimization Strategies
- Streaming responses for better UX
- Lazy loading of 3D models
- Efficient memory management
- Database indexing
- Response caching

## Deployment Options

### Option 1: Desktop App (Recommended)
- Run `python app_launcher.py`
- Automatic service management
- Native window experience

### Option 2: Manual Services
- Terminal 1: `ollama serve`
- Terminal 2: `cd backend && python main.py`
- Terminal 3: `cd frontend && npm run dev`
- Browser: http://localhost:5173

### Option 3: Production Build
- Build frontend: `npm run build`
- Serve with static server
- Backend as systemd service (Linux) or Windows Service

## Monitoring & Logging

### Backend Logs
- Location: `backend/backend_log.txt`
- Level: INFO
- Includes: API calls, errors, AI responses

### Frontend Logs
- Location: Browser console (F12)
- Includes: Network requests, React errors, 3D rendering

### Ollama Logs
- Location: Terminal output
- Includes: Model loading, inference time

## Scalability

### Current Limitations
- Single-user design
- Local-only (no network access)
- Sequential request processing

### Future Enhancements
- Multi-user support
- Distributed processing
- Cloud sync (optional)
- Mobile app integration

## Dependencies

### Critical Dependencies
- Python 3.9+
- Node.js 18+
- Ollama
- CUDA (optional, for GPU)

### Python Packages
- fastapi, uvicorn (API)
- torch, transformers (AI)
- chromadb, faiss-cpu (RAG)
- whisper, librosa (Audio)

### Node Packages
- react, react-dom (UI)
- three, @react-three/fiber (3D)
- axios (HTTP)
- vite (Build)

---

**This architecture ensures a fully offline, privacy-focused AI assistant with modern UI and powerful features!**
