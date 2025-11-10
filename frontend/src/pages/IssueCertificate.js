import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import api from '../services/api';

const IssueCertificate = () => {
  const { isIssuer } = useAuth();
  const [users, setUsers] = useState([]);
  const [formData, setFormData] = useState({
    owner_id: '',
    student_name: '',
    course_name: '',
    issue_date: new Date().toISOString().split('T')[0],
    expiration_date: '',
    metadata: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    if (!isIssuer) {
      navigate('/dashboard');
      return;
    }
    fetchUsers();
  }, [isIssuer, navigate]);

  const fetchUsers = async () => {
    try {
      const response = await api.get('/api/auth/users');
      setUsers(response.data.users || []);
    } catch (err) {
      console.error('Error fetching users:', err);
    }
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    setLoading(true);

    try {
      const response = await api.post('/api/certificates/issue', formData);
      setSuccess('Certificate issued successfully!');
      setTimeout(() => {
        navigate(`/certificate/${response.data.certificate.certificate_id}`);
      }, 2000);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to issue certificate');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container main-content">
      <h1>Issue Certificate</h1>
      
      {error && <div className="alert alert-error">{error}</div>}
      {success && <div className="alert alert-success">{success}</div>}

      <div className="card">
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Owner (Student)</label>
            <select
              name="owner_id"
              value={formData.owner_id}
              onChange={handleChange}
              required
            >
              <option value="">Select a user</option>
              {users.map((user) => (
                <option key={user.id} value={user.id}>
                  {user.username} ({user.email})
                </option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label>Student Name</label>
            <input
              type="text"
              name="student_name"
              value={formData.student_name}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label>Course Name</label>
            <input
              type="text"
              name="course_name"
              value={formData.course_name}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label>Issue Date</label>
            <input
              type="date"
              name="issue_date"
              value={formData.issue_date}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label>Expiration Date (Optional)</label>
            <input
              type="date"
              name="expiration_date"
              value={formData.expiration_date}
              onChange={handleChange}
            />
          </div>

          <div className="form-group">
            <label>Metadata (JSON, Optional)</label>
            <textarea
              name="metadata"
              value={formData.metadata}
              onChange={handleChange}
              rows="4"
              placeholder='{"grade": "A", "credits": 3}'
            />
          </div>

          <button type="submit" className="btn btn-primary" disabled={loading}>
            {loading ? 'Issuing...' : 'Issue Certificate'}
          </button>
        </form>
      </div>
    </div>
  );
};

export default IssueCertificate;

