"""
Emotion-Aware Recommendation Engine for personalized wellness suggestions
Uses specific emotions detected by ML model to generate contextual recommendations
"""

class RecommendationEngine:
    """Generate emotion-aware personalized recommendations based on detected emotions"""
    
    # Emotion cluster definitions - maps individual emotions to their therapeutic categories
    EMOTION_CLUSTERS = {
        'anger': ['anger', 'annoyance', 'disapproval'],
        'rage': ['anger', 'disgust', 'disapproval'],
        'fear': ['fear', 'nervousness', 'confusion'],
        'sadness': ['sadness', 'disappointment', 'grief', 'remorse'],
        'anxiety': ['nervousness', 'fear', 'confusion', 'embarrassment'],
        'grief': ['grief', 'sadness', 'remorse', 'disappointment'],
        'social_stress': ['embarrassment', 'disapproval', 'nervousness', 'confusion'],
        'frustration': ['annoyance', 'disapproval', 'anger'],
        'overwhelm': ['confusion', 'nervousness', 'fear', 'sadness'],
        'positive': ['joy', 'gratitude', 'love', 'pride', 'optimism', 'relief', 'excitement', 'amusement', 'admiration', 'caring', 'approval'],
        'calm': ['realization', 'curiosity', 'desire', 'approval', 'relief', 'caring']
    }
    
    # Emotion-specific wellness recommendations
    EMOTION_RECOMMENDATIONS = {
        'anger': [
            {
                'title': 'Anger Release Exercise',
                'description': 'Physical activity like punch bag, running, or intensive workout to channel anger energy',
                'type': 'exercise',
                'duration': '20-30 minutes',
                'icon': '🥊'
            },
            {
                'title': 'Cooling Down Technique',
                'description': 'Count to 10 slowly, take deep breaths, step away from the situation temporarily',
                'type': 'coping',
                'duration': '5 minutes',
                'icon': '❄️'
            },
            {
                'title': 'Express Assertively',
                'description': 'Use "I feel..." statements to communicate your anger constructively without aggression',
                'type': 'communication',
                'duration': '10 minutes',
                'icon': '💬'
            },
            {
                'title': 'Identify Triggers',
                'description': 'Journal about what triggered your anger and explore underlying needs or boundaries',
                'type': 'journaling',
                'duration': '15 minutes',
                'icon': '📓'
            }
        ],
        'rage': [
            {
                'title': '🚨 Immediate Safety First',
                'description': 'Remove yourself from the situation. Use physical distance to prevent harmful actions',
                'type': 'safety',
                'duration': 'Immediate',
                'icon': '⚠️',
                'urgent': True
            },
            {
                'title': 'Intensive Physical Release',
                'description': 'High-intensity exercise, punch bag, or scream into pillow to release intense energy',
                'type': 'exercise',
                'duration': '30 minutes',
                'icon': '💥'
            },
            {
                'title': 'Anger Management Support',
                'description': 'Contact therapist or anger management counselor for professional guidance',
                'type': 'professional',
                'duration': 'Schedule appointment',
                'icon': '🏥'
            },
            {
                'title': 'Cold Water Therapy',
                'description': 'Splash cold water on face or take cold shower to activate calming response',
                'type': 'coping',
                'duration': '5 minutes',
                'icon': '🚿'
            }
        ],
        'fear': [
            {
                'title': 'Grounding Technique (5-4-3-2-1)',
                'description': 'Name 5 things you see, 4 you feel, 3 you hear, 2 you smell, 1 you taste',
                'type': 'grounding',
                'duration': '5 minutes',
                'icon': '🎯'
            },
            {
                'title': 'Safety Action Plan',
                'description': 'Identify what makes you feel safe and secure. Create a specific safety plan',
                'type': 'planning',
                'duration': '15 minutes',
                'icon': '🛡️'
            },
            {
                'title': 'Fear Exposure Journaling',
                'description': 'Write about your fears in detail. Often naming them reduces their power',
                'type': 'journaling',
                'duration': '10 minutes',
                'icon': '📝'
            },
            {
                'title': 'Calming Visualization',
                'description': 'Visualize a safe, peaceful place in detail. Engage all your senses',
                'type': 'meditation',
                'duration': '10 minutes',
                'icon': '🌅'
            }
        ],
        'sadness': [
            {
                'title': 'Emotional Release',
                'description': 'Allow yourself to cry or express sadness freely. Emotional release is healing',
                'type': 'coping',
                'duration': '15 minutes',
                'icon': '💧'
            },
            {
                'title': 'Mood-Lifting Activity',
                'description': 'Engage in something you usually enjoy: music, art, nature walk, or favorite hobby',
                'type': 'activity',
                'duration': '30 minutes',
                'icon': '🎨'
            },
            {
                'title': 'Social Connection',
                'description': 'Reach out to supportive friend or family member. Share your feelings if comfortable',
                'type': 'social',
                'duration': '20 minutes',
                'icon': '🤝'
            },
            {
                'title': 'Self-Compassion Practice',
                'description': 'Treat yourself with kindness as you would a good friend going through hard times',
                'type': 'meditation',
                'duration': '10 minutes',
                'icon': '💚'
            }
        ],
        'grief': [
            {
                'title': 'Honor Your Grief',
                'description': 'Create space to grieve. Light a candle, look at photos, or write a letter to whom/what you lost',
                'type': 'ritual',
                'duration': '20 minutes',
                'icon': '🕯️'
            },
            {
                'title': 'Grief Support Group',
                'description': 'Connect with others who understand loss. Shared grief can be deeply healing',
                'type': 'social',
                'duration': 'Weekly meetings',
                'icon': '👥'
            },
            {
                'title': 'Grief Counseling',
                'description': 'Consider working with a grief counselor or therapist specializing in loss',
                'type': 'professional',
                'duration': 'Regular sessions',
                'icon': '🏥'
            },
            {
                'title': 'Memory Journaling',
                'description': 'Write about your memories, feelings, and what you miss. This honors the loss',
                'type': 'journaling',
                'duration': '20 minutes',
                'icon': '📖'
            }
        ],
        'anxiety': [
            {
                'title': 'Box Breathing Exercise',
                'description': 'Breathe in 4 counts, hold 4, out 4, hold 4. Repeat until calm',
                'type': 'breathing',
                'duration': '5-10 minutes',
                'icon': '🌬️'
            },
            {
                'title': 'Progressive Muscle Relaxation',
                'description': 'Systematically tense and release muscle groups from toes to head',
                'type': 'relaxation',
                'duration': '15 minutes',
                'icon': '💆'
            },
            {
                'title': 'Worry Time Scheduling',
                'description': 'Set aside 15 minutes for worries. Outside that time, postpone anxious thoughts',
                'type': 'technique',
                'duration': '15 minutes',
                'icon': '⏰'
            },
            {
                'title': 'Reduce Caffeine & Stimulants',
                'description': 'Limit coffee, energy drinks, and sugar which can increase anxiety',
                'type': 'lifestyle',
                'duration': 'Ongoing',
                'icon': '☕'
            }
        ],
        'social_stress': [
            {
                'title': 'Self-Esteem Affirmations',
                'description': 'Write and repeat positive affirmations about yourself. You are enough',
                'type': 'affirmation',
                'duration': '5 minutes',
                'icon': '⭐'
            },
            {
                'title': 'Perspective Taking',
                'description': 'Remember others are focused on themselves, not judging you as much as you think',
                'type': 'cognitive',
                'duration': '10 minutes',
                'icon': '🔄'
            },
            {
                'title': 'Social Skills Practice',
                'description': 'Start small: smile at strangers, casual small talk, gradually build confidence',
                'type': 'practice',
                'duration': 'Daily',
                'icon': '👋'
            },
            {
                'title': 'Reframe the Narrative',
                'description': 'Challenge negative self-talk. Would you judge a friend this harshly?',
                'type': 'cognitive',
                'duration': '10 minutes',
                'icon': '💭'
            }
        ],
        'frustration': [
            {
                'title': 'Problem-Solving Session',
                'description': 'Break down the frustrating situation into smaller, actionable steps',
                'type': 'planning',
                'duration': '15 minutes',
                'icon': '🧩'
            },
            {
                'title': 'Set Realistic Expectations',
                'description': 'Adjust expectations. Perfection is impossible. Progress over perfection',
                'type': 'cognitive',
                'duration': '10 minutes',
                'icon': '🎯'
            },
            {
                'title': 'Take a Strategic Break',
                'description': 'Step away completely from the frustrating task. Return with fresh perspective',
                'type': 'coping',
                'duration': '20-30 minutes',
                'icon': '⏸️'
            },
            {
                'title': 'Express and Release',
                'description': 'Vent in journal, voice memo, or to trusted friend. Get it out of your system',
                'type': 'expression',
                'duration': '15 minutes',
                'icon': '📣'
            }
        ],
        'overwhelm': [
            {
                'title': 'Priority Simplification',
                'description': 'List everything overwhelming you. Pick top 3 priorities. Postpone or delegate rest',
                'type': 'planning',
                'duration': '20 minutes',
                'icon': '📋'
            },
            {
                'title': 'One Thing at a Time',
                'description': 'Stop multitasking. Focus completely on one task until completion or break',
                'type': 'technique',
                'duration': 'Ongoing',
                'icon': '1️⃣'
            },
            {
                'title': 'Seek Support',
                'description': 'Ask for help. Delegate tasks. You don\'t have to do everything alone',
                'type': 'social',
                'duration': '15 minutes',
                'icon': '🆘'
            },
            {
                'title': 'Restorative Rest',
                'description': 'Give yourself permission to rest. Take a nap, lie down, or do absolutely nothing',
                'type': 'rest',
                'duration': '30-60 minutes',
                'icon': '😴'
            }
        ],
        'positive': [
            {
                'title': 'Gratitude Amplification',
                'description': 'Write down what you\'re grateful for and why. Savor the positive emotions',
                'type': 'journaling',
                'duration': '10 minutes',
                'icon': '🙏'
            },
            {
                'title': 'Share the Joy',
                'description': 'Tell someone about your positive experience. Sharing amplifies happiness',
                'type': 'social',
                'duration': '15 minutes',
                'icon': '✨'
            },
            {
                'title': 'Celebrate Mindfully',
                'description': 'Take time to truly celebrate. Don\'t rush past positive moments',
                'type': 'mindfulness',
                'duration': '10 minutes',
                'icon': '🎉'
            },
            {
                'title': 'Pay It Forward',
                'description': 'Use your positive energy to help or uplift someone else',
                'type': 'action',
                'duration': '20 minutes',
                'icon': '🎁'
            }
        ],
        'calm': [
            {
                'title': 'Mindful Observation',
                'description': 'Take a few minutes to simply observe your surroundings without judgment',
                'type': 'mindfulness',
                'duration': '10 minutes',
                'icon': '👁️'
            },
            {
                'title': 'Reflective Journaling',
                'description': 'Write about your thoughts and realizations in a stream-of-consciousness style',
                'type': 'journaling',
                'duration': '15 minutes',
                'icon': '📔'
            },
            {
                'title': 'Learn Something New',
                'description': 'Follow your curiosity - read, watch a documentary, or explore a new topic',
                'type': 'activity',
                'duration': '30 minutes',
                'icon': '📚'
            },
            {
                'title': 'Peaceful Activity',
                'description': 'Engage in a calm hobby like reading, drawing, or gentle stretching',
                'type': 'activity',
                'duration': '20 minutes',
                'icon': '🧘'
            }
        ]
    }
    
    # Crisis/severe fallback recommendations
    CRISIS_RECOMMENDATIONS = [
        {
            'title': '🚨 Immediate Professional Help',
            'description': 'Contact mental health professional, crisis counselor, or emergency services',
            'type': 'professional',
            'duration': 'Urgent',
            'icon': '🏥',
            'urgent': True
        },
        {
            'title': 'Crisis Helpline',
            'description': 'Call 988 (Suicide & Crisis Lifeline) or local mental health emergency number',
            'type': 'professional',
            'duration': 'Immediate',
            'icon': '☎️',
            'urgent': True
        },
        {
            'title': 'Safety First',
            'description': 'Remove access to means of harm. Stay with someone you trust or go to safe location',
            'type': 'safety',
            'duration': 'Immediate',
            'icon': '🛡️',
            'urgent': True
        },
        {
            'title': 'Emergency Support System',
            'description': 'Contact trusted friend, family member, or therapist immediately. Don\'t isolate',
            'type': 'social',
            'duration': 'Immediate',
            'icon': '👥'
        }
    ]
    
    # Recommendation database organized by mental state and severity (FALLBACK ONLY)
    RECOMMENDATIONS = {
        'depression': {
            'mild': [
                {
                    'title': 'Morning Sunlight Exposure',
                    'description': 'Spend 15-20 minutes in natural sunlight, preferably in the morning',
                    'type': 'lifestyle',
                    'duration': '15-20 minutes',
                    'icon': '☀️'
                },
                {
                    'title': 'Gratitude Journaling',
                    'description': 'Write down 3 things you are grateful for each day',
                    'type': 'journaling',
                    'duration': '5 minutes',
                    'icon': '📝'
                },
                {
                    'title': 'Light Physical Activity',
                    'description': 'Take a 20-minute walk outdoors or do gentle stretching',
                    'type': 'exercise',
                    'duration': '20 minutes',
                    'icon': '🚶'
                },
                {
                    'title': 'Social Connection',
                    'description': 'Reach out to a friend or family member for a brief chat',
                    'type': 'social',
                    'duration': '15 minutes',
                    'icon': '💬'
                }
            ],
            'moderate': [
                {
                    'title': 'Structured Daily Routine',
                    'description': 'Create and follow a consistent daily schedule with regular sleep and meal times',
                    'type': 'lifestyle',
                    'duration': 'Daily',
                    'icon': '📅'
                },
                {
                    'title': 'Mindfulness Meditation',
                    'description': 'Practice 15-minute guided meditation focusing on breath and body awareness',
                    'type': 'meditation',
                    'duration': '15 minutes',
                    'icon': '🧘'
                },
                {
                    'title': 'Regular Exercise',
                    'description': 'Engage in 30 minutes of moderate exercise like jogging, cycling, or swimming',
                    'type': 'exercise',
                    'duration': '30 minutes',
                    'icon': '🏃'
                },
                {
                    'title': 'Limit Screen Time',
                    'description': 'Reduce screen time, especially before bed. Avoid social media scrolling',
                    'type': 'lifestyle',
                    'duration': 'Evening',
                    'icon': '📵'
                },
                {
                    'title': 'Expressive Writing',
                    'description': 'Write freely about your thoughts and feelings for emotional release',
                    'type': 'journaling',
                    'duration': '20 minutes',
                    'icon': '✍️'
                }
            ],
            'severe': [
                {
                    'title': '🚨 Seek Professional Help',
                    'description': 'Contact a mental health professional or therapist immediately',
                    'type': 'professional',
                    'duration': 'Urgent',
                    'icon': '🏥',
                    'urgent': True
                },
                {
                    'title': 'Crisis Helpline',
                    'description': 'Call mental health crisis helpline for immediate support',
                    'type': 'professional',
                    'duration': 'Immediate',
                    'icon': '☎️',
                    'urgent': True
                },
                {
                    'title': 'Structured Support System',
                    'description': 'Inform trusted friends or family and establish a daily check-in routine',
                    'type': 'social',
                    'duration': 'Daily',
                    'icon': '👥'
                },
                {
                    'title': 'Gentle Self-Care',
                    'description': 'Focus on basic needs: sleep, nutrition, and hygiene',
                    'type': 'lifestyle',
                    'duration': 'Daily',
                    'icon': '💚'
                }
            ]
        },
        'anxiety': {
            'mild': [
                {
                    'title': 'Deep Breathing Exercise',
                    'description': '4-7-8 breathing: Inhale for 4 counts, hold for 7, exhale for 8',
                    'type': 'breathing',
                    'duration': '5 minutes',
                    'icon': '🌬️'
                },
                {
                    'title': 'Progressive Muscle Relaxation',
                    'description': 'Systematically tense and relax muscle groups from toes to head',
                    'type': 'relaxation',
                    'duration': '10 minutes',
                    'icon': '💆'
                },
                {
                    'title': 'Limit Caffeine',
                    'description': 'Reduce or eliminate coffee, energy drinks, and caffeinated beverages',
                    'type': 'lifestyle',
                    'duration': 'Daily',
                    'icon': '☕'
                },
                {
                    'title': 'Nature Walk',
                    'description': 'Spend time in nature, focusing on sights and sounds around you',
                    'type': 'exercise',
                    'duration': '20 minutes',
                    'icon': '🌳'
                }
            ],
            'moderate': [
                {
                    'title': 'Anxiety Management Meditation',
                    'description': 'Practice guided meditation specifically for anxiety reduction',
                    'type': 'meditation',
                    'duration': '15-20 minutes',
                    'icon': '🧘'
                },
                {
                    'title': 'Worry Journal',
                    'description': 'Write down worries and schedule specific "worry time" to address them',
                    'type': 'journaling',
                    'duration': '15 minutes',
                    'icon': '📓'
                },
                {
                    'title': 'Grounding Technique (5-4-3-2-1)',
                    'description': 'Name 5 things you see, 4 you feel, 3 you hear, 2 you smell, 1 you taste',
                    'type': 'coping',
                    'duration': '5 minutes',
                    'icon': '🎯'
                },
                {
                    'title': 'Regular Sleep Schedule',
                    'description': 'Maintain consistent sleep and wake times, aim for 7-9 hours',
                    'type': 'lifestyle',
                    'duration': 'Daily',
                    'icon': '😴'
                },
                {
                    'title': 'Yoga Practice',
                    'description': 'Gentle yoga focusing on breath coordination and body awareness',
                    'type': 'exercise',
                    'duration': '30 minutes',
                    'icon': '🧘‍♀️'
                }
            ],
            'severe': [
                {
                    'title': '🚨 Professional Assessment',
                    'description': 'Seek evaluation from a mental health professional or psychiatrist',
                    'type': 'professional',
                    'duration': 'Urgent',
                    'icon': '🏥',
                    'urgent': True
                },
                {
                    'title': 'Emergency Breathing Protocol',
                    'description': 'Practice box breathing: 4 counts in, hold 4, out 4, hold 4',
                    'type': 'breathing',
                    'duration': '10 minutes',
                    'icon': '🌬️'
                },
                {
                    'title': 'Avoid Triggers',
                    'description': 'Identify and temporarily avoid known anxiety triggers',
                    'type': 'lifestyle',
                    'duration': 'Ongoing',
                    'icon': '⚠️'
                },
                {
                    'title': 'Structured Support',
                    'description': 'Establish regular check-ins with therapist or support group',
                    'type': 'professional',
                    'duration': 'Weekly',
                    'icon': '👥'
                }
            ]
        },
        'stress': {
            'mild': [
                {
                    'title': 'Time Management',
                    'description': 'Prioritize tasks using a to-do list, focus on one thing at a time',
                    'type': 'lifestyle',
                    'duration': '15 minutes',
                    'icon': '✅'
                },
                {
                    'title': 'Quick Relaxation Break',
                    'description': 'Take 5-minute breaks every hour to stretch and breathe deeply',
                    'type': 'relaxation',
                    'duration': '5 minutes',
                    'icon': '⏸️'
                },
                {
                    'title': 'Physical Activity',
                    'description': 'Engage in 20-30 minutes of physical exercise to release tension',
                    'type': 'exercise',
                    'duration': '20-30 minutes',
                    'icon': '🏋️'
                },
                {
                    'title': 'Hobby Time',
                    'description': 'Spend time on enjoyable activities unrelated to work or stress',
                    'type': 'lifestyle',
                    'duration': '30 minutes',
                    'icon': '🎨'
                }
            ],
            'moderate': [
                {
                    'title': 'Stress Management Meditation',
                    'description': 'Practice body scan meditation to release physical tension',
                    'type': 'meditation',
                    'duration': '15 minutes',
                    'icon': '🧘'
                },
                {
                    'title': 'Set Boundaries',
                    'description': 'Learn to say no and establish clear work-life boundaries',
                    'type': 'lifestyle',
                    'duration': 'Ongoing',
                    'icon': '🚧'
                },
                {
                    'title': 'Intensive Exercise',
                    'description': 'High-intensity workout or sports to channel stress energy',
                    'type': 'exercise',
                    'duration': '30-45 minutes',
                    'icon': '💪'
                },
                {
                    'title': 'Social Support',
                    'description': 'Talk to trusted friends or family about your stressors',
                    'type': 'social',
                    'duration': '30 minutes',
                    'icon': '🗣️'
                },
                {
                    'title': 'Digital Detox',
                    'description': 'Take breaks from email, notifications, and social media',
                    'type': 'lifestyle',
                    'duration': 'Evening',
                    'icon': '📴'
                }
            ],
            'severe': [
                {
                    'title': '⚠️ Professional Stress Management',
                    'description': 'Consult a counselor or therapist specializing in stress management',
                    'type': 'professional',
                    'duration': 'Schedule appointment',
                    'icon': '🏥',
                    'urgent': True
                },
                {
                    'title': 'Immediate Load Reduction',
                    'description': 'Delegate tasks, take time off, or reduce commitments immediately',
                    'type': 'lifestyle',
                    'duration': 'Immediate',
                    'icon': '🔻'
                },
                {
                    'title': 'Daily Stress Release',
                    'description': 'Commit to daily meditation, exercise, or relaxation practice',
                    'type': 'meditation',
                    'duration': '30 minutes',
                    'icon': '🧘‍♂️'
                },
                {
                    'title': 'Review Life Balance',
                    'description': 'Assess and restructure priorities with professional guidance',
                    'type': 'professional',
                    'duration': 'Ongoing',
                    'icon': '⚖️'
                }
            ]
        },
        'normal': [
            {
                'title': 'Maintain Good Habits',
                'description': 'Continue your healthy routines: exercise, sleep, and balanced diet',
                'type': 'lifestyle',
                'duration': 'Daily',
                'icon': '✨'
            },
            {
                'title': 'Preventive Meditation',
                'description': 'Practice mindfulness meditation to maintain emotional balance',
                'type': 'meditation',
                'duration': '10 minutes',
                'icon': '🧘'
            },
            {
                'title': 'Social Connection',
                'description': 'Nurture relationships with friends and family',
                'type': 'social',
                'duration': 'Regular',
                'icon': '👫'
            },
            {
                'title': 'Personal Growth',
                'description': 'Engage in learning, hobbies, or activities that bring you joy',
                'type': 'lifestyle',
                'duration': 'Weekly',
                'icon': '🌱'
            }
        ]
    }
    
    @staticmethod
    def analyze_emotional_profile(emotions):
        """
        Analyze emotions dict to identify dominant emotion clusters
        
        Args:
            emotions: Dict of emotion names to probability scores (0-1)
            
        Returns:
            List of (cluster_name, intensity) tuples, sorted by intensity
        """
        cluster_scores = {}
        
        # Calculate score for each emotion cluster based on detected emotions
        for cluster_name, cluster_emotions in RecommendationEngine.EMOTION_CLUSTERS.items():
            cluster_score = 0
            matching_emotions = []
            
            for emotion in cluster_emotions:
                if emotion in emotions:
                    cluster_score += emotions[emotion]
                    matching_emotions.append((emotion, emotions[emotion]))
            
            if cluster_score > 0:
                # Use the maximum emotion intensity in cluster for prioritization
                max_intensity = max([score for _, score in matching_emotions]) if matching_emotions else 0
                cluster_scores[cluster_name] = {
                    'total_score': cluster_score,
                    'max_intensity': max_intensity,
                    'emotion_count': len(matching_emotions),
                    'emotions': matching_emotions
                }
        
        # Sort clusters by maximum intensity (most intense emotion matters most)
        sorted_clusters = sorted(
            cluster_scores.items(),
            key=lambda x: (x[1]['max_intensity'], x[1]['total_score']),
            reverse=True
        )
        
        return [(name, data['max_intensity']) for name, data in sorted_clusters]
    
    @staticmethod
    def get_emotion_aware_recommendations(emotions, mental_state='normal', severity='mild', max_recommendations=4):
        """
        Generate personalized recommendations based on specific detected emotions
        
        Args:
            emotions: Dict of emotion names to probability scores (e.g., {'sadness': 0.82, 'disappointment': 0.34})
            mental_state: Fallback mental state classification
            severity: Severity level (mild, moderate, severe)
            max_recommendations: Maximum number of recommendations to return
            
        Returns:
            List of recommendation dictionaries
        """
        # Handle crisis/severe cases first
        if severity == 'severe':
            # Check for suicidal/crisis emotions
            crisis_emotions = ['grief', 'sadness', 'remorse', 'disappointment']
            high_intensity_crisis = any(
                emotions.get(e, 0) > 0.7 for e in crisis_emotions
            )
            
            if high_intensity_crisis and mental_state == 'depression':
                return RecommendationEngine.CRISIS_RECOMMENDATIONS[:max_recommendations]
        
        # Analyze emotional profile to identify dominant clusters
        emotion_clusters = RecommendationEngine.analyze_emotional_profile(emotions)
        
        if not emotion_clusters:
            # No significant emotions detected, use mental state fallback
            return RecommendationEngine._fallback_recommendations(mental_state, severity, max_recommendations)
        
        # Collect recommendations from detected emotion clusters
        collected_recommendations = []
        seen_titles = set()
        
        # Prioritize recommendations from top emotion clusters
        for cluster_name, intensity in emotion_clusters[:3]:  # Top 3 emotion clusters
            if cluster_name in RecommendationEngine.EMOTION_RECOMMENDATIONS:
                cluster_recs = RecommendationEngine.EMOTION_RECOMMENDATIONS[cluster_name]
                
                # Add recommendations from this cluster (avoid duplicates)
                for rec in cluster_recs:
                    if rec['title'] not in seen_titles:
                        # Add intensity context to recommendation
                        rec_copy = rec.copy()
                        rec_copy['emotion_cluster'] = cluster_name
                        rec_copy['emotion_intensity'] = round(intensity * 100)
                        collected_recommendations.append(rec_copy)
                        seen_titles.add(rec['title'])
                        
                        if len(collected_recommendations) >= max_recommendations:
                            break
                
                if len(collected_recommendations) >= max_recommendations:
                    break
        
        # If we have enough recommendations, return them
        if len(collected_recommendations) >= max_recommendations:
            return collected_recommendations[:max_recommendations]
        
        # If not enough emotion-specific recs, supplement with mental state recommendations
        fallback_recs = RecommendationEngine._fallback_recommendations(mental_state, severity, max_recommendations - len(collected_recommendations))
        for rec in fallback_recs:
            if rec['title'] not in seen_titles:
                collected_recommendations.append(rec)
                seen_titles.add(rec['title'])
                if len(collected_recommendations) >= max_recommendations:
                    break
        
        return collected_recommendations[:max_recommendations]
    
    @staticmethod
    def _fallback_recommendations(mental_state, severity, count):
        """Fallback to mental state-based recommendations"""
        if mental_state == 'normal' or severity == 'none':
            return RecommendationEngine.RECOMMENDATIONS['normal'][:count]
        
        if mental_state in RecommendationEngine.RECOMMENDATIONS:
            if severity in RecommendationEngine.RECOMMENDATIONS[mental_state]:
                return RecommendationEngine.RECOMMENDATIONS[mental_state][severity][:count]
        
        # Ultimate fallback
        return RecommendationEngine.RECOMMENDATIONS['normal'][:count]
    
    @staticmethod
    def get_recommendations(mental_state, severity='mild', emotions=None):
        """
        Main recommendation method - uses emotion-aware system if emotions provided
        
        Args:
            mental_state: One of 'depression', 'anxiety', 'stress', 'normal'
            severity: One of 'mild', 'moderate', 'severe', 'none'
            emotions: Optional dict of detected emotions (e.g., {'sadness': 0.82, 'fear': 0.45})
            
        Returns:
            List of recommendation dictionaries
        """
        # If emotions are provided, use emotion-aware system
        if emotions and isinstance(emotions, dict) and len(emotions) > 0:
            return RecommendationEngine.get_emotion_aware_recommendations(
                emotions=emotions,
                mental_state=mental_state,
                severity=severity,
                max_recommendations=4
            )
        
        # Otherwise, fall back to traditional mental state-based system
        if mental_state == 'normal' or severity == 'none':
            return RecommendationEngine.RECOMMENDATIONS['normal']
        
        if mental_state in RecommendationEngine.RECOMMENDATIONS:
            if severity in RecommendationEngine.RECOMMENDATIONS[mental_state]:
                return RecommendationEngine.RECOMMENDATIONS[mental_state][severity]
        
        # Default to normal recommendations
        return RecommendationEngine.RECOMMENDATIONS['normal']
    
    @staticmethod
    def get_daily_tip(mental_state='normal'):
        """Get a single daily wellness tip"""
        recommendations = RecommendationEngine.get_recommendations(mental_state, 'mild')
        if recommendations:
            return recommendations[0]
        return None
    
    @staticmethod
    def get_emergency_resources():
        """Get emergency mental health resources"""
        return {
            'crisis_helplines': [
                {
                    'name': 'National Suicide Prevention Lifeline',
                    'number': '988',
                    'description': '24/7 crisis support'
                },
                {
                    'name': 'Crisis Text Line',
                    'number': 'Text HOME to 741741',
                    'description': 'Text-based crisis support'
                },
                {
                    'name': 'SAMHSA National Helpline',
                    'number': '1-800-662-4357',
                    'description': 'Mental health and substance abuse support'
                }
            ],
            'message': 'If you are in crisis or experiencing severe distress, please reach out for professional help immediately.'
        }
