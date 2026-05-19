interface Recommendation {
  title: string;
  description: string;
  category: string;
}

interface Props {
  recommendations: Recommendation[];
  mentalState: string;
}

const AIRecommendations = ({ recommendations, mentalState }: Props) => {
  const stateColor = {
    'Depression': 'bg-blue-50 border-blue-200 text-blue-900',
    'Anxiety': 'bg-violet-50 border-violet-200 text-violet-900',
    'Stress': 'bg-orange-50 border-orange-200 text-orange-900',
    'Normal': 'bg-teal-50 border-teal-200 text-teal-900'
  };

  const stateIcon = {
    'Depression': 'ri-mental-health-line',
    'Anxiety': 'ri-pulse-line',
    'Stress': 'ri-flashlight-line',
    'Normal': 'ri-checkbox-circle-line'
  };

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
      <div className="flex items-center gap-3 mb-5">
        <div className={`w-12 h-12 ${stateColor[mentalState as keyof typeof stateColor] || stateColor.Normal} rounded-full flex items-center justify-center border`}>
          <i className={`${stateIcon[mentalState as keyof typeof stateIcon] || stateIcon.Normal} text-xl`}></i>
        </div>
        <div>
          <h2 className="text-xl font-bold text-gray-900">AI Wellness Recommendations</h2>
          <p className="text-sm text-gray-600">Personalized tips based on your emotional state</p>
        </div>
      </div>

      {recommendations && recommendations.length > 0 ? (
        <div className="space-y-3">
          {recommendations.map((rec, index) => (
            <div 
              key={index}
              className="p-4 rounded-lg border border-gray-200 hover:border-teal-300 hover:bg-teal-50 transition-all group"
            >
              <div className="flex items-start gap-3">
                <div className="flex-shrink-0 w-8 h-8 bg-teal-100 group-hover:bg-teal-200 rounded-full flex items-center justify-center text-teal-700 font-semibold text-sm transition-colors">
                  {index + 1}
                </div>
                <div className="flex-1">
                  <h3 className="font-semibold text-gray-900 mb-1 group-hover:text-teal-700 transition-colors">
                    {rec.title}
                  </h3>
                  <p className="text-sm text-gray-600 leading-relaxed">
                    {rec.description}
                  </p>
                  <div className="mt-2">
                    <span className="inline-flex items-center gap-1 px-2 py-1 bg-gray-100 group-hover:bg-teal-100 rounded text-xs font-medium text-gray-600 group-hover:text-teal-700 transition-colors">
                      <i className="ri-price-tag-3-line"></i>
                      {rec.category}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="text-center py-8 text-gray-500">
          <i className="ri-emotion-happy-line text-4xl mb-2"></i>
          <p>No specific recommendations at this time. Keep expressing yourself!</p>
        </div>
      )}

      <div className="mt-5 p-4 bg-gradient-to-r from-teal-50 to-blue-50 rounded-lg border border-teal-200">
        <div className="flex items-center gap-3">
          <i className="ri-information-line text-teal-600 text-xl flex-shrink-0"></i>
          <p className="text-sm text-gray-700">
            <strong className="text-teal-900">Remember:</strong> These are AI-generated suggestions. For professional support, consult a qualified mental health professional.
          </p>
        </div>
      </div>
    </div>
  );
};

export default AIRecommendations;
