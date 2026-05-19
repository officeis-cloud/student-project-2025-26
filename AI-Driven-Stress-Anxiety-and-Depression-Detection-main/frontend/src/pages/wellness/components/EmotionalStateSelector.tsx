
import { EmotionalState } from '../page';

interface Props {
  activeState: EmotionalState;
  onSelect: (state: EmotionalState) => void;
}

const states: { id: EmotionalState; label: string; icon: string; color: string; activeColor: string; desc: string }[] = [
  {
    id: 'stress',
    label: 'Stress',
    icon: 'ri-fire-line',
    color: 'border-orange-200 text-orange-700 bg-orange-50 hover:bg-orange-100',
    activeColor: 'border-orange-500 bg-orange-500 text-white shadow-lg shadow-orange-200',
    desc: 'Feeling overwhelmed or under pressure',
  },
  {
    id: 'anxiety',
    label: 'Anxiety',
    icon: 'ri-pulse-line',
    color: 'border-yellow-200 text-yellow-700 bg-yellow-50 hover:bg-yellow-100',
    activeColor: 'border-yellow-500 bg-yellow-500 text-white shadow-lg shadow-yellow-200',
    desc: 'Feeling worried or restless',
  },
  {
    id: 'depression',
    label: 'Depression',
    icon: 'ri-emotion-sad-line',
    color: 'border-blue-200 text-blue-700 bg-blue-50 hover:bg-blue-100',
    activeColor: 'border-blue-500 bg-blue-500 text-white shadow-lg shadow-blue-200',
    desc: 'Feeling low, hopeless, or unmotivated',
  },
  {
    id: 'normal',
    label: 'Feeling Good',
    icon: 'ri-emotion-happy-line',
    color: 'border-teal-200 text-teal-700 bg-teal-50 hover:bg-teal-100',
    activeColor: 'border-teal-500 bg-teal-500 text-white shadow-lg shadow-teal-200',
    desc: 'Balanced and emotionally stable',
  },
];

export default function EmotionalStateSelector({ activeState, onSelect }: Props) {
  return (
    <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-6">
      <p className="text-sm font-semibold text-gray-700 mb-4">
        Select your current emotional state to get tailored recommendations:
      </p>
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {states.map((s) => {
          const isActive = activeState === s.id;
          return (
            <button
              key={s.id}
              onClick={() => onSelect(s.id)}
              className={`flex flex-col items-center gap-3 p-5 rounded-xl border-2 transition-all cursor-pointer whitespace-nowrap ${
                isActive ? s.activeColor : s.color
              }`}
            >
              <div className="w-10 h-10 flex items-center justify-center">
                <i className={`${s.icon} text-2xl`}></i>
              </div>
              <span className="text-sm font-bold">{s.label}</span>
              <span className={`text-xs text-center leading-snug ${isActive ? 'text-white/80' : 'text-gray-500'}`}>
                {s.desc}
              </span>
            </button>
          );
        })}
      </div>
    </div>
  );
}
