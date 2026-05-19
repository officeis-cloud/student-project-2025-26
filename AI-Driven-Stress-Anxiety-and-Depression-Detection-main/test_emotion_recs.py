"""
Test emotion-aware recommendation system
"""
from backend.emotion_predictor import emotion_predictor
from backend.recommendation_engine import RecommendationEngine

# Test phrases
test_cases = [
    {
        'name': 'Anger/Rage (Stress)',
        'text': "I'm absolutely furious and disgusted! This is completely unacceptable and I'm at my breaking point!"
    },
    {
        'name': 'Sadness/Grief (Depression)',
        'text': "I feel so empty inside. I've been crying all day and can't find joy in anything anymore."
    },
    {
        'name': 'Fear/Anxiety',
        'text': "I'm terrified and can't stop panicking. My heart is racing and I feel like something terrible is going to happen."
    },
    {
        'name': 'Mixed Emotions',
        'text': "I'm excited about this new job but absolutely terrified I'll fail and disappoint everyone."
    },
    {
        'name': 'Positive Emotions',
        'text': "I'm so grateful for all the amazing people in my life! Everything is wonderful and I feel blessed!"
    }
]

print("="*80)
print("EMOTION-AWARE RECOMMENDATION SYSTEM TEST")
print("="*80)

for test in test_cases:
    print(f"\n{'='*80}")
    print(f"TEST: {test['name']}")
    print(f"TEXT: {test['text']}")
    print("="*80)
    
    # Get prediction
    prediction = emotion_predictor.classify_mental_state(test['text'])
    
    if 'error' in prediction:
        print(f"\n❌ ERROR: {prediction['error']}")
        continue
    
    # Display detected emotions
    print("\n📊 DETECTED EMOTIONS:")
    if 'emotions' in prediction and prediction['emotions']:
        sorted_emotions = sorted(prediction['emotions'].items(), key=lambda x: x[1], reverse=True)[:5]
        for emotion, score in sorted_emotions:
            print(f"  • {emotion}: {score*100:.1f}%")
    else:
        print("  No emotions detected")
        print(f"  Prediction keys: {list(prediction.keys())}")
    
    # Display mental state
    print(f"\n🧠 MENTAL STATE: {prediction['mental_state'].upper()}")
    print(f"⚠️  SEVERITY: {prediction['severity'].upper()} ({prediction['severity_score']*100:.1f}%)")
    
    # Get OLD recommendations (mental state only)
    old_recs = RecommendationEngine.get_recommendations(
        mental_state=prediction['mental_state'],
        severity=prediction['severity'],
        emotions=None  # No emotions = old system
    )
    
    # Get NEW emotion-aware recommendations
    new_recs = RecommendationEngine.get_recommendations(
        mental_state=prediction['mental_state'],
        severity=prediction['severity'],
        emotions=prediction['emotions']  # With emotions = new system
    )
    
    # Compare
    print(f"\n❌ OLD RECOMMENDATIONS (Mental State Only):")
    for i, rec in enumerate(old_recs[:4], 1):
        print(f"  {i}. {rec['title']}")
        print(f"     {rec['description']}")
    
    print(f"\n✅ NEW EMOTION-AWARE RECOMMENDATIONS:")
    for i, rec in enumerate(new_recs[:4], 1):
        emotion_info = ""
        if 'emotion_cluster' in rec:
            emotion_info = f" [{rec['emotion_cluster']} - {rec['emotion_intensity']}%]"
        print(f"  {i}. {rec['title']}{emotion_info}")
        print(f"     {rec['description']}")
    
    print()

print("\n" + "="*80)
print("TEST COMPLETE")
print("="*80)
