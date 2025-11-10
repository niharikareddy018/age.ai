from flask import Flask
from flask_cors import CORS
from datetime import timedelta
import os
from dotenv import load_dotenv
from extensions import db, jwt

load_dotenv()

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///certificates.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-change-in-production')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)

# Initialize extensions with app
db.init_app(app)
jwt.init_app(app)
CORS(app)

# Import models (after db initialization)
from models import User, Certificate, ShareLink

# Register blueprints
from routes.auth import auth_bp
from routes.certificates import certificates_bp

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(certificates_bp, url_prefix='/api/certificates')

@app.route('/api/health', methods=['GET'])
def health_check():
    return {'status': 'healthy', 'message': 'Certificate Vault API is running'}, 200

def create_tables():
    with app.app_context():
        db.create_all()

# Create tables on startup
create_tables()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

