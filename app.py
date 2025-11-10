from flask import Flask, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from models import db
import os

def create_app():
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    
    # Database configuration
    # Use PostgreSQL in production (Render), SQLite in development
    database_url = os.getenv('DATABASE_URL')
    
    if database_url:
        # Fix for Render.com - replace postgres:// with postgresql://
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    else:
        # Development - use SQLite
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///certificates.db'
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JSON_SORT_KEYS'] = False
    
    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    CORS(app)
    
    # Import and register blueprints
    from routes.auth import auth_bp
    from routes.certificates import certificates_bp
    from routes.share import share_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(certificates_bp)
    app.register_blueprint(share_bp)
    
    # Health check endpoint
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({
            'status': 'healthy',
            'message': 'Certificate Vault API is running'
        }), 200
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Resource not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500
    
    # Create database tables
    with app.app_context():
        db.create_all()
        print("✅ Database tables created successfully!")
    
    return app


# For Render.com deployment
app = create_app()

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)