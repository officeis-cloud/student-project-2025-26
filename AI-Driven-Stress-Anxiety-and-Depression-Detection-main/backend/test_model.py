"""
Quick test to verify the trained model works correctly
"""
from emotion_predictor import EmotionPredictor

# Test texts
test_texts = [
    "I'm so happy and excited about this!",
    "I'm feeling really sad and disappointed today",
    "This makes me so angry and frustrated",
    "I'm worried and anxious about the exam"
]

print("=" * 80)
print("TESTING TRAINED MODEL")
print("=" * 80)
print()

# Initialize predictor
predictor = EmotionPredictor(model_path='./models/distilbert-goemotions-mental')

if predictor.model is None:
    print("❌ Model failed to load!")
    exit(1)

print("✅ Model loaded successfully!")
print()

# Test predictions
for i, text in enumerate(test_texts, 1):
    print(f"Test {i}: \"{text}\"")
    print("-" * 80)
    
    result = predictor.predict_emotions(text)
    
    if 'error' in result:
        print(f"❌ Error: {result['error']}")
    else:
        if result:
            print("Detected Emotions:")
            for emotion, prob in list(result.items())[:3]:
                print(f"  {emotion}: {prob*100:.1f}%")
        else:
            print("  No emotions detected above threshold")
        print()

print("=" * 80)
print("✅ MODEL TEST COMPLETE")
print("=" * 80)
