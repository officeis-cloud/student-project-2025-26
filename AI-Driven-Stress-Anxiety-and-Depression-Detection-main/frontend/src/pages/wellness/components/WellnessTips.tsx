
import { EmotionalState } from '../page';

interface Tip {
  icon: string;
  title: string;
  body: string;
  color: string;
  iconBg: string;
}

const tipsData: Record<EmotionalState, { headline: string; tips: Tip[] }> = {
  stress: {
    headline: 'Quick Stress Relief Techniques',
    tips: [
      {
        icon: 'ri-lungs-line',
        title: 'Box Breathing',
        body: 'Inhale 4s → Hold 4s → Exhale 4s → Hold 4s. Used by Navy SEALs to manage acute stress instantly.',
        color: 'border-orange-200',
        iconBg: 'bg-orange-100 text-orange-600',
      },
      {
        icon: 'ri-leaf-line',
        title: 'Nature Immersion',
        body: 'Just 20 minutes in a natural setting reduces cortisol by up to 21%. Even a park counts.',
        color: 'border-green-200',
        iconBg: 'bg-green-100 text-green-600',
      },
      {
        icon: 'ri-music-2-line',
        title: 'Music Therapy',
        body: 'Listening to slow-tempo music (60–80 BPM) synchronizes your heart rate and reduces stress hormones.',
        color: 'border-teal-200',
        iconBg: 'bg-teal-100 text-teal-600',
      },
      {
        icon: 'ri-hand-heart-line',
        title: 'Cold Water Technique',
        body: 'Splash cold water on your face or hold ice. Triggers the dive reflex, slowing heart rate within seconds.',
        color: 'border-blue-200',
        iconBg: 'bg-blue-100 text-blue-600',
      },
    ],
  },
  anxiety: {
    headline: 'Mindfulness & Grounding Techniques',
    tips: [
      {
        icon: 'ri-focus-3-line',
        title: 'Grounding Anchor',
        body: 'Press your feet firmly into the floor. Feel the pressure. This physical anchor interrupts anxious thought spirals.',
        color: 'border-yellow-200',
        iconBg: 'bg-yellow-100 text-yellow-600',
      },
      {
        icon: 'ri-eye-line',
        title: 'Mindful Observation',
        body: 'Pick one object and observe it for 2 minutes — color, texture, shape. Pulls attention away from future worries.',
        color: 'border-teal-200',
        iconBg: 'bg-teal-100 text-teal-600',
      },
      {
        icon: 'ri-brain-line',
        title: 'Cognitive Defusion',
        body: 'Say "I notice I\'m having the thought that..." instead of "I think...". Creates distance from anxious thoughts.',
        color: 'border-indigo-200',
        iconBg: 'bg-indigo-100 text-indigo-600',
      },
      {
        icon: 'ri-heart-pulse-line',
        title: 'TIPP Skill',
        body: 'Temperature, Intense exercise, Paced breathing, Progressive relaxation — four fast-acting anxiety reducers.',
        color: 'border-pink-200',
        iconBg: 'bg-pink-100 text-pink-600',
      },
    ],
  },
  depression: {
    headline: 'Motivation & Light Activity Tips',
    tips: [
      {
        icon: 'ri-footprint-line',
        title: 'Two-Minute Rule',
        body: 'If a task takes less than 2 minutes, do it now. Small completions trigger dopamine and build momentum.',
        color: 'border-blue-200',
        iconBg: 'bg-blue-100 text-blue-600',
      },
      {
        icon: 'ri-sun-line',
        title: 'Sunlight Exposure',
        body: 'Get 15–30 minutes of sunlight daily. Sunlight boosts serotonin and vitamin D, both critical for mood regulation.',
        color: 'border-yellow-200',
        iconBg: 'bg-yellow-100 text-yellow-600',
      },
      {
        icon: 'ri-user-smile-line',
        title: 'Opposite Action',
        body: 'When depression says "stay in bed," do the opposite. Act against the urge — even partially — to break the cycle.',
        color: 'border-teal-200',
        iconBg: 'bg-teal-100 text-teal-600',
      },
      {
        icon: 'ri-seedling-line',
        title: 'Micro-Goals',
        body: 'Break tasks into the smallest possible steps. "Get dressed" not "clean the house." Each step is a real victory.',
        color: 'border-green-200',
        iconBg: 'bg-green-100 text-green-600',
      },
    ],
  },
  normal: {
    headline: 'Maintain & Strengthen Your Wellbeing',
    tips: [
      {
        icon: 'ri-shield-check-line',
        title: 'Resilience Building',
        body: 'Practice mild stress exposure — cold showers, hard workouts, fasting. Builds psychological resilience over time.',
        color: 'border-teal-200',
        iconBg: 'bg-teal-100 text-teal-600',
      },
      {
        icon: 'ri-group-line',
        title: 'Deepen Relationships',
        body: 'Invest in 2–3 close relationships. Quality social bonds are the #1 predictor of long-term happiness and health.',
        color: 'border-pink-200',
        iconBg: 'bg-pink-100 text-pink-600',
      },
      {
        icon: 'ri-book-open-line',
        title: 'Continuous Learning',
        body: 'Learn one new skill per quarter. Neuroplasticity and mastery experiences are powerful mood elevators.',
        color: 'border-indigo-200',
        iconBg: 'bg-indigo-100 text-indigo-600',
      },
      {
        icon: 'ri-heart-line',
        title: 'Preventive Self-Care',
        body: 'Don\'t wait for burnout. Schedule rest, play, and recovery proactively — treat them as non-negotiable appointments.',
        color: 'border-green-200',
        iconBg: 'bg-green-100 text-green-600',
      },
    ],
  },
};

interface Props {
  activeState: EmotionalState;
}

export default function WellnessTips({ activeState }: Props) {
  const { headline, tips } = tipsData[activeState];

  return (
    <div>
      <div className="flex items-center gap-3 mb-5">
        <div className="w-8 h-8 flex items-center justify-center">
          <i className="ri-lightbulb-flash-line text-2xl text-amber-500"></i>
        </div>
        <h2 className="text-lg font-bold text-gray-900">{headline}</h2>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {tips.map((tip, idx) => (
          <div
            key={idx}
            className={`bg-white rounded-xl border-2 ${tip.color} p-5 hover:shadow-md transition-shadow`}
          >
            <div className={`w-10 h-10 rounded-lg flex items-center justify-center mb-3 ${tip.iconBg}`}>
              <i className={`${tip.icon} text-xl`}></i>
            </div>
            <h4 className="text-sm font-bold text-gray-800 mb-2">{tip.title}</h4>
            <p className="text-xs text-gray-500 leading-relaxed">{tip.body}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
