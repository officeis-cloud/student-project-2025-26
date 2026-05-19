import requests
import json

print("=" * 80)
print("TESTING AI MENTAL HEALTH SYSTEM")
print("=" * 80)
print()

# Test Backend
print("1. Testing Backend API (http://localhost:5000)...")
try:
    response = requests.get("http://localhost:5000/api/health", timeout=5)
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Backend is RUNNING")
        print(f"   Status: {data.get('status')}")
        print(f"   Model Loaded: {data.get('model_loaded')}")
        print(f"   Database: {data.get('database')}")
    else:
        print(f"   ❌ Backend returned status code: {response.status_code}")
except requests.exceptions.ConnectionError:
    print("   ❌ Backend is NOT running (Connection refused)")
    print("   Make sure to run: python app.py")
except Exception as e:
    print(f"   ❌ Error: {e}")

print()

# Test Frontend
print("2. Testing Frontend (http://localhost:3000)...")
try:
    response = requests.get("http://localhost:3000", timeout=5)
    if response.status_code == 200:
        print("   ✅ Frontend is RUNNING")
        print("   Open in browser: http://localhost:3000")
    else:
        print(f"   ❌ Frontend returned status code: {response.status_code}")
except requests.exceptions.ConnectionError:
    print("   ❌ Frontend is NOT running")
    print("   Make sure to run: npm run dev")
except Exception as e:
    print(f"   ❌ Error: {e}")

print()

# Test Authentication & Emotion Prediction
print("3. Testing User Registration and Authentication...")
try:
    # Register a test user
    register_data = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "Test123!@#"
    }
    
    response = requests.post(
        "http://localhost:5000/api/auth/register",
        json=register_data,
        headers={"Content-Type": "application/json"},
        timeout=10
    )
    
    if response.status_code == 201:
        print("   ✅ User Registration WORKING")
        data = response.json()
        access_token = data.get('access_token')
    elif response.status_code == 400 or response.status_code == 409:
        print("   ℹ️  User already exists, logging in...")
        # Login instead
        response = requests.post(
            "http://localhost:5000/api/auth/login",
            json={"email": register_data["email"], "password": register_data["password"]},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        if response.status_code == 200:
            print("   ✅ Login SUCCESSFUL")
            data = response.json()
            access_token = data.get('access_token')
        else:
            print(f"   ❌ Login failed: {response.status_code}")
            access_token = None
    else:
        print(f"   ❌ Registration failed: {response.status_code}")
        print(f"   Response: {response.text}")
        access_token = None
    
    # Test emotion prediction with token
    if access_token:
        print()
        print("4. Testing Emotion Prediction API (Authenticated)...")
        test_text = "I'm feeling really happy and excited about this project!"
        response = requests.post(
            "http://localhost:5000/api/predict",
            json={"text": test_text},
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}"
            },
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Emotion Detection WORKING")
            print(f"   Test Text: \"{test_text}\"")
            print(f"   Mental State: {data.get('mental_state', 'N/A')}")
            print(f"   Severity: {data.get('severity', 'N/A')}")
            if 'emotions' in data and data['emotions']:
                print("   Detected Emotions:")
                for emotion, prob in list(data['emotions'].items())[:3]:
                    print(f"      - {emotion}: {prob*100:.1f}%")
            if 'recommendations' in data:
                print(f"   Recommendations: {len(data['recommendations'])} tips provided")
        else:
            print(f"   ⚠️  API returned status: {response.status_code}")
            print(f"   Response: {response.text}")
    
except requests.exceptions.ConnectionError:
    print("   ❌ Cannot connect to API")
except Exception as e:
    print(f"   ❌ Error: {e}")

print()
print("=" * 80)
print("TEST COMPLETE")
print("=" * 80)
print()
print("📱 Open your browser to: http://localhost:3000")
print("🔧 API Documentation: http://localhost:5000/api/health")
