import { Link, Route, Routes } from 'react-router-dom';
import HomePage from './pages/HomePage';
import DashboardPage from './pages/DashboardPage';
import QuantumPage from './pages/QuantumPage';

export default function App() {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <nav className="mx-auto flex max-w-6xl items-center justify-between p-4">
        <Link to="/" className="text-xl font-bold text-cyan-300">CycloneQ</Link>
        <div className="space-x-4 text-sm">
          <Link to="/dashboard" className="hover:text-cyan-300">Dashboard</Link>
          <Link to="/quantum" className="hover:text-cyan-300">About Quantum</Link>
        </div>
      </nav>
      <main className="mx-auto max-w-6xl p-4">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/quantum" element={<QuantumPage />} />
        </Routes>
      </main>
    </div>
  );
}
