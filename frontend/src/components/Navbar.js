// frontend/src/components/Navbar.js
import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext'; // Adjust path if needed

const Navbar = () => {
  const { isAuthenticated, logout, currentUser } = useAuth();

  return (
    <nav style={{ padding: '1rem', background: '#eee', display: 'flex', gap: '1rem', alignItems: 'center' }}>
      <Link to="/">Home</Link>
      {isAuthenticated ? (
        <>
          <Link to="/dashboard">Dashboard</Link>
          <span style={{ marginLeft: 'auto' }}>Hello, {currentUser?.username}</span>
          <button onClick={logout}>Logout</button>
        </>
      ) : (
        <>
          <Link to="/login" style={{ marginLeft: 'auto' }}>Login</Link>
          <Link to="/register">Register</Link>
        </>
      )}
    </nav>
  );
};
export default Navbar;
