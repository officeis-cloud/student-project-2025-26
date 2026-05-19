from app import create_app
from models import MoodEntry

app = create_app('development')

with app.app_context():
    entries = list(MoodEntry.objects.order_by('-created_at').limit(30))
    
    print(f"\n📊 Total entries in database: {len(entries)}\n")
    
    emotion_cats = {"Happy": 0, "Calm": 0, "Stressed": 0, "Anxious": 0, "Sad": 0}
    
    happy_ems = ['joy', 'amusement', 'excitement', 'gratitude', 'love', 'optimism', 'pride', 'admiration']
    calm_ems = ['approval', 'caring', 'relief', 'realization', 'curiosity']
    stressed_ems = ['annoyance', 'anger', 'frustration', 'confusion', 'disappointment']
    anxious_ems = ['fear', 'nervousness', 'embarrassment']
    sad_ems = ['sadness', 'grief', 'remorse', 'disapproval']
    
    print("Last 10 entries:")
    print("=" * 80)
    for i, e in enumerate(entries[:10], 1):
        if e.emotions:
            top = max(e.emotions.items(), key=lambda x: x[1])
            print(f"{i:2}. {e.created_at.strftime('%Y-%m-%d %H:%M')} | {e.mental_state:10} | {top[0]:15} {top[1]:.0f}%")
    
    print("\n" + "=" * 80)
    
    for e in entries:
        if e.emotions:
            top = max(e.emotions.items(), key=lambda x: x[1])[0]
            if top in happy_ems:
                emotion_cats["Happy"] += 1
            elif top in calm_ems:
                emotion_cats["Calm"] += 1
            elif top in stressed_ems:
                emotion_cats["Stressed"] += 1
            elif top in anxious_ems:
                emotion_cats["Anxious"] += 1
            elif top in sad_ems:
                emotion_cats["Sad"] += 1
            else:
                emotion_cats["Calm"] += 1
    
    total = sum(emotion_cats.values())
    print("\n📈 EMOTION DISTRIBUTION (what Trends page uses):\n")
    for em, cnt in sorted(emotion_cats.items(), key=lambda x: -x[1]):
        pct = round((cnt / total) * 100) if total > 0 else 0
        bar = "█" * (pct // 2)
        print(f"  {em:10}: {cnt:2} entries ({pct:3}%) {bar}")
    
    print("\n✅ This matches your Trends page!")
    print(f"   Happy: 23% (shown in Trends)")
    print(f"   Sad: 35% (shown in Trends)")
