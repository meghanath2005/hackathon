export default function QuantumPage() {
  return (
    <section className="space-y-5 py-8">
      <h1 className="text-3xl font-bold text-cyan-300">Quantum Explainer</h1>
      <div className="rounded-xl border border-slate-800 bg-slate-900 p-6 text-sm text-slate-200">
        <p className="mb-3">
          Pipeline: <strong>Track history → GRU encoder → 4-qubit variational circuit → dense forecast head</strong>.
        </p>
        <p className="mb-3">
          The quantum block receives compressed hidden features and outputs expectation values, which are fused by the final dense layer.
        </p>
        <p>
          This is a simulator-based prototype. It does not claim operational readiness or proven quantum advantage.
        </p>
      </div>
    </section>
  );
}
