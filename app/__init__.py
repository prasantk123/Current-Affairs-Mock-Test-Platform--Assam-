from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Load environment variables from backend/.env
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

def create_app():
    app = Flask(__name__)
    
    # Database configuration
    database_url = os.getenv('DATABASE_URL')
    if database_url and database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url or 'sqlite:///current_affairs.db'
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
    
    from app.models.models import db
    db.init_app(app)
    
    # CORS configuration for production
    CORS(app, origins=[
        "http://localhost:3000",
        "https://*.onrender.com",
        "https://*.netlify.app",
        "https://*.vercel.app"
    ])
    
    from app.routes.admin import admin_bp
    from app.routes.test import test_bp
    
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(test_bp, url_prefix='/api/test')
    
    return app