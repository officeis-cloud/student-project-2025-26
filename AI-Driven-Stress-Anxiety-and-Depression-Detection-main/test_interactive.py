import requests
import json

print("=" * 80)
print("AI MENTAL HEALTH - EMOTION PREDICTION TEST")
print("=" * 80)
print()

# Get authentication token
print("🔐 Logging in...")
login_response = requests.post(
    "http://localhost:5000/api/auth/login",
    json={"email": "test@example.com", "password": "Test123!@#"},
    headers={"Content-Type": "application/json"}
)

if login_response.status_code != 200:
    print("❌ Login failed. Make sure you've registered first.")
    print("   Run: python test_system.py")
    exit(1)

token = login_response.json()['access_token']
print("✅ Logged in successfully!")
print()

# Interactive testing loop
while True:
    print("-" * 80)
    print("Enter your text (or 'quit' to exit):")
    print("-" * 80)
    user_text = input("> ").strip()
    
    if user_text.lower() in ['quit', 'exit', 'q']:
        print("\n👋 Goodbye!")
        break
    
    if len(user_text) < 10:
        print("⚠️  Please enter at least 10 characters.\n")
        continue
    
    # Make prediction request
    print("\n🔍 Analyzing your text...")
    response = requests.post(
        "http://localhost:5000/api/predict/",
        json={"text": user_text},
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
    )
    
    if response.status_code == 200:
        result = response.json()
        
        print("\n" + "=" * 80)
        print("📊 EMOTION ANALYSIS RESULTS")
        print("=" * 80)
        
        # Display emotions
        print("\n🎭 Detected Emotions:")
        emotions = result['emotions']
        sorted_emotions = sorted(emotions.items(), key=lambda x: x[1], reverse=True)
        
        for i, (emotion, score) in enumerate(sorted_emotions[:8], 1):
            percentage = score * 100
            bar_length = int(percentage / 2)
            bar = "█" * bar_length + "░" * (50 - bar_length)
            print(f"  {i}. {emotion:15s} {bar} {percentage:5.1f}%")
        
        # Display mental state
        print(f"\n🧠 Mental State: {result['mental_state'].upper()}")
        print(f"⚠️  Severity: {result['severity'].upper()}")
        print(f"📈 Severity Score: {result['severity_score']:.2%}")
        
        # Display state scores
        if 'state_scores' in result and result['state_scores']:
            print(f"\n📋 Mental State Analysis:")
            for state, score in sorted(result['state_scores'].items(), key=lambda x: x[1], reverse=True):
                print(f"   - {state.capitalize():15s}: {score:.2%}")
        
        # Display recommendations
        if result['recommendations']:
            print(f"\n💡 Recommendations ({len(result['recommendations'])} tips):")
            for i, rec in enumerate(result['recommendations'][:3], 1):
                print(f"   {i}. {rec['title']}")
                print(f"      {rec['description'][:80]}...")
        
        print("\n" + "=" * 80)
        print()
    else:
        print(f"❌ Error: {response.status_code}")
        print(f"   {response.text}")
        print()
