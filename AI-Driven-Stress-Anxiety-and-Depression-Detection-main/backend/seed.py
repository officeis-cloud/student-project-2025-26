"""
Database seeding script
Run this to populate initial data
"""
from app import create_app, db
from models import WellnessTip

def seed_wellness_tips():
    """Seed wellness tips database"""
    
    tips = [
        # Depression Tips
        {
            'category': 'depression',
            'title': 'Morning Sunlight Therapy',
            'description': 'Exposure to natural sunlight helps regulate mood and increases serotonin production. Spend 15-20 minutes outdoors in the morning.',
            'type': 'lifestyle',
            'duration': '15-20 minutes'
        },
        {
            'category': 'depression',
            'title': 'Gratitude Practice',
            'description': 'Write down three things you are grateful for each day. This simple practice can shift focus to positive aspects of life.',
            'type': 'journaling',
            'duration': '5 minutes'
        },
        {
            'category': 'depression',
            'title': 'Social Connection',
            'description': 'Reach out to friends or family, even if it feels difficult. Social support is crucial for recovery.',
            'type': 'social',
            'duration': '15-30 minutes'
        },
        
        # Anxiety Tips
        {
            'category': 'anxiety',
            'title': '4-7-8 Breathing Technique',
            'description': 'Inhale for 4 counts, hold for 7, exhale for 8. This activates the parasympathetic nervous system, reducing anxiety.',
            'type': 'breathing',
            'duration': '5 minutes'
        },
        {
            'category': 'anxiety',
            'title': 'Progressive Muscle Relaxation',
            'description': 'Systematically tense and relax each muscle group from toes to head. Helps release physical tension associated with anxiety.',
            'type': 'relaxation',
            'duration': '10-15 minutes'
        },
        {
            'category': 'anxiety',
            'title': 'Limit Caffeine Intake',
            'description': 'Caffeine can trigger or worsen anxiety symptoms. Try reducing or eliminating coffee and energy drinks.',
            'type': 'lifestyle',
            'duration': 'Daily'
        },
        
        # Stress Tips
        {
            'category': 'stress',
            'title': 'Time Blocking',
            'description': 'Organize your day into focused time blocks. This reduces overwhelm and increases productivity.',
            'type': 'productivity',
            'duration': '15 minutes planning'
        },
        {
            'category': 'stress',
            'title': 'Physical Exercise',
            'description': 'Exercise releases endorphins and reduces stress hormones. Even a 20-minute walk can make a difference.',
            'type': 'exercise',
            'duration': '20-30 minutes'
        },
        {
            'category': 'stress',
            'title': 'Digital Detox',
            'description': 'Take regular breaks from screens and social media. Constant connectivity increases stress levels.',
            'type': 'lifestyle',
            'duration': 'Evening hours'
        },
        
        # General Wellness
        {
            'category': 'general',
            'title': 'Mindfulness Meditation',
            'description': 'Practice present-moment awareness through meditation. Even 5 minutes daily can improve mental wellbeing.',
            'type': 'meditation',
            'duration': '5-20 minutes'
        },
        {
            'category': 'general',
            'title': 'Sleep Hygiene',
            'description': 'Maintain consistent sleep schedule, avoid screens before bed, and create a relaxing bedtime routine.',
            'type': 'lifestyle',
            'duration': 'Daily'
        },
        {
            'category': 'general',
            'title': 'Balanced Nutrition',
            'description': 'Eat regular meals with whole foods, fruits, and vegetables. Nutrition significantly impacts mood and energy.',
            'type': 'nutrition',
            'duration': 'Daily'
        },
        {
            'category': 'general',
            'title': 'Creative Expression',
            'description': 'Engage in creative activities like art, music, or writing. Creative expression is therapeutic and reduces stress.',
            'type': 'hobby',
            'duration': '30 minutes'
        },
        {
            'category': 'general',
            'title': 'Nature Immersion',
            'description': 'Spend time in natural environments. Nature exposure reduces stress and improves overall wellbeing.',
            'type': 'lifestyle',
            'duration': '30+ minutes'
        }
    ]
    
    print("Seeding wellness tips...")
    
    for tip_data in tips:
        # Check if tip already exists
        existing = WellnessTip.query.filter_by(
            title=tip_data['title']
        ).first()
        
        if not existing:
            tip = WellnessTip(**tip_data)
            db.session.add(tip)
            print(f"  ✅ Added: {tip_data['title']}")
        else:
            print(f"  ⏭️  Skipped (exists): {tip_data['title']}")
    
    db.session.commit()
    print("\n✅ Wellness tips seeded successfully!")


def seed_all():
    """Run all seeding functions"""
    print("Starting database seeding...\n")
    seed_wellness_tips()
    print("\n🎉 All seeding completed!")


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        seed_all()
