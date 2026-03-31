import React from 'react';
import { BrowserRouter as Router, Routes, Route, useLocation } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import { ThemeProvider } from './contexts/ThemeContext';
import Header from './components/Header';
import Landing from './pages/Landing';
import About from './pages/About';
import Login from './pages/Login';
import Register from './pages/Register';
import ForgotPassword from './pages/ForgotPassword';

import Dashboard from './pages/Dashboard';
import Analysis from './pages/Analysis';
import Compare from './pages/Compare';
import JobData from './pages/JobData';

// Component to conditionally render header
const AppContent = () => {
  const location = useLocation();
  const hideHeaderRoutes = ['/login', '/register', '/forgot-password'];
  const showHeader = !hideHeaderRoutes.includes(location.pathname);
  const isLandingPage = location.pathname === '/';
  const loggedInUser = localStorage.getItem('user');

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 transition-colors duration-300">
      {showHeader && (!isLandingPage || loggedInUser) && <Header />}
      <main className={isLandingPage && !loggedInUser ? '' : isLandingPage ? 'container mx-auto px-4 py-8' : 'container mx-auto px-4 py-8'}>
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/about" element={<About />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/forgot-password" element={<ForgotPassword />} />
          
          <Route path="/job-data" element={<JobData />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/analysis" element={<Analysis />} />
          <Route path="/compare" element={<Compare />} />
        </Routes>
      </main>
      <Toaster 
        position="top-right"
        toastOptions={{
          duration: 4000,
          style: {
            background: '#363636',
            color: '#fff',
          },
        }}
      />
    </div>
  );
};

function App() {
  return (
    <ThemeProvider>
      <Router>
        <AppContent />
      </Router>
    </ThemeProvider>
  );
}

export default App;