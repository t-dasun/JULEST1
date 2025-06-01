import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import apiClient from '../services/api'; // Adjust path

const RegisterPage = () => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [role, setRole] = useState('customer'); // Default role
  const [error, setError] = useState('');
  const [successMessage, setSuccessMessage] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccessMessage('');
    try {
      await apiClient.post('/auth/register/', { username, email, password, role });
      setSuccessMessage('Registration successful! Please login.');
      // Optionally, redirect to login after a short delay or let user click
      // For now, we will let the user click the link to login.
      // setTimeout(() => {
      //   navigate('/login');
      // }, 2000);
    } catch (err) {
      if (err.response && err.response.data) {
        let errorMsg = 'Failed to register.';
        // Attempt to parse and join backend errors
        try {
            const errors = err.response.data;
            Object.keys(errors).forEach((key) => {
                if (Array.isArray(errors[key])) {
                    errorMsg += ` ${key.charAt(0).toUpperCase() + key.slice(1)}: ${errors[key].join(' ')}`;
                } else {
                    errorMsg += ` ${key.charAt(0).toUpperCase() + key.slice(1)}: ${errors[key]}`;
                }
            });
        } catch (parseError) {
            // If parsing fails, use a generic message or the raw error if it's a string
            if (typeof err.response.data === 'string') {
                 errorMsg = err.response.data;
            }
            console.error("Error parsing backend error response:", parseError);
        }
        setError(errorMsg.trim());
      } else {
        setError('Failed to register. Please try again.');
      }
      console.error(err);
    }
  };

  return (
    <div>
      <h2>Register Page</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="reg-username">Username:</label>
          <input id="reg-username" type="text" value={username} onChange={e => setUsername(e.target.value)} required />
        </div>
        <div>
          <label htmlFor="reg-email">Email:</label>
          <input id="reg-email" type="email" value={email} onChange={e => setEmail(e.target.value)} required />
        </div>
        <div>
          <label htmlFor="reg-password">Password:</label>
          <input id="reg-password" type="password" value={password} onChange={e => setPassword(e.target.value)} required />
        </div>
        <div>
          <label htmlFor="reg-role">Role:</label>
          <select id="reg-role" value={role} onChange={e => setRole(e.target.value)}>
            <option value="customer">Customer</option>
            <option value="owner">Restaurant Owner</option>
          </select>
        </div>
        {error && <p style={{ color: 'red' }}>{error}</p>}
        {successMessage && <p style={{ color: 'green' }}>{successMessage}</p>}
        <button type="submit">Register</button>
      </form>
      <p>Already have an account? <Link to="/login">Login here</Link></p>
    </div>
  );
};
export default RegisterPage;
