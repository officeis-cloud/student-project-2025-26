# Backend API - AI-Driven Mental Health System

Flask backend for emotion detection, mental state classification, and personalized wellness recommendations.

## 🚀 Features

- **Emotion Detection**: Multi-label emotion classification using fine-tuned DistilBERT
- **Mental State Analysis**: Classifies stress, anxiety, and depression with severity levels
- **Personalized Recommendations**: Context-aware wellness tips and lifestyle suggestions
- **Mood History Tracking**: Store and analyze emotional patterns over time
- **User Authentication**: Secure JWT-based authentication
- **RESTful API**: Clean, well-documented endpoints

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Trained DistilBERT model (see Model Training section below)

## 🧠 Model Training (Required First Step)

**You need to train the emotion detection model before running the backend!**

### Quick Training (Recommended for First Time)
```bash
cd backend
pip install -r requirements-training.txt
python train_model_quick.py
```
**Time**: 5-10 minutes  
**Use case**: Testing and development

### Full Training (For Production)
```bash
cd backend
pip install -r requirements-training.txt
python train_model.py
```
**Time**: 1-3 hours (CPU), 30-60 minutes (GPU)  
**Use case**: Production deployment

### Automated Training
```powershell
cd backend
.\start-training.ps1
# Follow the interactive prompts
```

📖 **Detailed guide**: See [TRAINING_GUIDE.md](TRAINING_GUIDE.md) for complete instructions

## 📊 Training Metrics & Analysis

After training completes, comprehensive metrics are automatically generated and saved in a `metrics/` folder within your model directory.

### Generated Metrics Files

**Quick Training** (`models/quick-training/metrics/`):
- `metrics_report.json` - Structured metrics for programmatic analysis
- `classification_report.txt` - Human-readable performance report

**Production Training** (`models/distilbert-goemotions-mental/metrics/`):
- `metrics_report.json` - Complete metrics including per-emotion performance
- `classification_report.txt` - Detailed analysis with top/bottom performers
- `sample_predictions.json` - 100 sample predictions for error analysis

### Analyzing Metrics

Use the provided analysis script to quickly review performance:

```bash
# Analyze a trained model
python analyze_metrics.py models/quick-training

# Compare two models
python analyze_metrics.py models/quick-training models/distilbert-goemotions-mental
```

**Example Output:**
```
📊 Overall Performance:
  Micro F1:     96.23%
  Macro F1:     92.45%
  Exact Match:  71.34%

✅ Top 5 Best Performing Emotions:
  1. joy            F1:  97.82%
  2. sadness        F1:  96.45%
  3. anger          F1:  95.23%
  ...
```

### Understanding Metrics

- **Micro F1**: Overall prediction accuracy (weighted by frequency)
  - Target: >95% for production, >80% for quick training
- **Macro F1**: Average performance across all emotions
  - Target: >90% for production, >75% for quick training
- **Exact Match**: Strict metric where all emotions must match
  - Target: >70% for production, >60% for quick training

📖 **Detailed explanation**: See [METRICS_GUIDE.md](METRICS_GUIDE.md) for complete metrics documentation

## 🛠️ Installation

1. **Train the model (see above)** - This creates the required model files

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables:**
```bash
# Copy example env file
copy .env.example .env

# Edit .env and update the values
```

4. **Initialize database:**
```bash
python app.py
# This will create the SQLite database automatically
```

5. **Seed wellness tips (optional):**
```bash
python seed.py
```

## 📁 Project Structure

```
backend/
├── app.py                      # Main Flask application
├── config.py                   # Configuration settings
├── models.py                   # Database models
├── emotion_predictor.py        # Emotion prediction service
├── recommendation_engine.py    # Recommendation logic
├── seed.py                     # Database seeding script
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
└── routes/
    ├── auth.py                # Authentication endpoints
    └── predict.py             # Prediction & analysis endpoints
```

## 🚀 Running the Server

### Development Mode
```bash
python app.py
```

The server will start on `http://localhost:5000`

### Production Mode
```bash
# Using gunicorn
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 📡 API Endpoints

### Authentication

#### Register User
```http
POST /api/auth/register
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "securepassword",
  "age": 25,
  "gender": "male"
}
```

#### Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "securepassword"
}
```

#### Get Current User
```http
GET /api/auth/me
Authorization: Bearer <access_token>
```

### Emotion Prediction

#### Analyze Text
```http
POST /api/predict/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "text": "I feel overwhelmed and tired today..."
}
```

**Response:**
```json
{
  "success": true,
  "entry_id": 1,
  "emotions": {
    "sadness": 0.82,
    "disappointment": 0.65,
    "fatigue": 0.71
  },
  "mental_state": "depression",
  "severity": "moderate",
  "severity_score": 0.55,
  "recommendations": [
    {
      "title": "Morning Sunlight Exposure",
      "description": "...",
      "type": "lifestyle",
      "duration": "15-20 minutes"
    }
  ]
}
```

#### Get Mood History
```http
GET /api/predict/history?page=1&per_page=10
Authorization: Bearer <access_token>
```

#### Get Statistics
```http
GET /api/predict/stats?days=30
Authorization: Bearer <access_token>
```

#### Get Recommendations
```http
GET /api/predict/recommendations
Authorization: Bearer <access_token>
```

## 🧠 Model Integration

The backend expects a trained DistilBERT model in the following location:
```
backend/models/distilbert-goemotions-mental/
```

Make sure your model directory contains:
- `config.json`
- `pytorch_model.bin`
- `tokenizer_config.json`
- `vocab.txt`

Update the model path in `.env`:
```
MODEL_PATH=./models/distilbert-goemotions-mental
```

## 🗄️ Database Schema

### Users Table
- id (Primary Key)
- name
- email (Unique)
- password_hash
- age
- gender
- created_at
- updated_at

### Mood Entries Table
- id (Primary Key)
- user_id (Foreign Key)
- text
- emotions (JSON)
- mental_state
- severity
- severity_score
- recommendations (JSON)
- created_at

### Wellness Tips Table
- id (Primary Key)
- category
- title
- description
- type
- duration
- created_at

## 🔒 Security

- Passwords are hashed using bcrypt
- JWT tokens for authentication
- CORS configured for frontend origin
- Environment variables for sensitive data

## 🐛 Troubleshooting

### Model not loading
```bash
# Check if model path is correct in .env
# Verify model files exist
ls backend/models/distilbert-goemotions-mental/
```

### Database errors
```bash
# Delete and recreate database
rm mental_health.db
python app.py
```

### Import errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

## 📊 Testing

Test the API using curl or Postman:

```bash
# Health check
curl http://localhost:5000/api/health

# Register user
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Test User","email":"test@example.com","password":"test123"}'
```

## 🚀 Next Steps (Phase 4)

- [ ] Add more sophisticated recommendation algorithms
- [ ] Implement user feedback on recommendations
- [ ] Add professional consultation booking
- [ ] Create admin dashboard
- [ ] Add email notifications
- [ ] Implement data export features
- [ ] Add multi-language support

## 📝 License

This project is part of the AI-Driven Mental Health System academic project.

## 👥 Team

- Disha T.S (4PS22IS019)
- M. Chakravarthy (4PS22IS031)
- Sanjana L (4PS22IS047)
- Vaishak M.A (4PS22IS054)

**P.E.S. College of Engineering, Mandya**
