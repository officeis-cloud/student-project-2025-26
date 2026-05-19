from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from models import User
from datetime import datetime
from bson import ObjectId

user_bp = Blueprint('user', __name__, url_prefix='/api/user')

def get_or_create_demo_user():
    """Get or create a demo user for non-authenticated access"""
    demo_email = 'demo@mindcare.ai'
    
    # Try to find existing demo user
    user = User.objects(email=demo_email).first()
    
    if not user:
        # Create demo user
        user = User(
            name='Demo User',
            email=demo_email,
            age=None,
            gender=None
        )
        user.set_password('demo_password_not_used')
        user.save()
    
    return user

@user_bp.route('/profile', methods=['GET'])
def get_profile():
    """Get user profile - uses demo user if not authenticated"""
    try:
        # Try to get authenticated user
        try:
            verify_jwt_in_request(optional=True)
            current_user_id = get_jwt_identity()
            
            if current_user_id:
                user = User.objects(id=ObjectId(current_user_id)).first()
                if user:
                    return jsonify({'user': user.to_dict()}), 200
        except:
            pass
        
        # Fall back to demo user
        user = get_or_create_demo_user()
        return jsonify({'user': user.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@user_bp.route('/profile', methods=['PUT'])
def update_profile():
    """Update user profile - uses demo user if not authenticated"""
    try:
        # Try to get authenticated user
        try:
            verify_jwt_in_request(optional=True)
            current_user_id = get_jwt_identity()
            
            if current_user_id:
                user = User.objects(id=ObjectId(current_user_id)).first()
                if user:
                    data = request.get_json()
                    
                    # Update allowed fields
                    if 'name' in data:
                        user.name = data['name']
                    if 'email' in data:
                        user.email = data['email']
                    if 'age' in data:
                        user.age = data['age']
                    if 'gender' in data:
                        user.gender = data['gender']
                    
                    user.updated_at = datetime.utcnow()
                    user.save()
                    
                    return jsonify({
                        'success': True,
                        'message': 'Profile updated successfully',
                        'user': user.to_dict()
                    }), 200
        except:
            pass
        
        # Fall back to demo user
        user = get_or_create_demo_user()
        data = request.get_json()
        
        # Update allowed fields
        if 'name' in data:
            user.name = data['name']
        if 'email' in data:
            user.email = data['email']
        if 'age' in data:
            user.age = data['age']
        if 'gender' in data:
            user.gender = data['gender']
        
        user.updated_at = datetime.utcnow()
        user.save()
        
        return jsonify({
            'success': True,
            'message': 'Profile updated successfully',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@user_bp.route('/change-password', methods=['POST'])
def change_password():
    """Change user password with validation"""
    try:
        data = request.get_json()
        current_password = data.get('currentPassword')
        new_password = data.get('newPassword')
        
        if not current_password or not new_password:
            return jsonify({'error': 'All fields are required'}), 400
        
        # Try to get authenticated user
        try:
            verify_jwt_in_request(optional=True)
            current_user_id = get_jwt_identity()
            
            if current_user_id:
                user = User.objects(id=ObjectId(current_user_id)).first()
                if user:
                    # Verify current password
                    if not user.check_password(current_password):
                        return jsonify({'error': 'Current password is incorrect'}), 401
                    
                    # Set new password
                    user.set_password(new_password)
                    user.updated_at = datetime.utcnow()
                    user.save()
                    
                    return jsonify({
                        'success': True,
                        'message': 'Password changed successfully'
                    }), 200
        except:
            pass
        
        # Fall back to demo user
        user = get_or_create_demo_user()
        
        # Verify current password
        if not user.check_password(current_password):
            return jsonify({'error': 'Current password is incorrect'}), 401
        
        # Set new password
        user.set_password(new_password)
        user.updated_at = datetime.utcnow()
        user.save()
        
        return jsonify({
            'success': True,
            'message': 'Password changed successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@user_bp.route('/account', methods=['DELETE'])
def delete_account():
    """Delete user account and all associated data"""
    try:
        from models import MoodEntry  # Import here to avoid circular imports
        
        # Try to get authenticated user
        try:
            verify_jwt_in_request(optional=True)
            current_user_id = get_jwt_identity()
            
            if current_user_id:
                user = User.objects(id=ObjectId(current_user_id)).first()
                if user:
                    # Delete all mood entries for this user
                    MoodEntry.objects(user_id=ObjectId(current_user_id)).delete()
                    
                    # Delete the user
                    user.delete()
                    
                    return jsonify({
                        'success': True,
                        'message': 'Account deleted successfully'
                    }), 200
        except:
            pass
        
        # Don't allow deleting demo user
        return jsonify({'error': 'Cannot delete demo account'}), 403
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
