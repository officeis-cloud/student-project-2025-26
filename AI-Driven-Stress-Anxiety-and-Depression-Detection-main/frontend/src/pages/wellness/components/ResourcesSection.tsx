
const resources = [
  {
    icon: 'ri-phone-line',
    title: 'Crisis Helpline',
    description: 'National Suicide Prevention Lifeline',
    contact: '988 (call or text)',
    available: '24/7 Available',
    color: 'border-red-200 bg-red-50',
    iconColor: 'bg-red-100 text-red-600',
    badgeColor: 'bg-red-100 text-red-700',
  },
  {
    icon: 'ri-message-3-line',
    title: 'Crisis Text Line',
    description: 'Text-based mental health support',
    contact: 'Text HOME to 741741',
    available: '24/7 Available',
    color: 'border-orange-200 bg-orange-50',
    iconColor: 'bg-orange-100 text-orange-600',
    badgeColor: 'bg-orange-100 text-orange-700',
  },
  {
    icon: 'ri-global-line',
    title: 'NAMI Helpline',
    description: 'National Alliance on Mental Illness',
    contact: '1-800-950-6264',
    available: 'Mon–Fri, 10am–10pm ET',
    color: 'border-teal-200 bg-teal-50',
    iconColor: 'bg-teal-100 text-teal-600',
    badgeColor: 'bg-teal-100 text-teal-700',
  },
  {
    icon: 'ri-user-heart-line',
    title: 'Find a Therapist',
    description: 'Psychology Today therapist directory',
    contact: 'psychologytoday.com',
    available: 'Online Directory',
    color: 'border-indigo-200 bg-indigo-50',
    iconColor: 'bg-indigo-100 text-indigo-600',
    badgeColor: 'bg-indigo-100 text-indigo-700',
  },
];

export default function ResourcesSection() {
  return (
    <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-6">
      <div className="flex items-center gap-3 mb-6">
        <div className="w-8 h-8 flex items-center justify-center">
          <i className="ri-hospital-line text-2xl text-teal-600"></i>
        </div>
        <div>
          <h2 className="text-lg font-bold text-gray-900">Mental Health Resources</h2>
          <p className="text-sm text-gray-500">Professional support is always available — you are not alone</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        {resources.map((r, idx) => (
          <div key={idx} className={`rounded-xl border-2 ${r.color} p-4`}>
            <div className={`w-10 h-10 rounded-lg flex items-center justify-center mb-3 ${r.iconColor}`}>
              <i className={`${r.icon} text-xl`}></i>
            </div>
            <h4 className="text-sm font-bold text-gray-800 mb-1">{r.title}</h4>
            <p className="text-xs text-gray-500 mb-2">{r.description}</p>
            <p className="text-sm font-semibold text-gray-800 mb-2">{r.contact}</p>
            <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${r.badgeColor}`}>
              {r.available}
            </span>
          </div>
        ))}
      </div>

      <div className="flex items-start gap-3 p-4 bg-amber-50 border border-amber-200 rounded-lg">
        <div className="w-6 h-6 flex items-center justify-center flex-shrink-0 mt-0.5">
          <i className="ri-information-line text-amber-600 text-lg"></i>
        </div>
        <p className="text-xs text-amber-800 leading-relaxed">
          <strong>Important Disclaimer:</strong> This system provides emotional insights and wellness suggestions for informational purposes only.
          It is <strong>not a substitute for professional medical advice, diagnosis, or treatment.</strong> If you are experiencing a mental health crisis,
          please contact a licensed mental health professional or emergency services immediately.
        </p>
      </div>
    </div>
  );
}
