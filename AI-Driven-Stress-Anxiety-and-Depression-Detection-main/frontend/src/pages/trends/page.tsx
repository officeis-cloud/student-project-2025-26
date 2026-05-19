import { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import DashboardLayout from '../../components/feature/DashboardLayout';
import { getJournalHistory, JournalEntry } from '../../services/api';

type TimeRange = 'week' | 'month' | '3months';

export default function TrendsPage() {
  const location = useLocation();
  const [timeRange, setTimeRange] = useState<TimeRange>('week');
  const [entries, setEntries] = useState<JournalEntry[]>([]);
  const [loading, setLoading] = useState(true);

  // Fetch real journal entries - refetch when navigating to this page
  useEffect(() => {
    const fetchEntries = async () => {
      try {
        setLoading(true);
        const response = await getJournalHistory(1, 100); // Fetch last 100 entries
        setEntries(response.entries);
      } catch (error) {
        console.error('Failed to fetch entries:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchEntries();
  }, [location.pathname]); // Refetch when route changes

  // Helper: Get entries within date range
  const getEntriesInRange = (days: number) => {
    const now = new Date();
    const cutoff = new Date(now.getTime() - days * 24 * 60 * 60 * 1000);
    return entries.filter(entry => new Date(entry.created_at) >= cutoff);
  };

  // Calculate daily wellness scores (last 7 days)
  const getLast7Days = () => {
    const days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
    const today = new Date();
    const last7Days = [];
    
    for (let i = 6; i >= 0; i--) {
      const date = new Date(today);
      date.setDate(date.getDate() - i);
      const dayName = days[date.getDay()];
      
      // Get entries for this day
      const dayEntries = entries.filter(entry => {
        const entryDate = new Date(entry.created_at);
        return entryDate.toDateString() === date.toDateString();
      });
      
      // Calculate average wellness score (100 - severity_score)
      // severity_score is 0-1 decimal, convert to 0-100 percentage
      // Return null for days with no entries instead of mock data
      const avgScore = dayEntries.length > 0
        ? Math.round(dayEntries.reduce((sum, e) => sum + (100 - (e.severity_score * 100)), 0) / dayEntries.length)
        : null;
      
      last7Days.push({ day: dayName, score: avgScore });
    }
    return last7Days;
  };

  const weeklyMoodData = getLast7Days();

  // Map ML emotions to display categories (consistent with backend and Dashboard)
  const getEmotionCategory = (emotion: string): string => {
    const emotionLower = emotion.toLowerCase();
    
    // Happy/Positive (9 emotions)
    if (['joy', 'love', 'excitement', 'gratitude', 'pride', 'admiration', 'amusement', 
         'optimism', 'surprise'].includes(emotionLower)) {
      return 'Happy';
    }
    // Calm (6 emotions - matches backend calm cluster)
    if (['realization', 'curiosity', 'desire', 'approval', 'relief', 'caring'].includes(emotionLower)) {
      return 'Calm';
    }
    // Stressed/Angry (7 emotions)
    if (['anger', 'annoyance', 'disapproval', 'disgust', 'embarrassment', 'confusion', 'disappointment'].includes(emotionLower)) {
      return 'Stressed';
    }
    // Anxious/Fear (2 emotions)
    if (['fear', 'nervousness'].includes(emotionLower)) {
      return 'Anxious';
    }
    // Sad (3 emotions)
    if (['sadness', 'remorse', 'grief'].includes(emotionLower)) {
      return 'Sad';
    }
    
    return 'Calm';
  };

  // Calculate emotion distribution from real entries
  const calculateEmotionDistribution = () => {
    const rangeEntries = getEntriesInRange(7);
    if (rangeEntries.length === 0) {
      return [
        { emotion: 'Happy', percentage: 20, color: '#10B981' },
        { emotion: 'Calm', percentage: 20, color: '#3B82F6' },
        { emotion: 'Stressed', percentage: 20, color: '#F59E0B' },
        { emotion: 'Anxious', percentage: 20, color: '#EF4444' },
        { emotion: 'Sad', percentage: 20, color: '#6B7280' },
      ];
    }

    const categoryCounts: Record<string, number> = {
      Happy: 0,
      Calm: 0,
      Stressed: 0,
      Anxious: 0,
      Sad: 0
    };

    rangeEntries.forEach(entry => {
      if (entry.emotions && Object.keys(entry.emotions).length > 0) {
        // Get top emotion from emotions dictionary
        const emotionsArray = Object.entries(entry.emotions).sort((a, b) => b[1] - a[1]);
        const topEmotion = emotionsArray[0][0]; // Get emotion name
        const category = getEmotionCategory(topEmotion);
        categoryCounts[category]++;
      }
    });

    const total = rangeEntries.length;
    const colors: Record<string, string> = {
      Happy: '#10B981',
      Calm: '#3B82F6',
      Stressed: '#F59E0B',
      Anxious: '#EF4444',
      Sad: '#6B7280'
    };

    const distribution = Object.entries(categoryCounts)
      .map(([emotion, count]) => ({
        emotion,
        percentage: (count / total) * 100,
        color: colors[emotion]
      }))
      .filter(item => item.percentage > 0)
      .sort((a, b) => b.percentage - a.percentage);

    // Normalize to ensure exactly 100%
    const sum = distribution.reduce((acc, item) => acc + item.percentage, 0);
    if (sum > 0) {
      distribution.forEach(item => {
        item.percentage = Math.round((item.percentage / sum) * 100);
      });
    }

    // Ensure we have at least one entry
    if (distribution.length === 0) {
      return [{ emotion: 'Calm', percentage: 100, color: '#3B82F6' }];
    }

    return distribution;
  };

  const emotionDistribution = calculateEmotionDistribution();

  // Calculate mental health trends (4 weeks) - REAL DATA ONLY
  const calculateMentalHealthTrends = () => {
    const weeks = [];
    for (let i = 3; i >= 0; i--) {
      const weekStart = new Date();
      weekStart.setDate(weekStart.getDate() - (i + 1) * 7);
      const weekEnd = new Date();
      weekEnd.setDate(weekEnd.getDate() - i * 7);

      const weekEntries = entries.filter(entry => {
        const entryDate = new Date(entry.created_at);
        return entryDate >= weekStart && entryDate < weekEnd;
      });

      let stress = 0, anxiety = 0, depression = 0;

      if (weekEntries.length > 0) {
        // Calculate ONLY from actual entries with that mental state
        const stressEntries = weekEntries.filter(e => e.mental_state === 'stress');
        const anxietyEntries = weekEntries.filter(e => e.mental_state === 'anxiety');
        const depressionEntries = weekEntries.filter(e => e.mental_state === 'depression');

        // Convert decimal to percentage (severity_score is 0-1, need 0-100)
        stress = stressEntries.length > 0 
          ? Math.round(stressEntries.reduce((sum, e) => sum + (e.severity_score * 100), 0) / stressEntries.length)
          : 0;
        anxiety = anxietyEntries.length > 0
          ? Math.round(anxietyEntries.reduce((sum, e) => sum + (e.severity_score * 100), 0) / anxietyEntries.length)
          : 0;
        depression = depressionEntries.length > 0
          ? Math.round(depressionEntries.reduce((sum, e) => sum + (e.severity_score * 100), 0) / depressionEntries.length)
          : 0;
      }

      weeks.push({ 
        week: `Week ${4 - i}`, 
        stress: Math.min(stress, 100), 
        anxiety: Math.min(anxiety, 100), 
        depression: Math.min(depression, 100)
      });
    }
    return weeks;
  };

  const mentalHealthTrends = calculateMentalHealthTrends();

  // Calculate pie chart segments
  let cumulativePercentage = 0;
  const pieSegments = emotionDistribution.map((item) => {
    const startPercentage = cumulativePercentage;
    cumulativePercentage += item.percentage;
    return {
      ...item,
      startPercentage,
      endPercentage: cumulativePercentage,
    };
  });

  // Helper function to calculate pie chart path
  const getPieSlicePath = (startPercentage: number, endPercentage: number) => {
    const startAngle = (startPercentage / 100) * 2 * Math.PI - Math.PI / 2;
    const endAngle = (endPercentage / 100) * 2 * Math.PI - Math.PI / 2;
    const x1 = 50 + 40 * Math.cos(startAngle);
    const y1 = 50 + 40 * Math.sin(startAngle);
    const x2 = 50 + 40 * Math.cos(endAngle);
    const y2 = 50 + 40 * Math.sin(endAngle);
    const largeArc = endPercentage - startPercentage > 50 ? 1 : 0;
    return `M 50 50 L ${x1} ${y1} A 40 40 0 ${largeArc} 1 ${x2} ${y2} Z`;
  };

  // Summary insights - Calculate from ACTUAL entries only
  const calculateAverageWellness = () => {
    const recentEntries = getEntriesInRange(7); // Last 7 days
    if (recentEntries.length === 0) return 50;
    
    const totalWellness = recentEntries.reduce((sum, entry) => {
      // severity_score is 0-1 decimal, convert to 0-100 percentage
      return sum + (100 - (entry.severity_score * 100));
    }, 0);
    
    return Math.round(totalWellness / recentEntries.length);
  };

  const averageWellness = calculateAverageWellness();
  const dominantEmotion = emotionDistribution[0] || { emotion: 'Calm', percentage: 100, color: '#3B82F6' };
  
  // Find highest stress day - only from days with actual entries
  const calculateHighestStressDay = () => {
    const daysWithEntries = weeklyMoodData.filter((_, index) => {
      const date = new Date();
      date.setDate(date.getDate() - (6 - index));
      const dayEntries = entries.filter(entry => {
        const entryDate = new Date(entry.created_at);
        return entryDate.toDateString() === date.toDateString();
      });
      return dayEntries.length > 0;
    });
    
    if (daysWithEntries.length === 0) return { day: 'N/A', score: 50 };
    
    return daysWithEntries.reduce((prev, current) => 
      current.score < prev.score ? current : prev
    );
  };
  
  const highestStressDay = calculateHighestStressDay();

  if (loading) {
    return (
      <DashboardLayout>
        <div className="p-8 bg-gray-50 min-h-screen flex items-center justify-center">
          <div className="text-center">
            <div className="w-16 h-16 border-4 border-teal-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
            <p className="text-gray-600">Loading your emotional trends...</p>
          </div>
        </div>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <div className="p-8 bg-gray-50 min-h-screen">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-800 mb-2">Trend Analysis</h1>
          <p className="text-gray-600">Track your emotional patterns and mental health trends over time</p>
        </div>

        {/* Time Range Selector */}
        <div className="bg-white rounded-xl p-2 inline-flex gap-2 mb-8 shadow-sm">
          <button
            onClick={() => setTimeRange('week')}
            className={`px-6 py-2 rounded-lg font-medium transition-all whitespace-nowrap cursor-pointer ${
              timeRange === 'week'
                ? 'bg-teal-500 text-white'
                : 'text-gray-600 hover:bg-gray-50'
            }`}
          >
            This Week
          </button>
          <button
            onClick={() => setTimeRange('month')}
            className={`px-6 py-2 rounded-lg font-medium transition-all whitespace-nowrap cursor-pointer ${
              timeRange === 'month'
                ? 'bg-teal-500 text-white'
                : 'text-gray-600 hover:bg-gray-50'
            }`}
          >
            This Month
          </button>
          <button
            onClick={() => setTimeRange('3months')}
            className={`px-6 py-2 rounded-lg font-medium transition-all whitespace-nowrap cursor-pointer ${
              timeRange === '3months'
                ? 'bg-teal-500 text-white'
                : 'text-gray-600 hover:bg-gray-50'
            }`}
          >
            Last 3 Months
          </button>
        </div>

        {/* Summary Insight Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
            <div className="flex items-center gap-3 mb-3">
              <div className="w-12 h-12 bg-teal-100 rounded-lg flex items-center justify-center">
                <i className="ri-heart-pulse-line text-teal-600 text-2xl w-6 h-6 flex items-center justify-center"></i>
              </div>
              <div>
                <p className="text-sm text-gray-500">Average Wellness</p>
                <p className="text-2xl font-bold text-gray-800">{averageWellness}%</p>
              </div>
            </div>
            <p className="text-sm text-gray-600">Your overall wellness score this week</p>
          </div>

          <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
            <div className="flex items-center gap-3 mb-3">
              <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
                <i className="ri-emotion-happy-line text-green-600 text-2xl w-6 h-6 flex items-center justify-center"></i>
              </div>
              <div>
                <p className="text-sm text-gray-500">Most Frequent</p>
                <p className="text-2xl font-bold text-gray-800">{dominantEmotion.emotion}</p>
              </div>
            </div>
            <p className="text-sm text-gray-600">{dominantEmotion.percentage}% of your emotional state</p>
          </div>

          <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
            <div className="flex items-center gap-3 mb-3">
              <div className="w-12 h-12 bg-orange-100 rounded-lg flex items-center justify-center">
                <i className="ri-alert-line text-orange-600 text-2xl w-6 h-6 flex items-center justify-center"></i>
              </div>
              <div>
                <p className="text-sm text-gray-500">Highest Stress Day</p>
                <p className="text-2xl font-bold text-gray-800">{highestStressDay.day}</p>
              </div>
            </div>
            <p className="text-sm text-gray-600">Wellness score: {highestStressDay.score}%</p>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          {/* Weekly Mood Trend Line Graph */}
          <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
            <h2 className="text-xl font-bold text-gray-800 mb-6">Weekly Mood Trend</h2>
            {weeklyMoodData.filter(d => d.score !== null).length > 0 ? (
              <div className="relative h-64">
                {/* Y-axis labels */}
                <div className="absolute left-0 top-0 bottom-8 flex flex-col justify-between text-xs text-gray-500">
                  <span>100</span>
                  <span>75</span>
                  <span>50</span>
                  <span>25</span>
                  <span>0</span>
                </div>

                {/* Chart area */}
                <div className="ml-8 h-full relative">
                  {/* Grid lines */}
                  <div className="absolute inset-0 flex flex-col justify-between">
                    {[0, 1, 2, 3, 4].map((i) => (
                      <div key={i} className="border-t border-gray-100"></div>
                    ))}
                  </div>

                  {/* SVG Line Chart */}
                  <svg className="absolute inset-0 w-full h-full" style={{ height: 'calc(100% - 2rem)' }}>
                    {/* Line path */}
                    <polyline
                      points={weeklyMoodData
                        .filter(item => item.score !== null)
                        .map((item, index, filtered) => {
                          const originalIndex = weeklyMoodData.indexOf(item);
                          const x = (originalIndex / (weeklyMoodData.length - 1)) * 100;
                          const y = 100 - item.score;
                          return `${x}%,${y}%`;
                        })
                        .join(' ')}
                      fill="none"
                      stroke="#14B8A6"
                      strokeWidth="3"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    />
                    {/* Data points */}
                    {weeklyMoodData.map((item, index) => {
                      if (item.score === null) return null;
                      const x = (index / (weeklyMoodData.length - 1)) * 100;
                      const y = 100 - item.score;
                      return (
                        <circle
                          key={index}
                          cx={`${x}%`}
                          cy={`${y}%`}
                          r="5"
                          fill="#14B8A6"
                          stroke="white"
                          strokeWidth="2"
                        />
                      );
                    })}
                  </svg>

                  {/* X-axis labels */}
                  <div className="absolute bottom-0 left-0 right-0 flex justify-between text-xs text-gray-500 pt-2">
                    {weeklyMoodData.map((item, index) => (
                      <span key={index}>{item.day}</span>
                    ))}
                  </div>
                </div>
              </div>
            ) : (
              <div className="flex items-center justify-center h-64 text-gray-400">
                <div className="text-center">
                  <i className="ri-line-chart-line text-4xl mb-2"></i>
                  <p className="text-sm">No mood data available yet.</p>
                  <p className="text-xs mt-1">Start journaling to see your trends!</p>
                </div>
              </div>
            )}
          </div>

          {/* Emotion Distribution Pie Chart */}
          <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
            <h2 className="text-xl font-bold text-gray-800 mb-6">Emotion Distribution</h2>
            <div className="flex items-center justify-center gap-8">
              {/* Pie Chart */}
              <div className="relative w-48 h-48">
                <svg viewBox="0 0 100 100" className="w-full h-full transform -rotate-90">
                  {pieSegments.map((segment, index) => (
                    <path
                      key={index}
                      d={getPieSlicePath(segment.startPercentage, segment.endPercentage)}
                      fill={segment.color}
                      className="transition-all hover:opacity-80 cursor-pointer"
                    />
                  ))}
                  {/* Center circle for donut effect */}
                  <circle cx="50" cy="50" r="20" fill="white" />
                </svg>
                <div className="absolute inset-0 flex items-center justify-center">
                  <div className="text-center">
                    <p className="text-2xl font-bold text-gray-800">100%</p>
                    <p className="text-xs text-gray-500">Total</p>
                  </div>
                </div>
              </div>

              {/* Legend */}
              <div className="space-y-3">
                {emotionDistribution.map((item, index) => (
                  <div key={index} className="flex items-center gap-3">
                    <div
                      className="w-4 h-4 rounded-full"
                      style={{ backgroundColor: item.color }}
                    ></div>
                    <div className="flex-1">
                      <p className="text-sm font-medium text-gray-700">{item.emotion}</p>
                      <p className="text-xs text-gray-500">{item.percentage}%</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Mental Health Trends (4 weeks) */}
        <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100 mb-8">
          <h2 className="text-xl font-bold text-gray-800 mb-6">Mental Health Trends (4 Weeks)</h2>
          <div className="space-y-8">
            {/* Stress Trend */}
            <div>
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 bg-orange-500 rounded-full"></div>
                  <span className="font-medium text-gray-700">Stress Level</span>
                </div>
                <span className="text-sm text-gray-500">Average: {Math.round(mentalHealthTrends.reduce((sum, w) => sum + w.stress, 0) / 4)}%</span>
              </div>
              <div className="grid grid-cols-4 gap-4">
                {mentalHealthTrends.map((week, index) => (
                  <div key={index}>
                    <div className="bg-gray-100 rounded-lg h-32 flex items-end overflow-hidden">
                      <div
                        className="w-full bg-orange-500 rounded-t-lg transition-all duration-500"
                        style={{ height: `${week.stress}%` }}
                      ></div>
                    </div>
                    <p className="text-xs text-gray-600 text-center mt-2">{week.week}</p>
                    <p className="text-sm font-medium text-gray-800 text-center">{week.stress}%</p>
                  </div>
                ))}
              </div>
            </div>

            {/* Anxiety Trend */}
            <div>
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 bg-red-500 rounded-full"></div>
                  <span className="font-medium text-gray-700">Anxiety Level</span>
                </div>
                <span className="text-sm text-gray-500">Average: {Math.round(mentalHealthTrends.reduce((sum, w) => sum + w.anxiety, 0) / 4)}%</span>
              </div>
              <div className="grid grid-cols-4 gap-4">
                {mentalHealthTrends.map((week, index) => (
                  <div key={index}>
                    <div className="bg-gray-100 rounded-lg h-32 flex items-end overflow-hidden">
                      <div
                        className="w-full bg-red-500 rounded-t-lg transition-all duration-500"
                        style={{ height: `${week.anxiety}%` }}
                      ></div>
                    </div>
                    <p className="text-xs text-gray-600 text-center mt-2">{week.week}</p>
                    <p className="text-sm font-medium text-gray-800 text-center">{week.anxiety}%</p>
                  </div>
                ))}
              </div>
            </div>

            {/* Depression Trend */}
            <div>
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 bg-gray-600 rounded-full"></div>
                  <span className="font-medium text-gray-700">Depression Indicator</span>
                </div>
                <span className="text-sm text-gray-500">Average: {Math.round(mentalHealthTrends.reduce((sum, w) => sum + w.depression, 0) / 4)}%</span>
              </div>
              <div className="grid grid-cols-4 gap-4">
                {mentalHealthTrends.map((week, index) => (
                  <div key={index}>
                    <div className="bg-gray-100 rounded-lg h-32 flex items-end overflow-hidden">
                      <div
                        className="w-full bg-gray-600 rounded-t-lg transition-all duration-500"
                        style={{ height: `${week.depression}%` }}
                      ></div>
                    </div>
                    <p className="text-xs text-gray-600 text-center mt-2">{week.week}</p>
                    <p className="text-sm font-medium text-gray-800 text-center">{week.depression}%</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Dominant Emotion of the Week */}
        <div className="bg-gradient-to-br from-teal-500 to-blue-600 rounded-xl p-8 shadow-lg text-white">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-teal-100 mb-2">Dominant Emotion This Week</p>
              <h2 className="text-4xl font-bold mb-2">{dominantEmotion.emotion}</h2>
              <p className="text-teal-100">Represents {dominantEmotion.percentage}% of your emotional state</p>
            </div>
            <div className="w-24 h-24 bg-white/20 rounded-full flex items-center justify-center">
              <i className={`text-6xl w-16 h-16 flex items-center justify-center ${
                dominantEmotion.emotion === 'Happy' ? 'ri-emotion-happy-line' :
                dominantEmotion.emotion === 'Sad' ? 'ri-emotion-sad-line' :
                dominantEmotion.emotion === 'Anxious' ? 'ri-emotion-unhappy-line' :
                dominantEmotion.emotion === 'Stressed' ? 'ri-fire-line' :
                'ri-emotion-normal-line'
              }`}></i>
            </div>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}