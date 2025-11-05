import React, { useState, useEffect } from 'react';
import axios from 'axios';

function AdminDashboard({ user, onLogout }) {
  const [leaves, setLeaves] = useState([]);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

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

  const handleStatusUpdate = async (leaveId, status) => {
    setLoading(true);
    try {
      await axios.patch(`/leaves/${leaveId}/status`, { status });
      fetchLeaves();
    } catch (err) {
      setError('Failed to update leave status');
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
        <h1>Admin Dashboard - {user.name}</h1>
        <button onClick={onLogout} className="logout-btn">Logout</button>
      </header>

      <div className="dashboard-content">
        {error && <div className="error-message">{error}</div>}

        <div className="leaves-section">
          <h3>All Leave Requests</h3>
          {leaves.length === 0 ? (
            <p>No leave requests found.</p>
          ) : (
            <div className="leaves-list">
              {leaves.map(leave => (
                <div key={leave.id} className="leave-card">
                  <div className="leave-info">
                    <p><strong>Employee:</strong> {leave.employee_name}</p>
                    <p><strong>Dates:</strong> {leave.start_date} to {leave.end_date}</p>
                    <p><strong>Reason:</strong> {leave.reason}</p>
                    <p><strong>Status:</strong> <span className={getStatusColor(leave.status)}>{leave.status}</span></p>
                    <p><strong>Requested:</strong> {new Date(leave.created_at).toLocaleDateString()}</p>
                  </div>
                  {leave.status === 'pending' && (
                    <div className="leave-actions">
                      <button
                        onClick={() => handleStatusUpdate(leave.id, 'approved')}
                        disabled={loading}
                        className="btn-approve"
                      >
                        Approve
                      </button>
                      <button
                        onClick={() => handleStatusUpdate(leave.id, 'rejected')}
                        disabled={loading}
                        className="btn-reject"
                      >
                        Reject
                      </button>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default AdminDashboard;
