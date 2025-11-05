import React, { useState, useEffect } from 'react';
import axios from 'axios';

function EmployeeDashboard({ user, onLogout }) {
  const [leaves, setLeaves] = useState([]);
  const [formData, setFormData] = useState({
    start_date: '',
    end_date: '',
    reason: ''
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [showForm, setShowForm] = useState(false);

  useEffect(() => {
    fetchLeaves();
  }, []);

  const fetchLeaves = async () => {
    try {
      const response = await axios.get('/leaves');
      setLeaves(response.data);
    } catch (err) {
      setError('Failed to fetch leave requests');
    }
  };

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      await axios.post('/leaves', formData);
      setFormData({ start_date: '', end_date: '', reason: '' });
      setShowForm(false);
      fetchLeaves();
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to create leave request');
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'approved': return 'status-approved';
      case 'rejected': return 'status-rejected';
      default: return 'status-pending';
    }
  };

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <h1>Welcome, {user.name}</h1>
        <button onClick={onLogout} className="logout-btn">Logout</button>
      </header>

      <div className="dashboard-content">
        <div className="dashboard-actions">
          <button onClick={() => setShowForm(!showForm)} className="btn-primary">
            {showForm ? 'Cancel' : 'Request Leave'}
          </button>
        </div>

        {error && <div className="error-message">{error}</div>}

        {showForm && (
          <div className="form-card">
            <h3>New Leave Request</h3>
            <form onSubmit={handleSubmit}>
              <div className="form-group">
                <label>Start Date</label>
                <input
                  type="date"
                  name="start_date"
                  value={formData.start_date}
                  onChange={handleChange}
                  required
                />
              </div>

              <div className="form-group">
                <label>End Date</label>
                <input
                  type="date"
                  name="end_date"
                  value={formData.end_date}
                  onChange={handleChange}
                  required
                />
              </div>

              <div className="form-group">
                <label>Reason</label>
                <textarea
                  name="reason"
                  value={formData.reason}
                  onChange={handleChange}
                  required
                  placeholder="Please provide a reason for your leave request"
                  rows="3"
                />
              </div>

              <button type="submit" disabled={loading} className="btn-primary">
                {loading ? 'Submitting...' : 'Submit Request'}
              </button>
            </form>
          </div>
        )}

        <div className="leaves-section">
          <h3>Your Leave Requests</h3>
          {leaves.length === 0 ? (
            <p>No leave requests found.</p>
          ) : (
            <div className="leaves-list">
              {leaves.map(leave => (
                <div key={leave.id} className="leave-card">
                  <div className="leave-info">
                    <p><strong>Dates:</strong> {leave.start_date} to {leave.end_date}</p>
                    <p><strong>Reason:</strong> {leave.reason}</p>
                    <p><strong>Status:</strong> <span className={getStatusColor(leave.status)}>{leave.status}</span></p>
                    <p><strong>Requested:</strong> {new Date(leave.created_at).toLocaleDateString()}</p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default EmployeeDashboard;
