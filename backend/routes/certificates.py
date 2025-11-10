from flask import Blueprint, request, jsonify
from models import Certificate, User, ShareLink
from extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timedelta
from blockchain_utils import calculate_certificate_hash, store_certificate_on_blockchain, verify_certificate_on_blockchain
import json

certificates_bp = Blueprint('certificates', __name__)

@certificates_bp.route('/issue', methods=['POST'])
@jwt_required()
def issue_certificate():
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or current_user.role != 'issuer':
            return jsonify({'error': 'Unauthorized. Only issuers can issue certificates'}), 403
        
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        student_name = data.get('student_name')
        course_name = data.get('course_name')
        owner_id = data.get('owner_id')  # User ID of the certificate owner
        issue_date = data.get('issue_date')
        expiration_date = data.get('expiration_date')
        metadata = data.get('metadata')
        
        if not student_name or not course_name or not owner_id:
            return jsonify({'error': 'student_name, course_name, and owner_id are required'}), 400
        
        # Verify owner exists
        owner = User.query.get(owner_id)
        if not owner:
            return jsonify({'error': 'Owner not found'}), 404
        
        # Parse dates
        try:
            if issue_date:
                issue_date = datetime.strptime(issue_date, '%Y-%m-%d').date()
            else:
                issue_date = datetime.utcnow().date()
            
            if expiration_date:
                expiration_date = datetime.strptime(expiration_date, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
        
        # Create certificate
        certificate = Certificate(
            owner_id=owner_id,
            issuer_id=current_user_id,
            student_name=student_name,
            course_name=course_name,
            issue_date=issue_date,
            expiration_date=expiration_date,
            metadata=json.dumps(metadata) if metadata else None
        )
        
        # Calculate certificate hash
        certificate_hash = calculate_certificate_hash(
            student_name=student_name,
            course_name=course_name,
            issue_date=str(issue_date),
            issuer_id=current_user_id,
            owner_id=owner_id
        )
        certificate.certificate_hash = certificate_hash
        
        db.session.add(certificate)
        db.session.flush()  # Get the certificate ID
        
        # Store on blockchain
        try:
            tx_hash = store_certificate_on_blockchain(
                certificate_id=certificate.certificate_id,
                certificate_hash=certificate_hash,
                student_name=student_name,
                course_name=course_name,
                issue_date=str(issue_date)
            )
            certificate.blockchain_tx_hash = tx_hash
            certificate.blockchain_status = 'confirmed'
        except Exception as e:
            certificate.blockchain_status = 'failed'
            db.session.commit()
            return jsonify({
                'error': 'Failed to store certificate on blockchain',
                'details': str(e),
                'certificate': certificate.to_dict()
            }), 500
        
        db.session.commit()
        
        return jsonify({
            'message': 'Certificate issued successfully',
            'certificate': certificate.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@certificates_bp.route('/verify', methods=['POST'])
def verify_certificate():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        certificate_hash = data.get('certificate_hash')
        certificate_id = data.get('certificate_id')
        
        if not certificate_hash and not certificate_id:
            return jsonify({'error': 'certificate_hash or certificate_id is required'}), 400
        
        # Find certificate in database
        if certificate_id:
            certificate = Certificate.query.filter_by(certificate_id=certificate_id).first()
        else:
            certificate = Certificate.query.filter_by(certificate_hash=certificate_hash).first()
        
        if not certificate:
            return jsonify({
                'verified': False,
                'message': 'Certificate not found in database'
            }), 404
        
        if certificate.is_revoked:
            return jsonify({
                'verified': False,
                'message': 'Certificate has been revoked'
            }), 200
        
        # Verify on blockchain
        try:
            blockchain_verified = verify_certificate_on_blockchain(certificate.certificate_hash)
            
            return jsonify({
                'verified': blockchain_verified,
                'certificate': certificate.to_dict(),
                'blockchain_verified': blockchain_verified,
                'message': 'Certificate verified successfully' if blockchain_verified else 'Certificate not found on blockchain'
            }), 200
        except Exception as e:
            return jsonify({
                'verified': False,
                'error': 'Blockchain verification failed',
                'details': str(e),
                'certificate': certificate.to_dict()
            }), 500
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@certificates_bp.route('/my-certificates', methods=['GET'])
@jwt_required()
def get_my_certificates():
    try:
        current_user_id = get_jwt_identity()
        
        certificates = Certificate.query.filter_by(owner_id=current_user_id).all()
        
        return jsonify({
            'certificates': [cert.to_dict() for cert in certificates]
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@certificates_bp.route('/issued', methods=['GET'])
@jwt_required()
def get_issued_certificates():
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or current_user.role != 'issuer':
            return jsonify({'error': 'Unauthorized. Only issuers can view issued certificates'}), 403
        
        certificates = Certificate.query.filter_by(issuer_id=current_user_id).all()
        
        return jsonify({
            'certificates': [cert.to_dict() for cert in certificates]
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@certificates_bp.route('/<certificate_id>', methods=['GET'])
def get_certificate(certificate_id):
    try:
        certificate = Certificate.query.filter_by(certificate_id=certificate_id).first()
        
        if not certificate:
            return jsonify({'error': 'Certificate not found'}), 404
        
        return jsonify({'certificate': certificate.to_dict()}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@certificates_bp.route('/<certificate_id>/share', methods=['POST'])
@jwt_required()
def create_share_link(certificate_id):
    try:
        current_user_id = get_jwt_identity()
        
        certificate = Certificate.query.filter_by(certificate_id=certificate_id).first()
        
        if not certificate:
            return jsonify({'error': 'Certificate not found'}), 404
        
        if certificate.owner_id != current_user_id:
            return jsonify({'error': 'Unauthorized. You can only share your own certificates'}), 403
        
        data = request.get_json()
        expires_in_days = data.get('expires_in_days', 7) if data else 7
        
        expires_at = datetime.utcnow() + timedelta(days=expires_in_days)
        
        share_link = ShareLink(
            certificate_id=certificate.id,
            expires_at=expires_at
        )
        
        db.session.add(share_link)
        db.session.commit()
        
        return jsonify({
            'message': 'Share link created successfully',
            'share_link': share_link.to_dict(),
            'share_url': f'/verify/share/{share_link.link_token}'
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@certificates_bp.route('/share/<link_token>', methods=['GET'])
def get_shared_certificate(link_token):
    try:
        share_link = ShareLink.query.filter_by(link_token=link_token).first()
        
        if not share_link:
            return jsonify({'error': 'Share link not found'}), 404
        
        if share_link.is_expired() or not share_link.is_active:
            return jsonify({'error': 'Share link has expired'}), 410
        
        share_link.access_count += 1
        db.session.commit()
        
        certificate = Certificate.query.get(share_link.certificate_id)
        
        return jsonify({
            'certificate': certificate.to_dict(),
            'share_link': share_link.to_dict()
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@certificates_bp.route('/<certificate_id>/revoke', methods=['POST'])
@jwt_required()
def revoke_certificate(certificate_id):
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        certificate = Certificate.query.filter_by(certificate_id=certificate_id).first()
        
        if not certificate:
            return jsonify({'error': 'Certificate not found'}), 404
        
        if certificate.issuer_id != current_user_id and current_user.role != 'issuer':
            return jsonify({'error': 'Unauthorized. Only the issuer can revoke certificates'}), 403
        
        certificate.is_revoked = True
        certificate.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Certificate revoked successfully',
            'certificate': certificate.to_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

