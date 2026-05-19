
import { AnalysisResult } from '../page';

interface Props {
  result: AnalysisResult;
}

const categoryConfig = {
  depression: { label: 'Depression', color: 'text-blue-700', bg: 'bg-blue-50', border: 'border-blue-200', dot: 'bg-blue-500' },
  stress: { label: 'Stress', color: 'text-orange-700', bg: 'bg-orange-50', border: 'border-orange-200', dot: 'bg-orange-500' },
  anxiety: { label: 'Anxiety', color: 'text-violet-700', bg: 'bg-violet-50', border: 'border-violet-200', dot: 'bg-violet-500' },
  fatigue: { label: 'Fatigue', color: 'text-gray-700', bg: 'bg-gray-50', border: 'border-gray-200', dot: 'bg-gray-500' },
};

const severityBadge = {
  high: 'bg-red-100 text-red-700 border border-red-200',
  medium: 'bg-orange-100 text-orange-700 border border-orange-200',
  low: 'bg-teal-100 text-teal-700 border border-teal-200',
};

const severityIcon = {
  high: 'ri-alarm-warning-line',
  medium: 'ri-error-warning-line',
  low: 'ri-information-line',
};

function HighlightedText({ text, triggers }: { text: string; triggers: AnalysisResult['triggers'] }) {
  if (!triggers.length) {
    return <span className="text-gray-700 text-sm leading-relaxed">{text}</span>;
  }

  const sortedTriggers = [...triggers].sort((a, b) => b.word.length - a.word.length);
  const parts: { text: string; trigger?: AnalysisResult['triggers'][0] }[] = [];
  let remaining = text;
  let lastIndex = 0;
  const usedRanges: [number, number][] = [];

  const lowerText = text.toLowerCase();
  const matchPositions: { start: number; end: number; trigger: AnalysisResult['triggers'][0] }[] = [];

  for (const trigger of sortedTriggers) {
    let searchFrom = 0;
    while (true) {
      const idx = lowerText.indexOf(trigger.word.toLowerCase(), searchFrom);
      if (idx === -1) break;
      const end = idx + trigger.word.length;
      const overlaps = usedRanges.some(([s, e]) => idx < e && end > s);
      if (!overlaps) {
        matchPositions.push({ start: idx, end, trigger });
        usedRanges.push([idx, end]);
      }
      searchFrom = idx + 1;
    }
  }

  matchPositions.sort((a, b) => a.start - b.start);

  let cursor = 0;
  for (const match of matchPositions) {
    if (match.start > cursor) {
      parts.push({ text: text.slice(cursor, match.start) });
    }
    parts.push({ text: text.slice(match.start, match.end), trigger: match.trigger });
    cursor = match.end;
  }
  if (cursor < text.length) {
    parts.push({ text: text.slice(cursor) });
  }

  const highlightColors: Record<string, string> = {
    depression: 'bg-blue-100 text-blue-800 border-b-2 border-blue-400',
    stress: 'bg-orange-100 text-orange-800 border-b-2 border-orange-400',
    anxiety: 'bg-violet-100 text-violet-800 border-b-2 border-violet-400',
    fatigue: 'bg-gray-100 text-gray-800 border-b-2 border-gray-400',
  };

  return (
    <span className="text-gray-700 text-sm leading-relaxed">
      {parts.map((part, i) =>
        part.trigger ? (
          <span
            key={i}
            className={`px-0.5 rounded font-semibold cursor-default ${highlightColors[part.trigger.category]}`}
            title={`${part.trigger.indicator} (${part.trigger.confidence}% confidence)`}
          >
            {part.text}
          </span>
        ) : (
          <span key={i}>{part.text}</span>
        )
      )}
    </span>
  );
}

export default function ExplainableInsights({ result }: Props) {
  const { triggers, stressTriggers, originalText } = result;

  const categoryCounts = triggers.reduce<Record<string, number>>((acc, t) => {
    acc[t.category] = (acc[t.category] || 0) + 1;
    return acc;
  }, {});

  return (
    <div className="space-y-5">
      {/* Section Header */}
      <div className="flex items-center gap-3">
        <div className="w-8 h-8 flex items-center justify-center bg-teal-600 rounded-lg">
          <i className="ri-lightbulb-flash-line text-white text-base"></i>
        </div>
        <div>
          <h2 className="text-lg font-bold text-gray-800">Explainable AI Insights</h2>
          <p className="text-xs text-gray-400">Understanding what influenced the AI prediction</p>
        </div>
      </div>

      {/* Keyword Highlight Panel */}
      <div className="bg-white rounded-xl border border-gray-200 p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-sm font-bold text-gray-700 flex items-center gap-2">
            <i className="ri-mark-pen-line text-teal-500"></i>
            Keyword Highlights in Your Text
          </h3>
          <span className="text-xs text-gray-400 bg-gray-50 px-2 py-1 rounded-full border border-gray-200">
            {triggers.length} indicator{triggers.length !== 1 ? 's' : ''} detected
          </span>
        </div>

        {/* Highlighted text block */}
        <div className="bg-gray-50 rounded-lg border border-gray-200 px-5 py-4 mb-5 leading-8">
          {triggers.length > 0 ? (
            <HighlightedText text={originalText} triggers={triggers} />
          ) : (
            <span className="text-gray-700 text-sm leading-relaxed">{originalText}</span>
          )}
        </div>

        {/* Legend */}
        <div className="flex flex-wrap gap-3 mb-5">
          {Object.entries(categoryConfig).map(([key, cfg]) => (
            <div key={key} className="flex items-center gap-1.5">
              <div className={`w-2.5 h-2.5 rounded-full ${cfg.dot}`}></div>
              <span className="text-xs text-gray-500">{cfg.label} indicator</span>
            </div>
          ))}
        </div>

        {/* Keyword cards */}
        {triggers.length > 0 ? (
          <div className="grid grid-cols-1 gap-3">
            {triggers.map((t, i) => {
              const cfg = categoryConfig[t.category];
              return (
                <div
                  key={i}
                  className={`flex items-start gap-4 p-4 rounded-lg border ${cfg.bg} ${cfg.border}`}
                >
                  <div className={`w-8 h-8 flex items-center justify-center rounded-lg bg-white border ${cfg.border} shrink-0`}>
                    <i className={`ri-key-2-line text-sm ${cfg.color}`}></i>
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 flex-wrap">
                      <span className={`font-bold text-sm ${cfg.color}`}>"{t.word}"</span>
                      <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${cfg.bg} ${cfg.color} border ${cfg.border}`}>
                        {cfg.label}
                      </span>
                    </div>
                    <p className="text-xs text-gray-600 mt-1">{t.indicator}</p>
                  </div>
                  <div className="shrink-0 text-right">
                    <div className="text-xs font-bold text-gray-700">{t.confidence}%</div>
                    <div className="text-xs text-gray-400">confidence</div>
                    <div className="mt-1.5 w-16 h-1.5 bg-gray-200 rounded-full overflow-hidden">
                      <div
                        className={`h-full rounded-full ${cfg.dot}`}
                        style={{ width: `${t.confidence}%` }}
                      />
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        ) : (
          <div className="flex items-center gap-3 p-4 bg-emerald-50 border border-emerald-200 rounded-lg">
            <i className="ri-checkbox-circle-line text-emerald-500 text-xl w-6 h-6 flex items-center justify-center"></i>
            <p className="text-sm text-emerald-700">No significant distress keywords detected in your text.</p>
          </div>
        )}
      </div>

      {/* Category Summary */}
      {triggers.length > 0 && (
        <div className="bg-white rounded-xl border border-gray-200 p-6">
          <h3 className="text-sm font-bold text-gray-700 mb-4 flex items-center gap-2">
            <i className="ri-pie-chart-2-line text-teal-500"></i>
            Indicator Category Breakdown
          </h3>
          <div className="grid grid-cols-4 gap-3">
            {Object.entries(categoryConfig).map(([key, cfg]) => {
              const count = categoryCounts[key] || 0;
              return (
                <div key={key} className={`rounded-lg p-4 border text-center ${count > 0 ? `${cfg.bg} ${cfg.border}` : 'bg-gray-50 border-gray-200'}`}>
                  <div className={`text-2xl font-bold ${count > 0 ? cfg.color : 'text-gray-300'}`}>{count}</div>
                  <div className={`text-xs font-medium mt-1 ${count > 0 ? cfg.color : 'text-gray-400'}`}>{cfg.label}</div>
                  <div className="text-xs text-gray-400 mt-0.5">indicator{count !== 1 ? 's' : ''}</div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Stress Trigger Detection */}
      <div className="bg-white rounded-xl border border-gray-200 p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-sm font-bold text-gray-700 flex items-center gap-2">
            <i className="ri-radar-line text-orange-500"></i>
            Possible Stress Trigger Detection
          </h3>
          <span className="text-xs text-gray-400 bg-gray-50 px-2 py-1 rounded-full border border-gray-200">
            {stressTriggers.length} trigger{stressTriggers.length !== 1 ? 's' : ''} identified
          </span>
        </div>

        <div className="grid grid-cols-1 gap-3">
          {stressTriggers.map((trigger, i) => (
            <div
              key={i}
              className="flex items-center gap-4 p-4 rounded-lg border border-gray-100 bg-gray-50 hover:bg-white hover:border-gray-200 transition-all"
            >
              <div className="w-10 h-10 flex items-center justify-center bg-white rounded-lg border border-gray-200 shrink-0">
                <i className={`${trigger.icon} text-lg text-gray-600`}></i>
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 flex-wrap">
                  <span className="text-sm font-semibold text-gray-800">{trigger.label}</span>
                  <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${severityBadge[trigger.severity]}`}>
                    <i className={`${severityIcon[trigger.severity]} mr-1`}></i>
                    {trigger.severity.charAt(0).toUpperCase() + trigger.severity.slice(1)} Impact
                  </span>
                </div>
                <p className="text-xs text-gray-500 mt-0.5">{trigger.description}</p>
              </div>
              <div className="shrink-0">
                <div className={`w-2.5 h-2.5 rounded-full ${
                  trigger.severity === 'high' ? 'bg-red-400' :
                  trigger.severity === 'medium' ? 'bg-orange-400' : 'bg-teal-400'
                }`}></div>
              </div>
            </div>
          ))}
        </div>

        {/* AI Disclaimer */}
        <div className="mt-5 flex items-start gap-3 p-4 bg-amber-50 border border-amber-200 rounded-lg">
          <i className="ri-information-line text-amber-500 text-base w-5 h-5 flex items-center justify-center shrink-0 mt-0.5"></i>
          <p className="text-xs text-amber-700 leading-relaxed">
            <strong>AI Insight Disclaimer:</strong> These insights are generated by an AI model based on language patterns and are intended for informational purposes only. They do not constitute a medical diagnosis. Please consult a qualified mental health professional for clinical assessment.
          </p>
        </div>
      </div>
    </div>
  );
}
