#!/usr/bin/env python3
"""
User Authentication System
JWT-based authentication with user registration, login, and session management
"""

import jwt
import bcrypt
import sqlite3
import logging
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify, current_app
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AuthManager:
    """Handle user authentication and authorization"""
    
    def __init__(self, db_path=None):
        if db_path is None:
            backend_dir = os.path.dirname(os.path.abspath(__file__))
            self.db_path = os.path.join(backend_dir, "database", "jobs.db")
        else:
            self.db_path = db_path
        
        self.secret_key = os.environ.get('JWT_SECRET_KEY', 'your-secret-key-change-in-production')
        self.token_expiry_hours = 24
        
        # Initialize user tables
        self._create_user_tables()
        logger.info("Authentication manager initialized")
    
    def _create_user_tables(self):
        """Create user-related database tables"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Users table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    first_name TEXT,
                    last_name TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP,
                    is_active BOOLEAN DEFAULT 1,
                    profile_data TEXT
                )
            """)
            
            # User sessions table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_sessions (
                    session_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    token_hash TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    expires_at TIMESTAMP,
                    is_active BOOLEAN DEFAULT 1,
                    FOREIGN KEY(user_id) REFERENCES users(user_id)
                )
            """)
            
            conn.commit()
            conn.close()
            logger.info("User authentication tables created successfully")
            
        except Exception as e:
            logger.error(f"Error creating user tables: {e}")
            raise
    
    def hash_password(self, password: str) -> str:
        """Hash password using bcrypt"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    def verify_password(self, password: str, password_hash: str) -> bool:
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
    
    def generate_token(self, user_id: int, email: str) -> str:
        """Generate JWT token for user"""
        payload = {
            'user_id': user_id,
            'email': email,
            'exp': datetime.utcnow() + timedelta(hours=self.token_expiry_hours),
            'iat': datetime.utcnow()
        }
        return jwt.encode(payload, self.secret_key, algorithm='HS256')
    
    def verify_token(self, token: str) -> dict:
        """Verify JWT token and return payload"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            return {'error': 'Token has expired'}
        except jwt.InvalidTokenError:
            return {'error': 'Invalid token'}
    
    def register_user(self, email: str, password: str, first_name: str = None, last_name: str = None) -> dict:
        """Register a new user"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Check if user already exists
            cursor.execute("SELECT user_id FROM users WHERE email = ?", (email,))
            if cursor.fetchone():
                return {'error': 'User already exists with this email'}
            
            # Hash password and create user
            password_hash = self.hash_password(password)
            cursor.execute("""
                INSERT INTO users (email, password_hash, first_name, last_name)
                VALUES (?, ?, ?, ?)
            """, (email, password_hash, first_name, last_name))
            
            user_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            # Generate token
            token = self.generate_token(user_id, email)
            
            logger.info(f"User registered successfully: {email}")
            return {
                'success': True,
                'user_id': user_id,
                'email': email,
                'token': token,
                'message': 'User registered successfully'
            }
            
        except Exception as e:
            logger.error(f"Error registering user: {e}")
            return {'error': 'Registration failed'}
    
    def login_user(self, email: str, password: str) -> dict:
        """Authenticate user login"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get user data
            cursor.execute("""
                SELECT user_id, email, password_hash, first_name, last_name, is_active
                FROM users WHERE email = ?
            """, (email,))
            
            user_data = cursor.fetchone()
            if not user_data:
                return {'error': 'Invalid email or password'}
            
            user_id, email, password_hash, first_name, last_name, is_active = user_data
            
            if not is_active:
                return {'error': 'Account is deactivated'}
            
            # Verify password
            if not self.verify_password(password, password_hash):
                return {'error': 'Invalid email or password'}
            
            # Update last login
            cursor.execute("""
                UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE user_id = ?
            """, (user_id,))
            
            conn.commit()
            conn.close()
            
            # Generate token
            token = self.generate_token(user_id, email)
            
            logger.info(f"User logged in successfully: {email}")
            return {
                'success': True,
                'user_id': user_id,
                'email': email,
                'first_name': first_name,
                'last_name': last_name,
                'token': token,
                'message': 'Login successful'
            }
            
        except Exception as e:
            logger.error(f"Error during login: {e}")
            return {'error': 'Login failed'}
    
    def get_user_profile(self, user_id: int) -> dict:
        """Get user profile information"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT user_id, email, first_name, last_name, created_at, last_login, profile_data
                FROM users WHERE user_id = ? AND is_active = 1
            """, (user_id,))
            
            user_data = cursor.fetchone()
            conn.close()
            
            if not user_data:
                return {'error': 'User not found'}
            
            user_id, email, first_name, last_name, created_at, last_login, profile_data = user_data
            
            return {
                'user_id': user_id,
                'email': email,
                'first_name': first_name,
                'last_name': last_name,
                'created_at': created_at,
                'last_login': last_login,
                'profile_data': profile_data
            }
            
        except Exception as e:
            logger.error(f"Error getting user profile: {e}")
            return {'error': 'Failed to get user profile'}

def require_auth(f):
    """Decorator to require authentication for routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'No token provided'}), 401
        
        if token.startswith('Bearer '):
            token = token[7:]
        
        auth_manager = AuthManager()
        payload = auth_manager.verify_token(token)
        
        if 'error' in payload:
            return jsonify({'error': payload['error']}), 401
        
        # Add user info to request context
        request.current_user = payload
        return f(*args, **kwargs)
    
    return decorated_function