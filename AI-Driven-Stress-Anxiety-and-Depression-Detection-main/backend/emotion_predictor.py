import warnings
warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', category=UserWarning)

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import numpy as np
import os

class EmotionPredictor:
    """Service for emotion prediction using trained DistilBERT model"""
    
    # GoEmotions 27 emotion labels
    EMOTION_LABELS = [
        'admiration', 'amusement', 'anger', 'annoyance', 'approval', 'caring',
        'confusion', 'curiosity', 'desire', 'disappointment', 'disapproval',
        'disgust', 'embarrassment', 'excitement', 'fear', 'gratitude', 'grief',
        'joy', 'love', 'nervousness', 'optimism', 'pride', 'realization',
        'relief', 'remorse', 'sadness', 'surprise'
    ]
    
    # Mapping emotions to mental states
    MENTAL_STATE_MAPPING = {
        'depression': ['sadness', 'grief', 'disappointment', 'remorse', 'disapproval'],
        'anxiety': ['fear', 'nervousness', 'confusion', 'annoyance'],
        'stress': ['anger', 'annoyance', 'disapproval', 'disgust', 'embarrassment']
    }
    
    def __init__(self, model_path=None):
        """Initialize the emotion predictor with trained model"""
        self.model = None
        self.tokenizer = None
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        if model_path and os.path.exists(model_path):
            self.load_model(model_path)
    
    def load_model(self, model_path):
        """Load the trained model and tokenizer"""
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_path)
            self.model = AutoModelForSequenceClassification.from_pretrained(model_path)
            self.model.to(self.device)
            self.model.eval()
            print(f"✅ Model loaded successfully from {model_path}")
            return True
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            return False
    
    def predict_emotions(self, text, threshold=0.5):
        """
        Predict emotions from text
        
        Args:
            text: Input text string
            threshold: Probability threshold for emotion detection
            
        Returns:
            Dictionary with emotion labels and their probabilities
        """
        if not self.model or not self.tokenizer:
            return {'error': 'Model not loaded'}
        
        try:
            # Tokenize input
            inputs = self.tokenizer(
                text,
                return_tensors='pt',
                truncation=True,
                padding=True,
                max_length=512
            )
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # Get predictions
            with torch.no_grad():
                outputs = self.model(**inputs)
                logits = outputs.logits
                probs = torch.sigmoid(logits).cpu().numpy()[0]
            
            # Filter emotions above threshold (ensure we don't exceed label count)
            emotions = {}
            num_labels = min(len(probs), len(self.EMOTION_LABELS))
            for idx in range(num_labels):
                if probs[idx] >= threshold:
                    emotions[self.EMOTION_LABELS[idx]] = float(probs[idx])
            
            # Sort by probability
            emotions = dict(sorted(emotions.items(), key=lambda x: x[1], reverse=True))
            
            return emotions
            
        except Exception as e:
            print(f"Error in prediction: {e}")
            return {'error': str(e)}
    
    def classify_mental_state(self, text):
        """
        Classify mental state and severity from text
        
        Returns:
            Dictionary with mental_state, severity, severity_score, and emotions
        """
        # Get emotion predictions with lower threshold to catch subtle emotions
        emotions = self.predict_emotions(text, threshold=0.15)
        
        if 'error' in emotions:
            return emotions
        
        # If no emotions detected
        if not emotions:
            return {
                'emotions': {},
                'mental_state': 'normal',
                'severity': 'none',
                'severity_score': 0.0,
                'state_scores': {'depression': 0.0, 'anxiety': 0.0, 'stress': 0.0}
            }
        
        # Calculate scores for each mental state
        # Use only detected emotions (above threshold) to avoid dilution
        state_scores = {}
        for state, emotion_list in self.MENTAL_STATE_MAPPING.items():
            # Get only emotions that were actually detected
            detected_scores = [emotions[emotion] for emotion in emotion_list if emotion in emotions]
            if detected_scores:
                # Use the maximum detected emotion for that state (more sensitive)
                state_scores[state] = max(detected_scores)
            else:
                state_scores[state] = 0
        
        # Get dominant mental state
        max_state = max(state_scores.items(), key=lambda x: x[1])
        mental_state = max_state[0] if max_state[1] > 0.20 else 'normal'
        severity_score = max_state[1]
        
        # Determine severity level based on mental state
        if mental_state == 'normal':
            severity = 'none'
        elif severity_score < 0.40:
            severity = 'mild'
        elif severity_score < 0.60:
            severity = 'moderate'
        else:
            severity = 'severe'
        
        return {
            'emotions': emotions,
            'mental_state': mental_state,
            'severity': severity,
            'severity_score': float(severity_score),
            'state_scores': {k: float(v) for k, v in state_scores.items()}
        }
    
    def get_top_emotions(self, text, top_n=5):
        """Get top N emotions from text"""
        emotions = self.predict_emotions(text)
        
        if 'error' in emotions:
            return emotions
        
        # Sort and get top N
        sorted_emotions = sorted(emotions.items(), key=lambda x: x[1], reverse=True)
        return dict(sorted_emotions[:top_n])


# Global predictor instance (loaded on app startup)
emotion_predictor = EmotionPredictor()
