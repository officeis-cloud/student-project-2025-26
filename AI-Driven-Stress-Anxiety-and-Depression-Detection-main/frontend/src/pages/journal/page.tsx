import { useState, useEffect } from 'react';
import DashboardLayout from '../../components/feature/DashboardLayout';
import { getJournalHistory, predictEmotion, deleteJournalEntry, type JournalEntry } from '../../services/api';

const mentalStateColors = {
  'normal': 'bg-emerald-100 text-emerald-700 border-emerald-300',
  'stress': 'bg-orange-100 text-orange-700 border-orange-300',
  'anxiety': 'bg-violet-100 text-violet-700 border-violet-300',
  'depression': 'bg-blue-100 text-blue-700 border-blue-300',
};

const severityColors = {
  'none': 'bg-gray-50 text-gray-700',
  'mild': 'bg-yellow-50 text-yellow-700',
  'moderate': 'bg-orange-50 text-orange-700',
  'severe': 'bg-red-50 text-red-700'
};

export default function JournalPage() {
  const [entries, setEntries] = useState<JournalEntry[]>([]);
  const [newEntry, setNewEntry] = useState('');
  const [selectedFilter, setSelectedFilter] = useState<string>('All');
  const [showSuccess, setShowSuccess] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const maxChars = 1000;
  const charCount = newEntry.length;

  const mentalStateFilters = ['All', 'Normal', 'Stress', 'Anxiety', 'Depression'];

  // Fetch journal entries from backend on component mount
  useEffect(() => {
    fetchEntries();
  }, []);

  const fetchEntries = async () => {
    try {
      setIsLoading(true);
      setError(null);
      const response = await getJournalHistory(1, 50); // Get last 50 entries
      setEntries(response.entries);
    } catch (err: any) {
      console.error('Failed to fetch journal entries:', err);
      setError(err.response?.data?.error || 'Failed to load journal entries');
    } finally {
      setIsLoading(false);
    }
  };

  const filteredEntries = selectedFilter === 'All' 
    ? entries 
    : entries.filter(entry => entry.mental_state.toLowerCase() === selectedFilter.toLowerCase());

  const handleSaveEntry = async () => {
    if (newEntry.trim().length < 10) {
      alert('Please write at least 10 characters to save your entry.');
      return;
    }

    try {
      setIsSaving(true);
      setError(null);
      
      // Call ML model to analyze the entry
      const prediction = await predictEmotion(newEntry);
      
      // Entry is already saved in backend, just refresh the list
      await fetchEntries();
      
      setNewEntry('');
      setShowSuccess(true);
      setTimeout(() => setShowSuccess(false), 3000);
    } catch (err: any) {
      console.error('Failed to save entry:', err);
      setError(err.response?.data?.error || 'Failed to save journal entry');
    } finally {
      setIsSaving(false);
    }
  };

  const handleDeleteEntry = async (id: string) => {
    if (confirm('Are you sure you want to delete this entry?')) {
      try {
        await deleteJournalEntry(id);
        // Remove from local state
        setEntries(entries.filter(entry => entry.id !== id));
      } catch (err: any) {
        console.error('Failed to delete entry:', err);
        alert(err.response?.data?.error || 'Failed to delete entry');
      }
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const today = new Date();
    const yesterday = new Date(today);
    yesterday.setDate(yesterday.getDate() - 1);

    if (date.toDateString() === today.toDateString()) {
      return 'Today';
    } else if (date.toDateString() === yesterday.toDateString()) {
      return 'Yesterday';
    } else {
      return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
    }
  };

  const formatTime = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
  };

  const getTopEmotions = (emotions: Record<string, number>, count: number = 3) => {
    return Object.entries(emotions)
      .sort(([, a], [, b]) => b - a)
      .slice(0, count)
      .map(([emotion, score]) => ({
        emotion: emotion.charAt(0).toUpperCase() + emotion.slice(1),
        score: Math.round(score * 100)
      }));
  };

  return (
    <DashboardLayout>
      <div className="space-y-8">
        {/* Header */}
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Mood Journal</h1>
          <p className="text-gray-600 mt-2">Track your emotional journey and reflect on your feelings</p>
        </div>

        {/* Error Message */}
        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 flex items-center gap-3">
            <i className="ri-error-warning-line text-red-600 text-xl"></i>
            <p className="text-red-800">{error}</p>
          </div>
        )}

        {/* Success Message */}
        {showSuccess && (
          <div className="bg-teal-50 border border-teal-200 rounded-lg p-4 flex items-center gap-3">
            <i className="ri-checkbox-circle-fill text-teal-600 text-xl"></i>
            <p className="text-teal-800 font-medium">Journal entry analyzed and saved successfully!</p>
          </div>
        )}

        {/* Journal Editor */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <div className="flex items-center gap-2 mb-4">
            <i className="ri-quill-pen-line text-teal-600 text-xl"></i>
            <h2 className="text-xl font-semibold text-gray-900">Write New Entry</h2>
          </div>
          
          <textarea
            value={newEntry}
            onChange={(e) => setNewEntry(e.target.value.slice(0, maxChars))}
            placeholder="How are you feeling today? Write about your emotions, thoughts, and experiences..."
            className="w-full h-40 p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent resize-none text-gray-700"
            disabled={isSaving}
          />
          
          <div className="flex items-center justify-between mt-4">
            <div className="flex items-center gap-2 text-sm text-gray-500">
              <i className="ri-lock-line"></i>
              <span>Your entries are private and secure</span>
            </div>
            <span className={`text-sm font-medium ${charCount > maxChars * 0.9 ? 'text-orange-600' : 'text-gray-500'}`}>
              {charCount} / {maxChars}
            </span>
          </div>

          <button
            onClick={handleSaveEntry}
            disabled={charCount < 10 || isSaving}
            className="mt-4 px-6 py-3 bg-teal-600 text-white rounded-lg font-medium hover:bg-teal-700 transition-colors disabled:bg-gray-300 disabled:cursor-not-allowed whitespace-nowrap w-full sm:w-auto flex items-center justify-center gap-2"
          >
            {isSaving ? (
              <>
                <i className="ri-loader-4-line animate-spin"></i>
                Analyzing with AI...
              </>
            ) : (
              <>
                <i className="ri-save-line"></i>
                Save & Analyze Entry
              </>
            )}
          </button>
        </div>

        {/* Filter Bar */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-4">
          <div className="flex items-center gap-2 mb-3">
            <i className="ri-filter-3-line text-gray-600"></i>
            <span className="text-sm font-medium text-gray-700">Filter by mental state:</span>
          </div>
          <div className="flex flex-wrap gap-2">
            {mentalStateFilters.map((filter) => (
              <button
                key={filter}
                onClick={() => setSelectedFilter(filter)}
                className={`px-4 py-2 rounded-full text-sm font-medium transition-all whitespace-nowrap ${
                  selectedFilter === filter
                    ? 'bg-teal-600 text-white shadow-md'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                {filter}
              </button>
            ))}
          </div>
        </div>

        {/* Timeline */}
        <div>
          <h2 className="text-xl font-semibold text-gray-900 mb-4 flex items-center gap-2">
            <i className="ri-time-line text-teal-600"></i>
            Journal Timeline
            <span className="text-sm font-normal text-gray-500 ml-2">
              ({filteredEntries.length} {filteredEntries.length === 1 ? 'entry' : 'entries'})
            </span>
          </h2>

          {isLoading ? (
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-12 text-center">
              <div className="w-16 h-16 border-4 border-teal-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
              <p className="text-gray-600">Loading your journal entries...</p>
            </div>
          ) : filteredEntries.length === 0 ? (
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-12 text-center">
              <div className="w-24 h-24 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <i className="ri-file-list-3-line text-4xl text-gray-400"></i>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">No entries found</h3>
              <p className="text-gray-600">
                {selectedFilter === 'All' 
                  ? 'Start writing your first journal entry to track your emotional journey.'
                  : `No entries found with "${selectedFilter}" mental state. Try a different filter.`}
              </p>
            </div>
          ) : (
            <div className="space-y-4">
              {filteredEntries.map((entry, index) => {
                const topEmotions = getTopEmotions(entry.emotions);
                const mentalStateKey = entry.mental_state.toLowerCase() as keyof typeof mentalStateColors;
                const severityKey = entry.severity.toLowerCase() as keyof typeof severityColors;
                
                return (
                  <div
                    key={entry.id}
                    className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow"
                  >
                    <div className="flex items-start justify-between mb-3">
                      <div className="flex items-center gap-3">
                        <div className="w-10 h-10 bg-teal-100 rounded-full flex items-center justify-center">
                          <span className="text-teal-700 font-semibold">{index + 1}</span>
                        </div>
                        <div>
                          <p className="text-sm font-medium text-gray-900">{formatDate(entry.created_at)}</p>
                          <p className="text-xs text-gray-500">{formatTime(entry.created_at)}</p>
                        </div>
                      </div>
                      <button
                        onClick={() => handleDeleteEntry(entry.id)}
                        className="text-gray-400 hover:text-red-600 transition-colors p-2"
                        title="Delete entry"
                      >
                        <i className="ri-delete-bin-line text-lg"></i>
                      </button>
                    </div>

                    <p className="text-gray-700 leading-relaxed mb-4">{entry.text}</p>

                    {/* ML Detection Results */}
                    <div className="space-y-3">
                      {/* Mental State and Severity */}
                      <div className="flex flex-wrap items-center gap-2">
                        <span className={`px-3 py-1.5 rounded-full text-sm font-medium border ${mentalStateColors[mentalStateKey] || mentalStateColors.normal}`}>
                          <i className="ri-brain-line mr-1"></i>
                          {entry.mental_state.charAt(0).toUpperCase() + entry.mental_state.slice(1)}
                        </span>
                        <span className={`px-3 py-1.5 rounded-full text-sm font-medium ${severityColors[severityKey] || severityColors.none}`}>
                          <i className="ri-pulse-line mr-1"></i>
                          {entry.severity.charAt(0).toUpperCase() + entry.severity.slice(1)} ({Math.round(entry.severity_score * 100)}%)
                        </span>
                      </div>

                      {/* Top Detected Emotions */}
                      <div className="flex flex-wrap items-center gap-2">
                        <span className="text-xs text-gray-500 font-medium">Top Emotions:</span>
                        {topEmotions.map((emotion, i) => (
                          <span 
                            key={i}
                            className="px-2 py-1 bg-gray-100 text-gray-700 rounded text-xs font-medium"
                          >
                            {emotion.emotion} {emotion.score}%
                          </span>
                        ))}
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>
      </div>
    </DashboardLayout>
  );
}