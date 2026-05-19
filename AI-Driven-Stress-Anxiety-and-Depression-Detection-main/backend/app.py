import warnings
warnings.filterwarnings('ignore', category=FutureWarning, module='transformers')
warnings.filterwarnings('ignore', message='.*torch.utils._pytree.*')

from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import config
from models import init_db
from emotion_predictor import emotion_predictor
import os

def create_app(config_name='development'):
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    init_db(app)  # MongoDB initialization
    CORS(app, resources={
        r"/api/*": {
            "origins": app.config['CORS_ORIGINS'],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    })
    JWTManager(app)
    
    # Register blueprints
    from routes.auth import auth_bp
    from routes.predict import predict_bp
    from routes.user import user_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(predict_bp)
    app.register_blueprint(user_bp)
    
    # Health check endpoint
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({
            'status': 'healthy',
            'model_loaded': emotion_predictor.model is not None,
            'database': 'connected'
        }), 200
    
    # Root endpoint
    @app.route('/', methods=['GET'])
    def root():
        return jsonify({
            'message': 'AI-Driven Mental Health API',
            'version': '1.0.0',
            'endpoints': {
                'auth': '/api/auth',
                'predict': '/api/predict',
                'health': '/api/health'
            }
        }), 200
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Endpoint not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500
    
    # Initialize database and load model
    with app.app_context():
        # MongoDB doesn't require schema creation
        print("✅ MongoDB connected")
        
        # Load emotion prediction model
        model_path = app.config.get('MODEL_PATH')
        if model_path and os.path.exists(model_path):
            emotion_predictor.load_model(model_path)
        else:
            print(f"⚠️  Model not found at {model_path}")
            print("   You can still use the API, but predictions will not work until model is loaded")
    
    return app


if __name__ == '__main__':
    app = create_app()
    # use_reloader=False prevents Windows socket errors in terminal
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
