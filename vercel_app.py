"""
Personal AI Employee - Vercel Serverless Entry Point
Minimal version for Vercel deployment
"""

import sys
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set environment for Vercel
os.environ['VERCEL'] = '1'
os.environ['VAULT_PATH'] = '/tmp/vault'

# Create /tmp/vault directory for Vercel
try:
    os.makedirs('/tmp/vault', exist_ok=True)
except:
    pass

# Minimal Flask app for Vercel
from flask import Flask, request, jsonify, send_file, redirect
from flask_cors import CORS
from pathlib import Path
import sqlite3
import jwt
import bcrypt
import datetime
import re
from functools import wraps

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# Project root
PROJECT_ROOT = Path(__file__).parent
DATABASE_PATH = PROJECT_ROOT / "auth_database.db"
HTML_ROOT = PROJECT_ROOT

# Secret key for JWT
SECRET_KEY = os.environ.get("SECRET_KEY", "your-secret-key-change-in-production")

# Database initialization
def init_db():
    """Initialize the authentication database"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        # Create tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                full_name TEXT,
                role TEXT DEFAULT 'user',
                tier TEXT DEFAULT 'bronze',
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                token TEXT UNIQUE NOT NULL,
                expires_at TIMESTAMP NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS audit_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                action TEXT NOT NULL,
                details TEXT,
                ip_address TEXT,
                user_agent TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE,
                phone TEXT,
                company TEXT,
                address TEXT,
                balance REAL DEFAULT 0,
                status TEXT DEFAULT 'active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE,
                phone TEXT,
                role TEXT,
                department TEXT,
                salary REAL,
                hours_worked REAL DEFAULT 0,
                pay_rate REAL DEFAULT 0,
                status TEXT DEFAULT 'active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS payments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER,
                amount REAL NOT NULL,
                type TEXT NOT NULL,
                status TEXT DEFAULT 'pending',
                description TEXT,
                payment_method TEXT,
                transaction_id TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES customers(id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL,
                party_name TEXT,
                amount REAL NOT NULL,
                status TEXT DEFAULT 'pending',
                description TEXT,
                reference TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS notifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                title TEXT NOT NULL,
                message TEXT NOT NULL,
                type TEXT DEFAULT 'info',
                is_read BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key_name TEXT UNIQUE NOT NULL,
                value TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create default admin user if not exists
        cursor.execute('SELECT COUNT(*) FROM users')
        if cursor.fetchone()[0] == 0:
            default_users = [
                ('admin@employee.ai', 'admin', 'Administrator', 'admin', 'platinum'),
                ('manager@employee.ai', 'manager', 'Manager', 'manager', 'gold'),
                ('user@employee.ai', 'user', 'User', 'user', 'bronze')
            ]
            
            for email, username, full_name, role, tier in default_users:
                password_hash = bcrypt.hashpw(
                    f'{role.capitalize()}@2026!'.encode('utf-8'),
                    bcrypt.gensalt(rounds=12)
                ).decode('utf-8')
                
                cursor.execute('''
                    INSERT INTO users (email, username, password_hash, full_name, role, tier)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (email, username, password_hash, full_name, role, tier))
        
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Database init error: {e}")

# Initialize database on first request
_db_initialized = False

def ensure_db():
    global _db_initialized
    if not _db_initialized:
        init_db()
        _db_initialized = True

# Helper functions
def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(' ')[1]
            except IndexError:
                return jsonify({'error': 'Invalid token format'}), 401
        
        if not token:
            token = request.args.get('token')
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            current_user = data['username']
            user_id = data['user_id']
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
        
        return f(current_user, user_id, *args, **kwargs)
    return decorated

# Routes
@app.route('/')
def index():
    return redirect('/login-page')

@app.route('/login-page')
def login_page():
    try:
        return send_file(HTML_ROOT / "login_custom.html")
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/status')
def status_page():
    try:
        return send_file(HTML_ROOT / "status.html")
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/bronze')
def bronze_dashboard():
    try:
        return send_file(HTML_ROOT / "bronze_dashboard.html")
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/silver')
def silver_dashboard():
    try:
        return send_file(HTML_ROOT / "silver_dashboard.html")
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/gold')
def gold_dashboard():
    try:
        return send_file(HTML_ROOT / "gold_dashboard.html")
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/platinum')
def platinum_dashboard():
    try:
        return send_file(HTML_ROOT / "platinum_dashboard.html")
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/dashboard')
def complete_dashboard():
    try:
        return send_file(HTML_ROOT / "complete_dashboard.html")
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/main-dashboard')
def main_dashboard():
    try:
        return send_file(HTML_ROOT / "dashboard.html")
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/templates/<path:filename>')
def serve_template(filename):
    try:
        return send_file(HTML_ROOT / "templates" / filename)
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/notifications')
def notifications_page():
    try:
        return send_file(HTML_ROOT / "templates" / "notifications.html")
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/settings')
def settings_page():
    try:
        return send_file(HTML_ROOT / "templates" / "settings.html")
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/payments')
def payments_page():
    try:
        return send_file(HTML_ROOT / "templates" / "payments.html")
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/customers')
def customers_page():
    try:
        return send_file(HTML_ROOT / "templates" / "customers.html")
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/employees')
def employees_page():
    try:
        return send_file(HTML_ROOT / "templates" / "employees.html")
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/banking_system.html')
def banking_system():
    try:
        return send_file(HTML_ROOT / "banking_system.html")
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/analytics.html')
def analytics_page():
    try:
        return send_file(HTML_ROOT / "analytics.html")
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/social_media_dashboard.html')
def social_media_dashboard():
    try:
        return send_file(HTML_ROOT / "social_media_dashboard.html")
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/whatsapp-manager')
def whatsapp_manager():
    try:
        return send_file(HTML_ROOT / "whatsapp_manager.html")
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/agent-skills')
def agent_skills_page():
    try:
        return send_file(HTML_ROOT / "agent_skills.html")
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/all-tiers')
def all_tiers():
    try:
        return send_file(HTML_ROOT / "all_tiers_form.html")
    except Exception as e:
        return jsonify({'error': str(e)}), 404

# API Routes
@app.route('/api/health', methods=['GET'])
def health_check():
    ensure_db()
    return jsonify({
        'status': 'healthy',
        'message': 'Personal AI Employee API is running',
        'timestamp': datetime.datetime.utcnow().isoformat()
    }), 200

@app.route('/api/version', methods=['GET'])
def version():
    return jsonify({
        'version': '2.0.0',
        'name': 'Personal AI Employee',
        'tier_system': 'Bronze, Silver, Gold, Platinum'
    }), 200

@app.route('/api/auth/login', methods=['POST'])
def login():
    ensure_db()
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')
    
    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            SELECT id, email, username, password_hash, full_name, role, tier
            FROM users
            WHERE email = ? AND is_active = 1
        ''', (email,))
        
        user = cursor.fetchone()
        
        if not user:
            return jsonify({'error': 'Invalid email or password'}), 401
        
        if not bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
            return jsonify({'error': 'Invalid email or password'}), 401
        
        token_data = {
            'user_id': user['id'],
            'username': user['username'],
            'email': user['email'],
            'role': user['role'],
            'tier': user['tier'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }
        
        access_token = jwt.encode(token_data, SECRET_KEY, algorithm='HS256')
        
        return jsonify({
            'status': 'SUCCESS',
            'access_token': access_token,
            'user': {
                'id': user['id'],
                'email': user['email'],
                'username': user['username'],
                'full_name': user['full_name'],
                'role': user['role'],
                'tier': user['tier']
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500
    finally:
        conn.close()

@app.route('/api/auth/register', methods=['POST'])
def register():
    ensure_db()
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    email = data.get('email', '').strip().lower()
    username = data.get('username', '').strip()
    password = data.get('password', '')
    full_name = data.get('full_name', '').strip()
    
    if not email or not username or not password:
        return jsonify({'error': 'Email, username, and password are required'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('SELECT id FROM users WHERE email = ?', (email,))
        if cursor.fetchone():
            return jsonify({'error': 'Email already registered'}), 409
        
        cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
        if cursor.fetchone():
            return jsonify({'error': 'Username already taken'}), 409
        
        password_hash = bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt(rounds=12)
        ).decode('utf-8')
        
        cursor.execute('''
            INSERT INTO users (email, username, password_hash, full_name, role, tier)
            VALUES (?, ?, ?, ?, 'user', 'bronze')
        ''', (email, username, password_hash, full_name))
        
        conn.commit()
        user_id = cursor.lastrowid
        
        return jsonify({
            'status': 'SUCCESS',
            'message': 'User registered successfully',
            'user_id': user_id
        }), 201
        
    except Exception as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500
    finally:
        conn.close()

@app.route('/api/auth/me', methods=['GET'])
@token_required
def get_current_user(current_user, user_id):
    ensure_db()
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, email, username, full_name, role, tier, created_at
        FROM users
        WHERE id = ?
    ''', (user_id,))
    
    user = cursor.fetchone()
    conn.close()
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({
        'user': {
            'id': user['id'],
            'email': user['email'],
            'username': user['username'],
            'full_name': user['full_name'],
            'role': user['role'],
            'tier': user['tier'],
            'created_at': user['created_at']
        }
    }), 200

# Static files
@app.route('/<path:filename>')
def serve_static(filename):
    try:
        return send_file(HTML_ROOT / filename)
    except Exception as e:
        return jsonify({'error': str(e)}), 404

# Vercel serverless handler
def handler(request):
    return app(request.environ, lambda *args: None)

# Initialize database on module load for Vercel
try:
    init_db()
except Exception as e:
    print(f"Init error: {e}")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
