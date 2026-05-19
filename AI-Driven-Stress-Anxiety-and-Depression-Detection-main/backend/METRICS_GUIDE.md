# Model Training Metrics Guide

This guide explains the comprehensive metrics generated during model training.

## 📊 Metrics Folder Structure

After training, you'll find a `metrics/` folder inside your model directory:

### Quick Training
```
backend/models/quick-training/
  ├── metrics/
  │   ├── metrics_report.json          # Structured metrics data
  │   ├── classification_report.txt    # Human-readable report
  │   └── (training artifacts)
  ├── config.json
  ├── model.safetensors
  └── ...
```

### Production Training
```
backend/models/distilbert-goemotions-mental/
  ├── metrics/
  │   ├── metrics_report.json          # Structured metrics data
  │   ├── classification_report.txt    # Detailed per-emotion analysis
  │   ├── sample_predictions.json      # 100 sample predictions
  │   └── (training artifacts)
  ├── config.json
  ├── model.safetensors
  └── ...
```

## 📄 Metrics Files Explained

### 1. metrics_report.json

**Purpose**: Structured JSON file with all training metrics

**Contents**:
- **model_name**: Base model used (DistilBERT)
- **training_config**: Hyperparameters used
  - train/val/test sample counts
  - batch size, learning rate, epochs
  - max sequence length
- **training_duration**: Total time taken
- **overall_metrics**: 
  - **micro_f1**: Average F1 across all predictions (weighted by support)
  - **macro_f1**: Average F1 across all emotions (unweighted)
  - **exact_match**: Percentage where ALL emotions match exactly
- **per_emotion_metrics**: For each of the 27 emotions:
  - **precision**: Of predicted emotions, how many were correct
  - **recall**: Of actual emotions, how many were detected
  - **f1**: Harmonic mean of precision and recall
  - **support**: Number of samples with this emotion

**Usage**: 
- Load into Python for analysis
- Create visualizations
- Compare training runs
- Track model improvements

```python
import json

with open('metrics/metrics_report.json') as f:
    metrics = json.load(f)
    
# Example: Get emotions performing below 80% F1
low_performers = {
    emotion: data['f1'] 
    for emotion, data in metrics['per_emotion_metrics'].items() 
    if data['f1'] < 0.8
}
```

### 2. classification_report.txt

**Purpose**: Human-readable detailed analysis report

**Sections**:

#### Header
- Model name and configuration
- Training mode (Quick/Production)
- Training date and duration
- Dataset sizes

#### Overall Metrics
- Micro F1, Macro F1, Exact Match
- Quick interpretation of model performance

#### Per-Emotion Performance Table
All 27 emotions with their metrics:
```
Emotion              Precision    Recall       F1-Score     Support   
--------------------------------------------------------------------------------
joy                      95.23%      93.45%      94.33%         1250
sadness                  92.15%      91.87%      92.01%         1120
...
```

#### Top 5 Best Performing Emotions
Shows which emotions the model predicts most accurately

#### Bottom 5 Emotions (Need Improvement)
Identifies emotions that may need more training data or attention

**Usage**: 
- Quick performance overview
- Share with stakeholders
- Identify improvement areas
- Documentation for reports

### 3. sample_predictions.json

**Purpose**: Detailed predictions for 100 test samples (Production training only)

**Structure**:
```json
{
  "samples": [
    {
      "index": 0,
      "true_emotions": ["joy", "excitement"],
      "predicted_emotions": ["joy", "excitement", "optimism"],
      "probabilities": {
        "joy": 0.95,
        "excitement": 0.87,
        "optimism": 0.52,
        "admiration": 0.35
      }
    }
  ]
}
```

**Usage**:
- Error analysis
- Understand model behavior
- Identify systematic mistakes
- Debug specific emotion confusions

```python
import json

with open('metrics/sample_predictions.json') as f:
    samples = json.load(f)['samples']

# Find mismatches
errors = [s for s in samples 
          if set(s['true_emotions']) != set(s['predicted_emotions'])]

print(f"Error rate: {len(errors)/len(samples)*100:.1f}%")
```

## 📈 Understanding the Metrics

### Micro F1 vs Macro F1

**Micro F1** (Usually higher):
- Treats each prediction independently
- Weights by frequency (common emotions matter more)
- Good for overall system performance
- **Target**: > 95% for production

**Macro F1** (Usually lower):
- Averages across all emotions equally
- Rare emotions weighted same as common ones
- Good for balanced performance assessment
- **Target**: > 90% for production

### Exact Match Accuracy

**Definition**: Percentage where predicted emotions EXACTLY match true emotions

**Characteristics**:
- Very strict metric
- 70%+ is considered excellent for multi-label
- Lower than F1 scores is normal and expected

**Example**:
```
True:      [joy, excitement]
Predicted: [joy, excitement, optimism]
→ Exact Match: NO (even though 2/3 correct)
→ F1 Score: ~0.80 (accounts for partial match)
```

### Per-Emotion Metrics

**Precision**: "When I predict this emotion, am I usually right?"
- High = Few false positives
- Low = Model over-predicts this emotion

**Recall**: "When this emotion exists, do I detect it?"
- High = Few false negatives
- Low = Model misses this emotion

**F1 Score**: Balanced measure
- High = Good at both detecting and not over-predicting
- Low = Either missing emotions or predicting too many

## 🎯 Performance Targets

### Quick Training (5K samples, 1 epoch)
- **Micro F1**: 80-85%
- **Macro F1**: 75-80%
- **Exact Match**: 60-65%
- **Purpose**: Validate setup, fast experimentation

### Production Training (43K samples, 3 epochs)
- **Micro F1**: 95-97%
- **Macro F1**: 90-93%
- **Exact Match**: 70-75%
- **Purpose**: Production deployment

## 🔍 Common Issues and Solutions

### Low Macro F1 (but high Micro F1)
**Problem**: Some emotions performing poorly
**Solution**: 
- Check per-emotion metrics
- May need more training data for rare emotions
- Consider class weights or oversampling

### Low Exact Match (but decent F1)
**Problem**: Model predicts extra/missing emotions
**Solution**:
- Adjust prediction threshold (default 0.5)
- May be acceptable for mental health (better sensitive than specific)
- Review sample predictions for patterns

### Poor Performance on Specific Emotions
**Problem**: Some emotions <70% F1
**Solution**:
- Check support (sample count)
- May be similar to other emotions (confusion)
- Consider combining similar emotions
- Add more training examples

## 💡 Using Metrics for Improvement

### 1. Identify Weak Emotions
```python
# From metrics_report.json
weak_emotions = [
    (emotion, data['f1'], data['support']) 
    for emotion, data in per_emotion_metrics.items() 
    if data['f1'] < 0.85
]
weak_emotions.sort(key=lambda x: x[1])  # Sort by F1
```

### 2. Analyze Confusion Patterns
```python
# From sample_predictions.json
# Find what emotions are confused with each other
from collections import Counter

false_positives = Counter()
for sample in samples:
    false_preds = set(sample['predicted_emotions']) - set(sample['true_emotions'])
    false_positives.update(false_preds)
```

### 3. Monitor Training Progress
Save metrics from multiple training runs:
```python
metrics_history = []
for run in training_runs:
    with open(f'{run}/metrics/metrics_report.json') as f:
        metrics_history.append(json.load(f))

# Plot improvement over time
import matplotlib.pyplot as plt
plt.plot([m['overall_metrics']['micro_f1'] for m in metrics_history])
plt.title('Model Improvement Over Training Runs')
```

## 📚 Additional Resources

### Understanding Multi-Label Classification
- Multiple emotions can be true simultaneously
- Unlike multi-class (only one class)
- Common in text emotion analysis

### GoEmotions Dataset
- 27 emotion categories + neutral
- Based on Reddit comments
- Designed for fine-grained emotion detection

### Mental Health Application
- Emotions mapped to mental states (depression, anxiety, stress)
- Severity levels derived from emotion intensities
- Better to detect false positives than miss real issues

## 🚀 Next Steps After Training

1. **Review Metrics**
   - Check classification_report.txt
   - Identify any concerning patterns

2. **Test Integration**
   - Start backend server
   - Test with real journal entries
   - Validate emotion detection

3. **Monitor Production**
   - Log predictions
   - Collect feedback
   - Retrain periodically

4. **Continuous Improvement**
   - Gather more training data
   - Fine-tune thresholds
   - Update model regularly

---

For questions or issues, refer to TRAINING_GUIDE.md or the main README.md
