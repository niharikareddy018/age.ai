import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import './Navbar.css';

const Navbar = () => {
  const { user, logout, isAuthenticated, isIssuer } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-brand">
          Certificate Vault
        </Link>
        <div className="navbar-menu">
          {isAuthenticated ? (
            <>
              <Link to="/dashboard" className="navbar-link">
                Dashboard
              </Link>
              {isIssuer && (
                <Link to="/issue" className="navbar-link">
                  Issue Certificate
                </Link>
              )}
              <Link to="/verify" className="navbar-link">
                Verify
              </Link>
              <div className="navbar-user">
                <span>Welcome, {user?.username}</span>
                <button onClick={handleLogout} className="btn btn-secondary">
                  Logout
                </button>
              </div>
            </>
          ) : (
            <>
              <Link to="/login" className="navbar-link">
                Login
              </Link>
              <Link to="/register" className="navbar-link">
                Register
              </Link>
              <Link to="/verify" className="navbar-link">
                Verify
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;

