"""
Test emotion-aware recommendations via API
"""
import requests
import json

# Backend API base URL
BASE_URL = "http://localhost:5000/api"

# Login credentials (use existing test user or adjust as needed)
LOGIN_DATA = {
    "email": "test@example.com",
    "password": "Test123456"
}

def login():
    """Login and get JWT token"""
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=LOGIN_DATA)
        response.raise_for_status()
        return response.json()['access_token']
    except requests.exceptions.RequestException as e:
        print(f"❌ Login failed: {e}")
        print("Creating test account...")
        # Try to register
        register_data = {
            "name": "Test User",
            "email": "test@example.com",
            "password": "Test123456"
        }
        response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
        if response.status_code == 201:
            # Login after registration
            response = requests.post(f"{BASE_URL}/auth/login", json=LOGIN_DATA)
            return response.json()['access_token']
        else:
            print(f"Registration also failed: {response.text}")
            return None

def test_prediction(token, text):
    """Test emotion prediction with text"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(
        f"{BASE_URL}/predict",
        headers=headers,
        json={"text": text}
    )
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ Error: {response.status_code} - {response.text}")
        return None

# Test cases
test_cases = [
    {
        'name': '🔥 Anger/Rage (Stress)',
        'text': "I'm absolutely furious and disgusted! This is completely unacceptable and I'm at my breaking point!",
        'expected_emotions': ['anger', 'disgust', 'annoyance']
    },
    {
        'name': '😢 Sadness/Grief (Depression)',
        'text': "I feel so empty inside. I've been crying all day and can't find joy in anything anymore.",
        'expected_emotions': ['sadness', 'grief', 'disappointment']
    },
    {
        'name': '😰 Fear/Anxiety',
        'text': "I'm terrified and can't stop panicking. My heart is racing and I feel like something terrible is going to happen.",
        'expected_emotions': ['fear', 'nervousness', 'confusion']
    },
    {
        'name': '😊 Positive Emotions',
        'text': "I'm so grateful for all the amazing people in my life! Everything is wonderful and I feel blessed!",
        'expected_emotions': ['gratitude', 'joy', 'love']
    }
]

print("="*100)
print(" " * 30 + "EMOTION-AWARE RECOMMENDATION SYSTEM TEST")
print("="*100)

# Login
print("\n🔐 Logging in...")
token = login()

if not token:
    print("❌ Could not authenticate. Exiting.")
    exit(1)

print("✅ Authenticated successfully!\n")

# Run tests
for test in test_cases:
    print("\n" + "="*100)
    print(f"{test['name']}")
    print("="*100)
    print(f"📝 TEXT: {test['text']}")
    print("\n" + "-"*100)
    
    result = test_prediction(token, test['text'])
    
    if not result:
        print("❌ Prediction failed")
        continue
    
    # Display emotions
    print("\n📊 DETECTED EMOTIONS:")
    if 'emotions' in result:
        sorted_emotions = sorted(result['emotions'].items(), key=lambda x: x[1], reverse=True)[:5]
        for emotion, score in sorted_emotions:
            marker = "🎯" if emotion in test['expected_emotions'] else "  "
            print(f"  {marker} {emotion}: {score*100:.1f}%")
    
    # Display mental state
    print(f"\n🧠 MENTAL STATE: {result.get('mental_state', 'N/A').upper()}")
    print(f"⚠️  SEVERITY: {result.get('severity', 'N/A').upper()} ({result.get('severity_score', 0)*100:.1f}%)")
    
    # Display recommendations
    print("\n💡 EMOTION-AWARE RECOMMENDATIONS:")
    if 'recommendations' in result:
        for i, rec in enumerate(result['recommendations'][:4], 1):
            print(f"\n  {i}. {rec.get('title', 'N/A')}")
            print(f"     ➜ {rec.get('description', 'N/A')}")
            if 'type' in rec:
                print(f"     Type: {rec['type']} | Duration: {rec.get('duration', 'N/A')}")
    
    print()

print("\n" + "="*100)
print(" " * 40 + "✅ TEST COMPLETE")
print("="*100)
