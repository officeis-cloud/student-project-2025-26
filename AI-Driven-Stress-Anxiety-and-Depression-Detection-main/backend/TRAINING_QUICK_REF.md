# 🚀 Quick Training Reference

## Option 1: Automated (Recommended)

```powershell
cd backend
.\start-training.ps1
```

Then select:
- **Option 1**: Quick training (5-10 min) - For testing
- **Option 2**: Full training (1-3 hours) - For production

---

## Option 2: Manual Training

### Quick Training (Testing)
```bash
cd backend
pip install -r requirements-training.txt
python train_model_quick.py
```
**Time**: 5-10 minutes  
**Data**: 5,000 samples  
**Epochs**: 1

### Full Training (Production)
```bash
cd backend
pip install -r requirements-training.txt
python train_model.py
```
**Time**: 1-3 hours (CPU), 30-60 min (GPU)  
**Data**: 43,000+ samples  
**Epochs**: 3

---

## What Gets Installed

```bash
pip install -r requirements-training.txt
```

Installs:
- `datasets` - For GoEmotions dataset
- `transformers` - For DistilBERT model
- `torch` - Deep learning
- `accelerate` - Training optimization
- `evaluate` - Metrics

---

## Expected Performance

| Metric | Quick Training | Full Training |
|--------|---------------|---------------|
| Micro F1 | 85-90% | 96-97% |
| Training Time (CPU) | 5-10 min | 1-3 hours |
| Training Time (GPU) | 2-3 min | 30-60 min |
| Disk Space | ~500 MB | ~500 MB |
| RAM Usage | 4-6 GB | 6-8 GB |

---

## Output Location

Model saved to:
```
backend/models/distilbert-goemotions-mental/
├── config.json
├── pytorch_model.bin (260 MB)
├── tokenizer_config.json
├── vocab.txt
└── emotion_labels.json
```

---

## Verify Training Success

```bash
# Start backend
cd backend
python app.py

# Look for this message:
# ✅ Model loaded successfully from ./models/distilbert-goemotions-mental
```

---

## Troubleshooting

### Out of Memory
```python
# Edit train_model.py:
BATCH_SIZE = 8  # Reduce from 16
MAX_LENGTH = 256  # Reduce from 512
```

### Too Slow
```bash
# Use quick training instead
python train_model_quick.py
```

### Download Failed
- Check internet connection
- Try again (downloads can fail)
- Use VPN if needed

---

## After Training

1. ✅ Model trained and saved
2. Start backend: `python app.py`
3. Start frontend: `cd frontend && npm run dev`
4. Open http://localhost:5173
5. Test emotion predictions!

---

## Need Help?

📖 Read: [TRAINING_GUIDE.md](TRAINING_GUIDE.md) for detailed instructions

---

**Quick Status Check:**
- [ ] Python 3.8+ installed
- [ ] Training packages installed
- [ ] Internet connection available
- [ ] 10+ GB disk space free
- [ ] Training completed
- [ ] Model loads in backend
