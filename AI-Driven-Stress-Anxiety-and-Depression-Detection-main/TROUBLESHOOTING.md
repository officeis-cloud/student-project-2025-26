# 🚨 Common Problems & Solutions

This document lists common issues you might encounter and how to fix them.

---

## 🐍 Backend Issues

### 1. "ModuleNotFoundError: No module named 'X'"

**Problem**: Missing Python package

**Solution**:
```bash
# Activate virtual environment first!
cd backend
.venv\Scripts\Activate.ps1

# Install missing package
pip install package-name

# Or reinstall all requirements
pip install -r requirements.txt
```

**Root Cause**: Virtual environment not activated, or package not in requirements.txt

---

### 2. "No module named 'mongoengine'"

**Problem**: Missing MongoDB driver (we just fixed this!)

**Solution**:
```bash
pip install mongoengine pymongo
```

This is now in requirements.txt, so reinstalling should fix it:
```bash
pip install -r requirements.txt
```

---

### 3. "Port 5000 is already in use"

**Problem**: Another process using port 5000

**Solution (Windows)**:
```bash
# Find process using port 5000
netstat -ano | findstr :5000

# Kill the process (replace 1234 with actual PID)
taskkill /PID 1234 /F
```

**Solution (Alternative)**:
Change port in `backend/.env`:
```env
PORT=5001
```

---

### 4. "MongoDB connection failed" or "ServerSelectionTimeoutError"

**Problem**: Cannot connect to MongoDB

**Solutions**:

**A. Check connection string** in `backend/.env`:
```env
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/mindcare
```

**B. Whitelist your IP** in MongoDB Atlas:
1. Go to MongoDB Atlas dashboard
2. Network Access → Add IP Address
3. Add your current IP or use `0.0.0.0/0` (allow all, for development only)

**C. Verify credentials**:
- Username and password must be URL-encoded
- Database name in URI must match your cluster

**D. Test connection**:
```bash
python -c "from models import init_db; init_db(); print('Connected!')"
```

---

### 5. "torch not found" or CUDA errors

**Problem**: PyTorch installation issue

**Solution (CPU-only, recommended for most)**:
```bash
pip uninstall torch
pip install torch==2.1.0 --index-url https://download.pytorch.org/whl/cpu
```

**For GPU (NVIDIA only)**:
```bash
pip install torch==2.1.0 --index-url https://download.pytorch.org/whl/cu118
```

---

### 6. Virtual environment won't activate

**Problem**: PowerShell execution policy

**Solution**:
```powershell
# Run as Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Or bypass for one session
powershell -ExecutionPolicy Bypass
cd backend
.venv\Scripts\Activate.ps1
```

---

### 7. "HuggingFace model download failed"

**Problem**: Network issue downloading DistilBERT model

**Solution**:
```bash
# Clear cache and retry
Remove-Item -Recurse -Force $env:USERPROFILE\.cache\huggingface
python -c "from emotion_predictor import emotion_predictor"
```

**Alternative**: Manual download
1. Go to https://huggingface.co/distilbert-base-uncased
2. Download model files
3. Place in `backend/models/distilbert-base-uncased/`

---

### 8. "ImportError: cannot import name 'X' from 'Y'"

**Problem**: Outdated or incompatible package versions

**Solution**:
```bash
# Upgrade all packages
pip install --upgrade -r requirements.txt

# Or create fresh virtual environment
Remove-Item -Recurse -Force .venv
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

## ⚛️ Frontend Issues

### 9. "npm ERR! code ENOENT"

**Problem**: Missing node_modules or corrupted package-lock

**Solution**:
```bash
cd frontend

# Delete and reinstall
Remove-Item -Recurse -Force node_modules
Remove-Item package-lock.json
npm install
```

---

### 10. "CORS policy: No 'Access-Control-Allow-Origin' header"

**Problem**: Backend not allowing frontend requests

**Solution**:

**A. Verify backend is running**: http://localhost:5000

**B. Check CORS config** in `backend/app.py`:
```python
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:5173"],
        "methods": ["GET", "POST", "PUT", "DELETE"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})
```

**C. Frontend calling correct URL**:
- Should be: `http://localhost:5000/api/...`
- Not: `http://localhost:5173/api/...`

---

### 11. "Module not found: Can't resolve 'X'"

**Problem**: Missing React/TypeScript dependency

**Solution**:
```bash
# Install specific package
npm install package-name

# Or reinstall all
npm install
```

---

### 12. "Port 5173 is already in use"

**Problem**: Vite dev server port conflict

**Solution**:
```bash
# Kill process (Windows)
netstat -ano | findstr :5173
taskkill /PID <PID> /F

# Or use different port
npm run dev -- --port 3000
```

---

### 13. Build fails with TypeScript errors

**Problem**: Type checking errors

**Solution**:
```bash
# Check types without building
npm run type-check

# Fix errors shown, or temporarily skip
npm run build -- --mode development
```

---

## 🔐 Authentication Issues

### 14. "JWT token expired" or "Invalid token"

**Problem**: Token expiration

**Solution**:
- Logout and login again
- Token expires after 24 hours (configurable in `backend/config.py`)

---

### 15. "Password incorrect" but you know it's right

**Problem**: Password encoding issue

**Solution**:
Create new account or reset in MongoDB:
```python
from models import User
import bcrypt

user = User.objects(email='your@email.com').first()
user.password_hash = bcrypt.hashpw('newpassword'.encode('utf-8'), bcrypt.gensalt())
user.save()
```

---

## 🌐 Network Issues

### 16. "fetch failed" or "Network request failed"

**Problem**: Backend not reachable

**Checklist**:
- [ ] Backend server running? Check terminal
- [ ] Backend on port 5000? `netstat -ano | findstr :5000`
- [ ] Firewall blocking? Temporarily disable
- [ ] Antivirus blocking? Add exception
- [ ] Correct API URL in frontend?

---

### 17. Slow API responses

**Problem**: Model loading or slow prediction

**Solution**:
- First request is slow (~3-5 sec) as model loads
- Subsequent requests should be < 1 second
- If always slow, check CPU usage
- Consider using GPU (if available)

---

## 🗄️ Database Issues

### 18. "Duplicate key error"

**Problem**: Trying to create user with existing email

**Solution**:
- Use different email
- Or delete existing user in MongoDB Atlas

---

### 19. "Document validation failed"

**Problem**: Missing required fields

**Solution**: Check all required fields in model:
```python
# User model requires:
- name (string)
- email (string, unique)
- password_hash (string)
- age (int, 13-120)

# MoodEntry model requires:
- user_id (ObjectId)
- text (string, 10-5000 chars)
- emotions (dict)
- mental_state (string)
```

---

## 🔧 Development Issues

### 20. Changes not reflecting

**Problem**: Cached files

**Solution**:

**Backend**:
```bash
# Restart server (Ctrl+C, then)
python app.py
```

**Frontend**:
```bash
# Hard refresh: Ctrl+Shift+R
# Or clear cache and restart
npm run dev
```

---

### 21. "Cannot find module 'backend.X'"

**Problem**: Python path issue

**Solution**:
```bash
# Ensure backend/__init__.py exists
cd backend
echo > __init__.py

# Or run from correct directory
cd "stress raw 2"
python -m backend.app
```

---

## ⚙️ System-Specific Issues

### 22. Windows: "python is not recognized"

**Solution**:
1. Reinstall Python
2. Check "Add Python to PATH" during installation
3. Or manually add to PATH:
   - Search "Environment Variables" in Windows
   - Edit PATH, add: `C:\Python311\` and `C:\Python311\Scripts\`

---

### 23. macOS: "zsh: command not found: python"

**Solution**:
```bash
# Use python3 instead
python3 --version
python3 -m venv .venv

# Or create alias
echo "alias python=python3" >> ~/.zshrc
```

---

### 24. Linux: Permission denied

**Solution**:
```bash
# Add execute permission
chmod +x script.sh

# Or use sudo for system-wide packages
sudo pip install package-name  # Not recommended, use venv instead
```

---

## 🆘 Still Having Issues?

### Debug Checklist:

1. **Check versions**:
   ```bash
   python --version  # Need 3.10+
   node --version    # Need 18+
   npm --version
   ```

2. **Check virtual environment**:
   ```bash
   # Should see (.venv) in prompt
   echo $VIRTUAL_ENV  # Should show path to .venv
   ```

3. **Check environment variables**:
   ```bash
   # Backend
   cat backend/.env
   
   # Should have MONGODB_URI, JWT_SECRET_KEY, etc.
   ```

4. **Check logs**:
   - Backend: Look at terminal output for errors
   - Frontend: Open browser DevTools (F12) → Console
   - MongoDB: Check Atlas logs

5. **Verify installations**:
   ```bash
   # Backend packages
   pip list
   
   # Should see: flask, torch, transformers, mongoengine, etc.
   
   # Frontend packages
   npm list --depth=0
   ```

6. **Test each component**:
   ```bash
   # Test backend
   python backend/test_model.py
   
   # Test MongoDB connection
   python -c "from models import init_db; init_db()"
   
   # Test frontend build
   cd frontend && npm run build
   ```

---

## 📞 Resources

- **SETUP.md**: Complete setup guide
- **README.md**: Project overview
- **QUICKSTART.md**: Fast setup guide
- **Stack Overflow**: Search your error message
- **GitHub Issues**: Check if others had same problem

---

**Remember**: 
- **90% of issues are environment/configuration problems**
- **Always activate virtual environment before running Python code**
- **Check error messages carefully - they usually tell you what's wrong**
- **When in doubt, try deleting and reinstalling (virtual env, node_modules)**

---

**Last Updated**: March 5, 2026
