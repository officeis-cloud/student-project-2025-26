# 🚀 MindCare AI - Complete Setup Guide

This guide will help you set up and run the MindCare AI project from scratch on a new laptop.

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation Steps](#installation-steps)
3. [Backend Setup](#backend-setup)
4. [Frontend Setup](#frontend-setup)
5. [Running the Application](#running-the-application)
6. [Environment Variables](#environment-variables)
7. [Common Issues & Solutions](#common-issues--solutions)
8. [Project Structure](#project-structure)

---

## 📦 Prerequisites

Before you begin, ensure you have the following installed on your system:

### Required Software

1. **Python 3.10 or 3.11**
   - Download from: https://www.python.org/downloads/
   - ⚠️ **Important**: During installation, check "Add Python to PATH"
   - Verify installation:
     ```bash
     python --version
     ```

2. **Node.js 18+ and npm**
   - Download from: https://nodejs.org/ (LTS version recommended)
   - Verify installation:
     ```bash
     node --version
     npm --version
     ```

3. **Git**
   - Download from: https://git-scm.com/downloads
   - Verify installation:
     ```bash
     git --version
     ```

4. **MongoDB Atlas Account** (Cloud Database)
   - Sign up for free at: https://www.mongodb.com/cloud/atlas
   - Create a new cluster (free tier is sufficient)
   - Get your connection string

### Optional but Recommended

- **Visual Studio Code**: https://code.visualstudio.com/
- **Postman** (for API testing): https://www.postman.com/downloads/

---

## 🔧 Installation Steps

### Step 1: Clone the Repository

```bash
# Clone the project (or extract from ZIP if you received it that way)
cd "path/to/your/projects/folder"
git clone <repository-url>
cd "stress raw 2"

# Or if you already have the folder, just navigate to it
cd "c:\Users\YourName\OneDrive\Desktop\stress raw 2"
```

### Step 2: Verify Project Structure

Make sure you have these main folders:
```
stress raw 2/
├── backend/           # Flask Python backend
├── frontend/          # React TypeScript frontend
├── diagrams/          # System diagrams
├── README.md          # Project overview
└── SETUP.md          # This file
```

---

## 🐍 Backend Setup

### Step 1: Create Virtual Environment

```bash
# Navigate to backend folder
cd backend

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows PowerShell:
.venv\Scripts\Activate.ps1

# On Windows CMD:
.venv\Scripts\activate.bat

# On macOS/Linux:
source .venv/bin/activate
```

**Note**: If you get an execution policy error on Windows PowerShell, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Step 2: Install Python Dependencies

```bash
# Make sure virtual environment is activated (you should see (.venv) in prompt)
pip install --upgrade pip
pip install -r requirements.txt
```

**⏱️ This will take 5-15 minutes** depending on your internet speed (PyTorch is large ~2GB).

### Step 3: Create Environment Variables

Create a file named `.env` in the `backend/` folder:

```bash
# Create .env file
# On Windows:
type nul > .env

# On macOS/Linux:
touch .env
```

Edit `.env` and add the following:

```env
# Database Configuration
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/mindcare?retryWrites=true&w=majority

# JWT Secret (generate a random secret key)
JWT_SECRET_KEY=your-super-secret-jwt-key-here-change-this-in-production

# Flask Configuration
FLASK_ENV=development
FLASK_APP=app.py
SECRET_KEY=your-flask-secret-key-here

# Port Configuration
PORT=5000
```

**🔑 Important**: 
- Replace `MONGODB_URI` with your actual MongoDB Atlas connection string
- Generate strong secret keys for production (use a password generator)

### Step 4: Download AI Model (First Time Setup)

The DistilBERT model will be downloaded automatically on first run (~250MB). This happens when you:
- Start the Flask server for the first time
- Or run `python test_model.py`

To pre-download the model:
```bash
python -c "from emotion_predictor import emotion_predictor; print('Model loaded successfully!')"
```

### Step 5: Verify Backend Setup

```bash
# Test the backend server
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
 * Emotion predictor initialized successfully
```

Press `Ctrl+C` to stop the server.

---

## ⚛️ Frontend Setup

### Step 1: Navigate to Frontend Folder

```bash
# From project root
cd frontend

# Or if you're in backend folder:
cd ../frontend
```

### Step 2: Install Node Dependencies

```bash
# Install all npm packages
npm install
```

**⏱️ This will take 2-5 minutes**.

### Step 3: Create Environment Variables (Optional)

If you need custom API configuration, create `.env` in `frontend/`:

```env
VITE_API_URL=http://localhost:5000/api
```

The default configuration points to `http://localhost:5000/api`, so this step is optional for local development.

### Step 4: Verify Frontend Setup

```bash
# Start development server
npm run dev
```

You should see:
```
  VITE v7.0.3  ready in 500 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

Press `Ctrl+C` to stop the server.

---

## 🚀 Running the Application

### Method 1: Development Mode (Recommended)

You need **TWO terminal windows**:

**Terminal 1 - Backend:**
```bash
cd backend
.venv\Scripts\Activate.ps1    # Activate virtual environment
python app.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

Then open your browser and go to:
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:5000

### Method 2: Using PowerShell Script (Advanced)

Create a file `start-dev.ps1` in the project root:

```powershell
# Start backend in background
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; .\.venv\Scripts\Activate.ps1; python app.py"

# Wait 5 seconds for backend to start
Start-Sleep -Seconds 5

# Start frontend
cd frontend
npm run dev
```

Run it:
```bash
.\start-dev.ps1
```

---

## 🔐 Environment Variables

### Backend `.env` (Required)

| Variable | Description | Example |
|----------|-------------|---------|
| `MONGODB_URI` | MongoDB connection string | `mongodb+srv://...` |
| `JWT_SECRET_KEY` | Secret for JWT tokens | `your-secret-key-123` |
| `FLASK_ENV` | Flask environment | `development` |
| `PORT` | Backend server port | `5000` |

### Frontend `.env` (Optional)

| Variable | Description | Default |
|----------|-------------|---------|
| `VITE_API_URL` | Backend API URL | `http://localhost:5000/api` |

---

## 🔧 Common Issues & Solutions

### Issue 1: "Python not found" or "Module not found"

**Solution:**
```bash
# Ensure virtual environment is activated
cd backend
.venv\Scripts\Activate.ps1

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue 2: "Port 5000 already in use"

**Solution:**
```bash
# Find process using port 5000 (Windows)
netstat -ano | findstr :5000

# Kill the process (replace PID with actual process ID)
taskkill /PID <PID> /F

# Or use a different port in backend/.env
PORT=5001
```

### Issue 3: "CORS error" when frontend calls backend

**Solution:**
- Ensure backend is running on port 5000
- Check `backend/app.py` has CORS enabled
- Verify frontend is calling correct API URL

### Issue 4: "MongoDB connection failed"

**Solution:**
1. Check your MongoDB Atlas connection string
2. Ensure your IP address is whitelisted in MongoDB Atlas
3. Verify database user credentials are correct

### Issue 5: "npm ERR! code ENOENT" or Node errors

**Solution:**
```bash
# Delete node_modules and package-lock.json
cd frontend
Remove-Item -Recurse -Force node_modules
Remove-Item package-lock.json

# Reinstall
npm install
```

### Issue 6: "Execution policy error" on Windows

**Solution:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Issue 7: Model download fails or is slow

**Solution:**
- The DistilBERT model is ~250MB and downloads from HuggingFace
- Use a stable internet connection
- If download fails, delete `backend/.cache/` and try again
- Or manually download from: https://huggingface.co/distilbert-base-uncased

### Issue 8: Virtual environment activation fails

**Solution:**
```bash
# Recreate virtual environment
cd backend
Remove-Item -Recurse -Force .venv
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

## 📁 Project Structure

```
stress raw 2/
│
├── backend/                          # Flask backend
│   ├── app.py                       # Main Flask application
│   ├── models.py                    # Database models (User, MoodEntry)
│   ├── config.py                    # Configuration settings
│   ├── emotion_predictor.py         # AI emotion detection
│   ├── recommendation_engine.py     # Wellness recommendations
│   ├── requirements.txt             # Python dependencies
│   ├── .env                         # Environment variables (create this)
│   ├── .venv/                       # Virtual environment (created by setup)
│   │
│   └── routes/                      # API routes
│       ├── auth.py                  # Authentication endpoints
│       ├── predict.py               # Emotion prediction endpoints
│       └── user.py                  # User management endpoints
│
├── frontend/                         # React frontend
│   ├── src/
│   │   ├── App.tsx                  # Main React component
│   │   ├── main.tsx                 # Entry point
│   │   ├── pages/                   # Page components
│   │   │   ├── home/
│   │   │   ├── login/
│   │   │   ├── journal/
│   │   │   ├── analyze/
│   │   │   ├── trends/
│   │   │   ├── insights/
│   │   │   └── wellness/
│   │   │
│   │   ├── components/              # Reusable components
│   │   └── router/                  # React Router configuration
│   │
│   ├── package.json                 # Node dependencies
│   ├── vite.config.ts              # Vite configuration
│   ├── tailwind.config.ts          # TailwindCSS configuration
│   └── node_modules/               # Node packages (created by npm install)
│
├── diagrams/                         # System diagrams (PNG images)
│   ├── 01-sequence-diagram.png
│   ├── 02-context-diagram.png
│   └── ... (10 diagrams total)
│
├── README.md                         # Project overview
├── SETUP.md                         # This setup guide
├── MODEL_ARCHITECTURE_EXPLANATION.md # AI model documentation
└── MODEL_WORKFLOW_VISUAL.md         # AI workflow documentation
```

---

## 🧪 Testing the Setup

### 1. Test Backend API

```bash
# In backend terminal (with virtual env activated)
python test_model.py
```

Expected output:
```
Testing text: "I'm feeling happy today!"
Emotions detected: {'joy': 0.85, 'optimism': 0.72, ...}
```

### 2. Test Frontend Build

```bash
# In frontend terminal
npm run build
```

Should complete without errors.

### 3. Full Integration Test

1. Start backend: `python app.py`
2. Start frontend: `npm run dev`
3. Open http://localhost:5173
4. Click "Sign Up" and create test account
5. Login with credentials
6. Go to "Journal" page
7. Write a test entry (e.g., "I'm feeling great today!")
8. Click "Analyze & Save"
9. Check if emotions are detected and displayed

---

## 📚 Additional Resources

### Documentation
- [README.md](README.md) - Project overview and features
- [MODEL_ARCHITECTURE_EXPLANATION.md](MODEL_ARCHITECTURE_EXPLANATION.md) - AI model details
- [MODEL_WORKFLOW_VISUAL.md](MODEL_WORKFLOW_VISUAL.md) - Visual workflow guide

### Technologies Used
- **Backend**: Flask (Python), MongoDB, PyTorch, HuggingFace Transformers
- **Frontend**: React, TypeScript, TailwindCSS, Vite
- **AI Model**: DistilBERT fine-tuned on GoEmotions dataset

### External Links
- [Flask Documentation](https://flask.palletsprojects.com/)
- [React Documentation](https://react.dev/)
- [MongoDB Atlas](https://www.mongodb.com/docs/atlas/)
- [HuggingFace Transformers](https://huggingface.co/docs/transformers/)
- [TailwindCSS](https://tailwindcss.com/docs)

---

## 🆘 Getting Help

If you encounter issues not covered in this guide:

1. **Check the error message carefully** - it often tells you exactly what's wrong
2. **Search for the error** on Google or Stack Overflow
3. **Check your environment variables** - 90% of issues are configuration problems
4. **Verify all dependencies installed** - run `pip list` and `npm list`
5. **Try restarting** both backend and frontend servers

---

## ✅ Checklist: Verify Your Setup

Before running the application, ensure:

- [ ] Python 3.10+ installed and added to PATH
- [ ] Node.js 18+ and npm installed
- [ ] Git installed
- [ ] MongoDB Atlas account created and connection string obtained
- [ ] Backend virtual environment created and activated
- [ ] Backend dependencies installed (`pip install -r requirements.txt`)
- [ ] Backend `.env` file created with MongoDB URI and secrets
- [ ] Frontend dependencies installed (`npm install`)
- [ ] Both servers start without errors
- [ ] Can access frontend at http://localhost:5173
- [ ] Can access backend at http://localhost:5000

---

## 🎉 Success!

If all steps completed successfully, you should now have:
- ✅ Backend running on http://localhost:5000
- ✅ Frontend running on http://localhost:5173
- ✅ MongoDB connected
- ✅ AI model loaded and ready
- ✅ Complete development environment ready

**You're all set to use MindCare AI!** 🚀

---

**Last Updated**: March 5, 2026  
**Setup Time**: ~30-45 minutes (first time)  
**Support**: Check documentation or error messages for troubleshooting



<!-- mongodb+srv://sanjana120504_db_user:lDcaGIOX4YCUSVVP@cluster0.8quo5kf.mongodb.net/?appName=Cluster0 -->