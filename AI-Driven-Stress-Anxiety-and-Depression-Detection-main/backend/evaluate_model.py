"""
Evaluate a trained model and generate comprehensive metrics and visualizations
"""

import os
import json
import torch
import numpy as np
from datetime import datetime
from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer
from sklearn.metrics import (
    precision_recall_fscore_support,
    accuracy_score,
    hamming_loss,
    roc_auc_score,
    coverage_error,
    label_ranking_average_precision_score
)
from visualize_metrics import create_metrics_visualizations, generate_visualization_index

# Configuration
MODEL_DIR = "./models/distilbert-goemotions-mental"
MAX_LENGTH = 512
BATCH_SIZE = 16

print("=" * 80)
print("Model Evaluation & Metrics Generation")
print("=" * 80)
print()

# Setup device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"🖥️  Device: {device}")
if torch.cuda.is_available():
    print(f"  GPU: {torch.cuda.get_device_name(0)}")
print()

# Load dataset
print("📦 Loading GoEmotions dataset...")
dataset = load_dataset("google-research-datasets/go_emotions", "simplified")
emotion_labels = dataset['train'].features['labels'].feature.names
print(f"✓ Dataset loaded - {len(emotion_labels)} emotions")
print()

# Load model and tokenizer
print("🤖 Loading trained model...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_DIR)
model.to(device)
print(f"✓ Model loaded from: {MODEL_DIR}")
print()

# Tokenize test set
print("🔄 Tokenizing test set...")
num_labels = len(emotion_labels)

def tokenize_function(examples):
    # Tokenize text
    tokenized = tokenizer(
        examples['text'], 
        padding='max_length', 
        truncation=True, 
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

tokenized_test = dataset['test'].map(tokenize_function, batched=True, remove_columns=dataset['test'].column_names)
tokenized_test.set_format("torch", columns=["input_ids", "attention_mask", "labels"])
print(f"✓ Test set ready: {len(tokenized_test)} samples")
print()

# Setup trainer for prediction
import transformers

# Custom data collator for multi-label classification
def collate_fn(examples):
    import torch
    # Extract features - labels are already tensors from set_format
    batch = {
        'input_ids': torch.stack([ex['input_ids'] for ex in examples]),
        'attention_mask': torch.stack([ex['attention_mask'] for ex in examples]),
    }
    # Handle labels if they exist
    if 'labels' in examples[0]:
        labels = [ex['labels'] for ex in examples]
        # If labels are tensors, stack them; if lists, convert them
        if isinstance(labels[0], torch.Tensor):
            batch['labels'] = torch.stack(labels).float()
        else:
            batch['labels'] = torch.tensor(labels, dtype=torch.float)
    return batch

trainer = Trainer(
    model=model,
    data_collator=collate_fn,
)

# Get predictions
print("🔮 Generating predictions...")
predictions_output = trainer.predict(tokenized_test)
logits = predictions_output.predictions
labels_true = predictions_output.label_ids

# Convert to probabilities and binary predictions
probs = 1 / (1 + np.exp(-logits))  # Sigmoid
predictions = (probs > 0.5).astype(int)
print(f"✓ Predictions generated")
print()

# Compute comprehensive metrics
print("📊 Computing comprehensive metrics...")

# Overall metrics
hamming = hamming_loss(labels_true, predictions)
subset_accuracy = accuracy_score(labels_true, predictions)
sample_accuracy = (labels_true == predictions).mean()

# F1 scores
from sklearn.metrics import f1_score
micro_f1 = f1_score(labels_true, predictions, average='micro', zero_division=0)
macro_f1 = f1_score(labels_true, predictions, average='macro', zero_division=0)

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

print(f"  Micro F1: {micro_f1:.4f} ({micro_f1*100:.2f}%)")
print(f"  Macro F1: {macro_f1:.4f} ({macro_f1*100:.2f}%)")
print(f"  ROC-AUC (Micro): {roc_auc_micro:.4f} ({roc_auc_micro*100:.2f}%)")
print(f"  ROC-AUC (Macro): {roc_auc_macro:.4f} ({roc_auc_macro*100:.2f}%)")
print()

# Per-emotion metrics
per_emotion_metrics = {}
per_emotion_roc_data = {}

print("📊 Computing per-emotion metrics...")
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

print(f"✓ Per-emotion metrics computed for {len(emotion_labels)} emotions")
print()

# Save metrics report
metrics_dir = os.path.join(MODEL_DIR, "metrics")
os.makedirs(metrics_dir, exist_ok=True)

metrics_report = {
    'model_name': 'distilbert-base-uncased',
    'evaluation_date': datetime.now().isoformat(),
    'model_dir': MODEL_DIR,
    'test_samples': len(tokenized_test),
    'overall_metrics': {
        'micro_f1': float(micro_f1),
        'macro_f1': float(macro_f1),
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
    'roc_curve_data': per_emotion_roc_data
}

# Save JSON report
metrics_file = os.path.join(metrics_dir, "metrics_report.json")
with open(metrics_file, 'w') as f:
    json.dump(metrics_report, f, indent=2)
print(f"✓ Metrics saved to: {metrics_file}")

# Generate text report
report_file = os.path.join(metrics_dir, "classification_report.txt")
with open(report_file, 'w') as f:
    f.write("=" * 80 + "\n")
    f.write("COMPREHENSIVE MODEL EVALUATION REPORT\n")
    f.write("=" * 80 + "\n\n")
    
    f.write(f"Evaluation Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write(f"Model: {MODEL_DIR}\n")
    f.write(f"Test Samples: {len(tokenized_test)}\n\n")
    
    f.write("OVERALL METRICS:\n")
    f.write("-" * 80 + "\n")
    f.write(f"Micro F1 Score:              {micro_f1:.4f} ({micro_f1*100:.2f}%)\n")
    f.write(f"Macro F1 Score:              {macro_f1:.4f} ({macro_f1*100:.2f}%)\n")
    f.write(f"Subset Accuracy:             {subset_accuracy:.4f} ({subset_accuracy*100:.2f}%)\n")
    f.write(f"Sample Accuracy:             {sample_accuracy:.4f} ({sample_accuracy*100:.2f}%)\n")
    f.write(f"Hamming Loss:                {hamming:.4f}\n")
    f.write(f"ROC-AUC (Micro):            {roc_auc_micro:.4f} ({roc_auc_micro*100:.2f}%)\n")
    f.write(f"ROC-AUC (Macro):            {roc_auc_macro:.4f} ({roc_auc_macro*100:.2f}%)\n")
    f.write(f"ROC-AUC (Weighted):         {roc_auc_weighted:.4f} ({roc_auc_weighted*100:.2f}%)\n")
    f.write(f"Coverage Error:              {coverage:.4f}\n")
    f.write(f"Label Ranking Avg Precision: {lrap:.4f}\n\n")
    
    f.write("PER-EMOTION METRICS:\n")
    f.write("-" * 80 + "\n")
    f.write(f"{'Emotion':<15} {'Precision':<12} {'Recall':<12} {'F1':<12} {'Accuracy':<12} {'ROC-AUC':<12} {'Support':<10}\n")
    f.write("-" * 80 + "\n")
    
    for emotion, metrics in sorted(per_emotion_metrics.items(), key=lambda x: x[1]['f1'], reverse=True):
        f.write(f"{emotion:<15} "
                f"{metrics['precision']:.4f} ({metrics['precision']*100:>5.1f}%)  "
                f"{metrics['recall']:.4f} ({metrics['recall']*100:>5.1f}%)  "
                f"{metrics['f1']:.4f} ({metrics['f1']*100:>5.1f}%)  "
                f"{metrics['accuracy']:.4f} ({metrics['accuracy']*100:>5.1f}%)  "
                f"{metrics['roc_auc']:.4f} ({metrics['roc_auc']*100:>5.1f}%)  "
                f"{metrics['support']:<10}\n")

print(f"✓ Report saved to: {report_file}")
print()

# Generate visualizations
print("🎨 Generating visualizations...")
plots_dir = create_metrics_visualizations(metrics_dir, metrics_report)
index_file = generate_visualization_index(plots_dir)
print()

print("=" * 80)
print("✅ EVALUATION COMPLETE!")
print("=" * 80)
print()
print(f"📊 Metrics Report: {metrics_file}")
print(f"📄 Text Report: {report_file}")
print(f"🎨 Visualizations: {plots_dir}")
print(f"🌐 HTML Index: {index_file}")
print()
print("💡 Open the HTML index in your browser to view all visualizations!")
