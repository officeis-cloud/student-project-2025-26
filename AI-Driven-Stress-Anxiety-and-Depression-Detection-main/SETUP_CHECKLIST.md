# 📋 Setup Checklist

Use this checklist to ensure everything is properly set up.

## ☐ 1. Prerequisites Installed

- [ ] Python 3.8+ installed
  - Run: `python --version`
  - Should show: Python 3.8 or higher

- [ ] Node.js 18+ installed
  - Run: `node --version`
  - Should show: v18.0.0 or higher

- [ ] npm installed
  - Run: `npm --version`
  - Should show: 8.0.0 or higher

## ☐ 2. Backend Setup

- [ ] Navigate to backend directory
  ```bash
  cd backend
  ```

- [ ] Install Python dependencies
  ```bash
  pip install -r requirements.txt
  ```

- [ ] Verify .env file exists
  - Location: `backend/.env`
  - Should contain: SECRET_KEY, JWT_SECRET_KEY, etc.

- [ ] Add trained model
  - Create directory: `backend/models/distilbert-goemotions-mental/`
  - Copy these files from your Phase 2 training:
    - [ ] `config.json`
    - [ ] `pytorch_model.bin`
    - [ ] `tokenizer_config.json`
    - [ ] `vocab.txt`
    - [ ] Any other model files

- [ ] Initialize database
  ```bash
  python app.py
  ```
  - Press Ctrl+C when you see "Running on http://0.0.0.0:5000"

- [ ] Seed wellness tips (optional)
  ```bash
  python seed.py
  ```

- [ ] Verify backend starts without errors
  ```bash
  python app.py
  ```
  - Should see: "Model loaded successfully"
  - Should see: "Running on http://0.0.0.0:5000"

## ☐ 3. Frontend Setup

- [ ] Navigate to frontend directory (in a new terminal)
  ```bash
  cd frontend
  ```

- [ ] Install npm dependencies
  ```bash
  npm install
  ```

- [ ] Verify .env file exists
  - Location: `frontend/.env`
  - Should contain: `VITE_API_URL=http://localhost:5000/api`

- [ ] Start development server
  ```bash
  npm run dev
  ```
  - Should see: "Local: http://localhost:5173"

## ☐ 4. Verify Setup

- [ ] Backend is running on http://localhost:5000
- [ ] Frontend is running on http://localhost:5173
- [ ] Can access frontend in browser
- [ ] No errors in backend terminal
- [ ] No errors in frontend terminal

## ☐ 5. Test Basic Functionality

- [ ] Open http://localhost:5173 in browser
- [ ] Can see the login page
- [ ] Click "Sign Up"
- [ ] Fill registration form:
  - [ ] Enter name
  - [ ] Enter email
  - [ ] Enter password
  - [ ] Check consent checkbox
  - [ ] Click "Create Account"
- [ ] Successfully redirected to dashboard
- [ ] Can see user name in interface

## ☐ 6. Test Core Features

- [ ] Submit a test journal entry
  - Go to Journal page
  - Write: "I feel anxious and overwhelmed today"
  - Click "Analyze"
  - Should receive emotion predictions

- [ ] Check prediction results
  - [ ] Emotions displayed (e.g., anxiety: 0.85)
  - [ ] Mental state shown (e.g., "Anxiety")
  - [ ] Severity indicated (e.g., "Moderate")
  - [ ] Recommendations provided

- [ ] View mood history
  - [ ] Previous entries are listed
  - [ ] Can see timestamps
  - [ ] Can view details

- [ ] Check profile
  - [ ] User information displayed
  - [ ] Can update profile (optional)

## ☐ 7. Troubleshooting (If Needed)

If something doesn't work:

- [ ] Check both terminal windows for error messages
- [ ] Verify ports 5000 and 5173 are not in use by other apps
- [ ] Ensure model files are in correct location
- [ ] Try restarting both servers
- [ ] Clear browser cache
- [ ] Check browser console (F12) for errors

### Common Issues:

**Model not loading:**
- [ ] Verify model path in `backend/.env`
- [ ] Check all model files are present
- [ ] Ensure PyTorch is installed

**Cannot connect to API:**
- [ ] Backend is running on port 5000
- [ ] CORS_ORIGINS includes http://localhost:5173
- [ ] .env files are configured correctly

**Login/Register not working:**
- [ ] Check backend terminal for errors
- [ ] Check browser network tab (F12)
- [ ] Verify database was created

## ☐ 8. Final Verification

Run the automated checker:
```powershell
.\check-installation.ps1
```

All checks should pass ✓

## 🎉 Setup Complete!

If all items are checked, your system is ready to use!

### Quick Start Commands:

**Start both servers at once:**
```powershell
.\start.ps1
```

**Start manually:**

Terminal 1 (Backend):
```bash
cd backend
python app.py
```

Terminal 2 (Frontend):
```bash
cd frontend
npm run dev
```

### Documentation:
- Quick Start Guide: `QUICK_START.md`
- Implementation Details: `IMPLEMENTATION_SUMMARY.md`
- API Documentation: `README.md`
- Backend Docs: `backend/README.md`

---

**Need Help?**
- Check QUICK_START.md for detailed instructions
- Review IMPLEMENTATION_SUMMARY.md for what was built
- Check troubleshooting sections in documentation

**Status**: [ ] Setup Complete ✅
