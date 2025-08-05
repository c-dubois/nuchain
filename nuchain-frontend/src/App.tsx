import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import { ProtectedRoute } from './components/common/ProtectedRoute';
import { Header } from './components/common/Header';
import { Welcome } from './pages/Welcome';
import { Dashboard } from './pages/Dashboard';
import { Investments } from './pages/Investments';
import { Profile } from './pages/Profile';
import './styles/globals.css';
import './App.css';

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/" element={<Welcome />} />
          
          {/* Protected routes with Header */}
          <Route path="/dashboard" element={
            <ProtectedRoute>
              <div className="app-layout">
                <Header />
                <main className="main-content">
                  <Dashboard />
                </main>
              </div>
            </ProtectedRoute>
          } />
          
          <Route path="/invest" element={
            <ProtectedRoute>
              <div className="app-layout">
                <Header />
                <main className="main-content">
                  <Investments />
                </main>
              </div>
            </ProtectedRoute>
          } />
          
          <Route path="/profile" element={
            <ProtectedRoute>
              <div className="app-layout">
                <Header />
                <main className="main-content">
                  <Profile />
                </main>
              </div>
            </ProtectedRoute>
          } />
          
          {/* Redirect any unknown routes */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;