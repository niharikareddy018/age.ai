import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import api from '../services/api';
import './Dashboard.css';

const Dashboard = () => {
  const { user, isIssuer } = useAuth();
  const [certificates, setCertificates] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    fetchCertificates();
  }, []);

  const fetchCertificates = async () => {
    try {
      setLoading(true);
      const endpoint = isIssuer ? '/api/certificates/issued' : '/api/certificates/my-certificates';
      const response = await api.get(endpoint);
      setCertificates(response.data.certificates || []);
    } catch (err) {
      setError('Failed to fetch certificates');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleCertificateClick = (certificateId) => {
    navigate(`/certificate/${certificateId}`);
  };

  if (loading) {
    return <div className="container main-content">Loading...</div>;
  }

  return (
    <div className="container main-content">
      <h1>Dashboard</h1>
      <p>Welcome, {user?.username}!</p>
      
      {isIssuer && (
        <div className="dashboard-actions">
          <button
            className="btn btn-primary"
            onClick={() => navigate('/issue')}
          >
            Issue New Certificate
          </button>
        </div>
      )}

      {error && <div className="alert alert-error">{error}</div>}

      <h2>{isIssuer ? 'Issued Certificates' : 'My Certificates'}</h2>
      
      {certificates.length === 0 ? (
        <div className="card">
          <p>No certificates found.</p>
        </div>
      ) : (
        <div className="certificates-grid">
          {certificates.map((cert) => (
            <div
              key={cert.certificate_id}
              className="certificate-card"
              onClick={() => handleCertificateClick(cert.certificate_id)}
            >
              <h3>{cert.course_name}</h3>
              <p><strong>Student:</strong> {cert.student_name}</p>
              <p><strong>Issue Date:</strong> {new Date(cert.issue_date).toLocaleDateString()}</p>
              <p>
                <span className={`status-badge ${cert.blockchain_status}`}>
                  {cert.blockchain_status}
                </span>
              </p>
              {cert.is_revoked && (
                <span className="status-badge revoked">Revoked</span>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Dashboard;

