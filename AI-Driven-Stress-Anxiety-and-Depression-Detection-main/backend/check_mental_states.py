"""Check actual mental_state values in database"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from app import create_app
from models import MoodEntry

app = create_app()

with app.app_context():
    entries = MoodEntry.objects().order_by('-created_at').limit(20)
    
    print(f"\n📊 Last 20 Journal Entries - Mental States:")
    print("=" * 60)
    
    states_count = {}
    for entry in entries:
        state = entry.mental_state
        states_count[state] = states_count.get(state, 0) + 1
        
        # Show entry details
        text_preview = entry.text[:50] + "..." if len(entry.text) > 50 else entry.text
        print(f"\nMental State: '{state}' (type: {type(state).__name__})")
        print(f"  Severity: {entry.severity_score}%")
        print(f"  Text: {text_preview}")
        print(f"  Date: {entry.created_at.strftime('%Y-%m-%d %H:%M')}")
    
    print("\n" + "=" * 60)
    print("Mental State Value Counts:")
    for state, count in sorted(states_count.items(), key=lambda x: x[1], reverse=True):
        print(f"  '{state}': {count} entries")
    
    print("\n✅ Check complete!")
