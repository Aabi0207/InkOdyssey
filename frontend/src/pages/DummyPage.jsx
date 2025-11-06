import React from 'react';
import { useAuth } from '../context/AuthContext';

const DummyPage = () => {
  const { logout, user } = useAuth();

  return (
    <div style={{
      minHeight: '100vh',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      background: '#f7f9fc',
      padding: '2rem'
    }}>
      <img src="/logo.png" alt="Logo" style={{ height: 80, marginBottom: 16 }} />
      <h1 style={{ margin: 0, color: '#1A2A4F' }}>Protected Area</h1>
      <p style={{ color: '#4a5568', marginTop: 8 }}>Hello {user?.first_name || user?.email || 'user'} 👋</p>
      <button
        onClick={logout}
        style={{
          marginTop: 24,
          padding: '10px 20px',
          borderRadius: 999,
          border: '2px solid #1A2A4F',
          background: 'white',
          color: '#1A2A4F',
          fontWeight: 600,
          cursor: 'pointer'
        }}
      >
        Logout
      </button>
    </div>
  );
};

export default DummyPage;
