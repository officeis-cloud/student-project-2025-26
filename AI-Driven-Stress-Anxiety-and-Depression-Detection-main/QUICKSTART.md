# ⚡ Quick Start Guide

**For developers who want to get running fast!**

---

## 🎯 TL;DR - Fastest Setup (5 minutes)

### Prerequisites Check
```bash
python --version    # Need 3.10+
node --version      # Need 18+
```

### Backend (Terminal 1)
```bash
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1                    # Windows
pip install -r requirements.txt                # Takes 5-10 min
echo MONGODB_URI=your_connection_string > .env
echo JWT_SECRET_KEY=your_secret_key >> .env
python app.py
```

### Frontend (Terminal 2)
```bash
cd frontend
npm install        # Takes 2-5 min
npm run dev
```

### Open Browser
- Frontend: http://localhost:5173
- Backend: http://localhost:5000

---

## 📝 Environment Variables Required

**backend/.env:**
```env
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/mindcare
JWT_SECRET_KEY=your-secret-key-change-in-production
FLASK_ENV=development
PORT=5000
```

---

## 🐛 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| Port 5000 in use | `taskkill /F /IM python.exe` or change PORT in .env |
| Module not found | Activate virtual env: `.venv\Scripts\Activate.ps1` |
| Execution policy error | `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser` |
| CORS error | Ensure backend runs on port 5000 |
| MongoDB connection failed | Check connection string and IP whitelist |

---

## 📦 What Gets Installed

**Backend (~2.5GB):**
- PyTorch 2.1.0 (largest package)
- Transformers 4.36.0
- Flask + extensions
- MongoDB drivers
- ML libraries

**Frontend (~300MB):**
- React 19 + React Router
- TailwindCSS
- Vite build tool
- TypeScript

---

## 🚀 First Run

1. **Sign up** → Create account at http://localhost:5173/signup
2. **Login** → Use your credentials
3. **Journal** → Write "I'm feeling great today!"
4. **Analyze** → Click "Analyze & Save"
5. **Results** → See emotions detected

---

## ✅ Health Check

```bash
# Backend running?
curl http://localhost:5000/api/health

# Frontend running?
# Open http://localhost:5173 in browser
```

---

For detailed setup instructions, see [SETUP.md](SETUP.md)
