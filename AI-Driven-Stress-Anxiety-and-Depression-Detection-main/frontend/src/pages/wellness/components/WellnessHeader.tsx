
export default function WellnessHeader() {
  return (
    <div className="flex items-center justify-between">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Wellness Recommendations</h1>
        <p className="text-sm text-gray-500 mt-1">
          Personalized lifestyle suggestions based on your emotional state
        </p>
      </div>
      <div className="flex items-center gap-2 px-4 py-2 bg-teal-50 border border-teal-200 rounded-lg">
        <i className="ri-calendar-check-line text-teal-600 w-5 h-5 flex items-center justify-center"></i>
        <span className="text-sm font-medium text-teal-700">Today's Plan Active</span>
      </div>
    </div>
  );
}
