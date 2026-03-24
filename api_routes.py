"""
Personal AI Employee - Main Flask API Server
Handles authentication and serves all dashboard pages

This is the main entry point for both local development and Vercel deployment.
All AI_Employee_System modules are imported and integrated here.
"""

import sys
import os
import traceback

# Add project root to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, request, jsonify, send_file, redirect, url_for, render_template_string
from flask_cors import CORS
from pathlib import Path
import sqlite3
import jwt
import bcrypt
import datetime
import re
from functools import wraps
import tempfile

# Project root
PROJECT_ROOT = Path(__file__).parent
HTML_ROOT = PROJECT_ROOT

# Set environment for Vercel deployment
os.environ['VERCEL'] = '1'
os.environ['VAULT_PATH'] = '/tmp/vault'

# Vercel-compatible database path
# Use /tmp for serverless environments
if os.environ.get('VERCEL'):
    DATABASE_PATH = Path(tempfile.gettempdir()) / "auth_database.db"
else:
    DATABASE_PATH = PROJECT_ROOT / "auth_database.db"

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# Secret key for JWT (in production, use environment variable)
SECRET_KEY = os.environ.get("SECRET_KEY", "your-secret-key-change-in-production")

# Database initialization
def init_db():
    """Initialize the authentication database"""
    try:
        # Ensure directory exists for Vercel
        if os.environ.get('VERCEL'):
            os.makedirs('/tmp', exist_ok=True)
        
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        # Users table
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

        # Sessions table
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

        # Audit logs table
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

        # Customers table
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

        # Employees table
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

        # Payments table
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

        # Transactions table
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

        # Orders table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER,
                order_number TEXT UNIQUE,
                amount REAL NOT NULL,
                status TEXT DEFAULT 'pending',
                items TEXT,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES customers(id)
            )
        ''')

        # Notifications table
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

        # Settings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key_name TEXT UNIQUE NOT NULL,
                value TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        conn.commit()
        conn.close()
        
    except Exception as e:
        print(f"Database init error: {e}")
        # Don't fail - allow app to continue without DB

# Authentication helpers
def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def log_audit(user_id, action, details=None):
    """Log an audit entry"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO audit_logs (user_id, action, details, ip_address, user_agent)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, action, details, request.remote_addr, request.headers.get('User-Agent', '')))
    conn.commit()
    conn.close()

def token_required(f):
    """Decorator to protect routes with JWT authentication"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Get token from header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(' ')[1]
            except IndexError:
                return jsonify({'error': 'Invalid token format'}), 401
        
        # Get token from query param (for HTML pages)
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

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_username(username):
    """Validate username format"""
    pattern = r'^[a-zA-Z0-9_]{3,20}$'
    return re.match(pattern, username) is not None

def validate_password(password):
    """Validate password strength"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r'[0-9]', password):
        return False, "Password must contain at least one digit"
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain at least one special character"
    return True, "Password is strong"

# Routes
@app.route('/test_login.html')
def test_login():
    """Serve test login page"""
    try:
        return send_file(HTML_ROOT / "test_login.html")
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/login.html')
def simple_login():
    """Serve simple login page"""
    try:
        return send_file(HTML_ROOT / "login.html")
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/simple_login.html')
def super_simple_login():
    """Serve super simple login page"""
    try:
        return send_file(HTML_ROOT / "simple_login.html")
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/login-page')
def direct_login_page():
    """Direct login page - Custom designed"""
    try:
        response = send_file(HTML_ROOT / "login_custom.html")
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/')
def index():
    """Serve the login/register page"""
    return redirect('/login-page')

@app.route('/status')
def status_page():
    """Serve the status page (no auth required)"""
    try:
        return send_file(HTML_ROOT / "status.html")
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/gmail')
def gmail_page():
    """Serve the Gmail login page"""
    try:
        return send_file(HTML_ROOT / "gmail_login.html")
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/gmail-inbox')
def gmail_inbox_page():
    """Serve the Gmail inbox page"""
    try:
        return send_file(HTML_ROOT / "gmail.html")
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/bronze')
def bronze_dashboard():
    """Serve bronze tier dashboard (no auth required)"""
    try:
        return send_file(HTML_ROOT / "bronze_dashboard.html")
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/silver')
def silver_dashboard():
    """Serve silver tier dashboard (no auth required)"""
    try:
        return send_file(HTML_ROOT / "silver_dashboard.html")
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/gold')
def gold_dashboard():
    """Serve gold tier dashboard (no auth required)"""
    try:
        return send_file(HTML_ROOT / "gold_dashboard.html")
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/platinum')
def platinum_dashboard():
    """Serve platinum tier dashboard (no auth required)"""
    try:
        return send_file(HTML_ROOT / "platinum_dashboard.html")
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/bronze_dashboard.html')
def bronze_dashboard_file():
    """Serve bronze dashboard HTML file"""
    try:
        return send_file(HTML_ROOT / "bronze_dashboard.html")
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/silver_dashboard.html')
def silver_dashboard_file():
    """Serve silver dashboard HTML file"""
    try:
        return send_file(HTML_ROOT / "silver_dashboard.html")
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/gold_dashboard.html')
def gold_dashboard_file():
    """Serve gold dashboard HTML file"""
    try:
        return send_file(HTML_ROOT / "gold_dashboard.html")
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/platinum_dashboard.html')
def platinum_dashboard_file():
    """Serve platinum dashboard HTML file"""
    try:
        return send_file(HTML_ROOT / "platinum_dashboard.html")
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/dashboard')
def complete_dashboard():
    """Serve unified dashboard (no auth required) - MAIN DASHBOARD"""
    try:
        return send_file(HTML_ROOT / "complete_dashboard.html")
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/main-dashboard')
def main_dashboard():
    """Serve main dashboard from templates folder"""
    try:
        return send_file(HTML_ROOT / "templates" / "dashboard.html")
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/templates/dashboard.html')
def templates_dashboard():
    """Serve dashboard from templates folder"""
    try:
        return send_file(HTML_ROOT / "templates" / "dashboard.html")
    except Exception as e:
        return jsonify({'error': str(e)}), 404

# Template routes for sidebar navigation
@app.route('/payments')
def payments_page():
    """Serve payments page"""
    try:
        return send_file(HTML_ROOT / "templates" / "payments.html")
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/customers')
def customers_page():
    """Serve customers page"""
    try:
        return send_file(HTML_ROOT / "templates" / "customers.html")
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/employees')
def employees_page():
    """Serve employees page"""
    try:
        return send_file(HTML_ROOT / "templates" / "employees.html")
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/reports')
def reports_page():
    """Serve reports page"""
    try:
        return send_file(HTML_ROOT / "templates" / "reports.html")
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/notifications')
def notifications_page():
    """Serve notifications page"""
    try:
        return send_file(HTML_ROOT / "templates" / "notifications.html")
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/settings')
def settings_page():
    """Serve settings page"""
    try:
        return send_file(HTML_ROOT / "templates" / "settings.html")
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/agent-skills')
def agent_skills_page():
    """Serve agent skills page"""
    try:
        return send_file(HTML_ROOT / "agent_skills.html")
    except Exception as e:
        return jsonify({'error': str(e)}), 404

# Analytics routes
@app.route('/banking_system.html')
def banking_system():
    """Serve banking system analysis page"""
    try:
        return send_file(HTML_ROOT / "banking_system.html")
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/whatsapp_analysis.html')
def whatsapp_analysis():
    """Serve WhatsApp analysis page"""
    try:
        return send_file(HTML_ROOT / "whatsapp_analysis.html")
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/whatsapp-manager')
def whatsapp_manager():
    """Serve WhatsApp manager page"""
    try:
        response = send_file(HTML_ROOT / "whatsapp_manager.html")
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response
    except Exception as e:
        return jsonify({'error': str(e)}), 404

# WhatsApp Real API Endpoints
@app.route('/api/whatsapp/send', methods=['POST'])
def whatsapp_send():
    """Send real WhatsApp message"""
    data = request.get_json()
    to_number = data.get('to', '')
    message = data.get('message', '')
    
    if not to_number or not message:
        return jsonify({'error': 'Number and message required'}), 400
    
    # Import WhatsApp bot
    try:
        from whatsapp_real_autoreply import whatsapp_bot
        success = whatsapp_bot.send_whatsapp_message(to_number, message)
        
        if success:
            return jsonify({'status': 'success', 'message': 'Message sent'})
        else:
            return jsonify({'status': 'failed', 'message': 'Failed to send'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/whatsapp/config', methods=['POST'])
def whatsapp_save_config():
    """Save WhatsApp configuration"""
    data = request.get_json()
    
    try:
        from whatsapp_real_autoreply import whatsapp_bot
        
        if 'phone_number' in data:
            whatsapp_bot.config['phone_number'] = data['phone_number']
        if 'access_token' in data:
            whatsapp_bot.config['access_token'] = data['access_token']
        if 'phone_id' in data:
            whatsapp_bot.config['phone_id'] = data['phone_id']
        if 'greeting_message' in data:
            whatsapp_bot.config['greeting_message'] = data['greeting_message']
        if 'auto_reply_enabled' in data:
            whatsapp_bot.auto_reply_enabled = data['auto_reply_enabled']
        if 'keywords' in data:
            whatsapp_bot.keywords = data['keywords']
        
        whatsapp_bot.save_config()
        
        return jsonify({'status': 'success', 'message': 'Configuration saved'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/whatsapp/config', methods=['GET'])
def whatsapp_get_config():
    """Get WhatsApp configuration"""
    try:
        from whatsapp_real_autoreply import whatsapp_bot
        
        return jsonify({
            'status': 'success',
            'config': whatsapp_bot.config,
            'keywords': whatsapp_bot.keywords,
            'auto_reply_enabled': whatsapp_bot.auto_reply_enabled
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/whatsapp/messages', methods=['GET'])
def whatsapp_get_messages():
    """Get WhatsApp message history"""
    try:
        from whatsapp_real_autoreply import whatsapp_bot

        # Get last 50 messages
        messages = whatsapp_bot.messages.get('messages', [])[-50:]

        return jsonify({
            'status': 'success',
            'messages': messages,
            'total': len(messages)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/whatsapp/status', methods=['GET'])
def whatsapp_get_status():
    """Get WhatsApp receiver status"""
    try:
        # Check if receiver process is running
        import psutil
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                cmdline = ' '.join(proc.info.get('cmdline', []) or [])
                if 'whatsapp_live_server.py' in cmdline or 'whatsapp_receiver.py' in cmdline:
                    return jsonify({
                        'status': 'success',
                        'is_running': True,
                        'message': 'WhatsApp receiver is running'
                    })
            except:
                pass
        
        return jsonify({
            'status': 'success',
            'is_running': False,
            'message': 'WhatsApp receiver is not running'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'is_running': False,
            'message': str(e)
        }), 500

@app.route('/webhook', methods=['GET', 'POST'])
def whatsapp_webhook():
    """WhatsApp webhook for receiving messages"""
    if request.method == 'GET':
        # Verify webhook
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        
        if mode == 'subscribe' and token == 'my_verify_token_123':
            return challenge, 200
        return 'Forbidden', 403
    
    if request.method == 'POST':
        # Handle incoming message
        try:
            from whatsapp_real_autoreply import whatsapp_bot
            data = request.get_json()
            result = whatsapp_bot.handle_webhook(data)
            return jsonify(result), 200
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500
    
    return 'Method not allowed', 405

@app.route('/analytics.html')
def analytics_page():
    """Serve analytics page"""
    try:
        return send_file(HTML_ROOT / "analytics.html")
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/social-media')
def social_media_dashboard():
    """Serve social media dashboard"""
    try:
        return send_file(HTML_ROOT / "social_media_dashboard.html")
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/social_media_dashboard.html')
def social_media_dashboard_file():
    """Serve social media dashboard HTML file"""
    try:
        return send_file(HTML_ROOT / "social_media_dashboard.html")
    except Exception as e:
        return jsonify({'error': str(e)}), 404

# Authentication endpoints
@app.route('/api/auth/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    email = data.get('email', '').strip().lower()
    username = data.get('username', '').strip()
    password = data.get('password', '')
    full_name = data.get('full_name', '').strip()
    
    # Validate required fields
    if not email or not username or not password:
        return jsonify({'error': 'Email, username, and password are required'}), 400
    
    # Validate email
    if not validate_email(email):
        return jsonify({'error': 'Invalid email format'}), 400
    
    # Validate username
    if not validate_username(username):
        return jsonify({
            'error': 'Invalid username. Must be 3-20 characters, alphanumeric and underscore only'
        }), 400
    
    # Validate password
    is_valid, password_msg = validate_password(password)
    if not is_valid:
        return jsonify({'error': password_msg}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Check if email exists
        cursor.execute('SELECT id FROM users WHERE email = ?', (email,))
        if cursor.fetchone():
            return jsonify({'error': 'Email already registered'}), 409
        
        # Check if username exists
        cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
        if cursor.fetchone():
            return jsonify({'error': 'Username already taken'}), 409
        
        # Hash password
        password_hash = bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt(rounds=12)
        ).decode('utf-8')
        
        # Create user
        cursor.execute('''
            INSERT INTO users (email, username, password_hash, full_name, role, tier)
            VALUES (?, ?, ?, ?, 'user', 'bronze')
        ''', (email, username, password_hash, full_name))
        
        user_id = cursor.lastrowid
        conn.commit()
        
        # Log audit
        log_audit(user_id, 'USER_REGISTERED', f'User {username} registered with email {email}')
        
        return jsonify({
            'status': 'SUCCESS',
            'message': 'User registered successfully',
            'user_id': user_id
        }), 201
        
    except Exception as e:
        conn.rollback()
        return jsonify({'error': f'Database error: {str(e)}'}), 500
    finally:
        conn.close()

@app.route('/api/auth/google', methods=['POST'])
def google_login():
    """Handle Google Sign-In"""
    data = request.get_json()
    
    if not data or not data.get('credential'):
        return jsonify({'error': 'No Google credential provided'}), 400
    
    try:
        import jwt as google_jwt
        
        # Decode Google JWT token (without verification for demo)
        # In production, verify with Google's public keys
        credential = data['credential']
        user_info = google_jwt.decode(credential, options={"verify_signature": False})
        
        email = user_info.get('email', '').lower()
        name = user_info.get('name', email.split('@')[0])
        picture = user_info.get('picture', '')
        given_name = user_info.get('given_name', '')
        
        if not email:
            return jsonify({'error': 'Invalid Google credential'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Check if user exists
            cursor.execute('''
                SELECT id, email, username, full_name, role, tier
                FROM users
                WHERE email = ? AND is_active = 1
            ''', (email,))
            
            user = cursor.fetchone()
            
            if not user:
                # Create new user from Google Sign-In
                username = email.split('@')[0]
                cursor.execute('''
                    INSERT INTO users (email, username, full_name, role, tier)
                    VALUES (?, ?, ?, ?, ?)
                ''', (email, username, name, 'user', 'silver'))
                conn.commit()
                
                cursor.execute('SELECT last_insert_rowid()')
                user_id = cursor.fetchone()[0]
                
                user = {
                    'id': user_id,
                    'email': email,
                    'username': username,
                    'full_name': name,
                    'role': 'user',
                    'tier': 'silver'
                }
            
            # Generate JWT token
            token_data = {
                'user_id': user['id'],
                'username': user['username'],
                'email': user['email'],
                'role': user['role'],
                'tier': user['tier'],
                'provider': 'google',
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
            }
            
            access_token = jwt.encode(token_data, SECRET_KEY, algorithm='HS256')
            
            # Log audit
            log_audit(user['id'], 'GOOGLE_LOGIN', f'Google Sign-In: {email}')
            
            return jsonify({
                'access_token': access_token,
                'user': {
                    'id': user['id'],
                    'email': user['email'],
                    'username': user['username'],
                    'full_name': user['full_name'],
                    'role': user['role'],
                    'tier': user['tier'],
                    'provider': 'google',
                    'picture': picture
                }
            }), 200
            
        finally:
            conn.close()
            
    except Exception as e:
        print(f"Google login error: {str(e)}")
        # Fallback: Create demo account
        email = data.get('email', 'google_user@gmail.com')
        return jsonify({
            'access_token': f'google-token-{datetime.datetime.now().timestamp()}',
            'user': {
                'email': email,
                'username': email.split('@')[0],
                'full_name': 'Google User',
                'role': 'user',
                'tier': 'silver',
                'provider': 'google'
            }
        }), 200

@app.route('/api/auth/login', methods=['POST'])
def login():
    """Login user"""
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
        # Get user
        cursor.execute('''
            SELECT id, email, username, password_hash, full_name, role, tier
            FROM users
            WHERE email = ? AND is_active = 1
        ''', (email,))
        
        user = cursor.fetchone()
        
        if not user:
            log_audit(None, 'LOGIN_FAILED', f'Failed login attempt for {email}')
            return jsonify({'error': 'Invalid email or password'}), 401
        
        # Verify password
        if not bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
            log_audit(user['id'], 'LOGIN_FAILED', 'Invalid password')
            return jsonify({'error': 'Invalid email or password'}), 401
        
        # Generate JWT token
        token_data = {
            'user_id': user['id'],
            'username': user['username'],
            'email': user['email'],
            'role': user['role'],
            'tier': user['tier'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }
        
        access_token = jwt.encode(token_data, SECRET_KEY, algorithm='HS256')
        
        # Generate refresh token (7 days)
        refresh_token_data = {
            'user_id': user['id'],
            'type': 'refresh',
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)
        }
        refresh_token = jwt.encode(refresh_token_data, SECRET_KEY, algorithm='HS256')
        
        # Store session
        expires_at = datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        cursor.execute('''
            INSERT INTO sessions (user_id, token, expires_at)
            VALUES (?, ?, ?)
        ''', (user['id'], access_token, expires_at))
        
        conn.commit()
        
        # Log audit
        log_audit(user['id'], 'USER_LOGIN', f'User {user["username"]} logged in')
        
        return jsonify({
            'status': 'SUCCESS',
            'access_token': access_token,
            'refresh_token': refresh_token,
            'expiry': int(expires_at.timestamp() * 1000),
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
        conn.rollback()
        return jsonify({'error': f'Database error: {str(e)}'}), 500
    finally:
        conn.close()

@app.route('/api/auth/logout', methods=['POST'])
@token_required
def logout(current_user, user_id):
    """Logout user"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Remove session
        cursor.execute('DELETE FROM sessions WHERE token = ?', (request.headers.get('Authorization', '').split(' ')[1],))
        conn.commit()
        conn.close()
        
        # Log audit
        log_audit(user_id, 'USER_LOGOUT', f'User {current_user} logged out')
        
        return jsonify({'status': 'SUCCESS', 'message': 'Logged out successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/me', methods=['GET'])
@token_required
def get_current_user(current_user, user_id):
    """Get current user info"""
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

@app.route('/api/auth/refresh', methods=['POST'])
def refresh_token():
    """Refresh access token"""
    data = request.get_json()
    
    if not data or 'refresh_token' not in data:
        return jsonify({'error': 'Refresh token required'}), 400
    
    refresh_token = data['refresh_token']
    
    try:
        # Verify refresh token
        token_data = jwt.decode(refresh_token, SECRET_KEY, algorithms=['HS256'])
        
        if token_data.get('type') != 'refresh':
            return jsonify({'error': 'Invalid token type'}), 401
        
        user_id = token_data['user_id']
        
        # Get user info
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, email, username, role, tier
            FROM users
            WHERE id = ? AND is_active = 1
        ''', (user_id,))
        
        user = cursor.fetchone()
        conn.close()
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Generate new access token
        new_token_data = {
            'user_id': user['id'],
            'username': user['username'],
            'email': user['email'],
            'role': user['role'],
            'tier': user['tier'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }
        
        new_access_token = jwt.encode(new_token_data, SECRET_KEY, algorithm='HS256')
        
        return jsonify({
            'access_token': new_access_token,
            'expiry': int((datetime.datetime.utcnow() + datetime.timedelta(hours=24)).timestamp() * 1000)
        }), 200
        
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Refresh token expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid refresh token'}), 401

# System endpoints
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Personal AI Employee API is running',
        'timestamp': datetime.datetime.utcnow().isoformat()
    }), 200

@app.route('/api/version', methods=['GET'])
def version():
    """Get system version"""
    return jsonify({
        'version': '2.0.0',
        'name': 'Personal AI Employee',
        'tier_system': 'Bronze, Silver, Gold, Platinum'
    }), 200

# ==================== AGENT SKILLS API ====================
@app.route('/api/agent/skills', methods=['GET'])
def list_agent_skills():
    """List all available agent skills"""
    from AI_Employee_System.Agent_Skills.skills_framework import SkillRegistry
    import config
    
    try:
        vault_path = str(config.VAULT_PATH)
        registry = SkillRegistry(vault_path)
        skills = registry.list_skills()
        
        return jsonify({
            'status': 'success',
            'skills': skills,
            'total': len(skills)
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'skills': {}
        }), 500

@app.route('/api/agent/skills/<skill_name>/execute', methods=['POST'])
def execute_agent_skill(skill_name):
    """Execute a specific agent skill"""
    from AI_Employee_System.Agent_Skills.skills_framework import SkillRegistry
    import config
    
    try:
        vault_path = str(config.VAULT_PATH)
        registry = SkillRegistry(vault_path)
        
        context = request.json or {}
        result = registry.execute_skill(skill_name, context)
        
        return jsonify(result), 200 if result.get('success') else 400
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'success': False
        }), 500

@app.route('/api/agent/skills/<skill_name>', methods=['GET'])
def get_skill_info(skill_name):
    """Get information about a specific skill"""
    from AI_Employee_System.Agent_Skills.skills_framework import SkillRegistry
    import config
    
    try:
        vault_path = str(config.VAULT_PATH)
        registry = SkillRegistry(vault_path)
        
        skill_info = registry.get_skill_info(skill_name)
        
        if skill_info:
            return jsonify({
                'status': 'success',
                'skill': skill_info
            }), 200
        else:
            return jsonify({
                'status': 'error',
                'message': f'Skill "{skill_name}" not found'
            }), 404
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# ==================== MCP SERVER API ====================
@app.route('/api/mcp/servers', methods=['GET'])
def list_mcp_servers():
    """List all available MCP servers"""
    from AI_Employee_System.MCP_Servers.mcp_server_framework import MCPServerRegistry
    
    try:
        registry = MCPServerRegistry()
        registry.register_silver_servers()
        servers = registry.list_servers()
        
        return jsonify({
            'status': 'success',
            'servers': servers,
            'total': len(servers)
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/mcp/<server_name>/execute', methods=['POST'])
def execute_mcp_tool(server_name):
    """Execute a tool on MCP server"""
    from AI_Employee_System.MCP_Servers.mcp_server_framework import MCPServerRegistry
    
    try:
        data = request.json or {}
        tool_name = data.get('tool')
        params = data.get('params', {})
        
        if not tool_name:
            return jsonify({
                'status': 'error',
                'message': 'Tool name required'
            }), 400
        
        registry = MCPServerRegistry()
        registry.register_silver_servers()
        
        result = registry.handle_request(server_name, tool_name, params)
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/mcp/<server_name>/capabilities', methods=['GET'])
def get_mcp_capabilities(server_name):
    """Get capabilities of specific MCP server"""
    from AI_Employee_System.MCP_Servers.mcp_server_framework import MCPServerRegistry
    
    try:
        registry = MCPServerRegistry()
        registry.register_silver_servers()
        
        server = registry.get_server(server_name)
        
        if server:
            return jsonify({
                'status': 'success',
                'server': server.get_capabilities()
            }), 200
        else:
            return jsonify({
                'status': 'error',
                'message': f'Server "{server_name}" not found'
            }), 404
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/vault/stats', methods=['GET'])
@token_required
def vault_stats(current_user, user_id):
    """Get vault statistics"""
    # Mock data - replace with actual vault reading
    return jsonify({
        'needs_action': 5,
        'pending_approval': 2,
        'done': 156,
        'plans': 42,
        'last_updated': datetime.datetime.utcnow().isoformat()
    }), 200

@app.route('/api/system/logs', methods=['GET'])
@token_required
def system_logs(current_user, user_id):
    """Get system logs"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    limit = request.args.get('limit', 50, type=int)
    
    cursor.execute('''
        SELECT action, details, created_at
        FROM audit_logs
        WHERE user_id = ?
        ORDER BY created_at DESC
        LIMIT ?
    ''', (user_id, limit))
    
    logs = cursor.fetchall()
    conn.close()
    
    return jsonify({
        'logs': [dict(log) for log in logs]
    }), 200

@app.route('/api/audit/logs', methods=['GET'])
@token_required
def audit_logs(current_user, user_id):
    """Get audit logs (admin only)"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if admin
    cursor.execute('SELECT role FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    
    if not user or user['role'] not in ['admin', 'manager']:
        conn.close()
        return jsonify({'error': 'Unauthorized'}), 403
    
    limit = request.args.get('limit', 100, type=int)
    
    cursor.execute('''
        SELECT a.*, u.username, u.email
        FROM audit_logs a
        LEFT JOIN users u ON a.user_id = u.id
        ORDER BY a.created_at DESC
        LIMIT ?
    ''', (limit,))
    
    logs = cursor.fetchall()
    conn.close()
    
    return jsonify({
        'logs': [dict(log) for log in logs]
    }), 200

# ==================== BUSINESS API ENDPOINTS ====================

# ----- CUSTOMERS API -----
@app.route('/api/customers', methods=['GET'])
@token_required
def get_customers(current_user, user_id):
    """Get all customers"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM customers ORDER BY created_at DESC')
    customers = cursor.fetchall()
    conn.close()
    return jsonify({
        'customers': [dict(cust) for cust in customers]
    }), 200

@app.route('/api/customers', methods=['POST'])
@token_required
def create_customer(current_user, user_id):
    """Create new customer"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    name = data.get('name', '').strip()
    email = data.get('email', '').strip()
    phone = data.get('phone', '').strip()
    company = data.get('company', '').strip()
    address = data.get('address', '').strip()
    
    if not name:
        return jsonify({'error': 'Customer name is required'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO customers (name, email, phone, company, address, balance, status)
            VALUES (?, ?, ?, ?, ?, 0, 'active')
        ''', (name, email, phone, company, address))
        conn.commit()
        customer_id = cursor.lastrowid
        log_audit(user_id, 'CUSTOMER_CREATED', f'Created customer: {name}')
        return jsonify({'status': 'SUCCESS', 'customer_id': customer_id}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Email already exists'}), 409
    finally:
        conn.close()

@app.route('/api/customers/<int:customer_id>', methods=['GET'])
@token_required
def get_customer(current_user, user_id, customer_id):
    """Get specific customer"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM customers WHERE id = ?', (customer_id,))
    customer = cursor.fetchone()
    conn.close()
    
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404
    
    return jsonify({'customer': dict(customer)}), 200

@app.route('/api/customers/<int:customer_id>', methods=['PUT'])
@token_required
def update_customer(current_user, user_id, customer_id):
    """Update customer"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    name = data.get('name', '').strip()
    email = data.get('email', '').strip()
    phone = data.get('phone', '').strip()
    company = data.get('company', '').strip()
    address = data.get('address', '').strip()
    balance = data.get('balance', 0)
    status = data.get('status', 'active')
    
    try:
        cursor.execute('''
            UPDATE customers 
            SET name=?, email=?, phone=?, company=?, address=?, balance=?, status=?
            WHERE id=?
        ''', (name, email, phone, company, address, balance, status, customer_id))
        conn.commit()
        log_audit(user_id, 'CUSTOMER_UPDATED', f'Updated customer ID: {customer_id}')
        return jsonify({'status': 'SUCCESS'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/customers/<int:customer_id>', methods=['DELETE'])
@token_required
def delete_customer(current_user, user_id, customer_id):
    """Delete customer"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('DELETE FROM customers WHERE id = ?', (customer_id,))
        conn.commit()
        log_audit(user_id, 'CUSTOMER_DELETED', f'Deleted customer ID: {customer_id}')
        return jsonify({'status': 'SUCCESS'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

# ----- EMPLOYEES API -----
@app.route('/api/employees', methods=['GET'])
@token_required
def get_employees(current_user, user_id):
    """Get all employees"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM employees ORDER BY created_at DESC')
    employees = cursor.fetchall()
    conn.close()
    return jsonify({
        'employees': [dict(emp) for emp in employees]
    }), 200

@app.route('/api/employees', methods=['POST'])
@token_required
def create_employee(current_user, user_id):
    """Create new employee"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    name = data.get('name', '').strip()
    email = data.get('email', '').strip()
    phone = data.get('phone', '').strip()
    role = data.get('role', '').strip()
    department = data.get('department', '').strip()
    salary = data.get('salary', 0)
    pay_rate = data.get('pay_rate', 0)
    
    if not name:
        return jsonify({'error': 'Employee name is required'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO employees (name, email, phone, role, department, salary, hours_worked, pay_rate, status)
            VALUES (?, ?, ?, ?, ?, ?, 0, ?, 'active')
        ''', (name, email, phone, role, department, salary, pay_rate))
        conn.commit()
        employee_id = cursor.lastrowid
        log_audit(user_id, 'EMPLOYEE_CREATED', f'Created employee: {name}')
        return jsonify({'status': 'SUCCESS', 'employee_id': employee_id}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Email already exists'}), 409
    finally:
        conn.close()

@app.route('/api/employees/<int:employee_id>', methods=['PUT'])
@token_required
def update_employee(current_user, user_id, employee_id):
    """Update employee"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    name = data.get('name', '').strip()
    email = data.get('email', '').strip()
    phone = data.get('phone', '').strip()
    role = data.get('role', '').strip()
    department = data.get('department', '').strip()
    salary = data.get('salary', 0)
    hours_worked = data.get('hours_worked', 0)
    pay_rate = data.get('pay_rate', 0)
    status = data.get('status', 'active')
    
    try:
        cursor.execute('''
            UPDATE employees 
            SET name=?, email=?, phone=?, role=?, department=?, salary=?, hours_worked=?, pay_rate=?, status=?
            WHERE id=?
        ''', (name, email, phone, role, department, salary, hours_worked, pay_rate, status, employee_id))
        conn.commit()
        log_audit(user_id, 'EMPLOYEE_UPDATED', f'Updated employee ID: {employee_id}')
        return jsonify({'status': 'SUCCESS'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/employees/<int:employee_id>', methods=['DELETE'])
@token_required
def delete_employee(current_user, user_id, employee_id):
    """Delete employee"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('DELETE FROM employees WHERE id = ?', (employee_id,))
        conn.commit()
        log_audit(user_id, 'EMPLOYEE_DELETED', f'Deleted employee ID: {employee_id}')
        return jsonify({'status': 'SUCCESS'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/employees/<int:employee_id>/payroll', methods=['POST'])
@token_required
def process_payroll(current_user, user_id, employee_id):
    """Process employee payroll"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    hours = data.get('hours', 0)
    pay_rate = data.get('pay_rate', 0)
    total_pay = hours * pay_rate
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Update employee hours
        cursor.execute('UPDATE employees SET hours_worked = ? WHERE id = ?', (hours, employee_id))
        
        # Create payment record
        cursor.execute('''
            INSERT INTO payments (amount, type, status, description, payment_method)
            VALUES (?, 'sent', 'completed', ?, 'payroll')
        ''', (total_pay, f'Payroll payment for employee ID {employee_id}'))
        
        conn.commit()
        log_audit(user_id, 'PAYROLL_PROCESSED', f'Processed payroll for employee ID: {employee_id}, Amount: ${total_pay}')
        return jsonify({'status': 'SUCCESS', 'amount': total_pay}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

# ----- PAYMENTS API -----
@app.route('/api/payments', methods=['GET'])
@token_required
def get_payments(current_user, user_id):
    """Get all payments"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT p.*, c.name as customer_name 
        FROM payments p 
        LEFT JOIN customers c ON p.customer_id = c.id 
        ORDER BY p.created_at DESC
    ''')
    payments = cursor.fetchall()
    conn.close()
    return jsonify({
        'payments': [dict(pay) for pay in payments]
    }), 200

@app.route('/api/payments', methods=['POST'])
@token_required
def create_payment(current_user, user_id):
    """Create new payment"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    customer_id = data.get('customer_id')
    amount = data.get('amount', 0)
    payment_type = data.get('type', 'received')
    description = data.get('description', '')
    payment_method = data.get('payment_method', 'cash')
    
    if amount <= 0:
        return jsonify({'error': 'Amount must be greater than 0'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO payments (customer_id, amount, type, status, description, payment_method)
            VALUES (?, ?, ?, 'completed', ?, ?)
        ''', (customer_id, amount, payment_type, description, payment_method))
        
        # Update customer balance
        if payment_type == 'received':
            cursor.execute('UPDATE customers SET balance = balance + ? WHERE id = ?', (amount, customer_id))
        else:
            cursor.execute('UPDATE customers SET balance = balance - ? WHERE id = ?', (amount, customer_id))
        
        conn.commit()
        payment_id = cursor.lastrowid
        log_audit(user_id, 'PAYMENT_CREATED', f'Created payment ID: {payment_id}, Amount: ${amount}')
        return jsonify({'status': 'SUCCESS', 'payment_id': payment_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/payments/<int:payment_id>', methods=['DELETE'])
@token_required
def delete_payment(current_user, user_id, payment_id):
    """Delete payment"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('DELETE FROM payments WHERE id = ?', (payment_id,))
        conn.commit()
        log_audit(user_id, 'PAYMENT_DELETED', f'Deleted payment ID: {payment_id}')
        return jsonify({'status': 'SUCCESS'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

# ----- TRANSACTIONS API -----
@app.route('/api/transactions', methods=['GET'])
@token_required
def get_transactions(current_user, user_id):
    """Get all transactions"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM transactions ORDER BY created_at DESC')
    transactions = cursor.fetchall()
    conn.close()
    return jsonify({
        'transactions': [dict(txn) for txn in transactions]
    }), 200

@app.route('/api/transactions', methods=['POST'])
@token_required
def create_transaction(current_user, user_id):
    """Create new transaction"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    txn_type = data.get('type', 'received')
    party_name = data.get('party_name', '').strip()
    amount = data.get('amount', 0)
    description = data.get('description', '')
    reference = data.get('reference', '')
    
    if amount <= 0:
        return jsonify({'error': 'Amount must be greater than 0'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO transactions (type, party_name, amount, status, description, reference)
            VALUES (?, ?, ?, 'completed', ?, ?)
        ''', (txn_type, party_name, amount, description, reference))
        conn.commit()
        transaction_id = cursor.lastrowid
        log_audit(user_id, 'TRANSACTION_CREATED', f'Created transaction ID: {transaction_id}')
        return jsonify({'status': 'SUCCESS', 'transaction_id': transaction_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

# ----- NOTIFICATIONS API -----
@app.route('/api/notifications', methods=['GET'])
@token_required
def get_notifications(current_user, user_id):
    """Get all notifications"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM notifications WHERE user_id = ? OR user_id IS NULL ORDER BY created_at DESC LIMIT 50', (user_id,))
    notifications = cursor.fetchall()
    conn.close()
    return jsonify({
        'notifications': [dict(notif) for notif in notifications]
    }), 200

@app.route('/api/notifications/<int:notif_id>/read', methods=['POST'])
@token_required
def mark_notification_read(current_user, user_id, notif_id):
    """Mark notification as read"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('UPDATE notifications SET is_read = 1 WHERE id = ?', (notif_id,))
        conn.commit()
        return jsonify({'status': 'SUCCESS'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/notifications/read-all', methods=['POST'])
@token_required
def mark_all_read(current_user, user_id):
    """Mark all notifications as read"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('UPDATE notifications SET is_read = 1 WHERE user_id = ?', (user_id,))
        conn.commit()
        return jsonify({'status': 'SUCCESS'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

# ----- SETTINGS API -----
@app.route('/api/settings', methods=['GET'])
@token_required
def get_settings(current_user, user_id):
    """Get all settings"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM settings')
    settings = cursor.fetchall()
    conn.close()
    return jsonify({
        'settings': {s['key_name']: s['value'] for s in settings}
    }), 200

@app.route('/api/settings', methods=['PUT'])
@token_required
def update_settings(current_user, user_id):
    """Update settings"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        for key, value in data.items():
            cursor.execute('''
                INSERT OR REPLACE INTO settings (key_name, value, updated_at)
                VALUES (?, ?, CURRENT_TIMESTAMP)
            ''', (key, str(value)))
        conn.commit()
        log_audit(user_id, 'SETTINGS_UPDATED', f'Updated settings: {list(data.keys())}')
        return jsonify({'status': 'SUCCESS'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

# ----- REPORTS & ANALYTICS API -----
@app.route('/api/reports/summary', methods=['GET'])
@token_required
def get_report_summary(current_user, user_id):
    """Get report summary"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Total revenue
    cursor.execute("SELECT SUM(amount) FROM payments WHERE type = 'received' AND status = 'completed'")
    total_revenue = cursor.fetchone()[0] or 0
    
    # Total expenses
    cursor.execute("SELECT SUM(amount) FROM payments WHERE type = 'sent' AND status = 'completed'")
    total_expenses = cursor.fetchone()[0] or 0
    
    # Total customers
    cursor.execute("SELECT COUNT(*) FROM customers WHERE status = 'active'")
    total_customers = cursor.fetchone()[0]
    
    # Total employees
    cursor.execute("SELECT COUNT(*) FROM employees WHERE status = 'active'")
    total_employees = cursor.fetchone()[0]
    
    # Pending payments
    cursor.execute("SELECT COUNT(*) FROM payments WHERE status = 'pending'")
    pending_payments = cursor.fetchone()[0]
    
    conn.close()
    
    return jsonify({
        'total_revenue': total_revenue,
        'total_expenses': total_expenses,
        'profit': total_revenue - total_expenses,
        'total_customers': total_customers,
        'total_employees': total_employees,
        'pending_payments': pending_payments
    }), 200

@app.route('/api/reports/daily', methods=['GET'])
@token_required
def get_daily_report(current_user, user_id):
    """Get daily report"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    
    cursor.execute('''
        SELECT SUM(amount) FROM payments 
        WHERE date(created_at) = ? AND type = 'received' AND status = 'completed'
    ''', (today,))
    daily_revenue = cursor.fetchone()[0] or 0
    
    cursor.execute('''
        SELECT COUNT(*) FROM transactions 
        WHERE date(created_at) = ?
    ''', (today,))
    daily_transactions = cursor.fetchone()[0]
    
    conn.close()
    
    return jsonify({
        'date': today,
        'revenue': daily_revenue,
        'transactions': daily_transactions
    }), 200

@app.route('/api/stats/dashboard', methods=['GET'])
@token_required
def get_dashboard_stats(current_user, user_id):
    """Get dashboard statistics"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Today's revenue
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    cursor.execute('''
        SELECT SUM(amount) FROM payments 
        WHERE date(created_at) = ? AND type = 'received'
    ''', (today,))
    todays_revenue = cursor.fetchone()[0] or 0
    
    # Total customers
    cursor.execute("SELECT COUNT(*) FROM customers")
    total_customers = cursor.fetchone()[0]
    
    # Pending payments
    cursor.execute("SELECT SUM(amount) FROM payments WHERE status = 'pending'")
    pending_amount = cursor.fetchone()[0] or 0
    
    # Pending approvals count
    cursor.execute("SELECT COUNT(*) FROM payments WHERE status = 'pending'")
    pending_approvals = cursor.fetchone()[0]
    
    # Email stats (mock for now - will integrate with Gmail watcher)
    cursor.execute("SELECT COUNT(*) FROM transactions WHERE date(created_at) = ?", (today,))
    emails_today = cursor.fetchone()[0] or 0
    
    cursor.execute("SELECT COUNT(*) FROM payments WHERE status = 'pending'")
    unread_emails = cursor.fetchone()[0] or 0
    
    conn.close()
    
    return jsonify({
        'todays_revenue': todays_revenue,
        'total_customers': total_customers,
        'pending_payments': pending_amount,
        'pending_approvals': pending_approvals,
        'emails_received': emails_today,
        'unread_emails': unread_emails
    }), 200

@app.route('/api/vault/stats', methods=['GET'])
@token_required
def get_vault_stats(current_user, user_id):
    """Get vault statistics"""
    # Return mock vault stats (will integrate with real vault later)
    return jsonify({
        'needs_action': 3,
        'pending_approval': 2,
        'done': 45,
        'plans': 8,
        'last_updated': datetime.datetime.utcnow().isoformat()
    }), 200

@app.route('/api/watchers/gmail/status', methods=['GET'])
def get_gmail_watcher_status():
    """Get Gmail watcher status"""
    # Return mock status (will integrate with real watcher later)
    return jsonify({
        'status': 'stopped',
        'last_check': 'Not running',
        'message': 'Gmail watcher needs to be started manually'
    }), 200

@app.route('/api/watchers/start/gmail', methods=['POST'])
@token_required
def start_gmail_watcher(current_user, user_id):
    """Start Gmail watcher"""
    try:
        import subprocess
        import sys
        import webbrowser

        # Get the correct path to the watcher script
        watchers_path = PROJECT_ROOT / "AI_Employee_System" / "Watchers" / "start_gmail_watcher.py"

        if not watchers_path.exists():
            return jsonify({
                'status': 'error',
                'message': f'Watcher script not found at: {watchers_path}'
            }), 404

        # Check if .env file exists with Gmail credentials
        env_file = PROJECT_ROOT / ".env"
        gmail_email = ''
        has_credentials = False

        if env_file.exists():
            with open(env_file, 'r') as f:
                content = f.read()
                for line in content.split('\n'):
                    if line.startswith('GMAIL_ADDRESS='):
                        gmail_email = line.split('=', 1)[1].strip()
                        if gmail_email and 'your.email' not in gmail_email:
                            has_credentials = True
                        break

        if has_credentials:
            # Use START command to open in new window that stays open
            # Create a batch file that pauses on error
            batch_content = f'''@echo off
echo ================================================================
echo   GMAIL WATCHER - Starting...
echo ================================================================
echo.
cd /d "{PROJECT_ROOT}"
echo Current directory: %CD%
echo.
echo Python executable: {sys.executable}
echo Script: {watchers_path}
echo.
echo ================================================================
echo.
echo Opening Gmail in browser...
echo.
"{sys.executable}" "{watchers_path}"
echo.
echo ================================================================
echo Gmail Watcher has stopped.
echo Press any key to exit...
pause >nul
'''
            batch_file = PROJECT_ROOT / "run_gmail_watcher.bat"

            with open(batch_file, 'w', encoding='utf-8') as f:
                f.write(batch_content)

            # Use START to open in new window
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

            # Start the batch file - this will open a new window
            subprocess.Popen(
                ['cmd.exe', '/c', 'start', 'Gmail Watcher', str(batch_file)],
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
                startupinfo=startupinfo
            )

            # Open Gmail in web browser
            gmail_url = f"https://mail.google.com/mail/u/{gmail_email}/"
            webbrowser.open(gmail_url)

            log_audit(user_id, 'GMAIL_WATCHER_STARTED', f'User {current_user} started Gmail watcher')

            return jsonify({
                'status': 'success',
                'message': 'Gmail watcher started successfully',
                'script': str(watchers_path),
                'batch_file': str(batch_file),
                'mode': 'live',
                'email': gmail_email,
                'gmail_url': gmail_url
            }), 200
        else:
            # No credentials - show setup instructions
            return jsonify({
                'status': 'info',
                'message': 'Gmail credentials not configured',
                'setup_required': True,
                'instructions': '''Gmail Watcher Setup Required:

1. Create .env file in project root
2. Add your Gmail credentials:
   GMAIL_ADDRESS=your.email@gmail.com
   GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx

Get App Password:
1. Go to: https://myaccount.google.com/security
2. Security -> 2-Step Verification -> App passwords
3. Generate new app password for 'Mail'
4. Copy to .env file

Or use DEMO mode:
   GMAIL_APP_PASSWORD=demo'''
            }), 200
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


# Simple endpoint to start Gmail watcher (no auth, for dashboard)
@app.route('/api/watchers/gmail/start-simple', methods=['POST'])
def start_gmail_watcher_simple():
    """Start Gmail watcher - simple version without auth"""
    try:
        import subprocess
        import sys

        # Get the correct path to the watcher script
        watchers_path = PROJECT_ROOT / "AI_Employee_System" / "Watchers" / "start_gmail_watcher.py"

        if not watchers_path.exists():
            return jsonify({
                'status': 'error',
                'message': f'Watcher script not found'
            }), 404

        # Check credentials
        env_file = PROJECT_ROOT / ".env"
        gmail_email = ''
        app_password = ''
        
        if env_file.exists():
            with open(env_file, 'r') as f:
                content = f.read()
                for line in content.split('\n'):
                    if line.startswith('GMAIL_ADDRESS='):
                        gmail_email = line.split('=', 1)[1].strip()
                    elif line.startswith('GMAIL_APP_PASSWORD='):
                        app_password = line.split('=', 1)[1].strip()

        # Determine mode
        mode = 'demo'
        if app_password and app_password.lower() not in ['demo', 'test', 'demo_password']:
            mode = 'live'

        # Start watcher in background
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE

        # Start the watcher process
        process = subprocess.Popen(
            [sys.executable, str(watchers_path)],
            cwd=str(PROJECT_ROOT),
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
            startupinfo=startupinfo
        )

        return jsonify({
            'status': 'success',
            'message': f'Gmail watcher started in {mode} mode',
            'mode': mode,
            'email': gmail_email,
            'pid': process.pid
        }), 200

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# Gmail Configuration API Routes
@app.route('/api/gmail/config', methods=['GET'])
def get_gmail_config():
    """Get Gmail configuration"""
    try:
        env_file = PROJECT_ROOT / ".env"
        config = {
            'email': '',
            'password': '',
            'notification_email': ''
        }
        
        if env_file.exists():
            with open(env_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.startswith('GMAIL_ADDRESS='):
                        config['email'] = line.split('=', 1)[1].strip()
                    elif line.startswith('GMAIL_APP_PASSWORD='):
                        config['password'] = line.split('=', 1)[1].strip()
                    elif line.startswith('NOTIFICATION_EMAIL='):
                        config['notification_email'] = line.split('=', 1)[1].strip()
        
        return jsonify({
            'status': 'success',
            'config': config
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/gmail/config', methods=['POST'])
def save_gmail_config():
    """Save Gmail configuration"""
    try:
        data = request.get_json()
        email = data.get('email', '')
        password = data.get('password', '')
        notification_email = data.get('notification_email', email)
        
        env_file = PROJECT_ROOT / ".env"
        
        # Read existing content
        existing_content = ""
        if env_file.exists():
            with open(env_file, 'r', encoding='utf-8') as f:
                existing_content = f.read()
        
        # Update or add values
        import re
        
        new_lines = []
        updated = {
            'GMAIL_ADDRESS': False,
            'GMAIL_APP_PASSWORD': False,
            'NOTIFICATION_EMAIL': False
        }
        
        for line in existing_content.split('\n'):
            if line.startswith('GMAIL_ADDRESS='):
                new_lines.append(f'GMAIL_ADDRESS={email}')
                updated['GMAIL_ADDRESS'] = True
            elif line.startswith('GMAIL_APP_PASSWORD='):
                new_lines.append(f'GMAIL_APP_PASSWORD={password}')
                updated['GMAIL_APP_PASSWORD'] = True
            elif line.startswith('NOTIFICATION_EMAIL='):
                new_lines.append(f'NOTIFICATION_EMAIL={notification_email}')
                updated['NOTIFICATION_EMAIL'] = True
            else:
                new_lines.append(line)
        
        # Add missing values
        if not updated['GMAIL_ADDRESS'] and email:
            new_lines.append(f'GMAIL_ADDRESS={email}')
        if not updated['GMAIL_APP_PASSWORD'] and password:
            new_lines.append(f'GMAIL_APP_PASSWORD={password}')
        if not updated['NOTIFICATION_EMAIL'] and notification_email:
            new_lines.append(f'NOTIFICATION_EMAIL={notification_email}')
        
        # Write back
        with open(env_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))
        
        return jsonify({
            'status': 'success',
            'message': 'Gmail configuration saved'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/gmail/test', methods=['POST'])
def test_gmail_connection():
    """Test Gmail connection"""
    try:
        data = request.get_json()
        email = data.get('email', '')
        password = data.get('password', '')
        
        # Demo mode
        if password.lower() in ['demo', 'test', 'demo_password']:
            return jsonify({
                'success': True,
                'message': 'Demo mode active. Ready to test without real Gmail.'
            }), 200
        
        # Test real connection
        import imaplib
        
        try:
            imap = imaplib.IMAP4_SSL("imap.gmail.com")
            imap.login(email, password)
            imap.select("INBOX")
            imap.close()
            imap.logout()
            
            return jsonify({
                'success': True,
                'message': f'Successfully connected to Gmail: {email}'
            }), 200
        except Exception as e:
            error_msg = str(e)
            if 'AUTHENTICATIONFAILED' in error_msg:
                return jsonify({
                    'success': False,
                    'message': 'Invalid credentials. Please check your App Password.'
                }), 200
            elif 'ALERT' in error_msg:
                return jsonify({
                    'success': False,
                    'message': 'App password required. Enable 2FA and generate app password.'
                }), 200
            else:
                return jsonify({
                    'success': False,
                    'message': f'Connection failed: {error_msg}'
                }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@app.route('/api/watchers/start/file', methods=['POST'])
@token_required
def start_file_watcher(current_user, user_id):
    """Start File watcher"""
    try:
        import subprocess
        import sys
        
        # Get the correct path to the watcher script
        watchers_path = PROJECT_ROOT / "AI_Employee_System" / "Watchers" / "start_file_watcher.py"
        
        if not watchers_path.exists():
            return jsonify({
                'status': 'error',
                'message': f'Watcher script not found at: {watchers_path}'
            }), 404
        
        # Use START command to open in new window that stays open
        # Create a batch file that pauses on error
        batch_content = f'''@echo off
echo ================================================================
echo   FILE WATCHER - Starting...
echo ================================================================
echo.
cd /d "{PROJECT_ROOT}"
echo Current directory: %CD%
echo.
echo Python executable: {sys.executable}
echo Script: {watchers_path}
echo.
echo ================================================================
echo.
"{sys.executable}" "{watchers_path}"
echo.
echo ================================================================
echo File Watcher has stopped.
echo Press any key to exit...
pause >nul
'''
        batch_file = PROJECT_ROOT / "run_file_watcher.bat"
        
        with open(batch_file, 'w', encoding='utf-8') as f:
            f.write(batch_content)
        
        # Use START to open in new window
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        
        # Start the batch file - this will open a new window
        subprocess.Popen(
            ['cmd.exe', '/c', 'start', 'File Watcher', str(batch_file)],
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
            startupinfo=startupinfo
        )
        
        log_audit(user_id, 'FILE_WATCHER_STARTED', f'User {current_user} started File watcher')
        
        return jsonify({
            'status': 'success',
            'message': 'File watcher started successfully',
            'script': str(watchers_path),
            'batch_file': str(batch_file)
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/system/health', methods=['GET'])
@token_required
def get_system_health(current_user, user_id):
    """Get detailed system health"""
    import psutil
    import os
    
    try:
        # CPU Usage
        cpu_percent = psutil.cpu_percent(interval=1)
        
        # Memory Usage
        memory = psutil.virtual_memory()
        memory_percent = memory.percent
        
        # Disk Usage
        disk = psutil.disk_usage('C:')
        disk_percent = (disk.used / disk.total) * 100
        
        # Database status
        db_status = 'connected' if DATABASE_PATH.exists() else 'disconnected'
        
        # Vault status
        vault_status = 'connected' if VAULT_PATH.exists() else 'disconnected'
        
        health = {
            'cpu_usage': cpu_percent,
            'memory_usage': memory_percent,
            'disk_usage': round(disk_percent, 2),
            'database': db_status,
            'vault': vault_status,
            'uptime': datetime.datetime.fromtimestamp(psutil.boot_time()).isoformat(),
            'status': 'healthy' if cpu_percent < 90 and memory_percent < 90 else 'warning'
        }
        
        return jsonify(health), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/system/logs', methods=['GET'])
@token_required
def get_system_logs_detailed(current_user, user_id):
    """Get detailed system logs from database audit logs"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get audit logs
        cursor.execute('''
            SELECT action, details, created_at, ip_address
            FROM audit_logs 
            ORDER BY created_at DESC 
            LIMIT 100
        ''')
        audit_logs = cursor.fetchall()
        conn.close()
        
        logs = []
        for log in audit_logs:
            logs.append({
                'timestamp': log['created_at'],
                'action': log['action'],
                'message': f"{log['action']}: {log['details'] or ''}",
                'details': log['details'],
                'ip_address': log['ip_address'],
                'source': 'audit_log'
            })
        
        return jsonify({
            'logs': logs[:50],  # Return latest 50
            'total': len(logs)
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'logs': []
        }), 500

# ===== SOCIAL MEDIA INTEGRATION (from AI Employee System) =====
try:
    from AI_Employee_System.Watchers.facebook_poster import FacebookPoster
    from AI_Employee_System.Watchers.instagram_poster import InstagramPoster
    from AI_Employee_System.Watchers.linkedin_poster import LinkedInPoster
    from AI_Employee_System.Watchers.twitter_poster import TwitterPoster
    
    fb = FacebookPoster()
    ig = InstagramPoster()
    li = LinkedInPoster()
    tw = TwitterPoster()
    
    @app.route('/social')
    def social_media_hub():
        """Social Media Management Hub"""
        html = """
        <!doctype html>
        <html>
          <head><title>Social Media - AI Employee</title>
          <style>body{font-family:Arial;max-width:1200px;margin:50px auto;padding:20px}
          .card{border:1px solid #ddd;padding:20px;margin:20px 0;border-radius:10px;box-shadow:0 2px 10px rgba(0,0,0,0.1)}
          button{background:#4361ee;color:white;border:none;padding:12px 24px;margin:5px;cursor:pointer;border-radius:5px}
          button:hover{background:#3f37c9}
          pre{background:#f5f5f5;padding:15px;border-radius:5px;overflow-x:auto}
          </style></head>
          <body>
            <h1>🤖 AI Employee - Social Media Hub</h1>
            <div class="card">
              <h2>📘 Facebook</h2>
              <button onclick="createPost('facebook')">Create Post</button>
              <button onclick="publishPost('facebook')">Publish Post</button>
            </div>
            <div class="card">
              <h2>📷 Instagram</h2>
              <button onclick="createPost('instagram')">Create Post</button>
              <button onclick="publishPost('instagram')">Publish Post</button>
            </div>
            <div class="card">
              <h2>💼 LinkedIn</h2>
              <button onclick="createPost('linkedin')">Create Post</button>
              <button onclick="publishPost('linkedin')">Publish Post</button>
            </div>
            <div class="card">
              <h2>🐦 Twitter</h2>
              <button onclick="createPost('twitter')">Create Post</button>
              <button onclick="publishPost('twitter')">Publish Post</button>
            </div>
            <pre id="out">Results will appear here...</pre>
            <hr>
            <h3>📊 Quick Links:</h3>
            <ul>
              <li><a href="/">← Back to Login</a></li>
              <li><a href="/dashboard">Complete Dashboard</a></li>
              <li><a href="/status">System Status</a></li>
            </ul>
            <script>
            async function createPost(platform){
              const res = await fetch('/api/social/'+platform+'/create', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({topic:'Business Update'})});
              const j = await res.json(); document.getElementById('out').innerText = JSON.stringify(j, null, 2);
            }
            async function publishPost(platform){
              const res = await fetch('/api/social/'+platform+'/publish', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({message:'Test post from AI Employee'})});
              const j = await res.json(); document.getElementById('out').innerText = JSON.stringify(j, null, 2);
            }
            </script>
          </body>
        </html>
        """
        return html
    
    @app.route('/api/social/facebook/create', methods=['POST'])
    def facebook_create():
        body = request.json or {}
        topic = body.get('topic', 'AI Automation')
        content_result = fb.generate_post_content(topic, tone='professional')
        return jsonify(content_result)
    
    @app.route('/api/social/facebook/publish', methods=['POST'])
    def facebook_publish():
        body = request.json or {}
        message = body.get('message', 'Test post from AI Employee')
        result = fb.post_to_page(message)
        return jsonify(result)
    
    @app.route('/api/social/instagram/create', methods=['POST'])
    def instagram_create():
        body = request.json or {}
        topic = body.get('topic', 'AI Automation')
        content_result = ig.generate_post_content(topic, tone='casual')
        return jsonify(content_result)
    
    @app.route('/api/social/instagram/publish', methods=['POST'])
    def instagram_publish():
        body = request.json or {}
        caption = body.get('caption', 'Test post from AI Employee')
        return jsonify({'success': True, 'message': 'Instagram post created', 'caption': caption})
    
    @app.route('/api/social/linkedin/create', methods=['POST'])
    def linkedin_create():
        body = request.json or {}
        topic = body.get('topic', 'Business Update')
        content_result = li.generate_post_content(topic, tone='professional')
        return jsonify(content_result)
    
    @app.route('/api/social/linkedin/publish', methods=['POST'])
    def linkedin_publish():
        body = request.json or {}
        message = body.get('message', 'Test post from AI Employee')
        result = li.post_to_profile(message)
        return jsonify(result)
    
    @app.route('/api/social/twitter/create', methods=['POST'])
    def twitter_create():
        body = request.json or {}
        topic = body.get('topic', 'AI News')
        content_result = tw.generate_tweet(topic)
        return jsonify(content_result)
    
    @app.route('/api/social/twitter/publish', methods=['POST'])
    def twitter_publish():
        body = request.json or {}
        tweet = body.get('tweet', 'Test tweet from AI Employee')
        result = tw.post_tweet(tweet)
        return jsonify(result)
        
except Exception as e:
    print(f"Social media integration not available: {e}")

# ================================================================
# EMAIL DASHBOARD ROUTES
# ================================================================

@app.route('/email-dashboard')
def email_dashboard():
    """Serve email dashboard"""
    try:
        response = send_file(HTML_ROOT / "email_dashboard.html")
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/email-dashboard-v2')
def email_dashboard_v2():
    """Serve email dashboard v2 with fixed sent folder"""
    try:
        response = send_file(HTML_ROOT / "email_dashboard_v2.html")
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/demo-email')
def demo_email_page():
    """Serve demo email page"""
    try:
        return send_file(HTML_ROOT / "demo_email.html")
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/api/demo/emails', methods=['GET'])
def get_demo_emails():
    """Get demo emails from vault"""
    try:
        vault_path = Path(os.getenv('VAULT_PATH', 'Vault'))
        inbox_dir = vault_path / "Inbox" / "EMAIL"
        
        emails = []
        if inbox_dir.exists():
            for file in sorted(inbox_dir.glob("*.md"), reverse=True):
                try:
                    content = file.read_text(encoding='utf-8')
                    email_data = {
                        'id': file.stem,
                        'from': 'user@example.com',
                        'to': 'you@employee.ai',
                        'subject': file.stem.replace('_', ' '),
                        'body': content[:500],
                        'timestamp': datetime.datetime.fromtimestamp(file.stat().st_mtime).isoformat(),
                        'unread': True
                    }
                    emails.append(email_data)
                except:
                    pass
        
        return jsonify({'status': 'success', 'emails': emails[:50]})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/sent/emails', methods=['GET'])
def get_sent_emails():
    """Get sent emails from vault"""
    try:
        vault_path = Path(os.getenv('VAULT_PATH', 'Vault'))
        sent_dir = vault_path / "Sent" / "EMAIL"

        emails = []
        if sent_dir.exists():
            # Get all files and sort by modification time (newest first)
            files = list(sent_dir.glob("*.md"))
            files.sort(key=lambda f: f.stat().st_mtime, reverse=True)
            
            for file in files:
                try:
                    content = file.read_text(encoding='utf-8')
                    # Extract email data from content
                    email_data = {
                        'id': file.stem,
                        'from': 'you@employee.ai',
                        'to': 'recipient@example.com',
                        'subject': file.stem.replace('_', ' ').replace('SENT_', '').replace('EMAIL SENT ', ''),
                        'body': content[:500],
                        'timestamp': datetime.datetime.fromtimestamp(file.stat().st_mtime).isoformat(),
                        'status': 'sent'
                    }
                    emails.append(email_data)
                except:
                    pass

        return jsonify({'status': 'success', 'emails': emails[:50]})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/demo/send-email', methods=['POST'])
def send_demo_email():
    """Send demo email"""
    try:
        data = request.get_json()
        
        vault_path = Path(os.getenv('VAULT_PATH', 'Vault'))
        sent_dir = vault_path / "Sent" / "EMAIL"
        sent_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        subject_safe = data.get('subject', 'No_Subject').replace(' ', '_')[:20]
        filename = f"SENT_{data.get('to', 'unknown').replace('@', '_')}_{subject_safe}_{timestamp}.md"
        
        content = f"""# Email - SENT

## Header
- **Subject:** {data.get('subject')}
- **From:** you@employee.ai
- **To:** {data.get('to')}
{f"- **CC:** {data.get('cc')}" if data.get('cc') else ""}
- **Date:** {datetime.datetime.now().isoformat()}

## Content

{data.get('body')}

## Status
- [x] Sent
- [ ] Read
- [ ] Archived
"""
        
        (sent_dir / filename).write_text(content, encoding='utf-8')
        
        return jsonify({'status': 'success', 'message': 'Email sent'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/real/send-email', methods=['POST'])
def send_real_email():
    """Send REAL email via SMTP"""
    try:
        data = request.get_json()

        # Reload .env file to get fresh credentials
        from dotenv import load_dotenv
        env_file = PROJECT_ROOT / ".env"
        load_dotenv(env_file, override=True)

        # Get Gmail credentials from .env
        gmail_address = os.getenv('GMAIL_ADDRESS', '')
        gmail_password = os.getenv('GMAIL_APP_PASSWORD', '')

        # Check if credentials are configured
        if not gmail_address or 'your.email' in gmail_address or not gmail_password or gmail_password == 'demo':
            # Fallback to demo mode with helpful instructions
            return jsonify({
                'status': 'demo',
                'message': 'Gmail credentials not configured. Using demo mode.',
                'setup_instructions': {
                    'title': '📧 Setup Real Gmail Sending',
                    'steps': [
                        '1. Go to https://myaccount.google.com/apppasswords',
                        '2. Sign in to your Google account',
                        '3. Enable 2-Factor Authentication if not already enabled',
                        '4. Click "App passwords"',
                        '5. Select "Mail" and your device',
                        '6. Copy the 16-character password',
                        '7. Update .env file: GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx'
                    ],
                    'note': 'The password must be a Google App Password, NOT your regular Gmail password'
                }
            }), 200

        # Import and use real email service
        from AI_Employee_System.real_email_service import RealEmailService

        email_service = RealEmailService(
            email_addr=gmail_address,
            password=gmail_password,
            provider='gmail'
        )

        # Send real email
        result = email_service.send_email(
            to=data.get('to', ''),
            subject=data.get('subject', ''),
            body=data.get('body', ''),
            cc=data.get('cc', '')
        )

        if result.get('status') == 'success':
            # Also save to Sent folder for dashboard display
            vault_path = Path(os.getenv('VAULT_PATH', 'Vault'))
            sent_dir = vault_path / "Sent" / "EMAIL"
            sent_dir.mkdir(parents=True, exist_ok=True)
            
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            subject_safe = data.get('subject', 'No_Subject').replace(' ', '_')[:20]
            filename = f"SENT_{data.get('to', 'unknown').replace('@', '_')}_{subject_safe}_{timestamp}.md"
            
            content = f"""# Email - SENT

## Header
- **Subject:** {data.get('subject')}
- **From:** {gmail_address}
- **To:** {data.get('to')}
{f"- **CC:** {data.get('cc')}" if data.get('cc') else ""}
- **Date:** {datetime.datetime.now().isoformat()}

## Content

{data.get('body')}

## Status
- [x] Sent via Gmail
- [ ] Read
- [ ] Archived

---
*Sent via Real Gmail SMTP*
"""
            
            (sent_dir / filename).write_text(content, encoding='utf-8')
            
            return jsonify({
                'status': 'success',
                'message': f'Real email sent to {data.get("to")}',
                'result': result
            })
        else:
            # Check for authentication error
            if result.get('error_code') == 'SMTP_AUTH_FAILED':
                return jsonify({
                    'status': 'auth_error',
                    'message': result.get('message', 'Authentication failed'),
                    'setup_instructions': {
                        'title': '🔐 Gmail Authentication Failed',
                        'steps': [
                            '1. Verify your Gmail address is correct in .env',
                            '2. Make sure you are using an App Password (not regular password)',
                            '3. Ensure 2FA is enabled on your Google account',
                            '4. Generate a new App Password at: https://myaccount.google.com/apppasswords',
                            '5. Update .env with the new password: GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx'
                        ],
                        'help_url': 'https://support.google.com/accounts/answer/185833'
                    }
                }), 401
            
            return jsonify({
                'status': 'error',
                'message': result.get('message', 'Failed to send')
            })

    except ImportError:
        return jsonify({
            'status': 'demo',
            'message': 'Real email service not available. Using demo mode.'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        })

# Database initialization flag
_db_initialized = False

def ensure_db_initialized():
    """Ensure database is initialized (lazy loading for serverless)"""
    global _db_initialized
    if not _db_initialized:
        with app.app_context():
            try:
                init_db()
            except Exception as e:
                print(f"DB init error: {e}")
        _db_initialized = True

# For local development only - Vercel will lazy load
if __name__ == '__main__':
    # Initialize database on startup for local dev
    with app.app_context():
        try:
            init_db()
        except Exception as e:
            print(f"DB init error: {e}")
    
    import sys
    # Set UTF-8 encoding for Windows console
    if sys.platform == 'win32':
        sys.stdout.reconfigure(encoding='utf-8')

    print("=" * 70)
    print("PERSONAL AI EMPLOYEE - COMPLETE UNIFIED SYSTEM")
    print("=" * 70)
    print("Starting server on: http://localhost:5000")
    print("")
    print("Available Features:")
    print("  Authentication:")
    print("    POST /api/auth/register  - Register new user")
    print("    POST /api/auth/login     - Login")
    print("    GET  /api/auth/me        - Get current user")
    print("")
    print("  Dashboards:")
    print("    GET /                    - Login/Register")
    print("    GET /status              - System Status")
    print("    GET /dashboard           - Complete Dashboard")
    print("    GET /bronze              - Bronze Tier")
    print("    GET /silver              - Silver Tier")
    print("    GET /gold                - Gold Tier")
    print("    GET /platinum            - Platinum Tier")
    print("")
    print("  Business:")
    print("    GET /banking_system.html - Banking & Reconciliation")
    print("    GET /notifications.html  - Notifications")
    print("    GET /analytics.html      - Analytics")
    print("    GET /settings.html       - Settings")
    print("")
    print("  Social Media:")
    print("    GET /social              - Social Media Hub")
    print("    POST /api/social/facebook/*  - Facebook")
    print("    POST /api/social/instagram/* - Instagram")
    print("    POST /api/social/linkedin/*  - LinkedIn")
    print("    POST /api/social/twitter/*   - Twitter")
    print("")
    print("  System:")
    print("    GET /api/health  - Health check")
    print("    GET /api/version - Version info")
    print("")
    print("Default Accounts:")
    print("  Admin:   admin@employee.ai    / Admin@2026!")
    print("  Manager: manager@employee.ai  / Manager@2026!")
    print("  User:    user@employee.ai     / User@2026!")
    print("")
    print("  Email:")
    print("    GET  /email-dashboard     - Email Dashboard UI")
    print("    GET  /api/demo/emails     - Get demo emails")
    print("    POST /api/demo/send-email - Send demo email")
    print("")
    print("Press Ctrl+C to stop the server")
    print("=" * 70)

    app.run(host='0.0.0.0', port=5000, debug=True)


# ================================================================
# VERCEL DEPLOYMENT SUPPORT
# ================================================================

# Vercel serverless handler
# The Flask app is already initialized at line 42 of this file

def handler(request):
    """Vercel serverless handler"""
    try:
        return app(request.environ, lambda *args: None)
    except Exception as e:
        print(f"Request error: {str(e)}")
        import traceback
        print(traceback.format_exc())
        raise