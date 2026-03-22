import { Link } from 'react-router-dom';

export default function HomePage() {
  return (
    <section className="space-y-6 py-10">
      <h1 className="text-4xl font-extrabold text-cyan-300">CycloneQ</h1>
      <p className="max-w-3xl text-slate-200">
        Hybrid quantum-classical cyclone track forecasting for North Indian Ocean storms. This MVP compares
        a compact classical model and a small quantum-enhanced model for 24h/48h trajectory prediction.
      </p>
      <div className="grid gap-4 md:grid-cols-2">
        <div className="rounded-xl border border-slate-800 bg-slate-900 p-6">
          <h2 className="mb-2 text-lg font-semibold">Why this matters</h2>
          <p className="text-sm text-slate-300">Reliable cyclone path estimates can support preparedness and communication in high-risk coastal regions.</p>
        </div>
        <div className="rounded-xl border border-slate-800 bg-slate-900 p-6">
          <h2 className="mb-2 text-lg font-semibold">Quantum angle</h2>
          <p className="text-sm text-slate-300">A tiny variational quantum layer is used as a feature transform inside a larger classical pipeline.</p>
        </div>
      </div>
      <Link to="/dashboard" className="inline-block rounded-lg bg-cyan-500 px-5 py-3 font-semibold text-slate-950">
        Launch Forecast Dashboard
      </Link>
    </section>
  );
}
