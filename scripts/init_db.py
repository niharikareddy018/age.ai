#!/usr/bin/env python3
"""
Script to initialize the database and create initial admin user
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app import app, db
from models import User

def init_database():
    """Initialize the database and create tables"""
    with app.app_context():
        db.create_all()
        print("Database initialized successfully!")

def create_admin_user(username, email, password):
    """Create an admin/issuer user"""
    with app.app_context():
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            print(f"User '{username}' already exists!")
            return
        
        # Create issuer user
        user = User(
            username=username,
            email=email,
            role='issuer'
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        print(f"Issuer user '{username}' created successfully!")

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Initialize database and create admin user')
    parser.add_argument('--init-db', action='store_true', help='Initialize database')
    parser.add_argument('--create-issuer', action='store_true', help='Create issuer user')
    parser.add_argument('--username', type=str, help='Username for issuer')
    parser.add_argument('--email', type=str, help='Email for issuer')
    parser.add_argument('--password', type=str, help='Password for issuer')
    
    args = parser.parse_args()
    
    if args.init_db:
        init_database()
    
    if args.create_issuer:
        if not args.username or not args.email or not args.password:
            print("Error: --username, --email, and --password are required for creating issuer")
            sys.exit(1)
        create_admin_user(args.username, args.email, args.password)

