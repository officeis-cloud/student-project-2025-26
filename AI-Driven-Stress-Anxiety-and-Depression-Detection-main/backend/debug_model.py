"""
Quick debug script to check model output probabilities
"""
import torch
import numpy as np
from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification

MODEL_DIR = "./models/distilbert-goemotions-mental"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load model and tokenizer
print("Loading model...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_DIR)
model.to(device)
model.eval()

# Load a few test samples
dataset = load_dataset("google-research-datasets/go_emotions", "simplified")
test_samples = dataset['test'].select(range(10))

print("\nTesting on 10 samples:")
print("=" * 80)

with torch.no_grad():
    for idx, example in enumerate(test_samples):
        text = example['text']
        true_labels = example['labels']
        
        # Tokenize
        inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
        inputs = {k: v.to(device) for k, v in inputs.items()}
        
        # Get predictions
        outputs = model(**inputs)
        logits = outputs.logits[0].cpu().numpy()
        probs = torch.sigmoid(torch.tensor(logits)).numpy()
        
        print(f"\nSample {idx + 1}:")
        print(f"Text: {text[:80]}...")
        print(f"True labels: {true_labels}")
        print(f"Logit range: [{logits.min():.3f}, {logits.max():.3f}]")
        print(f"Prob range: [{probs.min():.3f}, {probs.max():.3f}]") 
        print(f"Probs > 0.5: {(probs > 0.5).sum()}")
        print(f"Probs > 0.3: {(probs > 0.3).sum()}")
        print(f"Top 5 probs: {sorted(probs, reverse=True)[:5]}")

print("\n" + "=" * 80)
print("Summary:")
print("If all probs < 0.5, the model might need calibration or lower threshold")
