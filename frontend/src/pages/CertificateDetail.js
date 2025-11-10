import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import api from '../services/api';
import './CertificateDetail.css';

const CertificateDetail = () => {
  const { certificateId, linkToken } = useParams();
  const { user, isIssuer } = useAuth();
  const [certificate, setCertificate] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [shareLink, setShareLink] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    fetchCertificate();
  }, [certificateId, linkToken]);

  const fetchCertificate = async () => {
    try {
      let response;
      if (linkToken) {
        // Fetch via share link
        response = await api.get(`/api/certificates/share/${linkToken}`);
        setCertificate(response.data.certificate);
      } else if (certificateId) {
        // Fetch via certificate ID
        response = await api.get(`/api/certificates/${certificateId}`);
        setCertificate(response.data.certificate);
      } else {
        setError('No certificate ID or share token provided');
        setLoading(false);
        return;
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to fetch certificate');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateShareLink = async () => {
    if (!certificate?.certificate_id) {
      setError('Certificate ID not available');
      return;
    }
    try {
      const response = await api.post(`/api/certificates/${certificate.certificate_id}/share`, {
        expires_in_days: 7
      });
      const baseUrl = window.location.origin;
      setShareLink(`${baseUrl}/verify/share/${response.data.share_link.link_token}`);
    } catch (err) {
      setError('Failed to create share link');
    }
  };

  const handleRevoke = async () => {
    if (!certificate?.certificate_id) {
      setError('Certificate ID not available');
      return;
    }
    if (!window.confirm('Are you sure you want to revoke this certificate?')) {
      return;
    }

    try {
      await api.post(`/api/certificates/${certificate.certificate_id}/revoke`);
      fetchCertificate();
    } catch (err) {
      setError('Failed to revoke certificate');
    }
  };

  if (loading) {
    return <div className="container main-content">Loading...</div>;
  }

  if (error && !certificate) {
    return <div className="container main-content"><div className="alert alert-error">{error}</div></div>;
  }

  if (!certificate) {
    return <div className="container main-content">Certificate not found</div>;
  }

  const isOwner = user && certificate && certificate.owner_id === user.id;
  const canShare = isOwner && !linkToken; // Can't create share link from a share link
  const canRevoke = isIssuer && certificate && certificate.issuer_id === user?.id && !linkToken;

  return (
    <div className="container main-content">
      <button onClick={() => navigate(-1)} className="btn btn-secondary" style={{ marginBottom: '20px' }}>
        ← Back
      </button>

      <div className="card">
        <h1>Certificate Details</h1>
        
        {certificate.is_revoked && (
          <div className="alert alert-error">
            <strong>This certificate has been revoked</strong>
          </div>
        )}

        <div className="certificate-info">
          <div className="info-row">
            <strong>Certificate ID:</strong>
            <code>{certificate.certificate_id}</code>
          </div>
          <div className="info-row">
            <strong>Student Name:</strong>
            <span>{certificate.student_name}</span>
          </div>
          <div className="info-row">
            <strong>Course Name:</strong>
            <span>{certificate.course_name}</span>
          </div>
          <div className="info-row">
            <strong>Issuer:</strong>
            <span>{certificate.issuer_name || 'Unknown'}</span>
          </div>
          <div className="info-row">
            <strong>Issue Date:</strong>
            <span>{new Date(certificate.issue_date).toLocaleDateString()}</span>
          </div>
          {certificate.expiration_date && (
            <div className="info-row">
              <strong>Expiration Date:</strong>
              <span>{new Date(certificate.expiration_date).toLocaleDateString()}</span>
            </div>
          )}
          <div className="info-row">
            <strong>Blockchain Status:</strong>
            <span className={`status-badge ${certificate.blockchain_status}`}>
              {certificate.blockchain_status}
            </span>
          </div>
          <div className="info-row">
            <strong>Certificate Hash:</strong>
            <code style={{ wordBreak: 'break-all' }}>{certificate.certificate_hash}</code>
          </div>
          {certificate.blockchain_tx_hash && (
            <div className="info-row">
              <strong>Blockchain Transaction:</strong>
              <code style={{ wordBreak: 'break-all' }}>{certificate.blockchain_tx_hash}</code>
            </div>
          )}
        </div>

        <div className="certificate-actions">
          {canShare && (
            <button onClick={handleCreateShareLink} className="btn btn-primary">
              Create Share Link
            </button>
          )}
          {canRevoke && !certificate.is_revoked && (
            <button onClick={handleRevoke} className="btn btn-danger">
              Revoke Certificate
            </button>
          )}
          <button
            onClick={() => navigate('/verify')}
            className="btn btn-secondary"
          >
            Verify Certificate
          </button>
        </div>

        {shareLink && (
          <div className="alert alert-success">
            <strong>Share Link Created:</strong>
            <input
              type="text"
              value={shareLink}
              readOnly
              style={{ width: '100%', marginTop: '10px', padding: '10px' }}
              onClick={(e) => e.target.select()}
            />
          </div>
        )}
      </div>
    </div>
  );
};

export default CertificateDetail;

