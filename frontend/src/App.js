// frontend/src/App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar'; // Adjust path
import HomePage from './pages/HomePage';   // Adjust path
import LoginPage from './pages/LoginPage'; // Adjust path
import RegisterPage from './pages/RegisterPage'; // Adjust path
import DashboardPage from './pages/DashboardPage'; // Adjust path
import ProtectedRoute from './components/ProtectedRoute'; // Adjust path
import './App.css'; // Keep or modify

function App() {
  return (
    <Router>
      <Navbar />
      <div className="container" style={{ padding: '1rem' }}> {/* Optional container */}
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route element={<ProtectedRoute />}>
            <Route path="/dashboard" element={<DashboardPage />} />
            {/* Other protected routes can be added here */}
          </Route>
          {/* <Route path="*" element={<div>Page Not Found</div>} /> */}
        </Routes>
      </div>
    </Router>
  );
}
export default App;
