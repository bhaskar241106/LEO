# Project Structure

## Overview

Leo AI is organized into a clean, modular structure for easy navigation and development.

## Directory Structure

```
bobmarleyy/
├── 📁 backend/              # Python FastAPI Backend
│   ├── core/               # Core AI functionality
│   │   ├── ai_engine.py           # AI model routing
│   │   ├── data_manager.py        # Data management
│   │   ├── emotion_analyzer.py    # Emotion detection
│   │   ├── hardware_detector.py   # Hardware detection
│   │   ├── language_detector.py   # Language detection
│   │   ├── memory_manager.py      # Conversation memory
│   │   ├── personality_manager.py # Personality modes
│   │   ├── rag_handler.py         # RAG system
│   │   └── transliteration_detector.py # Script detection
│   ├── services/           # Service layer
│   │   ├── audio_pipeline.py      # Audio processing
│   │   ├── image_generator.py     # Image generation
│   │   ├── phoneme_extractor.py   # Lip sync
│   │   ├── scheduler_service.py   # Task scheduling
│   │   ├── system_service.py      # System info
│   │   └── tiny_image_gen.py      # Lightweight image gen
│   ├── routes/             # API endpoints
│   ├── data/               # Database and storage
│   ├── venv/               # Python virtual environment
│   ├── .env                # Configuration
│   ├── main.py             # Entry point
│   └── requirements.txt    # Python dependencies
│
├── 📁 frontend/             # React Frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   │   ├── Avatar/            # 3D avatar
│   │   │   ├── Chat/              # Chat interface
│   │   │   ├── GestureControl/    # Gesture controls
│   │   │   ├── Navigation/        # Navigation
│   │   │   └── UI/                # UI components
│   │   ├── views/          # Page views
│   │   │   ├── ChatView.jsx       # Main chat
│   │   │   ├── ImageGeneratorView.jsx # Image gen
│   │   │   ├── MemoryView.jsx     # Memory browser
│   │   │   ├── SchedulerView.jsx  # Task scheduler
│   │   │   └── SettingsView.jsx   # Settings
│   │   ├── services/       # API services
│   │   ├── utils/          # Utilities
│   │   ├── App.jsx         # Main app
│   │   └── main.jsx        # Entry point
│   ├── public/             # Static assets
│   ├── dist/               # Build output
│   ├── package.json        # Node dependencies
│   └── vite.config.js      # Vite configuration
│
├── 📁 mobile/               # React Native Mobile App
│   ├── src/                # Mobile source code
│   ├── android/            # Android build
│   ├── ios/                # iOS build
│   └── package.json        # Mobile dependencies
│
├── 📁 docs/                 # 📚 Documentation
│   ├── ARCHITECTURE.md              # System architecture
│   ├── BENCHMARKS_AND_TESTING.md    # Performance tests
│   ├── CHANGELOG.md                 # Version history
│   ├── CLEANUP_SUMMARY.md           # Cleanup details
│   ├── COMPREHENSIVE_METRICS_REPORT.md # Metrics
│   ├── DATA_SECURITY_ARCHITECTURE.md # Security
│   ├── PROJECT_STRUCTURE.md         # This file
│   └── TTS_STT_TECHNOLOGIES.md      # Voice tech
│
├── 📁 tests/                # 🧪 Test Files
│   ├── test_multilingual.py         # Language tests
│   ├── test_backend_image.py        # Image gen tests
│   ├── test_performance.py          # Performance tests
│   ├── demo_multilingual.py         # Language demo
│   ├── CHECK_SETUP.py               # Setup verification
│   └── verify_security.py           # Security checks
│
├── 📁 scripts/              # 🔧 Utility Scripts
│   ├── app_launcher.py              # App launcher
│   ├── setup.ps1                    # Setup script
│   └── setup_desktop_icon.ps1       # Desktop shortcut
│
├── 📁 assets/               # 🎨 Assets
│   ├── icon.ico                     # Windows icon
│   └── icon.png                     # App icon
│
├── 📁 .git/                 # Git repository
├── 📁 .vscode/              # VS Code settings
│
├── 📄 .gitignore            # Git ignore rules
├── 📄 README.md             # Main documentation
├── ▶️ START.bat             # Start all servers
└── ⏹️ STOP.bat              # Stop all servers
```

## Key Files

### Root Level
- **README.md** - Main project documentation
- **START.bat** - Start backend and frontend
- **STOP.bat** - Stop all servers
- **.gitignore** - Git ignore configuration

### Backend
- **main.py** - FastAPI application entry point
- **.env** - Environment configuration
- **requirements.txt** - Python dependencies

### Frontend
- **src/App.jsx** - React application root
- **package.json** - Node.js dependencies
- **vite.config.js** - Build configuration

## Configuration Files

### Backend Configuration (`backend/.env`)
```env
# Server
PORT=8000
HOST=0.0.0.0

# AI Models
OLLAMA_URL=http://localhost:11434
FAST_MODEL=llama3.2:1b
EXPERT_MODEL=phi3:mini

# Settings
TEMPERATURE=0.85
ENABLE_GPU=true
CUDA_ENABLED=true
IMAGE_GEN_BACKEND=tiny_local
```

### Frontend Configuration (`frontend/vite.config.js`)
```javascript
export default {
  server: {
    port: 5173,
    proxy: {
      '/api': 'http://localhost:8000'
    }
  }
}
```

## Data Storage

### Backend Data
- **Location**: `backend/data/`
- **Database**: `memory.db` (SQLite)
- **Archives**: `archives/` folder

### Frontend Data
- **Location**: `frontend/data/`
- **Cache**: Browser localStorage
- **Temp**: Browser sessionStorage

## Build Outputs

### Frontend Build
- **Location**: `frontend/dist/`
- **Command**: `npm run build`
- **Output**: Static HTML, CSS, JS

### Mobile Build
- **Android**: `mobile/android/app/build/`
- **iOS**: `mobile/ios/build/`

## Development Workflow

### 1. Start Development
```bash
START.bat
```

### 2. Make Changes
- Backend: Edit files in `backend/`
- Frontend: Edit files in `frontend/src/`
- Mobile: Edit files in `mobile/src/`

### 3. Test Changes
```bash
cd tests
python test_multilingual.py
```

### 4. Build for Production
```bash
# Frontend
cd frontend
npm run build

# Mobile
cd mobile
npm run build:android
npm run build:ios
```

## Adding New Features

### New Backend Endpoint
1. Create route in `backend/routes/`
2. Add service in `backend/services/`
3. Update API docs

### New Frontend Component
1. Create component in `frontend/src/components/`
2. Import in view or App.jsx
3. Add styles

### New Test
1. Create test file in `tests/`
2. Follow naming: `test_*.py`
3. Run with `python tests/test_name.py`

## Documentation

All documentation is in the `docs/` folder:

| File | Purpose |
|------|---------|
| ARCHITECTURE.md | System design and architecture |
| BENCHMARKS_AND_TESTING.md | Performance benchmarks |
| CHANGELOG.md | Version history and changes |
| CLEANUP_SUMMARY.md | Project cleanup details |
| COMPREHENSIVE_METRICS_REPORT.md | Detailed metrics |
| DATA_SECURITY_ARCHITECTURE.md | Security implementation |
| PROJECT_STRUCTURE.md | This file |
| TTS_STT_TECHNOLOGIES.md | Voice technology details |

## Best Practices

### File Organization
- ✅ Keep related files together
- ✅ Use descriptive names
- ✅ Follow existing patterns
- ✅ Document complex code

### Code Style
- **Python**: Follow PEP 8
- **JavaScript**: Use ESLint rules
- **React**: Functional components with hooks

### Git Workflow
1. Create feature branch
2. Make changes
3. Test thoroughly
4. Commit with clear message
5. Merge to main

## Maintenance

### Regular Tasks
- Update dependencies monthly
- Review and clean logs
- Backup database weekly
- Test all features after updates

### Cleanup
- Remove unused files
- Clear old logs
- Archive old data
- Update documentation

---

**Last Updated**: April 24, 2026  
**Maintained By**: Leo AI Team
