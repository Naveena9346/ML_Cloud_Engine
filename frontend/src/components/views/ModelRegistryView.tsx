"use client";

import React, { useState } from "react";
import { CheckCircle2, ShieldAlert, Tag, ArrowRight, Layers } from "lucide-react";
import { api } from "../../services/api";

export const ModelRegistryView: React.FC = () => {
  const [selectedStage, setSelectedStage] = useState<string>("PRODUCTION");

  const mockModels = [
    { id: "v-01", name: "Customer_Churn_Classifier", version: 1, stage: "PRODUCTION", framework: "XGBoost", accuracy: "0.945", f1: "0.925", created: "2026-08-31" },
    { id: "v-02", name: "Customer_Churn_Classifier", version: 2, stage: "STAGING", framework: "LightGBM", accuracy: "0.952", f1: "0.938", created: "2026-08-31" },
    { id: "v-03", name: "Credit_Default_Predictor", version: 1, stage: "PRODUCTION", framework: "RandomForest", accuracy: "0.912", f1: "0.895", created: "2026-08-30" },
  ];

  const handleStagePromotion = async (versionId: string, targetStage: string) => {
    try {
      await api.updateModelStage(versionId, targetStage);
      alert(`Model version promoted to ${targetStage}`);
    } catch (err) {
      alert(`Model version promoted to ${targetStage} (Simulated)`);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-2xl font-bold text-white tracking-tight">Model Registry & Lifecycle Governance</h2>
        <p className="text-xs text-gray-400 mt-1">Manage model versions, approval staging (Draft → Staging → Production → Archived) and artifact signatures</p>
      </div>

      {/* Model Registry Table */}
      <div className="bg-dark-card border border-dark-border rounded-xl p-5 space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-base font-semibold text-white flex items-center space-x-2">
            <Layers className="w-4 h-4 text-emerald-400" />
            <span>Registered Model Versions</span>
          </h3>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-900 text-gray-400 uppercase font-semibold border-b border-dark-border">
              <tr>
                <th className="py-3 px-4">Model Name</th>
                <th className="py-3 px-4">Version</th>
                <th className="py-3 px-4">Framework</th>
                <th className="py-3 px-4">Accuracy / F1</th>
                <th className="py-3 px-4">Current Stage</th>
                <th className="py-3 px-4">Promote Stage</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-dark-border text-gray-300">
              {mockModels.map((m) => (
                <tr key={m.id} className="hover:bg-slate-800/40 transition-colors">
                  <td className="py-3 px-4 font-medium text-white">{m.name}</td>
                  <td className="py-3 px-4 font-mono text-sky-400">v{m.version}</td>
                  <td className="py-3 px-4 text-gray-300">{m.framework}</td>
                  <td className="py-3 px-4 font-semibold text-emerald-400">{m.accuracy} / {m.f1}</td>
                  <td className="py-3 px-4">
                    <span
                      className={`px-2.5 py-0.5 rounded text-[10px] font-bold ${
                        m.stage === "PRODUCTION"
                          ? "bg-emerald-950 text-emerald-400 border border-emerald-700"
                          : m.stage === "STAGING"
                          ? "bg-amber-950 text-amber-400 border border-amber-700"
                          : "bg-slate-800 text-gray-400"
                      }`}
                    >
                      {m.stage}
                    </span>
                  </td>
                  <td className="py-3 px-4">
                    <div className="flex items-center space-x-2">
                      <button
                        onClick={() => handleStagePromotion(m.id, "PRODUCTION")}
                        className="px-2.5 py-1 bg-emerald-600 hover:bg-emerald-500 text-white rounded text-[10px] font-semibold transition-colors"
                      >
                        Promote to Prod
                      </button>
                      <button
                        onClick={() => handleStagePromotion(m.id, "ARCHIVED")}
                        className="px-2 py-1 bg-slate-800 hover:bg-slate-700 text-gray-300 rounded text-[10px] font-semibold transition-colors"
                      >
                        Archive
                      </button>
                    </div>
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
