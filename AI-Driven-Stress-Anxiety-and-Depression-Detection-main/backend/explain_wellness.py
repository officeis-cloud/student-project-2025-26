from app import create_app
from models import MoodEntry

app = create_app('development')

with app.app_context():
    entries = list(MoodEntry.objects.order_by('-created_at').limit(10))
    
    print("\n💡 HOW 57% WELLNESS IS CALCULATED\n")
    print("=" * 60)
    
    print("\nYour Last 10 Entries:")
    print(f"{'State':<12} {'Severity':<10} {'Wellness':<10}")
    print("-" * 60)
    
    total_wellness = 0
    for entry in entries:
        wellness = 100 - entry.severity_score
        total_wellness += wellness
        print(f"{entry.mental_state:<12} {entry.severity_score:>3.0f}%       {wellness:>3.0f}%")
    
    avg = round(total_wellness / len(entries))
    
    print("-" * 60)
    print(f"Average: {total_wellness:.0f} / {len(entries)} entries = {avg}%")
    print("=" * 60)
    
    print("\n✅ REAL DATA from your journal entries!")
    print("📊 Formula: Wellness = 100 - Severity\n")
