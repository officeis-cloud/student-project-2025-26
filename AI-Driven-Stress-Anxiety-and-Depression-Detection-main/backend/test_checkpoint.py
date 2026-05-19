"""
Test the checkpoint-8142 (final training step)
"""
import torch
import numpy as np
from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Try the final checkpoint
MODEL_DIR = "./models/distilbert-goemotions-mental/checkpoint-8142"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

print(f"Testing checkpoint: {MODEL_DIR}")
print("=" * 80)

# Load model and tokenizer
try:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_DIR)
    model.to(device)
    model.eval()
    print("✓ Checkpoint loaded successfully")
except Exception as e:
    print(f"❌ Error loading checkpoint: {e}")
    exit(1)

# Load test samples
dataset = load_dataset("google-research-datasets/go_emotions", "simplified")
test_samples = dataset['test'].select(range(5))

print("\nTesting 5 samples:")
print("=" * 80)

with torch.no_grad():
    for idx, example in enumerate(test_samples):
        text = example['text']
        true_labels = example['labels']
        
        inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
        inputs = {k: v.to(device) for k, v in inputs.items()}
        
        outputs = model(**inputs)
        logits = outputs.logits[0].cpu().numpy()
        probs = torch.sigmoid(torch.tensor(logits)).numpy()
        
        print(f"\nSample {idx + 1}: {text[:60]}...")
        print(f"Logit range: [{logits.min():.3f}, {logits.max():.3f}]")
        print(f"Prob range: [{probs.min():.3f}, {probs.max():.3f}]")
        print(f"Max prob: {probs.max():.4f}, Probs > 0.5: {(probs > 0.5).sum()}")
