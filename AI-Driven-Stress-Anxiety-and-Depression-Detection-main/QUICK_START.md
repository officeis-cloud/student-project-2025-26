# 🚀 Quick Start Guide

This guide will help you get the AI-Driven Mental Health System up and running in minutes.

## ✅ Step 1: Install Prerequisites

Make sure you have installed:
- Python 3.8+ ([Download here](https://www.python.org/downloads/))
- Node.js 18+ ([Download here](https://nodejs.org/))

Verify installations:
```bash
python --version
node --version
npm --version
```

## 🔧 Step 2: Backend Setup

### Option A: Automated Setup (Windows)

1. Open PowerShell in the project root directory
2. Run the backend setup script:
```powershell
cd backend
python -m pip install -r requirements.txt
```

3. **IMPORTANT: Add Your Trained Model**
   - Create a folder: `backend/models/distilbert-goemotions-mental/`
   - Copy your Phase 2 trained model files into this folder:
     - `config.json`
     - `pytorch_model.bin` 
     - `tokenizer_config.json`
     - `vocab.txt`
     - Any other model files

4. Initialize the database:
```powershell
python app.py
```
Press `Ctrl+C` after you see "Running on http://0.0.0.0:5000", then seed the database:
```powershell
python seed.py
```

5. Start the backend server:
```powershell
python app.py
```

The backend should now be running on `http://localhost:5000`

### Option B: Manual Setup

1. Navigate to backend:
```bash
cd backend
```

2. Create virtual environment (recommended):
```bash
python -m venv venv
# Activate it:
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Add your trained model (see step 3 in Option A)

5. Run the server:
```bash
python app.py
```

## 🎨 Step 3: Frontend Setup

### In a new terminal:

1. Navigate to frontend:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start development server:
```bash
npm run dev
```

The frontend should now be running on `http://localhost:5173`

## 🎯 Step 4: Test the Application

1. **Open your browser** to `http://localhost:5173`

2. **Create an account:**
   - Click "Sign Up"
   - Fill in your details
   - Accept the consent checkbox
   - Click "Create Account"

3. **Test emotion analysis:**
   - Navigate to "Journal" page
   - Write some text expressing emotions
   - Click "Analyze"
   - View your emotional insights and recommendations

4. **Explore features:**
   - Dashboard: See your overview
   - Trends: View mood history
   - Insights: Get AI recommendations
   - Wellness: Access wellness tips

## ⚙️ Verification Checklist

✅ Backend running on port 5000  
✅ Frontend running on port 5173  
✅ Can access login page  
✅ Can create account  
✅ Can log in  
✅ Can submit journal entry  
✅ Receives emotion predictions  

## 🐛 Common Issues

### Backend won't start
**Error**: `ModuleNotFoundError: No module named 'flask'`  
**Solution**: Install requirements: `pip install -r requirements.txt`

**Error**: `Model not found`  
**Solution**: Copy your trained model to `backend/models/distilbert-goemotions-mental/`

### Frontend won't start
**Error**: `npm: command not found`  
**Solution**: Install Node.js from https://nodejs.org/

**Error**: `Cannot connect to backend`  
**Solution**: Ensure backend is running on port 5000

### Cannot login/register
**Error**: Network error  
**Solution**: Check if backend is running. Check browser console (F12) for errors.

**Error**: `CORS error`  
**Solution**: Verify `CORS_ORIGINS` in `backend/.env` includes `http://localhost:5173`

## 📝 Environment Variables

Both `.env` files are already created with default values.

### Backend (.env)
```env
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=dev-secret-key-12345
JWT_SECRET_KEY=jwt-secret-key-67890
DATABASE_URL=sqlite:///mental_health.db
MODEL_PATH=./models/distilbert-goemotions-mental
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

### Frontend (.env)
```env
VITE_API_URL=http://localhost:5000/api
```

## 🎓 Next Steps

1. **Explore the Dashboard** - Familiarize yourself with all features
2. **Add Multiple Entries** - Track your mood over several days
3. **View Trends** - Check the trends page after adding entries
4. **Read the Main README** - For detailed API documentation

## 🔗 Helpful Commands

### Backend
```bash
# Run server
python app.py

# Seed database
python seed.py

# Check if running
curl http://localhost:5000/api/health
```

### Frontend
```bash
# Development mode
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## 📚 Documentation

- **Main README**: [README.md](../README.md)
- **Backend README**: [backend/README.md](../backend/README.md)
- **API Documentation**: See main README
- **Project Details**: [project details/](../project%20details/)

## 💡 Tips

1. **Keep both terminals open** - One for backend, one for frontend
2. **Use browser DevTools** (F12) to debug frontend issues
3. **Check terminal output** for backend errors
4. **Clear browser cache** if you see old data
5. **Use Postman** to test API endpoints directly

## 🆘 Still Having Issues?

1. Check both terminal outputs for error messages
2. Verify all prerequisites are installed
3. Ensure ports 5000 and 5173 are not in use
4. Try restarting both servers
5. Delete `backend/mental_health.db` and restart backend to reset database

## ✅ Success!

If you can see the login page, create an account, and submit a journal entry that returns emotion predictions, you're all set! 🎉

Enjoy using the AI-Driven Mental Health System!

---

**Need help?** Check the troubleshooting section in the main README or review the project documentation.
