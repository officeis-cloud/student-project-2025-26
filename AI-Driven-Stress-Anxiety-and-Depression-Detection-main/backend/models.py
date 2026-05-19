from mongoengine import Document, fields, connect
from datetime import datetime
import bcrypt
import os

# Initialize MongoDB connection
def init_db(app):
    """Initialize MongoDB connection"""
    mongodb_uri = app.config['MONGODB_SETTINGS']['host']
    connect(host=mongodb_uri, alias='default')

class User(Document):
    """User model for authentication and profile"""
    meta = {
        'collection': 'users',
        'indexes': ['email']
    }
    
    name = fields.StringField(required=True, max_length=100)
    email = fields.EmailField(required=True, unique=True)
    password_hash = fields.StringField(required=True, max_length=255)
    age = fields.IntField()
    gender = fields.StringField(max_length=20)
    created_at = fields.DateTimeField(default=datetime.utcnow)
    updated_at = fields.DateTimeField(default=datetime.utcnow)
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self, password):
        """Verify password"""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
    def to_dict(self):
        """Convert user to dictionary"""
        return {
            'id': str(self.id),
            'name': self.name,
            'email': self.email,
            'age': self.age,
            'gender': self.gender,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class MoodEntry(Document):
    """Mood entry model for storing journal entries and predictions"""
    meta = {
        'collection': 'mood_entries',
        'indexes': ['user_id', '-created_at']
    }
    
    user_id = fields.ObjectIdField(required=True)
    text = fields.StringField(required=True)
    
    # Prediction results
    emotions = fields.DictField()  # Store emotion probabilities as dict
    mental_state = fields.StringField(max_length=50)  # stress, anxiety, depression, normal
    severity = fields.StringField(max_length=20)  # mild, moderate, severe
    severity_score = fields.FloatField()  # probability score
    
    # Recommendations
    recommendations = fields.ListField(fields.StringField())  # Store recommendations as list
    
    # Timestamps
    created_at = fields.DateTimeField(default=datetime.utcnow)
    
    def to_dict(self):
        """Convert mood entry to dictionary"""
        return {
            'id': str(self.id),
            'user_id': str(self.user_id),
            'text': self.text,
            'emotions': self.emotions,
            'mental_state': self.mental_state,
            'severity': self.severity,
            'severity_score': self.severity_score,
            'recommendations': self.recommendations,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class WellnessTip(Document):
    """Curated wellness tips and resources"""
    meta = {
        'collection': 'wellness_tips',
        'indexes': ['category']
    }
    
    category = fields.StringField(required=True, max_length=50)  # stress, anxiety, depression, general
    title = fields.StringField(required=True, max_length=200)
    description = fields.StringField(required=True)
    type = fields.StringField(required=True, max_length=50)  # meditation, exercise, breathing, journaling, etc.
    duration = fields.StringField(max_length=50)  # "10 minutes", "Daily", etc.
    created_at = fields.DateTimeField(default=datetime.utcnow)
    
    def to_dict(self):
        """Convert wellness tip to dictionary"""
        return {
            'id': str(self.id),
            'category': self.category,
            'title': self.title,
            'description': self.description,
            'type': self.type,
            'duration': self.duration
        }
