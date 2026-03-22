import { useEffect, useMemo, useState } from 'react';
import MetricCard from '../components/MetricCard';
import TrackMap from '../components/TrackMap';
import { getCyclones, predictClassical, predictHybrid } from '../api/client';

export default function DashboardPage() {
  const [cyclones, setCyclones] = useState([]);
  const [cycloneId, setCycloneId] = useState('');
  const [horizon, setHorizon] = useState(24);
  const [classical, setClassical] = useState(null);
  const [hybrid, setHybrid] = useState(null);

  useEffect(() => {
    getCyclones().then((data) => {
      setCyclones(data.cyclones);
      if (data.cyclones.length) setCycloneId(data.cyclones[0].cyclone_id);
    });
  }, []);

  const runClassical = async () => {
    setClassical(await predictClassical({ cyclone_id: cycloneId, forecast_horizon_hours: Number(horizon) }));
  };

  const runHybrid = async () => {
    setHybrid(await predictHybrid({ cyclone_id: cycloneId, forecast_horizon_hours: Number(horizon) }));
  };

  const actual = classical?.actual_track || hybrid?.actual_track || [];
  const comparison = useMemo(() => {
    if (!classical || !hybrid) return null;
    return hybrid.metrics.track_error_km - classical.metrics.track_error_km;
  }, [classical, hybrid]);

  return (
    <section className="space-y-5 py-6">
      <h1 className="text-3xl font-bold text-cyan-300">Forecast Dashboard</h1>
      <div className="grid gap-3 rounded-xl border border-slate-800 bg-slate-900 p-4 md:grid-cols-4">
        <select className="rounded bg-slate-800 p-2" value={cycloneId} onChange={(e) => setCycloneId(e.target.value)}>
          {cyclones.map((storm) => (
            <option key={storm.cyclone_id} value={storm.cyclone_id}>{storm.name} ({storm.season})</option>
          ))}
        </select>
        <select className="rounded bg-slate-800 p-2" value={horizon} onChange={(e) => setHorizon(e.target.value)}>
          <option value={24}>24 hours</option>
          <option value={48}>48 hours</option>
        </select>
        <button className="rounded bg-amber-400 px-3 py-2 font-semibold text-slate-950" onClick={runClassical}>Run Classical</button>
        <button className="rounded bg-emerald-400 px-3 py-2 font-semibold text-slate-950" onClick={runHybrid}>Run Hybrid</button>
      </div>
      <TrackMap actual={actual} classical={classical?.predicted_track || []} hybrid={hybrid?.predicted_track || []} />
      <div className="grid gap-3 md:grid-cols-4">
        <MetricCard label="Classical MAE" value={classical ? classical.metrics.mae : '-'} />
        <MetricCard label="Hybrid MAE" value={hybrid ? hybrid.metrics.mae : '-'} />
        <MetricCard label="Classical Track Error (km)" value={classical ? classical.metrics.track_error_km : '-'} />
        <MetricCard label="Hybrid Track Error (km)" value={hybrid ? hybrid.metrics.track_error_km : '-'} />
      </div>
      {comparison !== null && (
        <p className="text-sm text-slate-300">
          Comparison: Hybrid {comparison <= 0 ? 'improves' : 'underperforms'} classical by {Math.abs(comparison).toFixed(2)} km average track error.
        </p>
      )}
    </section>
  );
}
