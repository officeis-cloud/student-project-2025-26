"""Check if detected_emotions are populated in database"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from app import create_app
from models import MoodEntry

app = create_app()

with app.app_context():
    entries = MoodEntry.objects().order_by('-created_at').limit(10)
    
    print(f"\n📊 Last 10 Journal Entries - Emotion Detection:")
    print("=" * 80)
    
    for i, entry in enumerate(entries, 1):
        text_preview = entry.text[:40] + "..." if len(entry.text) > 40 else entry.text
        print(f"\n{i}. Entry: {text_preview}")
        print(f"   Mental State: {entry.mental_state}")
        print(f"   Severity: {entry.severity_score * 100:.1f}%")
        print(f"   Created: {entry.created_at.strftime('%Y-%m-%d %H:%M')}")
        
        # Check detected_emotions field
        if hasattr(entry, 'detected_emotions'):
            emotions = entry.detected_emotions
            if emotions and len(emotions) > 0:
                print(f"   ✅ Detected Emotions ({len(emotions)}):")
                for j, emotion in enumerate(emotions[:3], 1):
                    if isinstance(emotion, dict):
                        em_name = emotion.get('emotion', 'Unknown')
                        em_score = emotion.get('score', 0)
                        print(f"      {j}. {em_name}: {em_score * 100:.1f}%")
                    else:
                        print(f"      {j}. {emotion}")
            else:
                print(f"   ❌ No detected_emotions")
        else:
            print(f"   ❌ detected_emotions field missing")
    
    print("\n" + "=" * 80)
    print("✅ Check complete!")
