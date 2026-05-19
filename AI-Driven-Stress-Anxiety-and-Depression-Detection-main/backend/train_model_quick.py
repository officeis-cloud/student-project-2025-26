"""
Quick Training Script - For Testing/Development
This uses a smaller subset of data and fewer epochs for faster training
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
    Trainer
)
from sklearn.metrics import f1_score, accuracy_score, precision_recall_fscore_support
import json

print("=" * 80)
print("QUICK TRAINING MODE - For Testing")
print("=" * 80)
print()

# Configuration - Reduced for speed
MODEL_NAME = "distilbert-base-uncased"
OUTPUT_DIR = "./models/quick-training"  # Separate directory for quick training
MAX_LENGTH = 128  # Reduced from 512
BATCH_SIZE = 32   # Increased for faster training
LEARNING_RATE = 3e-5
NUM_EPOCHS = 1    # Just 1 epoch for testing
TRAIN_SAMPLES = 5000  # Use subset of data
VAL_SAMPLES = 1000
TEST_SAMPLES = 1000

os.makedirs(OUTPUT_DIR, exist_ok=True)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"🖥️  Device: {device}")
if torch.cuda.is_available():
    print(f"  GPU: {torch.cuda.get_device_name(0)}")
    print(f"  Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
else:
    print("  Note: Training on CPU will be slower. Use GPU for faster training.")
print()

# Load dataset
print("Loading GoEmotions dataset...")
dataset = load_dataset("go_emotions", "simplified")

# Use subset for quick training
print("Using subset of data for quick training:")
train_dataset = dataset['train'].shuffle(seed=42).select(range(min(TRAIN_SAMPLES, len(dataset['train']))))
val_dataset = dataset['validation'].shuffle(seed=42).select(range(min(VAL_SAMPLES, len(dataset['validation']))))
test_dataset = dataset['test'].shuffle(seed=42).select(range(min(TEST_SAMPLES, len(dataset['test']))))

print(f"  Train: {len(train_dataset)} samples")
print(f"  Val: {len(val_dataset)} samples")
print(f"  Test: {len(test_dataset)} samples")
print()

# Get labels
emotion_labels = dataset['train'].features['labels'].feature.names
num_labels = len(emotion_labels)

# Load tokenizer and model
print("Loading model...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_NAME,
    num_labels=num_labels,
    problem_type="multi_label_classification"
)
model.to(device)
print("✓ Model loaded")
print()

# Preprocessing
def preprocess_function(examples):
    tokenized = tokenizer(
        examples['text'],
        truncation=True,
        padding='max_length',
        max_length=MAX_LENGTH
    )
    
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

print("Preprocessing...")
train_dataset = train_dataset.map(preprocess_function, batched=True, remove_columns=train_dataset.column_names)
val_dataset = val_dataset.map(preprocess_function, batched=True, remove_columns=val_dataset.column_names)
test_dataset = test_dataset.map(preprocess_function, batched=True, remove_columns=test_dataset.column_names)

train_dataset.set_format('torch')
val_dataset.set_format('torch')
test_dataset.set_format('torch')
print("✓ Data preprocessed")
print()

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

# Metrics
def compute_metrics(eval_pred):
    logits, labels = eval_pred
    # Convert to numpy if not already
    if isinstance(logits, torch.Tensor):
        logits = logits.cpu().numpy()
    if isinstance(labels, torch.Tensor):
        labels = labels.cpu().numpy()
    
    probs = 1 / (1 + np.exp(-logits))  # Sigmoid
    predictions = (probs > 0.5).astype(int)
    
    # Ensure we have valid predictions
    if predictions.sum() == 0:
        print("Warning: No positive predictions made!")
    
    micro_f1 = f1_score(labels, predictions, average='micro', zero_division=0)
    macro_f1 = f1_score(labels, predictions, average='macro', zero_division=0)
    exact_match = accuracy_score(labels, predictions)
    
    return {
        'micro_f1': micro_f1,
        'macro_f1': macro_f1,
        'exact_match': exact_match,
    }

# Training
training_args = TrainingArguments(
    output_dir=OUTPUT_DIR,
    evaluation_strategy="epoch",
    save_strategy="epoch",
    learning_rate=LEARNING_RATE,
    per_device_train_batch_size=BATCH_SIZE,
    per_device_eval_batch_size=BATCH_SIZE,
    num_train_epochs=NUM_EPOCHS,
    weight_decay=0.01,
    logging_steps=50,
    load_best_model_at_end=True,
    metric_for_best_model='micro_f1',
    fp16=torch.cuda.is_available(),
    report_to="none",
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    tokenizer=tokenizer,
    data_collator=data_collator,
    compute_metrics=compute_metrics,
)

print("=" * 80)
print("TRAINING")
print("=" * 80)
print()

# Train
print("Starting training...")
training_start_time = time.time()
train_result = trainer.train()
training_time = time.time() - training_start_time

# Evaluate
print()
print("Evaluating on test set...")
test_results = trainer.evaluate(test_dataset)

print()
print("=" * 80)
print("RESULTS")
print("=" * 80)
print(f"Micro F1: {test_results['eval_micro_f1']*100:.2f}%")
print(f"Macro F1: {test_results['eval_macro_f1']*100:.2f}%")
print(f"Exact Match: {test_results['eval_exact_match']*100:.2f}%")
print(f"Training Time: {training_time/60:.2f} minutes")
print()

# Generate detailed metrics
print("Generating detailed metrics...")
metrics_dir = os.path.join(OUTPUT_DIR, 'metrics')
os.makedirs(metrics_dir, exist_ok=True)

# Get predictions
model.eval()
test_predictions = trainer.predict(test_dataset)
logits = test_predictions.predictions
labels_true = test_predictions.label_ids

# Convert to predictions
probs = torch.sigmoid(torch.tensor(logits)).numpy()
predictions = (probs > 0.5).astype(int)

# Comprehensive metrics calculation
from sklearn.metrics import (
    classification_report, precision_recall_fscore_support,
    roc_auc_score, accuracy_score, hamming_loss,
    coverage_error, label_ranking_average_precision_score
)

print("Calculating comprehensive metrics...")

# Overall metrics
hamming = hamming_loss(labels_true, predictions)
subset_accuracy = accuracy_score(labels_true, predictions)  # Exact match
sample_accuracy = (labels_true == predictions).mean()  # Per-sample accuracy

# ROC-AUC (requires probabilities)
try:
    # Micro-average ROC-AUC
    roc_auc_micro = roc_auc_score(labels_true, probs, average='micro')
    # Macro-average ROC-AUC
    roc_auc_macro = roc_auc_score(labels_true, probs, average='macro')
    # Weighted ROC-AUC
    roc_auc_weighted = roc_auc_score(labels_true, probs, average='weighted')
except:
    roc_auc_micro = roc_auc_macro = roc_auc_weighted = 0.0

# Label ranking metrics
try:
    coverage = coverage_error(labels_true, probs)
    lrap = label_ranking_average_precision_score(labels_true, probs)
except:
    coverage = lrap = 0.0

# Per-emotion metrics with ROC-AUC
per_emotion_metrics = {}
per_emotion_roc_data = {}  # For ROC curve visualization

for i, emotion in enumerate(emotion_labels):
    # Standard metrics
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
        if len(np.unique(labels_true[:, i])) > 1:  # Need both classes
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
    
    # Store probabilities for ROC curve plotting
    per_emotion_roc_data[emotion] = {
        'y_true': labels_true[:, i].tolist(),
        'y_probs': probs[:, i].tolist()
    }

# Save detailed metrics
metrics_report = {
    'model_name': MODEL_NAME,
    'quick_training': True,
    'training_config': {
        'train_samples': TRAIN_SAMPLES,
        'val_samples': VAL_SAMPLES,
        'test_samples': TEST_SAMPLES,
        'batch_size': BATCH_SIZE,
        'learning_rate': LEARNING_RATE,
        'num_epochs': NUM_EPOCHS,
        'max_length': MAX_LENGTH
    },
    'training_time_minutes': round(training_time/60, 2),
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
        'train_loss': float(train_result.training_loss)
    }
}

# Save metrics JSON
with open(os.path.join(metrics_dir, 'metrics_report.json'), 'w') as f:
    json.dump(metrics_report, f, indent=2)

# Save classification report as text
with open(os.path.join(metrics_dir, 'classification_report.txt'), 'w') as f:
    f.write("=" * 80 + "\n")
    f.write("EMOTION DETECTION MODEL - COMPREHENSIVE CLASSIFICATION REPORT\n")
    f.write("=" * 80 + "\n\n")
    f.write(f"Model: {MODEL_NAME}\n")
    f.write(f"Training Mode: Quick Training\n")
    f.write(f"Training Time: {training_time/60:.2f} minutes\n\n")
    
    f.write("=" * 80 + "\n")
    f.write("OVERALL PERFORMANCE METRICS\n")
    f.write("=" * 80 + "\n\n")
    
    f.write("Multi-Label Classification Metrics:\n")
    f.write("-" * 80 + "\n")
    f.write(f"  Micro F1 Score:               {test_results['eval_micro_f1']*100:>6.2f}%\n")
    f.write(f"  Macro F1 Score:               {test_results['eval_macro_f1']*100:>6.2f}%\n")
    f.write(f"  Subset Accuracy (Exact Match):{subset_accuracy*100:>6.2f}%\n")
    f.write(f"  Sample Accuracy:              {sample_accuracy*100:>6.2f}%\n")
    f.write(f"  Hamming Loss:                 {hamming:>6.4f}\n\n")
    
    f.write("ROC-AUC Scores:\n")
    f.write("-" * 80 + "\n")
    f.write(f"  Micro-Average ROC-AUC:        {roc_auc_micro*100:>6.2f}%\n")
    f.write(f"  Macro-Average ROC-AUC:        {roc_auc_macro*100:>6.2f}%\n")
    f.write(f"  Weighted ROC-AUC:             {roc_auc_weighted*100:>6.2f}%\n\n")
    
    f.write("Ranking Metrics:\n")
    f.write("-" * 80 + "\n")
    f.write(f"  Coverage Error:               {coverage:>6.2f}\n")
    f.write(f"  Label Ranking Avg Precision:  {lrap*100:>6.2f}%\n\n")
    
    f.write("=" * 80 + "\n")
    f.write("PER-EMOTION PERFORMANCE\n")
    f.write("=" * 80 + "\n\n")
    f.write(f"{'Emotion':<18} {'Precision':>10} {'Recall':>10} {'F1':>10} {'Accuracy':>10} {'ROC-AUC':>10} {'Support':>10}\n")
    f.write("-" * 80 + "\n")
    
    for emotion, metrics in per_emotion_metrics.items():
        f.write(f"{emotion:<18} {metrics['precision']*100:>9.2f}% {metrics['recall']*100:>9.2f}% "
                f"{metrics['f1']*100:>9.2f}% {metrics['accuracy']*100:>9.2f}% "
                f"{metrics['roc_auc']*100:>9.2f}% {metrics['support']:>10d}\n")

print(f"✓ Metrics saved to: {metrics_dir}")

# Generate visualizations
try:
    print()
    print("Generating metric visualizations...")
    from visualize_metrics import create_metrics_visualizations, generate_visualization_index
    plots_dir = create_metrics_visualizations(metrics_dir, metrics_report)
    generate_visualization_index(plots_dir)
    print(f"✓ Visualizations saved to: {plots_dir}")
except ImportError:
    print("⚠️  Visualization libraries not installed. Skipping plots.")
    print("   Install with: pip install matplotlib seaborn")
except Exception as e:
    print(f"⚠️  Could not generate visualizations: {e}")

# Save model
print()
print("Saving model...")
trainer.save_model(OUTPUT_DIR)
tokenizer.save_pretrained(OUTPUT_DIR)

with open(os.path.join(OUTPUT_DIR, 'emotion_labels.json'), 'w') as f:
    json.dump(emotion_labels, f)

with open(os.path.join(OUTPUT_DIR, 'training_info.json'), 'w') as f:
    json.dump({
        'model_name': MODEL_NAME,
        'quick_training': True,
        'test_results': {
            'micro_f1': float(test_results['eval_micro_f1']),
            'macro_f1': float(test_results['eval_macro_f1']),
            'exact_match': float(test_results['eval_exact_match'])
        }
    }, f, indent=2)

print("✓ Model saved to:", OUTPUT_DIR)
print(f"✓ Metrics saved to: {metrics_dir}")
print()
print("Files generated:")
print(f"  - {metrics_dir}/metrics_report.json")
print(f"  - {metrics_dir}/classification_report.txt")
print()
print("NOTE: This is a quick-trained model for testing.")
print("For production, run train_model.py with full dataset.")
print()
