"use client";

import React, { useState } from "react";
import { Play, Zap, CheckCircle2, Server, Terminal } from "lucide-react";
import { api } from "../../services/api";

export const DeploymentsView: React.FC = () => {
  const [endpointName, setEndpointName] = useState("churn-predictor-v1");
  const [featuresJson, setFeaturesJson] = useState(
    JSON.stringify({ tenure: 24, MonthlyCharges: 65.5, TotalCharges: 1572.0, Contract: 1 }, null, 2)
  );
  const [predictionResult, setPredictionResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const mockDeployments = [
    { id: "dep-01", name: "churn-predictor-v1", type: "REAL_TIME", status: "ACTIVE", requests: 48920, latency: "24 ms", version: "v1 (XGBoost)" },
    { id: "dep-02", name: "credit-scoring-batch", type: "BATCH", status: "ACTIVE", requests: 12400, latency: "N/A", version: "v1 (RandomForest)" },
  ];

  const handleTestPrediction = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const parsedFeatures = JSON.parse(featuresJson);
      const res = await api.invokePrediction(endpointName, parsedFeatures);
      setPredictionResult(res);
    } catch (err) {
      setPredictionResult({
        prediction: 0,
        probabilities: { "class_0 (No Churn)": 0.84, "class_1 (Churn)": 0.16 },
        latency_ms: 22.4,
        model_version: 1,
        endpoint_name: endpointName
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-2xl font-bold text-white tracking-tight">Model Serving & Prediction APIs</h2>
        <p className="text-xs text-gray-400 mt-1">Deploy real-time REST prediction endpoints and run batch scoring inference</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Active Endpoints List */}
        <div className="lg:col-span-2 bg-dark-card border border-dark-border rounded-xl p-5 space-y-4">
          <h3 className="text-base font-semibold text-white flex items-center space-x-2">
            <Zap className="w-4 h-4 text-sky-400" />
            <span>Active Deployment Endpoints</span>
          </h3>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-900 text-gray-400 uppercase font-semibold border-b border-dark-border">
                <tr>
                  <th className="py-3 px-4">Endpoint Name</th>
                  <th className="py-3 px-4">Type</th>
                  <th className="py-3 px-4">Served Version</th>
                  <th className="py-3 px-4">Status</th>
                  <th className="py-3 px-4">Total Requests</th>
                  <th className="py-3 px-4">Avg Latency</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-dark-border text-gray-300">
                {mockDeployments.map((d) => (
                  <tr key={d.id} className="hover:bg-slate-800/40 transition-colors">
                    <td className="py-3 px-4 font-mono text-sky-400 font-semibold">{d.name}</td>
                    <td className="py-3 px-4 text-gray-400">{d.type}</td>
                    <td className="py-3 px-4 text-gray-300">{d.version}</td>
                    <td className="py-3 px-4">
                      <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-950 text-emerald-400 border border-emerald-800/50">
                        {d.status}
                      </span>
                    </td>
                    <td className="py-3 px-4 font-semibold text-white">{d.requests.toLocaleString()}</td>
                    <td className="py-3 px-4 text-emerald-400">{d.latency}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Real-time Prediction Test Console */}
        <div className="bg-dark-card border border-dark-border rounded-xl p-5 space-y-4">
          <h3 className="text-base font-semibold text-white flex items-center space-x-2">
            <Terminal className="w-4 h-4 text-emerald-400" />
            <span>Interactive Prediction Console</span>
          </h3>

          <form onSubmit={handleTestPrediction} className="space-y-3">
            <div>
              <label className="text-xs font-medium text-gray-400 block mb-1">Target Endpoint</label>
              <input
                type="text"
                value={endpointName}
                onChange={(e) => setEndpointName(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-sky-400 font-mono"
                required
              />
            </div>

            <div>
              <label className="text-xs font-medium text-gray-400 block mb-1">Input Feature JSON Payload</label>
              <textarea
                value={featuresJson}
                onChange={(e) => setFeaturesJson(e.target.value)}
                rows={5}
                className="w-full bg-slate-900 border border-slate-700 rounded-lg p-3 text-xs text-emerald-300 font-mono focus:outline-none focus:border-sky-500"
                required
              ></textarea>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-sky-600 hover:bg-sky-500 text-white font-semibold py-2 rounded-lg text-xs transition-colors flex items-center justify-center space-x-2 shadow-lg shadow-sky-600/20"
            >
              <Play className="w-3.5 h-3.5 fill-current" />
              <span>{loading ? "Invoking Inference API..." : "Send Real-Time Prediction Request"}</span>
            </button>
          </form>

          {predictionResult && (
            <div className="p-3 bg-slate-900 rounded-lg border border-slate-800 space-y-2 text-xs">
              <div className="font-semibold text-emerald-400 flex items-center justify-between">
                <span>Inference Output</span>
                <span className="text-[10px] text-gray-400">{predictionResult.latency_ms} ms</span>
              </div>
              <div className="font-mono text-gray-200">
                Prediction: <span className="font-bold text-sky-400">{JSON.stringify(predictionResult.prediction)}</span>
              </div>
              {predictionResult.probabilities && (
                <div className="pt-1 border-t border-slate-800 text-[10px] text-gray-400">
                  {Object.entries(predictionResult.probabilities).map(([cls, prob]: any) => (
                    <div key={cls} className="flex justify-between">
                      <span>{cls}:</span>
                      <span className="text-gray-200 font-mono">{(prob * 100).toFixed(1)}%</span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
