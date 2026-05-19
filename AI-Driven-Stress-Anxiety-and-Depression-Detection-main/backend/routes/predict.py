from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User, MoodEntry
from emotion_predictor import emotion_predictor
from recommendation_engine import RecommendationEngine
from datetime import datetime, timedelta
from bson import ObjectId

predict_bp = Blueprint('predict', __name__, url_prefix='/api/predict')

@predict_bp.route('', methods=['POST'])
@predict_bp.route('/', methods=['POST'])
@jwt_required()
def predict_emotion():
    """
    Analyze text and predict emotions, mental state, and provide recommendations
    """
    try:
        current_user_id = get_jwt_identity()  # JWT identity is string ObjectId
        data = request.get_json()
        
        # Validate input
        if not data.get('text'):
            return jsonify({'error': 'Text is required'}), 400
        
        text = data['text'].strip()
        
        if len(text) < 10:
            return jsonify({'error': 'Text too short. Please write at least 10 characters'}), 400
        
        # Predict mental state and emotions
        prediction = emotion_predictor.classify_mental_state(text)
        
        if 'error' in prediction:
            return jsonify({'error': prediction['error']}), 500
        
        # Get emotion-aware recommendations based on detected emotions
        recommendations = RecommendationEngine.get_recommendations(
            mental_state=prediction['mental_state'],
            severity=prediction['severity'],
            emotions=prediction['emotions']  # Pass detected emotions for contextual recommendations
        )
        
        # Save mood entry to database
        mood_entry = MoodEntry(
            user_id=ObjectId(current_user_id),
            text=text,
            emotions=prediction['emotions'],
            mental_state=prediction['mental_state'],
            severity=prediction['severity'],
            severity_score=prediction['severity_score'],
            recommendations=[rec['title'] for rec in recommendations]
        )
        mood_entry.save()
        
        # Return complete prediction result
        return jsonify({
            'success': True,
            'entry_id': str(mood_entry.id),
            'emotions': prediction['emotions'],
            'mental_state': prediction['mental_state'],
            'severity': prediction['severity'],
            'severity_score': prediction['severity_score'],
            'state_scores': prediction.get('state_scores', {}),
            'recommendations': recommendations,
            'timestamp': mood_entry.created_at.isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@predict_bp.route('/quick', methods=['POST'])
@jwt_required()
def quick_predict():
    """
    Quick emotion prediction without saving to database
    """
    try:
        data = request.get_json()
        
        if not data.get('text'):
            return jsonify({'error': 'Text is required'}), 400
        
        text = data['text'].strip()
        
        # Predict emotions
        prediction = emotion_predictor.classify_mental_state(text)
        
        if 'error' in prediction:
            return jsonify({'error': prediction['error']}), 500
        
        return jsonify({
            'success': True,
            'emotions': prediction['emotions'],
            'mental_state': prediction['mental_state'],
            'severity': prediction['severity']
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@predict_bp.route('/history', methods=['GET'])
@jwt_required()
def get_prediction_history():
    """
    Get user's mood entry history with pagination
    """
    try:
        current_user_id = get_jwt_identity()  # JWT identity is string ObjectId
        
        # Get pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Query mood entries with pagination
        skip = (page - 1) * per_page
        entries = MoodEntry.objects(user_id=ObjectId(current_user_id)).order_by('-created_at').skip(skip).limit(per_page)
        
        total = MoodEntry.objects(user_id=ObjectId(current_user_id)).count()
        pages = (total + per_page - 1) // per_page
        
        return jsonify({
            'success': True,
            'entries': [entry.to_dict() for entry in entries],
            'total': total,
            'pages': pages,
            'current_page': page,
            'per_page': per_page
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@predict_bp.route('/history/<entry_id>', methods=['GET'])
@jwt_required()
def get_prediction_detail(entry_id):
    """
    Get detailed view of a specific mood entry
    """
    try:
        current_user_id = get_jwt_identity()  # JWT identity is string ObjectId
        
        entry = MoodEntry.objects(id=ObjectId(entry_id), user_id=ObjectId(current_user_id)).first()
        
        if not entry:
            return jsonify({'error': 'Entry not found'}), 404
        
        # Get emotion-aware recommendations for this entry
        recommendations = RecommendationEngine.get_recommendations(
            mental_state=entry.mental_state,
            severity=entry.severity,
            emotions=entry.emotions  # Use stored emotions for contextual recommendations
        )
        
        result = entry.to_dict()
        result['full_recommendations'] = recommendations
        
        return jsonify({
            'success': True,
            'entry': result
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@predict_bp.route('/history/<entry_id>', methods=['DELETE'])
@jwt_required()
def delete_prediction(entry_id):
    """
    Delete a mood entry
    """
    try:
        current_user_id = get_jwt_identity()  # JWT identity is string ObjectId
        
        entry = MoodEntry.objects(id=ObjectId(entry_id), user_id=ObjectId(current_user_id)).first()
        
        if not entry:
            return jsonify({'error': 'Entry not found'}), 404
        
        entry.delete()
        
        return jsonify({
            'success': True,
            'message': 'Entry deleted successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@predict_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_statistics():
    """
    Get user's mental health statistics and trends
    """
    try:
        current_user_id = get_jwt_identity()  # JWT identity is string ObjectId
        
        # Get date range (default: last 30 days)
        days = request.args.get('days', 30, type=int)
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Query entries in date range
        entries = MoodEntry.objects(user_id=ObjectId(current_user_id), created_at__gte=start_date)
        
        if not entries:
            return jsonify({
                'success': True,
                'total_entries': 0,
                'message': 'No entries found in this period'
            }), 200
        
        # Calculate statistics
        mental_state_counts = {}
        severity_counts = {}
        daily_entries = {}
        
        for entry in entries:
            # Count mental states
            state = entry.mental_state
            mental_state_counts[state] = mental_state_counts.get(state, 0) + 1
            
            # Count severities
            severity = entry.severity
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
            
            # Group by date
            date_key = entry.created_at.date().isoformat()
            if date_key not in daily_entries:
                daily_entries[date_key] = []
            daily_entries[date_key].append({
                'mental_state': entry.mental_state,
                'severity': entry.severity,
                'severity_score': entry.severity_score
            })
        
        # Calculate average severity scores by mental state
        state_scores = {}
        for entry in entries:
            state = entry.mental_state
            if state not in state_scores:
                state_scores[state] = []
            if entry.severity_score:
                state_scores[state].append(entry.severity_score)
        
        avg_state_scores = {
            state: sum(scores) / len(scores) if scores else 0
            for state, scores in state_scores.items()
        }
        
        return jsonify({
            'success': True,
            'total_entries': entries.count(),
            'date_range': {
                'start': start_date.isoformat(),
                'end': datetime.utcnow().isoformat(),
                'days': days
            },
            'mental_state_distribution': mental_state_counts,
            'severity_distribution': severity_counts,
            'average_severity_by_state': avg_state_scores,
            'daily_data': daily_entries,
            'most_common_state': max(mental_state_counts.items(), key=lambda x: x[1])[0] if mental_state_counts else None
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@predict_bp.route('/recommendations', methods=['GET'])
@jwt_required()
def get_current_recommendations():
    """
    Get personalized recommendations based on recent mood entries
    """
    try:
        current_user_id = get_jwt_identity()  # JWT identity is string ObjectId
        
        # Get most recent entry
        recent_entry = MoodEntry.objects(user_id=ObjectId(current_user_id)).order_by('-created_at').first()
        
        if not recent_entry:
            # Return general wellness recommendations
            recommendations = RecommendationEngine.get_recommendations('normal')
            return jsonify({
                'success': True,
                'mental_state': 'normal',
                'severity': 'none',
                'recommendations': recommendations,
                'message': 'No recent mood entries. Here are general wellness tips.'
            }), 200
        
        # Get emotion-aware recommendations based on latest state
        recommendations = RecommendationEngine.get_recommendations(
            mental_state=recent_entry.mental_state,
            severity=recent_entry.severity,
            emotions=recent_entry.emotions  # Use emotions from recent entry
        )
        
        # Include emergency resources if severe
        emergency = None
        if recent_entry.severity == 'severe':
            emergency = RecommendationEngine.get_emergency_resources()
        
        return jsonify({
            'success': True,
            'mental_state': recent_entry.mental_state,
            'severity': recent_entry.severity,
            'severity_score': recent_entry.severity_score,
            'recommendations': recommendations,
            'emergency_resources': emergency,
            'last_updated': recent_entry.created_at.isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
