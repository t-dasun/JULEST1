// frontend/src/App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar'; // Adjust path
import HomePage from './pages/HomePage';   // Adjust path
import LoginPage from './pages/LoginPage'; // Adjust path
import RegisterPage from './pages/RegisterPage';
import DashboardPage from './pages/DashboardPage';
import ProtectedRoute from './components/ProtectedRoute';
import RestaurantListPage from './pages/RestaurantListPage'; // Added
import RestaurantDetailPage from './pages/RestaurantDetailPage'; // Added
import './App.css';

function App() {
  return (
    <Router>
      <Navbar />
      <div className="container" style={{ padding: '1rem' }}> {/* Optional container */}
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/restaurants" element={<RestaurantListPage />} /> {/* Added */}
          <Route path="/restaurants/:restaurantId" element={<RestaurantDetailPage />} /> {/* Added */}
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
