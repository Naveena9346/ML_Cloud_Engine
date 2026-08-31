"use client";

import React from "react";
import { Activity, AlertOctagon, CheckCircle2, RefreshCw } from "lucide-react";

export const MonitoringView: React.FC = () => {
  const mockDriftDetails = [
    { feature: "tenure", psi: 0.024, ks_stat: 0.015, p_value: 0.84, status: "NO DRIFT" },
    { feature: "MonthlyCharges", psi: 0.048, ks_stat: 0.022, p_value: 0.62, status: "NO DRIFT" },
    { feature: "TotalCharges", psi: 0.182, ks_stat: 0.078, p_value: 0.08, status: "WARNING" },
    { feature: "Contract", psi: 0.012, ks_stat: 0.008, p_value: 0.95, status: "NO DRIFT" },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-white tracking-tight">Model Drift Monitoring & Telemetry</h2>
          <p className="text-xs text-gray-400 mt-1">Continuous Population Stability Index (PSI) & Kolmogorov-Smirnov (KS) feature drift detection</p>
        </div>
        <button className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-gray-200 border border-slate-700 rounded-lg text-xs font-semibold flex items-center space-x-2 transition-colors">
          <RefreshCw className="w-3.5 h-3.5" />
          <span>Recalculate Drift Metrics</span>
        </button>
      </div>

      {/* Overview Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-dark-card border border-dark-border rounded-xl p-4">
          <div className="text-xs text-gray-400">Overall PSI Drift Score</div>
          <div className="text-2xl font-bold text-emerald-400 mt-1">0.0665</div>
          <div className="text-[10px] text-gray-500 mt-1">PSI &lt; 0.1 indicates population stability</div>
        </div>

        <div className="bg-dark-card border border-dark-border rounded-xl p-4">
          <div className="text-xs text-gray-400">Concept / Data Drift Detected</div>
          <div className="text-2xl font-bold text-emerald-400 mt-1 flex items-center space-x-2">
            <CheckCircle2 className="w-6 h-6 text-emerald-400" />
            <span>NO DRIFT</span>
          </div>
        </div>

        <div className="bg-dark-card border border-dark-border rounded-xl p-4">
          <div className="text-xs text-gray-400">Inference Samples Analyzed</div>
          <div className="text-2xl font-bold text-white mt-1">500 Samples</div>
          <div className="text-[10px] text-gray-500 mt-1">Comparing live telemetry vs baseline training set</div>
        </div>
      </div>

      {/* Feature Drift Details Table */}
      <div className="bg-dark-card border border-dark-border rounded-xl p-5 space-y-4">
        <h3 className="text-base font-semibold text-white flex items-center space-x-2">
          <Activity className="w-4 h-4 text-sky-400" />
          <span>Feature-Level Drift Decomposition</span>
        </h3>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-900 text-gray-400 uppercase font-semibold border-b border-dark-border">
              <tr>
                <th className="py-3 px-4">Feature Name</th>
                <th className="py-3 px-4">PSI Score</th>
                <th className="py-3 px-4">KS Statistic</th>
                <th className="py-3 px-4">p-Value</th>
                <th className="py-3 px-4">Drift Assessment</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-dark-border text-gray-300">
              {mockDriftDetails.map((f) => (
                <tr key={f.feature} className="hover:bg-slate-800/40 transition-colors">
                  <td className="py-3 px-4 font-medium text-white">{f.feature}</td>
                  <td className="py-3 px-4 font-mono text-sky-400">{f.psi}</td>
                  <td className="py-3 px-4 text-gray-400">{f.ks_stat}</td>
                  <td className="py-3 px-4 text-gray-400">{f.p_value}</td>
                  <td className="py-3 px-4">
                    <span
                      className={`px-2.5 py-0.5 rounded text-[10px] font-bold ${
                        f.status === "NO DRIFT"
                          ? "bg-emerald-950 text-emerald-400 border border-emerald-800/50"
                          : "bg-amber-950 text-amber-400 border border-amber-800/50"
                      }`}
                    >
                      {f.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
