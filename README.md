# Face System Website

FastAPI backend + Vite frontend  
Works on **Windows, macOS, and Linux**

---

## Requirements

- Python 3.9+
- Node.js 18+
- npm

---

## Backend (FastAPI)

### Windows

```bash
cd face-system-website/backend
python -m venv venv
venv\Scripts\activate
pip install fastapi uvicorn sqlalchemy python-jose requests passlib[bcrypt]
python -m uvicorn app.main:app --reload
```
### Mac OS

```bash
cd face-system-website/backend
python3 -m venv venv
source venv/bin/activate
pip install fastapi uvicorn sqlalchemy python-jose requests passlib[bcrypt]
python3 -m uvicorn app.main:app --reload
```

### Frontend
```bash
cd face-system-website
npm install vite
npm install
npm run dev
