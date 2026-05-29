# 🚀 How to Start Leo AI

## Quick Start Guide

### Step 1: Navigate to Project Folder

From your Desktop, run:
```bash
cd "final sv llm\bobmarleyy"
```

Or from anywhere:
```bash
cd "C:\Users\bhaskar\Desktop\final sv llm\bobmarleyy"
```

### Step 2: Start Leo AI

Once you're in the `bobmarleyy` folder, run:
```bash
START.bat
```

This will:
1. Start the backend server (Python)
2. Start the frontend server (Node.js)
3. Open your browser automatically

### Step 3: Access Leo AI

After starting, Leo AI will be available at:
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000

---

## Common Errors

### Error: "The system cannot find the path specified"
**Problem**: You're not in the correct directory

**Solution**: Navigate to the project folder first
```bash
cd "C:\Users\bhaskar\Desktop\final sv llm\bobmarleyy"
```

### Error: "Could not read package.json"
**Problem**: You're trying to run npm from the wrong directory

**Solution**: Make sure you're in the `bobmarleyy` folder, then run `START.bat`

### Error: "Port already in use"
**Problem**: Backend or frontend is already running

**Solution**: Stop existing servers first
```bash
STOP.bat
```
Then start again:
```bash
START.bat
```

---

## Manual Start (Alternative)

If `START.bat` doesn't work, you can start manually:

### Start Backend
```bash
cd backend
venv\Scripts\activate
python main.py
```

### Start Frontend (in new terminal)
```bash
cd frontend
npm run dev
```

---

## Verify Everything is Working

Run the health check:
```bash
cd backend
venv\Scripts\python.exe ..\tests\test_system.py
```

---

## Stop Leo AI

To stop all servers:
```bash
STOP.bat
```

Or manually:
- Press `Ctrl+C` in each terminal window

---

## Directory Structure

Make sure you're in the right place:
```
C:\Users\bhaskar\Desktop\final sv llm\bobmarleyy\
├── backend/
├── frontend/
├── docs/
├── tests/
├── scripts/
├── START.bat    ← Run this to start
└── STOP.bat     ← Run this to stop
```

---

## Quick Commands Reference

| From | Command | Action |
|------|---------|--------|
| Desktop | `cd "final sv llm\bobmarleyy"` | Navigate to project |
| bobmarleyy/ | `START.bat` | Start everything |
| bobmarleyy/ | `STOP.bat` | Stop everything |
| Anywhere | `cd "C:\Users\bhaskar\Desktop\final sv llm\bobmarleyy"` | Go to project |

---

## Need Help?

1. Make sure you're in the `bobmarleyy` folder
2. Check that backend is running: http://localhost:8000/api/system/health
3. Check that frontend is running: http://localhost:5173
4. Run health check: `cd backend && venv\Scripts\python.exe ..\tests\test_system.py`

---

**Remember**: Always navigate to the `bobmarleyy` folder first before running any commands!
