"""
Model Training Script - Phase 2
Fine-tune DistilBERT on GoEmotions dataset for emotion classification
"""

import os
import torch
import time
import numpy as np
from datasets import load_dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer,
    EarlyStoppingCallback
)
from sklearn.metrics import f1_score, accuracy_score, precision_recall_fscore_support
import json
from datetime import datetime

print("=" * 80)
print("AI-Driven Mental Health System - Model Training")
print("Phase 2: Emotion Detection Model Training")
print("=" * 80)
print()

# Configuration
MODEL_NAME = "distilbert-base-uncased"
OUTPUT_DIR = "./models/distilbert-goemotions-mental"
MAX_LENGTH = 512
BATCH_SIZE = 16
LEARNING_RATE = 2e-5
NUM_EPOCHS = 3
WARMUP_STEPS = 500

# Create output directory
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs("./training_logs", exist_ok=True)

print("📦 Configuration:")
print(f"  Model: {MODEL_NAME}")
print(f"  Output: {OUTPUT_DIR}")
print(f"  Max Length: {MAX_LENGTH}")
print(f"  Batch Size: {BATCH_SIZE}")
print(f"  Learning Rate: {LEARNING_RATE}")
print(f"  Epochs: {NUM_EPOCHS}")
print()

# Check for GPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"🖥️  Device: {device}")
if torch.cuda.is_available():
    print(f"  GPU: {torch.cuda.get_device_name(0)}")
    print(f"  Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
print()

# =============================================================================
# STEP 1: Load GoEmotions Dataset
# =============================================================================
print("=" * 80)
print("STEP 1: Loading GoEmotions Dataset")
print("=" * 80)

try:
    print("Loading dataset from HuggingFace...")
    dataset = load_dataset("go_emotions", "simplified")
    
    print(f"✓ Dataset loaded successfully!")
    print(f"  Train samples: {len(dataset['train'])}")
    print(f"  Validation samples: {len(dataset['validation'])}")
    print(f"  Test samples: {len(dataset['test'])}")
    print()
    
    # Get emotion labels
    emotion_labels = dataset['train'].features['labels'].feature.names
    num_labels = len(emotion_labels)
    
    print(f"📊 Emotion Labels ({num_labels}):")
    for i, label in enumerate(emotion_labels):
        print(f"  {i:2d}. {label}")
    print()
    
except Exception as e:
    print(f"❌ Error loading dataset: {e}")
    print("Please ensure you have internet connection and the datasets library is installed.")
    exit(1)

# =============================================================================
# STEP 2: Initialize Tokenizer and Model
# =============================================================================
print("=" * 80)
print("STEP 2: Initializing Tokenizer and Model")
print("=" * 80)

try:
    print(f"Loading tokenizer: {MODEL_NAME}...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    
    print(f"Loading model: {MODEL_NAME}...")
    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_NAME,
        num_labels=num_labels,
        problem_type="multi_label_classification"
    )
    
    model.to(device)
    
    print("✓ Model and tokenizer loaded successfully!")
    print(f"  Parameters: {sum(p.numel() for p in model.parameters()):,}")
    print(f"  Trainable: {sum(p.numel() for p in model.parameters() if p.requires_grad):,}")
    print()
    
except Exception as e:
    print(f"❌ Error loading model: {e}")
    exit(1)

# =============================================================================
# STEP 3: Preprocess Dataset
# =============================================================================
print("=" * 80)
print("STEP 3: Preprocessing Dataset")
print("=" * 80)

def preprocess_function(examples):
    """Tokenize and prepare examples for training"""
    # Tokenize text
    tokenized = tokenizer(
        examples['text'],
        truncation=True,
        padding='max_length',
        max_length=MAX_LENGTH
    )
    
    # Convert labels to multi-hot encoding
    labels = []
    for label_list in examples['labels']:
        multi_hot = [0.0] * num_labels
        for label_id in label_list:
            multi_hot[label_id] = 1.0
        labels.append(multi_hot)
    
    # Convert labels to float explicitly
    import numpy as np
    tokenized['labels'] = np.array(labels, dtype=np.float32)
    return tokenized

try:
    print("Tokenizing dataset...")
    print("This may take a few minutes...")
    
    tokenized_datasets = dataset.map(
        preprocess_function,
        batched=True,
        remove_columns=dataset['train'].column_names
    )
    
    # Set format for PyTorch
    tokenized_datasets.set_format('torch')
    
    print("✓ Dataset preprocessed successfully!")
    print(f"  Train: {len(tokenized_datasets['train'])} samples")
    print(f"  Validation: {len(tokenized_datasets['validation'])} samples")
    print(f"  Test: {len(tokenized_datasets['test'])} samples")
    print()
    
except Exception as e:
    print(f"❌ Error preprocessing dataset: {e}")
    exit(1)

# Custom data collator to ensure labels are float
from dataclasses import dataclass
from typing import Any, Dict, List
from transformers import DataCollatorWithPadding

@dataclass
class MultiLabelDataCollator(DataCollatorWithPadding):
    def __call__(self, features: List[Dict[str, Any]]) -> Dict[str, Any]:
        batch = super().__call__(features)
        # Ensure labels are float tensors
        if 'labels' in batch:
            batch['labels'] = batch['labels'].float()
        return batch

data_collator = MultiLabelDataCollator(tokenizer=tokenizer)
print("✓ Data collator configured")
print()

# =============================================================================
# STEP 4: Define Evaluation Metrics
# =============================================================================
print("=" * 80)
print("STEP 4: Setting up Evaluation Metrics")
print("=" * 80)

def compute_metrics(eval_pred):
    """Compute multi-label classification metrics"""
    logits, labels = eval_pred
    
    # Apply sigmoid to get probabilities
    probs = torch.sigmoid(torch.tensor(logits))
    
    # Apply threshold
    predictions = (probs > 0.5).float().numpy()
    
    # Calculate metrics
    micro_f1 = f1_score(labels, predictions, average='micro', zero_division=0)
    macro_f1 = f1_score(labels, predictions, average='macro', zero_division=0)
    
    # Exact match accuracy (all labels must match)
    exact_match = accuracy_score(labels, predictions)
    
    return {
        'micro_f1': micro_f1,
        'macro_f1': macro_f1,
        'exact_match': exact_match,
    }

print("✓ Metrics configured:")
print("  - Micro F1 Score")
print("  - Macro F1 Score")
print("  - Exact Match Accuracy")
print()

# =============================================================================
# STEP 5: Configure Training
# =============================================================================
print("=" * 80)
print("STEP 5: Configuring Training")
print("=" * 80)

training_args = TrainingArguments(
    output_dir=OUTPUT_DIR,
    evaluation_strategy="epoch",
    save_strategy="epoch",
    learning_rate=LEARNING_RATE,
    per_device_train_batch_size=BATCH_SIZE,
    per_device_eval_batch_size=BATCH_SIZE,
    num_train_epochs=NUM_EPOCHS,
    weight_decay=0.01,
    warmup_steps=WARMUP_STEPS,
    logging_dir='./training_logs',
    logging_steps=100,
    load_best_model_at_end=True,
    metric_for_best_model='micro_f1',
    greater_is_better=True,
    save_total_limit=2,
    fp16=torch.cuda.is_available(),  # Use mixed precision if GPU available
    report_to="none",  # Disable wandb, tensorboard, etc.
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets['train'],
    eval_dataset=tokenized_datasets['validation'],
    tokenizer=tokenizer,
    data_collator=data_collator,
    compute_metrics=compute_metrics,
    callbacks=[EarlyStoppingCallback(early_stopping_patience=2)]
)

print("✓ Training configuration ready!")
print(f"  Total steps: {len(tokenized_datasets['train']) // BATCH_SIZE * NUM_EPOCHS}")
print(f"  Eval steps: {len(tokenized_datasets['train']) // BATCH_SIZE}")
print()

# =============================================================================
# STEP 6: Train Model
# =============================================================================
print("=" * 80)
print("STEP 6: Training Model")
print("=" * 80)
print()
print("🚀 Starting training...")
print("This will take some time. Progress will be shown below.")
print()

try:
    training_start = datetime.now()
    
    # Train the model
    train_result = trainer.train()
    
    training_end = datetime.now()
    training_duration = training_end - training_start
    
    print()
    print("✓ Training completed!")
    print(f"  Duration: {training_duration}")
    print(f"  Final loss: {train_result.training_loss:.4f}")
    print()
    
except Exception as e:
    print(f"❌ Error during training: {e}")
    exit(1)

# =============================================================================
# STEP 7: Evaluate on Test Set
# =============================================================================
print("=" * 80)
print("STEP 7: Evaluating on Test Set")
print("=" * 80)

try:
    print("Evaluating model on test data...")
    test_results = trainer.evaluate(tokenized_datasets['test'])
    
    print()
    print("📊 Test Results:")
    print(f"  Micro F1 Score: {test_results['eval_micro_f1']:.4f} ({test_results['eval_micro_f1']*100:.2f}%)")
    print(f"  Macro F1 Score: {test_results['eval_macro_f1']:.4f} ({test_results['eval_macro_f1']*100:.2f}%)")
    print(f"  Exact Match: {test_results['eval_exact_match']:.4f} ({test_results['eval_exact_match']*100:.2f}%)")
    print()
    
    # Generate detailed metrics
    print("Generating comprehensive metrics...")
    metrics_dir = os.path.join(OUTPUT_DIR, 'metrics')
    os.makedirs(metrics_dir, exist_ok=True)
    
    # Get predictions for detailed analysis
    print("  - Computing comprehensive metrics...")
    test_predictions = trainer.predict(tokenized_datasets['test'])
    logits = test_predictions.predictions
    labels_true = test_predictions.label_ids
    
    # Convert to predictions
    probs = torch.sigmoid(torch.tensor(logits)).numpy()
    predictions = (probs > 0.5).astype(int)
    
    # Overall metrics
    from sklearn.metrics import (
        hamming_loss, accuracy_score, roc_auc_score,
        coverage_error, label_ranking_average_precision_score
    )
    
    hamming = hamming_loss(labels_true, predictions)
    subset_accuracy = accuracy_score(labels_true, predictions)
    sample_accuracy = (labels_true == predictions).mean()
    
    # ROC-AUC scores
    try:
        roc_auc_micro = roc_auc_score(labels_true, probs, average='micro')
        roc_auc_macro = roc_auc_score(labels_true, probs, average='macro')
        roc_auc_weighted = roc_auc_score(labels_true, probs, average='weighted')
    except:
        roc_auc_micro = roc_auc_macro = roc_auc_weighted = 0.0
    
    # Ranking metrics
    try:
        coverage = coverage_error(labels_true, probs)
        lrap = label_ranking_average_precision_score(labels_true, probs)
    except:
        coverage = lrap = 0.0
    
    # Per-emotion metrics with ROC-AUC
    per_emotion_metrics = {}
    per_emotion_roc_data = {}
    
    for i, emotion in enumerate(emotion_labels):
        precision, recall, f1, support = precision_recall_fscore_support(
            labels_true[:, i], 
            predictions[:, i],
            average='binary',
            zero_division=0
        )
        
        # Accuracy for this label
        label_accuracy = accuracy_score(labels_true[:, i], predictions[:, i])
        
        # ROC-AUC for this label
        try:
            if len(np.unique(labels_true[:, i])) > 1:
                roc_auc = roc_auc_score(labels_true[:, i], probs[:, i])
            else:
                roc_auc = 0.0
        except:
            roc_auc = 0.0
        
        per_emotion_metrics[emotion] = {
            'precision': float(precision) if precision is not None else 0.0,
            'recall': float(recall) if recall is not None else 0.0,
            'f1': float(f1) if f1 is not None else 0.0,
            'accuracy': float(label_accuracy) if label_accuracy is not None else 0.0,
            'roc_auc': float(roc_auc) if roc_auc is not None else 0.0,
            'support': int(support) if support is not None else int(labels_true[:, i].sum())
        }
        
        per_emotion_roc_data[emotion] = {
            'y_true': labels_true[:, i].tolist(),
            'y_probs': probs[:, i].tolist()
        }
    
    # Save detailed metrics report
    print("  - Saving comprehensive metrics report...")
    metrics_report = {
        'model_name': MODEL_NAME,
        'production_training': True,
        'training_config': {
            'max_length': MAX_LENGTH,
            'batch_size': BATCH_SIZE,
            'learning_rate': LEARNING_RATE,
            'num_epochs': NUM_EPOCHS,
            'warmup_steps': WARMUP_STEPS,
            'train_samples': len(tokenized_datasets['train']),
            'val_samples': len(tokenized_datasets['validation']),
            'test_samples': len(tokenized_datasets['test'])
        },
        'training_duration': str(training_duration),
        'training_date': datetime.now().isoformat(),
        'overall_metrics': {
            'micro_f1': float(test_results['eval_micro_f1']),
            'macro_f1': float(test_results['eval_macro_f1']),
            'exact_match': float(test_results['eval_exact_match']),
            'subset_accuracy': float(subset_accuracy),
            'sample_accuracy': float(sample_accuracy),
            'hamming_loss': float(hamming),
            'roc_auc_micro': float(roc_auc_micro),
            'roc_auc_macro': float(roc_auc_macro),
            'roc_auc_weighted': float(roc_auc_weighted),
            'coverage_error': float(coverage),
            'label_ranking_avg_precision': float(lrap)
        },
        'per_emotion_metrics': per_emotion_metrics,
        'roc_curve_data': per_emotion_roc_data,
        'training_history': {
            'total_steps': train_result.global_step,
            'final_train_loss': float(train_result.training_loss)
        }
    }
    
    with open(os.path.join(metrics_dir, 'metrics_report.json'), 'w') as f:
        json.dump(metrics_report, f, indent=2)
    
    # Save classification report as text
    print("  - Creating comprehensive classification report...")
    with open(os.path.join(metrics_dir, 'classification_report.txt'), 'w') as f:
        f.write("=" * 80 + "\\n")
        f.write("EMOTION DETECTION MODEL - COMPREHENSIVE CLASSIFICATION REPORT\\n")
        f.write("=" * 80 + "\\n\\n")
        f.write(f"Model: {MODEL_NAME}\\n")
        f.write(f"Training Mode: Production (Full Dataset)\\n")
        f.write(f"Training Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\\n")
        f.write(f"Training Duration: {training_duration}\\n\\n")
        
        f.write("Dataset Sizes:\\n")
        f.write(f"  Training:   {len(tokenized_datasets['train']):>6d} samples\\n")
        f.write(f"  Validation: {len(tokenized_datasets['validation']):>6d} samples\\n")
        f.write(f"  Test:       {len(tokenized_datasets['test']):>6d} samples\\n\\n")
        
        f.write("=" * 80 + "\\n")
        f.write("OVERALL PERFORMANCE METRICS\\n")
        f.write("=" * 80 + "\\n\\n")
        
        f.write("Multi-Label Classification Metrics:\\n")
        f.write("-" * 80 + "\\n")
        f.write(f"  Micro F1 Score:               {test_results['eval_micro_f1']*100:>6.2f}%\\n")
        f.write(f"  Macro F1 Score:               {test_results['eval_macro_f1']*100:>6.2f}%\\n")
        f.write(f"  Subset Accuracy (Exact Match):{subset_accuracy*100:>6.2f}%\\n")
        f.write(f"  Sample Accuracy:              {sample_accuracy*100:>6.2f}%\\n")
        f.write(f"  Hamming Loss:                 {hamming:>6.4f}\\n\\n")
        
        f.write("ROC-AUC Scores:\\n")
        f.write("-" * 80 + "\\n")
        f.write(f"  Micro-Average ROC-AUC:        {roc_auc_micro*100:>6.2f}%\\n")
        f.write(f"  Macro-Average ROC-AUC:        {roc_auc_macro*100:>6.2f}%\\n")
        f.write(f"  Weighted ROC-AUC:             {roc_auc_weighted*100:>6.2f}%\\n\\n")
        
        f.write("Ranking Metrics:\\n")
        f.write("-" * 80 + "\\n")
        f.write(f"  Coverage Error:               {coverage:>6.2f}\\n")
        f.write(f"  Label Ranking Avg Precision:  {lrap*100:>6.2f}%\\n\\n")
        
        f.write("=" * 80 + "\\n")
        f.write("PER-EMOTION PERFORMANCE\\n")
        f.write("=" * 80 + "\\n\\n")
        f.write(f"{'Emotion':<18} {'Precision':>10} {'Recall':>10} {'F1':>10} {'Accuracy':>10} {'ROC-AUC':>10} {'Support':>10}\\n")
        f.write("-" * 80 + "\\n")
        
        # Sort by F1 score descending
        sorted_emotions = sorted(per_emotion_metrics.items(), key=lambda x: x[1]['f1'], reverse=True)
        for emotion, metrics in sorted_emotions:
            f.write(f"{emotion:<18} {metrics['precision']*100:>9.2f}% {metrics['recall']*100:>9.2f}% "
                    f"{metrics['f1']*100:>9.2f}% {metrics['accuracy']*100:>9.2f}% "
                    f"{metrics['roc_auc']*100:>9.2f}% {metrics['support']:>10d}\\n")
        
        f.write("\\n" + "=" * 80 + "\\n")
        f.write("Top 5 Best Performing Emotions:\\n")
        f.write("-" * 80 + "\\n")
        for i, (emotion, metrics) in enumerate(sorted_emotions[:5], 1):
            f.write(f"{i}. {emotion}: F1={metrics['f1']*100:.2f}%, ROC-AUC={metrics['roc_auc']*100:.2f}%\\n")
        
        f.write("\\n" + "=" * 80 + "\\n")
        f.write("Bottom 5 Emotions (Need Improvement):\\n")
        f.write("-" * 80 + "\\n")
        for i, (emotion, metrics) in enumerate(sorted_emotions[-5:], 1):
            f.write(f"{i}. {emotion}: F1={metrics['f1']*100:.2f}%, ROC-AUC={metrics['roc_auc']*100:.2f}%\\n")
    
    # Save predictions sample for analysis
    print("  - Saving sample predictions...")
    with open(os.path.join(metrics_dir, 'sample_predictions.json'), 'w') as f:
        sample_size = min(100, len(labels_true))
        samples = []
        for i in range(sample_size):
            true_emotions = [emotion_labels[j] for j in range(len(emotion_labels)) if labels_true[i][j] == 1]
            pred_emotions = [emotion_labels[j] for j in range(len(emotion_labels)) if predictions[i][j] == 1]
            samples.append({
                'index': i,
                'true_emotions': true_emotions,
                'predicted_emotions': pred_emotions,
                'probabilities': {emotion_labels[j]: float(probs[i][j]) for j in range(len(emotion_labels)) if probs[i][j] > 0.3}
            })
        json.dump({'samples': samples}, f, indent=2)
    
    print(f"✓ Comprehensive metrics saved to: {metrics_dir}")
    print(f"  - metrics_report.json (structured metrics)")
    print(f"  - classification_report.txt (human-readable report)")
    print(f"  - sample_predictions.json (100 sample predictions)")
    print()
    
    # Generate visualizations
    try:
        print("Generating comprehensive metric visualizations...")
        from visualize_metrics import create_metrics_visualizations, generate_visualization_index
        plots_dir = create_metrics_visualizations(metrics_dir, metrics_report)
        generate_visualization_index(plots_dir)
        print(f"✓ Visualizations saved to: {plots_dir}")
        print(f"  - 7 detailed plots generated")
        print(f"  - Open plots/index.html in browser to view all")
        print()
    except ImportError:
        print("⚠️  Visualization libraries not installed. Skipping plots.")
        print("   Install with: pip install matplotlib seaborn")
        print()
    except Exception as e:
        print(f"⚠️  Could not generate visualizations: {e}")
        print()
    
except Exception as e:
    print(f"❌ Error during evaluation: {e}")
    exit(1)

# =============================================================================
# STEP 8: Save Model
# =============================================================================
print("=" * 80)
print("STEP 8: Saving Model")
print("=" * 80)

try:
    print(f"Saving model to: {OUTPUT_DIR}")
    
    # Save the model and tokenizer
    trainer.save_model(OUTPUT_DIR)
    tokenizer.save_pretrained(OUTPUT_DIR)
    
    # Save emotion labels
    with open(os.path.join(OUTPUT_DIR, 'emotion_labels.json'), 'w') as f:
        json.dump(emotion_labels, f, indent=2)
    
    # Save training info
    training_info = {
        'model_name': MODEL_NAME,
        'num_labels': num_labels,
        'emotion_labels': emotion_labels,
        'training_date': datetime.now().isoformat(),
        'training_duration': str(training_duration),
        'test_results': {
            'micro_f1': float(test_results['eval_micro_f1']),
            'macro_f1': float(test_results['eval_macro_f1']),
            'exact_match': float(test_results['eval_exact_match'])
        },
        'hyperparameters': {
            'max_length': MAX_LENGTH,
            'batch_size': BATCH_SIZE,
            'learning_rate': LEARNING_RATE,
            'num_epochs': NUM_EPOCHS,
            'warmup_steps': WARMUP_STEPS
        }
    }
    
    with open(os.path.join(OUTPUT_DIR, 'training_info.json'), 'w') as f:
        json.dump(training_info, f, indent=2)
    
    print("✓ Model saved successfully!")
    print(f"  Model files: {OUTPUT_DIR}")
    print(f"  Size: {sum(os.path.getsize(os.path.join(OUTPUT_DIR, f)) for f in os.listdir(OUTPUT_DIR) if os.path.isfile(os.path.join(OUTPUT_DIR, f))) / 1e6:.2f} MB")
    print()
    
except Exception as e:
    print(f"❌ Error saving model: {e}")
    exit(1)

# =============================================================================
# STEP 9: Test Inference
# =============================================================================
print("=" * 80)
print("STEP 9: Testing Inference")
print("=" * 80)

def test_prediction(text):
    """Test the model with sample text"""
    inputs = tokenizer(text, return_tensors='pt', truncation=True, max_length=MAX_LENGTH)
    inputs = {k: v.to(device) for k, v in inputs.items()}
    
    with torch.no_grad():
        outputs = model(**inputs)
        probs = torch.sigmoid(outputs.logits).cpu().numpy()[0]
    
    # Get emotions above threshold
    threshold = 0.5
    detected_emotions = {}
    for idx, prob in enumerate(probs):
        if prob >= threshold:
            detected_emotions[emotion_labels[idx]] = float(prob)
    
    return detected_emotions

# Test with sample texts
test_samples = [
    "I'm feeling really happy and excited about my new job!",
    "I feel sad and lonely today, everything seems difficult.",
    "This situation makes me so angry and frustrated!",
    "I'm worried and anxious about the upcoming exam."
]

print("Testing model with sample inputs:")
print()

for i, text in enumerate(test_samples, 1):
    print(f"Sample {i}: \"{text}\"")
    emotions = test_prediction(text)
    
    if emotions:
        print("  Detected emotions:")
        for emotion, prob in sorted(emotions.items(), key=lambda x: x[1], reverse=True):
            print(f"    - {emotion}: {prob:.3f}")
    else:
        print("  No emotions detected above threshold")
    print()

# =============================================================================
# COMPLETE!
# =============================================================================
print("=" * 80)
print("✅ TRAINING COMPLETE!")
print("=" * 80)
print()
print("📁 Model Location:")
print(f"   {os.path.abspath(OUTPUT_DIR)}")
print()
print("📊 Performance Summary:")
print(f"   Micro F1 Score: {test_results['eval_micro_f1']*100:.2f}%")
print(f"   Macro F1 Score: {test_results['eval_macro_f1']*100:.2f}%")
print(f"   Exact Match: {test_results['eval_exact_match']*100:.2f}%")
print()
print("📈 Metrics Reports:")
print(f"   {os.path.abspath(metrics_dir)}")
print("   - metrics_report.json (structured metrics)")
print("   - classification_report.txt (detailed per-emotion analysis)")
print("   - sample_predictions.json (100 prediction samples)")
print()
print("🎯 Next Steps:")
print("   1. The trained model is saved in: backend/models/distilbert-goemotions-mental/")
print("   2. Review metrics: Check the metrics/ folder for detailed performance analysis")
print("   3. Start the backend server: cd backend && python app.py")
print("   4. The model will be loaded automatically")
print("   4. Test the API endpoints with your frontend")
print()
print("=" * 80)
