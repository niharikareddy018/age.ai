import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';

const VerifyCertificate = () => {
  const [certificateId, setCertificateId] = useState('');
  const [certificateHash, setCertificateHash] = useState('');
  const [verificationResult, setVerificationResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleVerify = async (e) => {
    e.preventDefault();
    setError('');
    setVerificationResult(null);
    setLoading(true);

    try {
      const data = {};
      if (certificateId) {
        data.certificate_id = certificateId;
      } else if (certificateHash) {
        data.certificate_hash = certificateHash;
      }

      const response = await api.post('/api/certificates/verify', data);
      setVerificationResult(response.data);
      
      if (response.data.certificate?.certificate_id) {
        // Navigate to certificate detail after a delay
        setTimeout(() => {
          navigate(`/certificate/${response.data.certificate.certificate_id}`);
        }, 2000);
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Verification failed');
      setVerificationResult({
        verified: false,
        message: 'Certificate not found or invalid'
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container main-content">
      <h1>Verify Certificate</h1>
      <p>Enter either the Certificate ID or Certificate Hash to verify</p>

      {error && <div className="alert alert-error">{error}</div>}

      <div className="card">
        <form onSubmit={handleVerify}>
          <div className="form-group">
            <label>Certificate ID</label>
            <input
              type="text"
              value={certificateId}
              onChange={(e) => {
                setCertificateId(e.target.value);
                setCertificateHash('');
              }}
              placeholder="Enter certificate ID"
            />
          </div>

          <div className="form-group">
            <label>OR Certificate Hash</label>
            <input
              type="text"
              value={certificateHash}
              onChange={(e) => {
                setCertificateHash(e.target.value);
                setCertificateId('');
              }}
              placeholder="Enter certificate hash"
            />
          </div>

          <button type="submit" className="btn btn-primary" disabled={loading || (!certificateId && !certificateHash)}>
            {loading ? 'Verifying...' : 'Verify Certificate'}
          </button>
        </form>
      </div>

      {verificationResult && (
        <div className="card">
          <h2>Verification Result</h2>
          {verificationResult.verified ? (
            <div className="alert alert-success">
              <strong>✓ Certificate Verified</strong>
              <p>{verificationResult.message}</p>
              {verificationResult.blockchain_verified && (
                <p>✓ Verified on blockchain</p>
              )}
            </div>
          ) : (
            <div className="alert alert-error">
              <strong>✗ Certificate Not Verified</strong>
              <p>{verificationResult.message}</p>
            </div>
          )}

          {verificationResult.certificate && (
            <div className="certificate-details">
              <h3>Certificate Details</h3>
              <p><strong>Student:</strong> {verificationResult.certificate.student_name}</p>
              <p><strong>Course:</strong> {verificationResult.certificate.course_name}</p>
              <p><strong>Issue Date:</strong> {new Date(verificationResult.certificate.issue_date).toLocaleDateString()}</p>
              <p><strong>Certificate ID:</strong> {verificationResult.certificate.certificate_id}</p>
              <p><strong>Hash:</strong> <code>{verificationResult.certificate.certificate_hash}</code></p>
              {verificationResult.certificate.blockchain_tx_hash && (
                <p><strong>Blockchain TX:</strong> <code>{verificationResult.certificate.blockchain_tx_hash}</code></p>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default VerifyCertificate;

