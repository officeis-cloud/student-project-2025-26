
import { AnalysisResult } from '../page';

interface Props {
  result: AnalysisResult;
}

const severityConfig: Record<string, { color: string; bg: string; icon: string }> = {
  Normal: { color: 'text-emerald-700', bg: 'bg-emerald-50 border-emerald-200', icon: 'ri-checkbox-circle-line' },
  Mild: { color: 'text-yellow-700', bg: 'bg-yellow-50 border-yellow-200', icon: 'ri-alert-line' },
  Moderate: { color: 'text-orange-700', bg: 'bg-orange-50 border-orange-200', icon: 'ri-error-warning-line' },
  Severe: { color: 'text-red-700', bg: 'bg-red-50 border-red-200', icon: 'ri-alarm-warning-line' },
};

const stateConfig: Record<string, { gradient: string; icon: string }> = {
  Normal: { gradient: 'from-emerald-500 to-teal-500', icon: 'ri-emotion-happy-line' },
  Stress: { gradient: 'from-orange-500 to-amber-500', icon: 'ri-mental-health-line' },
  Anxiety: { gradient: 'from-violet-500 to-purple-500', icon: 'ri-heart-pulse-line' },
  Depression: { gradient: 'from-blue-600 to-indigo-600', icon: 'ri-cloud-line' },
};

export default function EmotionResultCards({ result }: Props) {
  const sev = severityConfig[result.severity] ?? severityConfig['Mild'];
  const state = stateConfig[result.mentalState] ?? stateConfig['Normal'];

  return (
    <div className="space-y-5">
      {/* Top summary row */}
      <div className="grid grid-cols-3 gap-4">
        {/* Mental State */}
        <div className={`bg-gradient-to-br ${state.gradient} rounded-xl p-5 text-white`}>
          <div className="flex items-center justify-between mb-3">
            <span className="text-xs font-semibold uppercase tracking-wider opacity-80">Mental State</span>
            <div className="w-8 h-8 flex items-center justify-center bg-white/20 rounded-lg">
              <i className={`${state.icon} text-lg`}></i>
            </div>
          </div>
          <p className="text-2xl font-bold">{result.mentalState}</p>
          <p className="text-xs opacity-75 mt-1">Classified by AI model</p>
        </div>

        {/* Severity */}
        <div className={`rounded-xl p-5 border ${sev.bg}`}>
          <div className="flex items-center justify-between mb-3">
            <span className="text-xs font-semibold uppercase tracking-wider text-gray-500">Severity Level</span>
            <div className={`w-8 h-8 flex items-center justify-center rounded-lg bg-white`}>
              <i className={`${sev.icon} text-lg ${sev.color}`}></i>
            </div>
          </div>
          <p className={`text-2xl font-bold ${sev.color}`}>{result.severity}</p>
          <p className="text-xs text-gray-500 mt-1">Emotional intensity rating</p>
        </div>

        {/* Confidence */}
        <div className="bg-white rounded-xl p-5 border border-gray-200">
          <div className="flex items-center justify-between mb-3">
            <span className="text-xs font-semibold uppercase tracking-wider text-gray-500">AI Confidence</span>
            <div className="w-8 h-8 flex items-center justify-center bg-teal-50 rounded-lg">
              <i className="ri-bar-chart-2-line text-lg text-teal-600"></i>
            </div>
          </div>
          <p className="text-2xl font-bold text-gray-800">{result.confidence}%</p>
          <div className="mt-2 h-1.5 bg-gray-100 rounded-full overflow-hidden">
            <div
              className="h-full bg-teal-500 rounded-full transition-all duration-700"
              style={{ width: `${result.confidence}%` }}
            />
          </div>
        </div>
      </div>

      {/* Detected Emotions */}
      <div className="bg-white rounded-xl border border-gray-200 p-6">
        <h3 className="text-sm font-bold text-gray-700 mb-4 flex items-center gap-2">
          <i className="ri-emotion-line text-teal-500"></i>
          Detected Emotions
        </h3>
        <div className="space-y-3">
          {result.emotions.map((e) => (
            <div key={e.emotion}>
              <div className="flex justify-between items-center mb-1">
                <span className="text-sm font-medium text-gray-700">{e.emotion}</span>
                <span className="text-sm font-bold" style={{ color: e.color }}>{e.probability}%</span>
              </div>
              <div className="h-2.5 bg-gray-100 rounded-full overflow-hidden">
                <div
                  className="h-full rounded-full transition-all duration-700"
                  style={{ width: `${e.probability}%`, backgroundColor: e.color }}
                />
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
