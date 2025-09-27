import os
import json
import logging
from functools import wraps
from flask import request, jsonify
import firebase_admin
from firebase_admin import credentials, auth as firebase_auth
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

class FirebaseAuthManager:
    def __init__(self):
        self.app = None
        self._initialize_firebase()
    
    def _initialize_firebase(self):
        """Initialize Firebase Admin SDK"""
        try:
            # Check if Firebase is already initialized
            if firebase_admin._apps:
                self.app = firebase_admin.get_app()
                logger.info("Firebase Admin SDK already initialized")
                return
            
            # Try to initialize with service account key
            service_account_path = os.getenv('FIREBASE_SERVICE_ACCOUNT_PATH')
            if service_account_path and os.path.exists(service_account_path):
                cred = credentials.Certificate(service_account_path)
                self.app = firebase_admin.initialize_app(cred)
                logger.info("Firebase Admin SDK initialized with service account")
                return
            
            # Try to initialize with environment variables
            service_account_json = os.getenv('FIREBASE_SERVICE_ACCOUNT_JSON')
            if service_account_json:
                try:
                    service_account_info = json.loads(service_account_json)
                    cred = credentials.Certificate(service_account_info)
                    self.app = firebase_admin.initialize_app(cred)
                    logger.info("Firebase Admin SDK initialized with JSON credentials")
                    return
                except json.JSONDecodeError:
                    logger.error("Invalid JSON in FIREBASE_SERVICE_ACCOUNT_JSON")
            
            # Initialize with default credentials (for production with proper IAM)
            self.app = firebase_admin.initialize_app()
            logger.info("Firebase Admin SDK initialized with default credentials")
            
        except Exception as e:
            logger.error(f"Failed to initialize Firebase Admin SDK: {str(e)}")
            # For development, we'll allow the app to run without Firebase auth
            # In production, you should handle this error appropriately
            logger.warning("Running without Firebase authentication - this is not recommended for production")
    
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Verify Firebase ID token and return user information
        """
        if not self.app:
            logger.warning("Firebase not initialized - skipping token verification")
            return None
        
        try:
            # Verify the ID token
            decoded_token = firebase_auth.verify_id_token(token)
            
            # Extract user information
            user_info = {
                'uid': decoded_token['uid'],
                'email': decoded_token.get('email'),
                'email_verified': decoded_token.get('email_verified', False),
                'name': decoded_token.get('name'),
                'picture': decoded_token.get('picture'),
                'firebase': decoded_token.get('firebase', {}),
            }
            
            logger.info(f"Token verified for user: {user_info['uid']}")
            return user_info
            
        except firebase_auth.InvalidIdTokenError as e:
            logger.error(f"Invalid ID token: {str(e)}")
            return None
        except firebase_auth.ExpiredIdTokenError as e:
            logger.error(f"Expired ID token: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Token verification failed: {str(e)}")
            return None

# Global instance
firebase_auth_manager = FirebaseAuthManager()

def require_firebase_auth(f):
    """
    Decorator to require Firebase authentication for Flask routes
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get the Authorization header
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return jsonify({
                'error': 'Authorization header missing',
                'status': 'error'
            }), 401
        
        # Extract the token (expecting "Bearer <token>")
        try:
            token = auth_header.split(' ')[1]
        except IndexError:
            return jsonify({
                'error': 'Invalid authorization header format. Expected "Bearer <token>"',
                'status': 'error'
            }), 401
        
        # Verify the token
        user_info = firebase_auth_manager.verify_token(token)
        
        if not user_info:
            return jsonify({
                'error': 'Invalid or expired token',
                'status': 'error'
            }), 401
        
        # Add user info to the request context
        request.user = user_info
        
        return f(*args, **kwargs)
    
    return decorated_function

def optional_firebase_auth(f):
    """
    Decorator to optionally verify Firebase authentication for Flask routes
    Returns user info if token is valid, None otherwise
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get the Authorization header
        auth_header = request.headers.get('Authorization')
        
        if auth_header:
            try:
                token = auth_header.split(' ')[1]
                user_info = firebase_auth_manager.verify_token(token)
                request.user = user_info
            except (IndexError, Exception) as e:
                logger.warning(f"Failed to parse auth header: {str(e)}")
                request.user = None
        else:
            request.user = None
        
        return f(*args, **kwargs)
    
    return decorated_function
