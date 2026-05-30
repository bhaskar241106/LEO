# Contributing to LEO AI

Thank you for your interest in contributing to **LEO AI**! We welcome contributions to improve the offline voice synthesis, 3D animations, gesture controls, RAG indexers, or frontend layout styles.

---

## 🛠️ Local Development Setup

To establish a sandbox development environment on your local machine:

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/your-username/bobmarleyy.git
    cd bobmarleyy
    ```
2.  **Prerequisites:**
    Ensure you have the following installed:
    *   **Python 3.11+**
    *   **Node.js 18+**
    *   **Ollama App** (running locally in the background)
    *   **eSpeak-NG** (installed and added to system environmental path variables)
3.  **Boot the Backend Environment:**
    ```bash
    cd backend
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Unix/MacOS
    source venv/bin/activate
    
    pip install -r requirements.txt
    ```
4.  **Boot the Frontend Environment:**
    ```bash
    cd ../frontend
    npm install
    ```

---

## 🏗️ Codebase Organization

*   `/backend` — FastAPI web service. Core brain modules are located in `/backend/core/` (RAG handlers, language parsing, SQLite database adapters) and third-party integrations are located in `/backend/services/` (Whisper, Stable Diffusion, eSpeak, Piper).
*   `/frontend` — React 19 application built via Vite. The WebGL 3D avatar canvas is located in `src/components/Avatar/` (Scene3D, Avatar Loader).
*   `/tests` — Visual verification suites and health checkers.

---

## 🧪 Testing & Verification

We enforce strict test verification before submitting pull requests.

### 1. Run the Sanity Health Check:
Execute the system health checks in your terminal:
```bash
# Activate your backend virtual environment first, then run:
$env:PYTHONIOENCODING="utf-8" ; venv\Scripts\python.exe ..\tests\test_system.py
```
Verify that:
*   File structure checks return `PASS`.
*   Python dependency parses return `PASS`.
*   SQLite memory connection returns `PASS`.

### 2. Verify RAG Indexing:
Ensure that local database semantic search indexing is operational:
```bash
$env:PYTHONPATH="." ; $env:PYTHONIOENCODING="utf-8" ; backend\venv\Scripts\python.exe tests/init_rag.py
```

---

## 🎨 Styling & Component Guidelines

1.  **Strict Styling Constraints:** Use standard vanilla CSS styling inside `.css` stylesheets for maximum layout flexibility. Avoid installing TailwindCSS or utility frameworks unless explicitly approved.
2.  **Component Modularity:** Keep components focused and reusable. For instance, any new 3D graphics filters should be isolated inside `src/components/Effects/` or `src/components/Avatar/`.
3.  **Decoupled Controllers:** Keep frontend user interfaces isolated from standard state models using hooks (such as `useLipSync.js`).

---

## 📜 Pull Request Process

1.  Create a separate feature branch (`git checkout -b feature/amazing-improvement`).
2.  Commit your changes with clear, descriptive commit messages (`git commit -m "feat: integrate Piper audio streaming routes"`).
3.  Ensure all system verification tests pass without warning.
4.  Push your branch to GitHub and open a Pull Request.
5.  All PRs are reviewed and checked by project maintainers for runtime performance and thread safety.
