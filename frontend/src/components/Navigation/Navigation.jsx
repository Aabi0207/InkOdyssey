import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import './Navigation.css';

const Navigation = () => {
  const { user, logout } = useAuth();
  const location = useLocation();

  const isActive = (path) => {
    return location.pathname === path ? 'nav-link active' : 'nav-link';
  };

  return (
    <nav className="main-navigation">
      <div className="nav-container">
        <div className="nav-brand">
          <Link to="/diary">
            <span className="brand-icon">📖</span>
            <span className="brand-name">InkOdyssey</span>
          </Link>
        </div>
        
        <div className="nav-menu">
          <Link to="/diary" className={isActive('/diary')}>
            <span className="nav-icon">📝</span>
            Diary
          </Link>
          
          {/* Add more navigation items here as you build more features */}
          {/* <Link to="/calendar" className={isActive('/calendar')}>
            <span className="nav-icon">📅</span>
            Calendar
          </Link>
          
          <Link to="/search" className={isActive('/search')}>
            <span className="nav-icon">🔍</span>
            Search
          </Link>
          
          <Link to="/settings" className={isActive('/settings')}>
            <span className="nav-icon">⚙️</span>
            Settings
          </Link> */}
        </div>

        <div className="nav-user">
          {user && (
            <>
              <span className="user-name">
                {user.first_name} {user.last_name}
              </span>
              <button onClick={logout} className="logout-btn">
                Logout
              </button>
            </>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navigation;
