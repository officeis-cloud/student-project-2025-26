import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import DashboardLayout from '../../components/feature/DashboardLayout';
import { getJournalHistory, type JournalEntry } from '../../services/api';

export default function DashboardPage() {
  const [showRiskAlert, setShowRiskAlert] = useState(false);
  const [alertType, setAlertType] = useState<'severe' | 'mild'>('severe');
  const [entries, setEntries] = useState<JournalEntry[]>([]);
  const [loading, setLoading] = useState(true);

  // Fetch real journal entries
  useEffect(() => {
    const fetchEntries = async () => {
      try {
        setLoading(true);
        const response = await getJournalHistory(1, 100);
        setEntries(response.entries || []);
      } catch (error) {
        console.error('Failed to fetch journal entries:', error);
        setEntries([]);
      } finally {
        setLoading(false);
      }
    };

    fetchEntries();
  }, []);

  // Helper: Get entries in date range
  const getEntriesInRange = (days: number) => {
    const cutoffDate = new Date();
    cutoffDate.setDate(cutoffDate.getDate() - days);
    return entries.filter(entry => new Date(entry.created_at) >= cutoffDate);
  };

  // Calculate last 7 days mood data
  const getLast7Days = () => {
    const days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
    const today = new Date();
    const last7Days = [];
    
    for (let i = 6; i >= 0; i--) {
      const date = new Date(today);
      date.setDate(date.getDate() - i);
      const dayName = days[date.getDay()];
      
      const dayEntries = entries.filter(entry => {
        const entryDate = new Date(entry.created_at);
        return entryDate.toDateString() === date.toDateString();
      });
      
      // Calculate wellness score (severity_score is 0-1, convert to 0-100)
      // Return null for days with no entries instead of mock data
      const avgScore = dayEntries.length > 0
        ? Math.round(dayEntries.reduce((sum, e) => sum + (100 - (e.severity_score * 100)), 0) / dayEntries.length)
        : null;
      
      last7Days.push({ day: dayName, score: avgScore });
    }
    return last7Days;
  };

  // Map ML emotions to display categories (consistent with backend)
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

  // Calculate emotion distribution from last 7 days (matches Weekly Mood Trend)
  const calculateEmotionDistribution = () => {
    const last7DaysEntries = getEntriesInRange(7);
    
    if (last7DaysEntries.length === 0) {
      return [
        { emotion: 'Happy', percentage: 0, color: 'bg-green-500' },
        { emotion: 'Sad', percentage: 0, color: 'bg-blue-500' },
        { emotion: 'Anxious', percentage: 0, color: 'bg-orange-500' },
        { emotion: 'Stressed', percentage: 0, color: 'bg-red-500' },
        { emotion: 'Calm', percentage: 0, color: 'bg-teal-500' }
      ];
    }

    const emotionCounts: { [key: string]: number } = {
      Happy: 0,
      Calm: 0,
      Stressed: 0,
      Anxious: 0,
      Sad: 0
    };

    // Use last 7 days entries to match the weekly mood trend timeframe
    last7DaysEntries.forEach(entry => {
      if (entry.emotions && Object.keys(entry.emotions).length > 0) {
        // Get top emotion from emotions dictionary
        const emotionsArray = Object.entries(entry.emotions).sort((a, b) => b[1] - a[1]);
        const topEmotion = emotionsArray[0][0]; // Get emotion name
        const category = getEmotionCategory(topEmotion);
        emotionCounts[category]++;
      }
    });

    const total = Object.values(emotionCounts).reduce((sum, count) => sum + count, 0);
    
    if (total === 0) {
      return [
        { emotion: 'Happy', percentage: 0, color: 'bg-green-500' },
        { emotion: 'Sad', percentage: 0, color: 'bg-blue-500' },
        { emotion: 'Anxious', percentage: 0, color: 'bg-orange-500' },
        { emotion: 'Stressed', percentage: 0, color: 'bg-red-500' },
        { emotion: 'Calm', percentage: 0, color: 'bg-teal-500' }
      ];
    }

    return [
      { emotion: 'Happy', percentage: Math.round((emotionCounts.Happy / total) * 100), color: 'bg-green-500' },
      { emotion: 'Sad', percentage: Math.round((emotionCounts.Sad / total) * 100), color: 'bg-blue-500' },
      { emotion: 'Anxious', percentage: Math.round((emotionCounts.Anxious / total) * 100), color: 'bg-orange-500' },
      { emotion: 'Stressed', percentage: Math.round((emotionCounts.Stressed / total) * 100), color: 'bg-red-500' },
      { emotion: 'Calm', percentage: Math.round((emotionCounts.Calm / total) * 100), color: 'bg-teal-500' }
    ];
  };

  // Calculate summary data from real entries
  const calculateSummaryData = () => {
    const recentEntries = getEntriesInRange(7);
    
    if (recentEntries.length === 0) {
      return {
        stressLevel: 0,
        anxietyLevel: 0,
        depressionIndicator: 0,
        wellnessScore: 50
      };
    }

    const stressEntries = recentEntries.filter(e => e.mental_state === 'stress');
    const anxietyEntries = recentEntries.filter(e => e.mental_state === 'anxiety');
    const depressionEntries = recentEntries.filter(e => e.mental_state === 'depression');

    // Convert severity_score (0-1) to percentage (0-100)
    const stressLevel = stressEntries.length > 0
      ? Math.round(stressEntries.reduce((sum, e) => sum + (e.severity_score * 100), 0) / stressEntries.length)
      : 0;
    
    const anxietyLevel = anxietyEntries.length > 0
      ? Math.round(anxietyEntries.reduce((sum, e) => sum + (e.severity_score * 100), 0) / anxietyEntries.length)
      : 0;
    
    const depressionIndicator = depressionEntries.length > 0
      ? Math.round(depressionEntries.reduce((sum, e) => sum + (e.severity_score * 100), 0) / depressionEntries.length)
      : 0;

    // Overall wellness = 100 - average severity of all entries
    const totalWellness = recentEntries.reduce((sum, entry) => 
      sum + (100 - (entry.severity_score * 100)), 0);
    const wellnessScore = Math.round(totalWellness / recentEntries.length);

    return {
      stressLevel,
      anxietyLevel,
      depressionIndicator,
      wellnessScore
    };
  };

  const summaryData = calculateSummaryData();
  const weeklyMoodData = getLast7Days();
  const emotionDistribution = calculateEmotionDistribution();
  
  // Get dominant emotion
  const dominantEmotion = emotionDistribution.reduce((prev, current) => 
    current.percentage > prev.percentage ? current : prev
  );

  // Format recent entries for display
  const recentEntriesDisplay = entries
    .slice(0, 3)
    .map(entry => {
      const date = new Date(entry.created_at);
      const formattedDate = date.toLocaleDateString('en-US', { year: 'numeric', month: '2-digit', day: '2-digit' });
      
      // Use mental state from backend (matches Journal page exactly)
      const mentalState = entry.mental_state || 'normal';
      const mentalStateLabel = mentalState.charAt(0).toUpperCase() + mentalState.slice(1);
      
      const severityPercent = entry.severity_score * 100;
      let severityLabel = 'Normal';
      if (severityPercent >= 60) severityLabel = 'Severe';
      else if (severityPercent >= 40) severityLabel = 'Moderate';
      else if (severityPercent >= 20) severityLabel = 'Mild';

      return {
        id: entry._id || entry.id,
        date: formattedDate,
        text: entry.text,
        emotion: mentalStateLabel,
        severity: severityLabel
      };
    });

  // Check for emotional distress patterns
  useEffect(() => {
    if (loading || recentEntriesDisplay.length === 0) return;

    const severeCount = recentEntriesDisplay.filter(entry => 
      entry.severity === 'Severe' || entry.severity === 'Moderate'
    ).length;

    const mildCount = recentEntriesDisplay.filter(entry => 
      entry.severity === 'Mild'
    ).length;

    if (severeCount >= 2) {
      setAlertType('severe');
      setShowRiskAlert(true);
    } else if (mildCount >= 2 && severeCount === 0) {
      setAlertType('mild');
      setShowRiskAlert(true);
    } else {
      setShowRiskAlert(false);
    }
  }, [loading, entries]);

  const getScoreColor = (score: number) => {
    if (score >= 70) return 'text-red-600';
    if (score >= 50) return 'text-orange-600';
    if (score >= 30) return 'text-yellow-600';
    return 'text-green-600';
  };

  const getScoreLabel = (score: number) => {
    if (score >= 70) return 'High';
    if (score >= 50) return 'Moderate';
    if (score >= 30) return 'Mild';
    return 'Low';
  };

  return (
    <DashboardLayout>
      {loading ? (
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-teal-600"></div>
        </div>
      ) : (
        <div className="space-y-6">
        {/* Risk Alert Banner */}
        {showRiskAlert && alertType === 'severe' && (
          <div className="bg-red-50 border-l-4 border-red-500 rounded-lg p-4 flex items-start justify-between">
            <div className="flex items-start gap-3">
              <i className="ri-alert-line text-red-600 text-2xl mt-0.5"></i>
              <div>
                <h3 className="font-bold text-red-900 mb-1">⚠ Emotional Distress Detected Over Several Days</h3>
                <p className="text-sm text-red-800 leading-relaxed">
                  We've noticed patterns of elevated stress and anxiety over the past several days. 
                  Consider speaking with a mental health professional for personalized support.
                </p>
                <div className="flex items-center gap-4 mt-3">
                  <a 
                    href="tel:988" 
                    className="text-sm font-medium text-red-700 hover:text-red-800 cursor-pointer whitespace-nowrap"
                  >
                    📞 988 Crisis Helpline
                  </a>
                  <a 
                    href="https://www.psychologytoday.com/us/therapists" 
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-sm font-medium text-red-700 hover:text-red-800 cursor-pointer whitespace-nowrap"
                  >
                    🔍 Find a Therapist →
                  </a>
                </div>
              </div>
            </div>
            <button 
              onClick={() => setShowRiskAlert(false)}
              className="text-red-400 hover:text-red-600 cursor-pointer"
            >
              <i className="ri-close-line text-xl"></i>
            </button>
          </div>
        )}

        {/* Mild Concern Banner */}
        {showRiskAlert && alertType === 'mild' && (
          <div className="bg-yellow-50 border-l-4 border-yellow-400 rounded-lg p-4 flex items-start justify-between">
            <div className="flex items-start gap-3">
              <i className="ri-information-line text-yellow-600 text-2xl mt-0.5"></i>
              <div>
                <h3 className="font-bold text-yellow-900 mb-1">Mild Concern Detected</h3>
                <p className="text-sm text-yellow-800 leading-relaxed">
                  We've noticed some mild emotional fluctuations in your recent entries. 
                  Consider practicing self-care activities and monitoring your emotional patterns.
                </p>
                <div className="flex items-center gap-4 mt-3">
                  <Link 
                    to="/wellness" 
                    className="text-sm font-medium text-yellow-700 hover:text-yellow-800 cursor-pointer whitespace-nowrap"
                  >
                    View Wellness Tips →
                  </Link>
                  <Link 
                    to="/trends" 
                    className="text-sm font-medium text-yellow-700 hover:text-yellow-800 cursor-pointer whitespace-nowrap"
                  >
                    Check Your Trends →
                  </Link>
                </div>
              </div>
            </div>
            <button 
              onClick={() => setShowRiskAlert(false)}
              className="text-yellow-400 hover:text-yellow-600 cursor-pointer"
            >
              <i className="ri-close-line text-xl"></i>
            </button>
          </div>
        )}

        {/* Summary Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {/* Stress Level */}
          <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
            <div className="flex items-center justify-between mb-4">
              <div className="w-12 h-12 bg-red-100 rounded-lg flex items-center justify-center">
                <i className="ri-fire-line text-2xl text-red-600"></i>
              </div>
              <span className={`text-2xl font-bold ${getScoreColor(summaryData.stressLevel)}`}>
                {summaryData.stressLevel}%
              </span>
            </div>
            <h3 className="text-sm font-medium text-gray-600 mb-1">Stress Level</h3>
            <p className={`text-xs font-semibold ${getScoreColor(summaryData.stressLevel)}`}>
              {getScoreLabel(summaryData.stressLevel)}
            </p>
          </div>

          {/* Anxiety Level */}
          <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
            <div className="flex items-center justify-between mb-4">
              <div className="w-12 h-12 bg-orange-100 rounded-lg flex items-center justify-center">
                <i className="ri-pulse-line text-2xl text-orange-600"></i>
              </div>
              <span className={`text-2xl font-bold ${getScoreColor(summaryData.anxietyLevel)}`}>
                {summaryData.anxietyLevel}%
              </span>
            </div>
            <h3 className="text-sm font-medium text-gray-600 mb-1">Anxiety Level</h3>
            <p className={`text-xs font-semibold ${getScoreColor(summaryData.anxietyLevel)}`}>
              {getScoreLabel(summaryData.anxietyLevel)}
            </p>
          </div>

          {/* Depression Indicator */}
          <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
            <div className="flex items-center justify-between mb-4">
              <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                <i className="ri-emotion-sad-line text-2xl text-blue-600"></i>
              </div>
              <span className={`text-2xl font-bold ${getScoreColor(summaryData.depressionIndicator)}`}>
                {summaryData.depressionIndicator}%
              </span>
            </div>
            <h3 className="text-sm font-medium text-gray-600 mb-1">Depression Indicator</h3>
            <p className={`text-xs font-semibold ${getScoreColor(summaryData.depressionIndicator)}`}>
              {getScoreLabel(summaryData.depressionIndicator)}
            </p>
          </div>

          {/* Overall Wellness Score */}
          <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
            <div className="flex items-center justify-between mb-4">
              <div className="w-12 h-12 bg-teal-100 rounded-lg flex items-center justify-center">
                <i className="ri-heart-pulse-line text-2xl text-teal-600"></i>
              </div>
              <span className="text-2xl font-bold text-teal-600">
                {summaryData.wellnessScore}%
              </span>
            </div>
            <h3 className="text-sm font-medium text-gray-600 mb-1">Overall Wellness Score</h3>
            <p className="text-xs font-semibold text-teal-600">Good</p>
          </div>
        </div>

        {/* Charts Row */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Weekly Mood Trend */}
          <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
            <h3 className="text-lg font-semibold text-gray-800 mb-6">Weekly Mood Trend</h3>
            {weeklyMoodData.filter(d => d.score !== null).length > 0 ? (
              <div className="h-64 flex items-end justify-between gap-3">
                {weeklyMoodData.map((data, index) => (
                  <div key={index} className="flex-1 flex flex-col items-center gap-2">
                    <div className="w-full bg-gray-100 rounded-t-lg relative" style={{ height: '200px' }}>
                      {data.score !== null && (
                        <div 
                          className="absolute bottom-0 w-full bg-gradient-to-t from-teal-500 to-teal-400 rounded-t-lg transition-all hover:from-teal-600 hover:to-teal-500"
                          style={{ height: `${(data.score / 100) * 100}%` }}
                        ></div>
                      )}
                    </div>
                    <span className="text-xs font-medium text-gray-600">{data.day}</span>
                    <span className="text-xs text-gray-500">{data.score !== null ? data.score : '-'}</span>
                  </div>
                ))}
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

          {/* Emotion Distribution */}
          <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
            <h3 className="text-lg font-semibold text-gray-800 mb-6">Emotion Distribution</h3>
            <div className="space-y-4">
              {emotionDistribution.map((item, index) => (
                <div key={index}>
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm font-medium text-gray-700">{item.emotion}</span>
                    <span className="text-sm font-semibold text-gray-900">{item.percentage}%</span>
                  </div>
                  <div className="w-full bg-gray-100 rounded-full h-3">
                    <div 
                      className={`${item.color} h-3 rounded-full transition-all`}
                      style={{ width: `${item.percentage}%` }}
                    ></div>
                  </div>
                </div>
              ))}
            </div>
            <div className="mt-6 p-4 bg-teal-50 rounded-lg">
              <div className="flex items-center gap-3">
                <i className="ri-emotion-happy-line text-2xl text-teal-600"></i>
                <div>
                  <p className="text-sm font-semibold text-gray-800">Dominant Emotion</p>
                  <p className="text-xs text-gray-600">{dominantEmotion.emotion} ({dominantEmotion.percentage}% overall)</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Recent Journal Entries */}
        <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-lg font-semibold text-gray-800">Recent Journal Entries</h3>
            <Link to="/journal" className="text-sm font-medium text-teal-600 hover:text-teal-700 cursor-pointer">
              View All →
            </Link>
          </div>
          <div className="space-y-4">
            {recentEntriesDisplay.length > 0 ? (
              recentEntriesDisplay.map((entry) => (
                <div key={entry.id} className="p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
                  <div className="flex items-start justify-between mb-2">
                    <div className="flex items-center gap-3">
                      <span className="text-xs font-medium text-gray-500">{entry.date}</span>
                      <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                        entry.emotion === 'Happy' ? 'bg-green-100 text-green-700' :
                        entry.emotion === 'Stressed' ? 'bg-red-100 text-red-700' :
                        entry.emotion === 'Anxious' ? 'bg-orange-100 text-orange-700' :
                        entry.emotion === 'Sad' ? 'bg-blue-100 text-blue-700' :
                        'bg-teal-100 text-teal-700'
                      }`}>
                        {entry.emotion}
                      </span>
                      <span className="px-3 py-1 bg-gray-200 text-gray-700 rounded-full text-xs font-medium">
                        {entry.severity}
                      </span>
                    </div>
                  </div>
                  <p className="text-sm text-gray-700">{entry.text}</p>
                </div>
              ))
            ) : (
              <div className="text-center py-8 text-gray-500">
                <p className="text-sm">No journal entries yet. Start writing to track your emotions!</p>
              </div>
            )}
          </div>
        </div>

        {/* Quick Actions */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <Link 
            to="/analyze" 
            className="bg-gradient-to-br from-teal-500 to-teal-600 rounded-xl p-8 text-white hover:from-teal-600 hover:to-teal-700 transition-all shadow-lg hover:shadow-xl cursor-pointer"
          >
            <div className="flex items-center gap-4">
              <div className="w-14 h-14 bg-white/20 rounded-lg flex items-center justify-center">
                <i className="ri-brain-line text-3xl"></i>
              </div>
              <div>
                <h3 className="text-xl font-semibold mb-1">Analyze Emotion</h3>
                <p className="text-sm text-teal-100">Share how you're feeling today</p>
              </div>
            </div>
          </Link>

          <Link 
            to="/journal" 
            className="bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl p-8 text-white hover:from-blue-600 hover:to-blue-700 transition-all shadow-lg hover:shadow-xl cursor-pointer"
          >
            <div className="flex items-center gap-4">
              <div className="w-14 h-14 bg-white/20 rounded-lg flex items-center justify-center">
                <i className="ri-book-open-line text-3xl"></i>
              </div>
              <div>
                <h3 className="text-xl font-semibold mb-1">Write Journal Entry</h3>
                <p className="text-sm text-blue-100">Record your thoughts and feelings</p>
              </div>
            </div>
          </Link>
        </div>
      </div>
      )}
    </DashboardLayout>
  );
}