import './App.css'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'
import DummyPage from './pages/DummyPage'
import DiaryPage from './pages/DiaryPage'
import ProtectedRoute from './components/ProtectedRoute'
import PublicRoute from './components/PublicRoute'
import { AuthProvider } from './context/AuthContext'

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          {/* Public only */}
          <Route path="/login" element={<PublicRoute><LoginPage /></PublicRoute>} />
          <Route path="/register" element={<PublicRoute><RegisterPage /></PublicRoute>} />

          {/* Protected routes */}
          <Route path="/dummy" element={<ProtectedRoute><DummyPage /></ProtectedRoute>} />
          <Route path="/diary" element={<ProtectedRoute><DiaryPage /></ProtectedRoute>} />

          {/* Default route */}
          <Route path="/" element={<Navigate to="/diary" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  )
}

export default App
