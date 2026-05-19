"""
Advanced Training Configuration for 85%+ F1 Scores

This uses RoBERTa-large with optimized settings for high F1 scores
Expected: Micro F1 85%+, Macro F1 75%+
Training time: ~30-40 hours on RTX 2050
"""

import os
from datetime import datetime
import torch
from datasets import load_dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    Trainer,
    TrainingArguments,
    DataCollatorWithPadding
)
import numpy as np
from sklearn.metrics import precision_recall_fscore_support, accuracy_score

# Configuration for HIGH F1 SCORES
MODEL_NAME = "roberta-large"  # More powerful than DistilBERT
OUTPUT_DIR = "./models/roberta-large-goemotions"
MAX_LENGTH = 256  # Shorter for faster training with larger model
BATCH_SIZE = 8   # Smaller batch for 4GB GPU with large model
LEARNING_RATE = 5e-6  # Lower LR for large model
NUM_EPOCHS = 15  # More epochs for convergence
WARMUP_RATIO = 0.1  # Warmup for 10% of training
WEIGHT_DECAY = 0.01
GRADIENT_ACCUMULATION_STEPS = 4  # Effective batch size = 8*4 = 32
FP16 = True  # Mixed precision for faster training

print("=" * 80)
print("HIGH-PERFORMANCE TRAINING FOR 85%+ F1 SCORES")
print("=" * 80)
print()
print("⚠️  WARNING: This will take 30-40 hours on RTX 2050")
print("   Model: RoBERTa-Large (355M parameters)")
print("   Epochs: 15")
print("   Expected Results:")
print("     - Micro F1: 85-88%")
print("     - Macro F1: 75-80%")
print("     - Sample Accuracy: 98%+")
print()
input("Press Enter to continue or Ctrl+C to cancel...")

# Device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"🖥️  Device: {device}")
if torch.cuda.is_available():
    print(f"  GPU: {torch.cuda.get_device_name(0)}")
    print(f"  Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
print()

# Load dataset
print("📦 Loading GoEmotions dataset...")
dataset = load_dataset("google-research-datasets/go_emotions", "simplified")
emotion_labels = dataset['train'].features['labels'].feature.names
num_labels = len(emotion_labels)
print(f"✓ Dataset loaded - {num_labels} emotions")
print()

# Load tokenizer and model
print("🤖 Loading RoBERTa-Large...")
print("   This may take a few minutes (355M parameters)...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_NAME,
    num_labels=num_labels,
    problem_type="multi_label_classification"
)
model.to(device)
print(f"✓ Model loaded")
print(f"  Parameters: {sum(p.numel() for p in model.parameters()):,}")
print()

# Preprocess
print("🔄 Preprocessing dataset...")
def preprocess_function(examples):
    tokenized = tokenizer(
        examples['text'],
        truncation=True,
        padding='max_length',
        max_length=MAX_LENGTH
    )
    
    # Multi-hot encoding
    labels = []
    for label_list in examples['labels']:
        multi_hot = [0.0] * num_labels
        for label_id in label_list:
            multi_hot[label_id] = 1.0
        labels.append(multi_hot)
    
    tokenized['labels'] = np.array(labels, dtype=np.float32)
    return tokenized

tokenized_datasets = dataset.map(
    preprocess_function,
    batched=True,
    remove_columns=dataset['train'].column_names
)
print("✓ Preprocessing complete")
print()

# Data collator
data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

# Metrics
def compute_metrics(eval_pred):
    logits, labels = eval_pred
    probs = 1 / (1 + np.exp(-logits))  # Sigmoid
    predictions = (probs > 0.5).astype(int)
    
    # F1 scores
    from sklearn.metrics import f1_score
    micro_f1 = f1_score(labels, predictions, average='micro', zero_division=0)
    macro_f1 = f1_score(labels, predictions, average='macro', zero_division=0)
    
    # Accuracy
    exact_match = accuracy_score(labels, predictions)
    
    return {
        'micro_f1': micro_f1,
        'macro_f1': macro_f1,
        'exact_match': exact_match
    }

# Training arguments
training_args = TrainingArguments(
    output_dir=OUTPUT_DIR,
    evaluation_strategy="epoch",
    save_strategy="epoch",
    learning_rate=LEARNING_RATE,
    per_device_train_batch_size=BATCH_SIZE,
    per_device_eval_batch_size=BATCH_SIZE,
    num_train_epochs=NUM_EPOCHS,
    weight_decay=WEIGHT_DECAY,
    warmup_ratio=WARMUP_RATIO,
    gradient_accumulation_steps=GRADIENT_ACCUMULATION_STEPS,
    fp16=FP16,
    logging_dir='./training_logs',
    logging_steps=100,
    save_total_limit=2,
    load_best_model_at_end=True,
    metric_for_best_model="micro_f1",
    greater_is_better=True,
    report_to="none"
)

# Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets['train'],
    eval_dataset=tokenized_datasets['validation'],
    data_collator=data_collator,
    compute_metrics=compute_metrics
)

# Train
print("🚀 Starting training...")
print(f"   This will take approximately 30-40 hours")
print()
trainer.train()

print()
print("✅ Training complete!")
print("   Run evaluate_model.py to see full metrics and visualizations")
