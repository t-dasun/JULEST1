import React from 'react';
import { useAuth } from '../contexts/AuthContext'; // Correct path based on your structure

const DashboardPage = () => {
  const { currentUser } = useAuth();
  return (
    <div>
      <h2>Dashboard</h2>
      <p>Welcome, {currentUser ? currentUser.username : 'User'}!</p>
      <p>This is a protected area.</p>
    </div>
  );
};
export default DashboardPage;
