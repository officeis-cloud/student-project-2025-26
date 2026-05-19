import { useState } from 'react';
import DashboardLayout from '../../components/feature/DashboardLayout';
import EmotionResultCards from './components/EmotionResultCards';
import ExplainableInsights from './components/ExplainableInsights';
import AIRecommendations from './components/AIRecommendations';
import { predictEmotion } from '../../services/api';

interface EmotionResult {
  emotion: string;
  probability: number;
  color: string;
}

interface TriggerWord {
  word: string;
  indicator: string;
  category: 'depression' | 'stress' | 'anxiety' | 'fatigue';
  confidence: number;
}

interface StressTrigger {
  label: string;
  icon: string;
  severity: 'high' | 'medium' | 'low';
  description: string;
}

interface Recommendation {
  title: string;
  description: string;
  category: string;
}

export interface AnalysisResult {
  emotions: EmotionResult[];
  mentalState: string;
  severity: string;
  confidence: number;
  triggers: TriggerWord[];
  stressTriggers: StressTrigger[];
  heatmapData: number[][];
  originalText: string;
  recommendations?: Recommendation[];
}

const sampleInputs = [
  "I feel overwhelmed with exams.",
  "I feel lonely and tired lately.",
  "I feel happy and motivated today.",
  "I feel hopeless and exhausted, nothing seems to work out.",
  "Work pressure is making me anxious and I can't sleep well."
];

// Emotion to keyword mapping based on GoEmotions
const emotionKeywords: Record<string, { words: string[]; indicator: string; category: TriggerWord['category'] }> = {
  'sadness': { words: ['sad', 'unhappy', 'depressed', 'miserable', 'empty', 'hopeless'], indicator: 'Depression core indicator', category: 'depression' },
  'disappointment': { words: ['disappointed', 'let down', 'failed', 'useless'], indicator: 'Low self-esteem marker', category: 'depression' },
  'grief': { words: ['loss', 'grief', 'mourning', 'heartbroken'], indicator: 'Loss processing indicator', category: 'depression' },
  'fear': { words: ['afraid', 'scared', 'terrified', 'frightened', 'fear'], indicator: 'Fear activation marker', category: 'anxiety' },
  'nervousness': { words: ['nervous', 'anxious', 'worried', 'uneasy', 'tense'], indicator: 'Anxiety activation marker', category: 'anxiety' },
  'confusion': { words: ['confused', 'uncertain', 'lost', 'unclear'], indicator: 'Cognitive distress signal', category: 'anxiety' },
  'anger': { words: ['angry', 'furious', 'rage', 'mad', 'irritated'], indicator: 'Anger activation marker', category: 'stress' },
  'annoyance': { words: ['annoyed', 'irritated', 'bothered', 'frustrated'], indicator: 'Stress accumulation signal', category: 'stress' },
  'disgust': { words: ['disgusted', 'repulsed', 'sick'], indicator: 'Aversion response marker', category: 'stress' },
};

const generateTriggerKeywords = (text: string, emotions: Record<string, number>): TriggerWord[] => {
  const triggers: TriggerWord[] = [];
  const lower = text.toLowerCase();
  
  // For each detected emotion, check if related keywords appear in text
  Object.entries(emotions).forEach(([emotion, probability]) => {
    const emotionData = emotionKeywords[emotion.toLowerCase()];
    if (emotionData) {
      emotionData.words.forEach(word => {
        if (lower.includes(word)) {
          triggers.push({
            word,
            indicator: emotionData.indicator,
            category: emotionData.category,
            confidence: Math.round(probability * 100)
          });
        }
      });
    }
  });
  
  return triggers;
};

const buildStressTriggers = (mentalState: string, stateScores: any): StressTrigger[] => {
  const triggers: StressTrigger[] = [];
  
  // Add triggers based on actual mental state scores from ML model
  if (stateScores?.depression && stateScores.depression > 0.15) {
    const severity = stateScores.depression > 0.45 ? 'high' : stateScores.depression > 0.25 ? 'medium' : 'low';
    triggers.push({ 
      label: 'Depressive Symptoms', 
      icon: 'ri-mental-health-line', 
      severity, 
      description: `Detected ${Math.round(stateScores.depression * 100)}% depression indicators from emotional analysis` 
    });
  }
  
  if (stateScores?.anxiety && stateScores.anxiety > 0.15) {
    const severity = stateScores.anxiety > 0.45 ? 'high' : stateScores.anxiety > 0.25 ? 'medium' : 'low';
    triggers.push({ 
      label: 'Anxiety Indicators', 
      icon: 'ri-pulse-line', 
      severity, 
      description: `Detected ${Math.round(stateScores.anxiety * 100)}% anxiety markers from emotional analysis` 
    });
  }
  
  if (stateScores?.stress && stateScores.stress > 0.15) {
    const severity = stateScores.stress > 0.45 ? 'high' : stateScores.stress > 0.25 ? 'medium' : 'low';
    triggers.push({ 
      label: 'Stress Indicators', 
      icon: 'ri-flashlight-line', 
      severity, 
      description: `Detected ${Math.round(stateScores.stress * 100)}% stress signals from emotional analysis` 
    });
  }
  
  // If no significant triggers, it's a positive state
  if (triggers.length === 0) {
    triggers.push({ 
      label: 'Stable Emotional State', 
      icon: 'ri-emotion-happy-line', 
      severity: 'low', 
      description: 'No significant mental health concerns detected in emotional analysis' 
    });
  }
  
  return triggers;
};

const AnalyzePage = () => {
  const [text, setText] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [isSaved, setIsSaved] = useState(false);
  const [showSuccessBanner, setShowSuccessBanner] = useState(false);

  const handleSampleClick = (sample: string) => setText(sample);

  const analyzeEmotion = async () => {
    setIsAnalyzing(true);
    setResult(null);
    setIsSaved(false);
    setShowSuccessBanner(false);
    
    try {
      // Call real backend API
      const response = await predictEmotion(text);
      
      // Transform backend response to frontend format
      const emotionColors: Record<string, string> = {
        'sadness': '#3B82F6', 'joy': '#10B981', 'anger': '#EF4444', 
        'fear': '#8B5CF6', 'excitement': '#F59E0B', 'love': '#EC4899',
        'surprise': '#F59E0B', 'disgust': '#84CC16', 'confusion': '#06B6D4',
        'nervousness': '#8B5CF6', 'disappointment': '#6B7280', 'admiration': '#10B981',
        'gratitude': '#10B981', 'optimism': '#F59E0B', 'caring': '#EC4899',
        'pride': '#10B981', 'amusement': '#10B981', 'annoyance': '#EF4444',
        'disapproval': '#EF4444', 'embarrassment': '#EC4899', 'realization': '#06B6D4',
        'relief': '#10B981', 'remorse': '#6B7280', 'grief': '#3B82F6',
        'curiosity': '#06B6D4', 'desire': '#EC4899', 'approval': '#10B981'
      };
      
      // Convert emotions object to array and sort by probability
      const emotionsArray = Object.entries(response.emotions)
        .map(([emotion, probability]) => ({
          emotion: emotion.charAt(0).toUpperCase() + emotion.slice(1),
          probability: Math.round(probability * 100),
          color: emotionColors[emotion.toLowerCase()] || '#6B7280'
        }))
        .sort((a, b) => b.probability - a.probability)
        .slice(0, 5); // Top 5 emotions
      
      // Generate trigger keywords from detected emotions
      const foundTriggers = generateTriggerKeywords(text, response.emotions);
      
      // Map backend severity to frontend format
      const severityMap: Record<string, string> = {
        'none': 'Normal',
        'mild': 'Mild',
        'moderate': 'Moderate', 
        'severe': 'Severe'
      };
      
      const analysisResult: AnalysisResult = {
        originalText: text,
        emotions: emotionsArray,
        mentalState: response.mental_state.charAt(0).toUpperCase() + response.mental_state.slice(1),
        severity: severityMap[response.severity] || 'Normal',
        confidence: Math.round(response.severity_score * 100),
        triggers: foundTriggers,
        stressTriggers: buildStressTriggers(response.mental_state, response.state_scores),
        recommendations: response.recommendations,
        heatmapData: [] // Remove fake heatmap
      };
      
      setResult(analysisResult);
      // Entry is automatically saved to database by backend API
      setIsSaved(true);
    } catch (error) {
      console.error('Error analyzing emotion:', error);
      alert('Failed to analyze emotion. Please try again.');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleSaveToJournal = () => {
    if (!result || isSaved) return;
    
    // Entry was already saved to database by backend API during prediction
    // Just show the success banner
    setShowSuccessBanner(true);
  };

  return (
    <DashboardLayout>
      <div className="p-8 max-w-5xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-800 mb-2">Emotion Analysis</h1>
          <p className="text-gray-500 text-sm">Share your feelings and let AI analyze your emotional state with explainable insights</p>
        </div>

        {/* Input Section */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 mb-6">
          <label className="block text-sm font-semibold text-gray-700 mb-2">How are you feeling today?</label>
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value.slice(0, 500))}
            placeholder="Write how you feel today…"
            className="w-full h-40 px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent resize-none text-gray-700 text-sm leading-relaxed"
          />
          <div className="flex justify-between items-center mt-2 mb-4">
            <span className={`text-xs font-medium ${text.length >= 480 ? 'text-red-500' : 'text-gray-400'}`}>
              {text.length} / 500 characters
            </span>
            <div className="flex items-center gap-1.5 text-xs text-gray-400">
              <i className="ri-shield-check-line text-teal-500"></i>
              <span>Your entries are private and secure.</span>
            </div>
          </div>

          <p className="text-xs font-semibold text-gray-500 mb-2">Try a sample:</p>
          <div className="flex flex-wrap gap-2 mb-5">
            {sampleInputs.map((sample, i) => (
              <button
                key={i}
                onClick={() => handleSampleClick(sample)}
                className="px-3 py-1.5 bg-gray-50 hover:bg-teal-50 hover:border-teal-300 border border-gray-200 rounded-full text-xs text-gray-600 transition-colors whitespace-nowrap cursor-pointer"
              >
                {sample}
              </button>
            ))}
          </div>

          <button
            onClick={analyzeEmotion}
            disabled={!text.trim() || isAnalyzing}
            className="w-full py-3 bg-teal-600 hover:bg-teal-700 disabled:bg-gray-200 disabled:cursor-not-allowed text-white font-semibold rounded-lg transition-colors whitespace-nowrap cursor-pointer text-sm"
          >
            {isAnalyzing ? (
              <span className="flex items-center justify-center gap-2">
                <i className="ri-loader-4-line animate-spin"></i>
                Analyzing emotional state…
              </span>
            ) : (
              <span className="flex items-center justify-center gap-2">
                <i className="ri-brain-line"></i>
                Analyze Emotion
              </span>
            )}
          </button>
        </div>

        {/* Results */}
        {result && (
          <div className="space-y-6">
            <EmotionResultCards result={result} />
            <ExplainableInsights result={result} />
            
            {/* AI Recommendations */}
            {result.recommendations && result.recommendations.length > 0 && (
              <AIRecommendations 
                recommendations={result.recommendations} 
                mentalState={result.mentalState}
              />
            )}

            {/* Success Banner */}
            {showSuccessBanner && (
              <div className="bg-teal-50 border-l-4 border-teal-500 rounded-lg p-4 flex items-center justify-between shadow-sm">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 bg-teal-100 rounded-full flex items-center justify-center">
                    <i className="ri-checkbox-circle-fill text-teal-600 text-xl"></i>
                  </div>
                  <div>
                    <p className="text-teal-900 font-semibold">Analysis saved to your Mood Journal</p>
                    <p className="text-teal-700 text-sm">Your emotional insights have been recorded</p>
                  </div>
                </div>
                <a
                  href="/journal"
                  onClick={(e) => {
                    e.preventDefault();
                    window.REACT_APP_NAVIGATE('/journal');
                  }}
                  className="px-4 py-2 bg-teal-600 hover:bg-teal-700 text-white rounded-lg font-medium text-sm transition-colors whitespace-nowrap cursor-pointer flex items-center gap-2"
                >
                  View Journal
                  <i className="ri-arrow-right-line"></i>
                </a>
              </div>
            )}

            {/* Save to Journal Button */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 bg-teal-100 rounded-full flex items-center justify-center">
                    <i className="ri-save-line text-teal-600 text-xl"></i>
                  </div>
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900">Save Analysis to Journal</h3>
                    <p className="text-sm text-gray-600">Keep track of your emotional journey over time</p>
                  </div>
                </div>
                <button
                  onClick={handleSaveToJournal}
                  disabled={isSaved}
                  className={`px-6 py-3 rounded-lg font-semibold text-sm transition-all whitespace-nowrap cursor-pointer flex items-center gap-2 ${
                    isSaved
                      ? 'bg-gray-100 text-gray-500 cursor-not-allowed'
                      : 'bg-teal-600 hover:bg-teal-700 text-white shadow-md hover:shadow-lg'
                  }`}
                >
                  {isSaved ? (
                    <>
                      <i className="ri-checkbox-circle-fill"></i>
                      Saved
                    </>
                  ) : (
                    <>
                      <i className="ri-save-line"></i>
                      Save to Journal
                    </>
                  )}
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </DashboardLayout>
  );
};

export default AnalyzePage;
