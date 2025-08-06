import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import { ProtectedRoute } from './components/common/ProtectedRoute';
import { Header } from './components/common/Header';
import { Footer } from './components/common/Footer';
import { Welcome } from './pages/Welcome';
import { Dashboard } from './pages/Dashboard';
import { Investments } from './pages/Reactors';
import { Profile } from './pages/Profile';
import './styles/globals.css';
import './App.css';

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/" element={
            <div className="app-layout">
              <Welcome />
              <Footer />
            </div>
          } />

          <Route path="/dashboard" element={
            <ProtectedRoute>
              <div className="app-layout">
                <Header />
                <main className="main-content">
                  <Dashboard />
                </main>
                <Footer />
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
                <Footer />
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
                <Footer />
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