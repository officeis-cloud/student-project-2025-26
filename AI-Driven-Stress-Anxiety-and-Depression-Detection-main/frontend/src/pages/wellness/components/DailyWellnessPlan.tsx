
import { EmotionalState } from '../page';

interface Activity {
  time: string;
  title: string;
  duration: string;
  icon: string;
  description: string;
  tag: string;
  tagColor: string;
}

interface TimeSlot {
  period: 'Morning' | 'Afternoon' | 'Evening';
  icon: string;
  gradient: string;
  textColor: string;
  activities: Activity[];
}

const plans: Record<EmotionalState, TimeSlot[]> = {
  stress: [
    {
      period: 'Morning',
      icon: 'ri-sun-line',
      gradient: 'from-orange-400 to-amber-400',
      textColor: 'text-orange-600',
      activities: [
        {
          time: '7:00 AM',
          title: '4-7-8 Breathing Exercise',
          duration: '10 min',
          icon: 'ri-lungs-line',
          description: 'Inhale for 4 counts, hold for 7, exhale for 8. Repeat 4 cycles to activate your parasympathetic nervous system.',
          tag: 'Breathing',
          tagColor: 'bg-orange-100 text-orange-700',
        },
        {
          time: '7:15 AM',
          title: 'Gentle Morning Stretch',
          duration: '15 min',
          icon: 'ri-body-scan-line',
          description: 'Light full-body stretching to release physical tension stored overnight. Focus on neck, shoulders, and lower back.',
          tag: 'Movement',
          tagColor: 'bg-amber-100 text-amber-700',
        },
        {
          time: '8:00 AM',
          title: 'Mindful Breakfast',
          duration: '20 min',
          icon: 'ri-restaurant-line',
          description: 'Eat slowly without screens. Focus on flavors and textures. Avoid caffeine — opt for herbal tea or warm lemon water.',
          tag: 'Nutrition',
          tagColor: 'bg-green-100 text-green-700',
        },
      ],
    },
    {
      period: 'Afternoon',
      icon: 'ri-sun-foggy-line',
      gradient: 'from-teal-400 to-cyan-400',
      textColor: 'text-teal-600',
      activities: [
        {
          time: '12:30 PM',
          title: 'Progressive Muscle Relaxation',
          duration: '15 min',
          icon: 'ri-mental-health-line',
          description: 'Tense and release each muscle group from toes to head. Proven to reduce cortisol and physical stress symptoms.',
          tag: 'Relaxation',
          tagColor: 'bg-teal-100 text-teal-700',
        },
        {
          time: '1:00 PM',
          title: 'Nature Walk Break',
          duration: '20 min',
          icon: 'ri-walk-line',
          description: 'Step outside for a short walk. Natural light and movement significantly reduce stress hormones within minutes.',
          tag: 'Movement',
          tagColor: 'bg-amber-100 text-amber-700',
        },
        {
          time: '3:00 PM',
          title: 'Stress Journaling',
          duration: '10 min',
          icon: 'ri-edit-line',
          description: 'Write down your top 3 stressors and one small action you can take for each. Externalizing worries reduces mental load.',
          tag: 'Journaling',
          tagColor: 'bg-indigo-100 text-indigo-700',
        },
      ],
    },
    {
      period: 'Evening',
      icon: 'ri-moon-line',
      gradient: 'from-violet-400 to-purple-400',
      textColor: 'text-violet-600',
      activities: [
        {
          time: '7:00 PM',
          title: 'Digital Detox Hour',
          duration: '60 min',
          icon: 'ri-smartphone-line',
          description: 'Put away all screens. Read a physical book, listen to calm music, or do a creative hobby to decompress.',
          tag: 'Lifestyle',
          tagColor: 'bg-violet-100 text-violet-700',
        },
        {
          time: '8:30 PM',
          title: 'Warm Bath or Shower',
          duration: '20 min',
          icon: 'ri-drop-line',
          description: 'Warm water lowers cortisol and signals your body to relax. Add lavender essential oil for enhanced calming effect.',
          tag: 'Self-Care',
          tagColor: 'bg-pink-100 text-pink-700',
        },
        {
          time: '9:30 PM',
          title: 'Sleep Preparation Routine',
          duration: '15 min',
          icon: 'ri-zzz-line',
          description: 'Dim lights, practice box breathing, and set tomorrow\'s top 3 priorities. Aim for 7–9 hours of quality sleep.',
          tag: 'Sleep',
          tagColor: 'bg-blue-100 text-blue-700',
        },
      ],
    },
  ],
  anxiety: [
    {
      period: 'Morning',
      icon: 'ri-sun-line',
      gradient: 'from-yellow-400 to-amber-400',
      textColor: 'text-yellow-600',
      activities: [
        {
          time: '7:00 AM',
          title: '5-4-3-2-1 Grounding Exercise',
          duration: '10 min',
          icon: 'ri-focus-3-line',
          description: 'Name 5 things you see, 4 you can touch, 3 you hear, 2 you smell, 1 you taste. Anchors you to the present moment.',
          tag: 'Grounding',
          tagColor: 'bg-yellow-100 text-yellow-700',
        },
        {
          time: '7:15 AM',
          title: 'Guided Morning Meditation',
          duration: '15 min',
          icon: 'ri-mental-health-line',
          description: 'Use a guided meditation app or audio. Focus on breath awareness to calm the nervous system before the day begins.',
          tag: 'Mindfulness',
          tagColor: 'bg-teal-100 text-teal-700',
        },
        {
          time: '8:00 AM',
          title: 'Anxiety-Reducing Breakfast',
          duration: '20 min',
          icon: 'ri-restaurant-line',
          description: 'Eat foods rich in magnesium and omega-3s: oats, bananas, nuts, or eggs. Avoid sugar spikes that worsen anxiety.',
          tag: 'Nutrition',
          tagColor: 'bg-green-100 text-green-700',
        },
      ],
    },
    {
      period: 'Afternoon',
      icon: 'ri-sun-foggy-line',
      gradient: 'from-teal-400 to-green-400',
      textColor: 'text-teal-600',
      activities: [
        {
          time: '12:00 PM',
          title: 'Body Scan Mindfulness',
          duration: '15 min',
          icon: 'ri-body-scan-line',
          description: 'Slowly scan from head to toe, noticing sensations without judgment. Releases physical anxiety held in the body.',
          tag: 'Mindfulness',
          tagColor: 'bg-teal-100 text-teal-700',
        },
        {
          time: '2:00 PM',
          title: 'Worry Time Technique',
          duration: '15 min',
          icon: 'ri-time-line',
          description: 'Dedicate 15 minutes to write all worries. Outside this window, postpone anxious thoughts. Reduces rumination.',
          tag: 'Cognitive',
          tagColor: 'bg-indigo-100 text-indigo-700',
        },
        {
          time: '3:30 PM',
          title: 'Gentle Yoga Flow',
          duration: '20 min',
          icon: 'ri-heart-pulse-line',
          description: 'Child\'s pose, cat-cow, and forward folds activate the vagus nerve and reduce anxiety symptoms naturally.',
          tag: 'Movement',
          tagColor: 'bg-amber-100 text-amber-700',
        },
      ],
    },
    {
      period: 'Evening',
      icon: 'ri-moon-line',
      gradient: 'from-blue-400 to-indigo-400',
      textColor: 'text-blue-600',
      activities: [
        {
          time: '6:30 PM',
          title: 'Gratitude Journaling',
          duration: '10 min',
          icon: 'ri-heart-line',
          description: 'Write 3 specific things you\'re grateful for today. Shifts focus from threat to safety, reducing anxiety baseline.',
          tag: 'Journaling',
          tagColor: 'bg-pink-100 text-pink-700',
        },
        {
          time: '8:00 PM',
          title: 'Calming Music Therapy',
          duration: '30 min',
          icon: 'ri-music-line',
          description: 'Listen to 432Hz or nature soundscapes. Music at this frequency is clinically shown to reduce anxiety and heart rate.',
          tag: 'Self-Care',
          tagColor: 'bg-violet-100 text-violet-700',
        },
        {
          time: '9:00 PM',
          title: 'Diaphragmatic Breathing',
          duration: '10 min',
          icon: 'ri-lungs-line',
          description: 'Place one hand on chest, one on belly. Breathe so only the belly rises. 6 breaths per minute for optimal calm.',
          tag: 'Breathing',
          tagColor: 'bg-blue-100 text-blue-700',
        },
      ],
    },
  ],
  depression: [
    {
      period: 'Morning',
      icon: 'ri-sun-line',
      gradient: 'from-blue-400 to-sky-400',
      textColor: 'text-blue-600',
      activities: [
        {
          time: '8:00 AM',
          title: 'Light Exposure Therapy',
          duration: '20 min',
          icon: 'ri-sun-line',
          description: 'Sit near a bright window or use a light therapy lamp. Morning light boosts serotonin and regulates your circadian rhythm.',
          tag: 'Light Therapy',
          tagColor: 'bg-yellow-100 text-yellow-700',
        },
        {
          time: '8:30 AM',
          title: 'One Small Achievable Goal',
          duration: '5 min',
          icon: 'ri-checkbox-circle-line',
          description: 'Write one tiny goal for today — make your bed, drink water, send one message. Small wins rebuild motivation.',
          tag: 'Motivation',
          tagColor: 'bg-teal-100 text-teal-700',
        },
        {
          time: '9:00 AM',
          title: 'Short Walk Outside',
          duration: '15 min',
          icon: 'ri-walk-line',
          description: 'Even a 15-minute walk increases endorphins and dopamine. Don\'t aim for intensity — just movement and fresh air.',
          tag: 'Movement',
          tagColor: 'bg-green-100 text-green-700',
        },
      ],
    },
    {
      period: 'Afternoon',
      icon: 'ri-sun-foggy-line',
      gradient: 'from-sky-400 to-teal-400',
      textColor: 'text-sky-600',
      activities: [
        {
          time: '1:00 PM',
          title: 'Social Connection Check-in',
          duration: '15 min',
          icon: 'ri-user-heart-line',
          description: 'Send a message or call someone you trust. Social connection is one of the most powerful antidepressants available.',
          tag: 'Social',
          tagColor: 'bg-pink-100 text-pink-700',
        },
        {
          time: '2:30 PM',
          title: 'Creative Expression',
          duration: '30 min',
          icon: 'ri-palette-line',
          description: 'Draw, color, write poetry, or play music. Creative activities activate reward pathways and provide emotional release.',
          tag: 'Creative',
          tagColor: 'bg-violet-100 text-violet-700',
        },
        {
          time: '4:00 PM',
          title: 'Behavioral Activation',
          duration: '20 min',
          icon: 'ri-run-line',
          description: 'Do one activity you used to enjoy, even if you don\'t feel like it. Action precedes motivation — not the other way around.',
          tag: 'Activation',
          tagColor: 'bg-amber-100 text-amber-700',
        },
      ],
    },
    {
      period: 'Evening',
      icon: 'ri-moon-line',
      gradient: 'from-indigo-400 to-blue-400',
      textColor: 'text-indigo-600',
      activities: [
        {
          time: '6:00 PM',
          title: 'Nourishing Meal Preparation',
          duration: '30 min',
          icon: 'ri-restaurant-line',
          description: 'Cook a simple, nutritious meal. The act of preparing food for yourself is a powerful form of self-compassion.',
          tag: 'Nutrition',
          tagColor: 'bg-green-100 text-green-700',
        },
        {
          time: '8:00 PM',
          title: 'Self-Compassion Journaling',
          duration: '15 min',
          icon: 'ri-edit-line',
          description: 'Write as if comforting a dear friend. Acknowledge your pain without judgment. Self-compassion reduces depressive symptoms.',
          tag: 'Journaling',
          tagColor: 'bg-blue-100 text-blue-700',
        },
        {
          time: '9:30 PM',
          title: 'Consistent Sleep Schedule',
          duration: '8 hrs',
          icon: 'ri-zzz-line',
          description: 'Sleep at the same time every night. Irregular sleep worsens depression. Avoid screens 1 hour before bed.',
          tag: 'Sleep',
          tagColor: 'bg-indigo-100 text-indigo-700',
        },
      ],
    },
  ],
  normal: [
    {
      period: 'Morning',
      icon: 'ri-sun-line',
      gradient: 'from-teal-400 to-green-400',
      textColor: 'text-teal-600',
      activities: [
        {
          time: '6:30 AM',
          title: 'Morning Mindfulness',
          duration: '10 min',
          icon: 'ri-mental-health-line',
          description: 'Start with 10 minutes of mindful breathing or meditation to set a positive, focused tone for the day ahead.',
          tag: 'Mindfulness',
          tagColor: 'bg-teal-100 text-teal-700',
        },
        {
          time: '7:00 AM',
          title: 'Exercise Routine',
          duration: '30 min',
          icon: 'ri-run-line',
          description: 'Engage in moderate exercise — jogging, cycling, or yoga. Maintains serotonin and dopamine at healthy levels.',
          tag: 'Movement',
          tagColor: 'bg-amber-100 text-amber-700',
        },
        {
          time: '8:00 AM',
          title: 'Balanced Breakfast',
          duration: '20 min',
          icon: 'ri-restaurant-line',
          description: 'Fuel your day with protein, complex carbs, and healthy fats. Good nutrition sustains emotional stability.',
          tag: 'Nutrition',
          tagColor: 'bg-green-100 text-green-700',
        },
      ],
    },
    {
      period: 'Afternoon',
      icon: 'ri-sun-foggy-line',
      gradient: 'from-cyan-400 to-teal-400',
      textColor: 'text-cyan-600',
      activities: [
        {
          time: '12:00 PM',
          title: 'Mindful Lunch Break',
          duration: '30 min',
          icon: 'ri-leaf-line',
          description: 'Step away from work. Eat mindfully, take a short walk, or chat with a friend. Protects against afternoon burnout.',
          tag: 'Balance',
          tagColor: 'bg-teal-100 text-teal-700',
        },
        {
          time: '3:00 PM',
          title: 'Learning & Growth',
          duration: '20 min',
          icon: 'ri-book-open-line',
          description: 'Read an article, listen to a podcast, or learn something new. Intellectual stimulation boosts mood and confidence.',
          tag: 'Growth',
          tagColor: 'bg-indigo-100 text-indigo-700',
        },
        {
          time: '4:30 PM',
          title: 'Acts of Kindness',
          duration: '10 min',
          icon: 'ri-heart-line',
          description: 'Do one small kind act — compliment someone, help a colleague, or volunteer. Prosocial behavior elevates wellbeing.',
          tag: 'Social',
          tagColor: 'bg-pink-100 text-pink-700',
        },
      ],
    },
    {
      period: 'Evening',
      icon: 'ri-moon-line',
      gradient: 'from-green-400 to-teal-400',
      textColor: 'text-green-600',
      activities: [
        {
          time: '6:30 PM',
          title: 'Hobby Time',
          duration: '45 min',
          icon: 'ri-palette-line',
          description: 'Dedicate time to a hobby you love. Hobbies provide flow states that are deeply restorative for mental health.',
          tag: 'Joy',
          tagColor: 'bg-yellow-100 text-yellow-700',
        },
        {
          time: '8:00 PM',
          title: 'Gratitude Reflection',
          duration: '10 min',
          icon: 'ri-star-line',
          description: 'Write 3 wins from today, no matter how small. Gratitude practice strengthens neural pathways for positivity.',
          tag: 'Journaling',
          tagColor: 'bg-violet-100 text-violet-700',
        },
        {
          time: '9:30 PM',
          title: 'Wind-Down Routine',
          duration: '30 min',
          icon: 'ri-zzz-line',
          description: 'Dim lights, read, or do light stretching. A consistent wind-down routine improves sleep quality and next-day mood.',
          tag: 'Sleep',
          tagColor: 'bg-blue-100 text-blue-700',
        },
      ],
    },
  ],
};

const periodConfig = {
  Morning: { bg: 'bg-amber-50', border: 'border-amber-100', badge: 'bg-amber-100 text-amber-700' },
  Afternoon: { bg: 'bg-teal-50', border: 'border-teal-100', badge: 'bg-teal-100 text-teal-700' },
  Evening: { bg: 'bg-indigo-50', border: 'border-indigo-100', badge: 'bg-indigo-100 text-indigo-700' },
};

interface Props {
  activeState: EmotionalState;
}

export default function DailyWellnessPlan({ activeState }: Props) {
  const plan = plans[activeState];

  const stateLabels: Record<EmotionalState, string> = {
    stress: 'Stress Relief',
    anxiety: 'Anxiety Management',
    depression: 'Depression Support',
    normal: 'Wellness Maintenance',
  };

  return (
    <div>
      <div className="flex items-center gap-3 mb-6">
        <div className="w-8 h-8 flex items-center justify-center">
          <i className="ri-calendar-2-line text-2xl text-teal-600"></i>
        </div>
        <div>
          <h2 className="text-lg font-bold text-gray-900">Daily Wellness Plan</h2>
          <p className="text-sm text-gray-500">Optimized for: <span className="font-semibold text-teal-600">{stateLabels[activeState]}</span></p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {plan.map((slot) => {
          const cfg = periodConfig[slot.period];
          return (
            <div key={slot.period} className={`rounded-xl border ${cfg.border} ${cfg.bg} overflow-hidden`}>
              {/* Period Header */}
              <div className={`bg-gradient-to-r ${slot.gradient} p-4 flex items-center gap-3`}>
                <div className="w-9 h-9 bg-white/25 rounded-lg flex items-center justify-center">
                  <i className={`${slot.icon} text-white text-xl`}></i>
                </div>
                <div>
                  <h3 className="text-white font-bold text-base">{slot.period}</h3>
                  <p className="text-white/80 text-xs">{slot.activities.length} activities planned</p>
                </div>
              </div>

              {/* Activities */}
              <div className="p-4 space-y-4">
                {slot.activities.map((activity, idx) => (
                  <div key={idx} className="bg-white rounded-lg p-4 shadow-sm border border-white/80">
                    <div className="flex items-start gap-3">
                      <div className={`w-9 h-9 rounded-lg flex items-center justify-center flex-shrink-0 ${cfg.badge}`}>
                        <i className={`${activity.icon} text-lg`}></i>
                      </div>
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center justify-between gap-2 mb-1">
                          <h4 className="text-sm font-semibold text-gray-800 leading-tight">{activity.title}</h4>
                          <span className="text-xs text-gray-400 whitespace-nowrap flex-shrink-0">{activity.time}</span>
                        </div>
                        <p className="text-xs text-gray-500 leading-relaxed mb-2">{activity.description}</p>
                        <div className="flex items-center gap-2">
                          <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${activity.tagColor}`}>
                            {activity.tag}
                          </span>
                          <span className="flex items-center gap-1 text-xs text-gray-400">
                            <i className="ri-time-line"></i>
                            {activity.duration}
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
