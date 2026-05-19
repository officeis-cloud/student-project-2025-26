# 🎓 Model Training Guide

This guide will help you train the emotion detection model using DistilBERT and the GoEmotions dataset.

## 📋 Prerequisites

### System Requirements

**Minimum (CPU Training):**
- 8 GB RAM
- 10 GB free disk space
- Python 3.8+
- 2-3 hours training time

**Recommended (GPU Training):**
- 16 GB RAM
- NVIDIA GPU with 6+ GB VRAM
- 10 GB free disk space
- CUDA installed
- 30-60 minutes training time

### Check Your Setup

```bash
# Check Python
python --version

# Check if CUDA is available (GPU)
python -c "import torch; print(f'CUDA Available: {torch.cuda.is_available()}')"
```

## 🚀 Quick Start

### Option 1: Quick Training (Testing/Development)

Fast training with subset of data - **Good for testing the setup!**

```bash
cd backend

# Install training dependencies
pip install -r requirements-training.txt

# Run quick training (5-10 minutes)
python train_model_quick.py
```

This will:
- Use 5,000 training samples (instead of 43k)
- Train for 1 epoch only
- Complete in 5-10 minutes on CPU
- Give you a working model to test the system

### Option 2: Full Training (Production)

Complete training with full dataset - **For best performance!**

```bash
cd backend

# Install training dependencies
pip install -r requirements-training.txt

# Run full training (1-3 hours on CPU, 30-60 min on GPU)
python train_model.py
```

This will:
- Use full GoEmotions dataset (43k+ samples)
- Train for 3 epochs with early stopping
- Achieve ~96% F1 score
- Take 1-3 hours depending on hardware

## 📦 Installation

### Step 1: Install Training Dependencies

```bash
cd backend
pip install -r requirements-training.txt
```

This installs:
- `datasets` - For loading GoEmotions
- `transformers` - For DistilBERT model
- `torch` - Deep learning framework
- `accelerate` - For training optimization
- `evaluate` - For metrics

### Step 2: Verify Installation

```bash
python -c "from datasets import load_dataset; from transformers import AutoTokenizer; print('✓ All packages installed')"
```

## 🎯 Training Process

### What Happens During Training

1. **Dataset Loading** (1-2 minutes)
   - Downloads GoEmotions dataset from HuggingFace
   - ~50 MB download
   - Caches locally for future use

2. **Preprocessing** (2-5 minutes)
   - Tokenizes text
   - Creates multi-hot label encodings
   - Prepares batches

3. **Model Training** (Main time)
   - Fine-tunes DistilBERT
   - Updates every 100 steps
   - Evaluates each epoch
   - Saves best model

4. **Evaluation** (1-2 minutes)
   - Tests on test set
   - Calculates metrics
   - Creates performance report

5. **Model Saving** (<1 minute)
   - Saves model weights
   - Saves tokenizer
   - Saves configuration

### Expected Output

```
================================================================================
AI-Driven Mental Health System - Model Training
Phase 2: Emotion Detection Model Training
================================================================================

📦 Configuration:
  Model: distilbert-base-uncased
  Output: ./models/distilbert-goemotions-mental
  ...

🖥️  Device: cuda  (or cpu)

================================================================================
STEP 1: Loading GoEmotions Dataset
================================================================================
✓ Dataset loaded successfully!
  Train samples: 43,410
  Validation samples: 5,426
  Test samples: 5,427

📊 Emotion Labels (27):
   0. admiration
   1. amusement
   2. anger
   ...

[Training progress bars...]

================================================================================
✅ TRAINING COMPLETE!
================================================================================

📁 Model Location:
   C:\Users\...\backend\models\distilbert-goemotions-mental

📊 Performance Summary:
   Micro F1 Score: 96.96%
   Macro F1 Score: 58.23%
   Exact Match: 52.45%
```

## 📊 Understanding the Metrics

### Micro F1 Score (Most Important)
- **What it means**: Overall accuracy across all emotions
- **Target**: >95% is excellent
- **Your model should achieve**: ~96-97%

### Macro F1 Score
- **What it means**: Average F1 across each emotion class
- **Target**: >50% is good
- **Note**: Lower than micro because rare emotions are harder

### Exact Match
- **What it means**: Percentage where ALL labels match perfectly
- **Target**: >50% is good
- **Note**: Strict metric, partial matches count as wrong

## 🗂️ Output Files

After training, you'll find:

```
backend/models/distilbert-goemotions-mental/
├── config.json                 # Model configuration
├── pytorch_model.bin           # Model weights (~260 MB)
├── tokenizer_config.json       # Tokenizer settings
├── vocab.txt                   # Vocabulary
├── special_tokens_map.json     # Special tokens
├── emotion_labels.json         # List of 27 emotions
└── training_info.json          # Training metadata
```

## ⚙️ Training Configuration

### Default Settings (train_model.py)

```python
MODEL_NAME = "distilbert-base-uncased"  # Base model
MAX_LENGTH = 512                        # Max text length
BATCH_SIZE = 16                         # Batch size
LEARNING_RATE = 2e-5                    # Learning rate
NUM_EPOCHS = 3                          # Training epochs
```

### Quick Training Settings (train_model_quick.py)

```python
MAX_LENGTH = 128        # Shorter sequences
BATCH_SIZE = 32         # Larger batches
NUM_EPOCHS = 1          # Single epoch
TRAIN_SAMPLES = 5000    # Subset of data
```

### Customizing Training

Edit `train_model.py` to adjust:

```python
# For faster training
BATCH_SIZE = 32
NUM_EPOCHS = 2

# For better accuracy
BATCH_SIZE = 8
NUM_EPOCHS = 5
LEARNING_RATE = 1e-5

# For limited memory
BATCH_SIZE = 4
MAX_LENGTH = 256
```

## 🐛 Troubleshooting

### Out of Memory (OOM) Error

**Error**: `CUDA out of memory` or `RuntimeError: out of memory`

**Solutions**:
```python
# In train_model.py, reduce:
BATCH_SIZE = 8  # or even 4
MAX_LENGTH = 256  # instead of 512
```

Or use CPU training:
```python
device = torch.device("cpu")  # Force CPU
```

### Download Errors

**Error**: `ConnectionError` or dataset won't download

**Solutions**:
1. Check internet connection
2. Try again (downloads can be unreliable)
3. Use VPN if restricted
4. Download manually from HuggingFace

### Import Errors

**Error**: `ModuleNotFoundError: No module named 'datasets'`

**Solution**:
```bash
pip install -r requirements-training.txt
```

### Slow Training

**If training is very slow:**

1. **Use Quick Training** for testing:
   ```bash
   python train_model_quick.py
   ```

2. **Enable GPU** if available:
   - Install CUDA toolkit
   - Install GPU PyTorch: `pip install torch --index-url https://download.pytorch.org/whl/cu118`

3. **Reduce data size** in `train_model.py`:
   ```python
   # After loading dataset, add:
   dataset['train'] = dataset['train'].select(range(10000))
   ```

## 🎯 After Training

### Verify Model Works

```bash
cd backend
python app.py
```

Check for:
```
✅ Model loaded successfully from ./models/distilbert-goemotions-mental
✅ Database initialized
 * Running on http://0.0.0.0:5000
```

### Test Predictions

```bash
curl -X POST http://localhost:5000/api/predict/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"text":"I feel happy and excited!"}'
```

### Integration with Frontend

Once training is complete:
1. Model is automatically in correct location
2. Backend will load it on startup
3. Frontend can call prediction API
4. Users can analyze their journal entries

## 📈 Training Tips

### For Best Results

1. **Use GPU if available** - 10x faster
2. **Train with full data** - Use `train_model.py`
3. **Monitor metrics** - Aim for >95% micro F1
4. **Save training logs** - Check `training_logs/` folder
5. **Test incrementally** - Try quick training first

### For Testing/Development

1. **Use quick training** - `train_model_quick.py`
2. **Verify setup works** - Before full training
3. **Iterate fast** - Test changes quickly
4. **Save resources** - Good for laptops

## 🔄 Re-training

To retrain the model:

```bash
# Delete old model
rm -rf backend/models/distilbert-goemotions-mental/

# Train again
python train_model.py
```

## 📚 Advanced Options

### Using Different Models

Replace `MODEL_NAME` in script:
```python
MODEL_NAME = "bert-base-uncased"  # Larger, more accurate
MODEL_NAME = "distilroberta-base"  # Alternative
```

### Adding Custom Emotions

Edit the dataset or use a different one:
```python
dataset = load_dataset("your_custom_dataset")
```

### Hyperparameter Tuning

Experiment with:
- Learning rate: `1e-5` to `5e-5`
- Batch size: `8` to `32`
- Epochs: `2` to `5`
- Warmup steps: `100` to `1000`

## ✅ Success Checklist

- [ ] Python 3.8+ installed
- [ ] Dependencies installed (`requirements-training.txt`)
- [ ] Training script runs without errors
- [ ] Model achieves >90% micro F1 score
- [ ] Model saved in `backend/models/distilbert-goemotions-mental/`
- [ ] Backend loads model successfully
- [ ] Can make predictions through API

## 🆘 Need Help?

1. Check error messages carefully
2. Verify all dependencies installed
3. Try quick training first
4. Check available disk space (10+ GB)
5. Monitor RAM usage during training
6. Read troubleshooting section above

## 🎉 Next Steps

After successful training:

1. ✅ Model is trained and saved
2. Start backend: `cd backend && python app.py`
3. Start frontend: `cd frontend && npm run dev`
4. Test full application flow
5. Submit journal entries
6. View emotion predictions
7. Get recommendations

---

**Training time estimates:**
- Quick training: 5-10 minutes (CPU), 2-3 minutes (GPU)
- Full training: 1-3 hours (CPU), 30-60 minutes (GPU)

**Model size:** ~260 MB

**Performance:** 96-97% F1 Score on GoEmotions dataset
