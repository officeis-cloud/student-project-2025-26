
import { useState, useEffect } from 'react';
import DashboardLayout from '../../components/feature/DashboardLayout';
import WellnessHeader from './components/WellnessHeader';
import EmotionalStateSelector from './components/EmotionalStateSelector';
import DailyWellnessPlan from './components/DailyWellnessPlan';
import WellnessTips from './components/WellnessTips';
import ResourcesSection from './components/ResourcesSection';
import { getJournalHistory } from '../../services/api';

export type EmotionalState = 'stress' | 'anxiety' | 'depression' | 'normal';

export default function WellnessPage() {
  const [activeState, setActiveState] = useState<EmotionalState>('stress');
  const [loading, setLoading] = useState(true);

  // Fetch latest journal entry to determine actual emotional state
  useEffect(() => {
    const fetchLatestState = async () => {
      try {
        const response = await getJournalHistory(1, 1);
        if (response.entries.length > 0) {
          const latestEntry = response.entries[0];
          // Map backend mental states to wellness page states
          const stateMap: Record<string, EmotionalState> = {
            'depression': 'depression',
            'anxiety': 'anxiety',
            'stress': 'stress',
            'normal': 'normal'
          };
          const detectedState = stateMap[latestEntry.mental_state.toLowerCase()] || 'normal';
          setActiveState(detectedState);
        }
      } catch (error) {
        console.error('Failed to fetch latest emotional state:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchLatestState();
  }, []);

  if (loading) {
    return (
      <DashboardLayout>
        <div className="p-8 flex justify-center items-center min-h-screen">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-teal-500"></div>
        </div>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <div className="p-8 space-y-8">
        <WellnessHeader />
        <EmotionalStateSelector activeState={activeState} onSelect={setActiveState} />
        <DailyWellnessPlan activeState={activeState} />
        <WellnessTips activeState={activeState} />
        <ResourcesSection />
      </div>
    </DashboardLayout>
  );
}
