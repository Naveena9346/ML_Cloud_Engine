"use client";

import React, { useState } from "react";
import { FolderGit2, Plus, Users, Shield, Layers } from "lucide-react";

export const WorkspacesView: React.FC = () => {
  const [workspaceName, setWorkspaceName] = useState("");
  const [projectName, setProjectName] = useState("");

  const mockProjects = [
    { id: "p-01", name: "Customer-Churn-ML", slug: "customer-churn-ml", datasets: 4, models: 3, status: "ACTIVE", created: "2026-08-30" },
    { id: "p-02", name: "Credit-Default-Risk", slug: "credit-default-risk", datasets: 2, models: 2, status: "ACTIVE", created: "2026-08-31" },
    { id: "p-03", name: "Fraud-Detection-Engine", slug: "fraud-detection-engine", datasets: 6, models: 3, status: "ACTIVE", created: "2026-08-31" },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-2xl font-bold text-white tracking-tight">Workspaces & Project Governance</h2>
        <p className="text-xs text-gray-400 mt-1">Multi-tenancy isolation, project scoping, and role-based team management</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Create Project Card */}
        <div className="bg-dark-card border border-dark-border rounded-xl p-5 space-y-4">
          <h3 className="text-base font-semibold text-white flex items-center space-x-2">
            <Plus className="w-4 h-4 text-sky-400" />
            <span>Create New ML Project</span>
          </h3>

          <form className="space-y-3">
            <div>
              <label className="text-xs font-medium text-gray-400 block mb-1">Project Name</label>
              <input
                type="text"
                value={projectName}
                onChange={(e) => setProjectName(e.target.value)}
                placeholder="e.g. Sales-Forecasting-Model"
                className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-xs text-gray-200 placeholder-gray-500 focus:outline-none focus:border-sky-500"
                required
              />
            </div>

            <div>
              <label className="text-xs font-medium text-gray-400 block mb-1">Description</label>
              <textarea
                rows={3}
                placeholder="Brief description of the ML project objectives..."
                className="w-full bg-slate-900 border border-slate-700 rounded-lg p-3 text-xs text-gray-200 placeholder-gray-500 focus:outline-none focus:border-sky-500"
              ></textarea>
            </div>

            <button
              type="submit"
              className="w-full bg-sky-600 hover:bg-sky-500 text-white font-semibold py-2 rounded-lg text-xs transition-colors flex items-center justify-center space-x-2 shadow-lg shadow-sky-600/20"
            >
              <span>Create Project</span>
            </button>
          </form>
        </div>

        {/* Projects List */}
        <div className="lg:col-span-2 bg-dark-card border border-dark-border rounded-xl p-5 space-y-4">
          <h3 className="text-base font-semibold text-white flex items-center space-x-2">
            <FolderGit2 className="w-4 h-4 text-emerald-400" />
            <span>Active Projects in Workspace</span>
          </h3>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {mockProjects.map((p) => (
              <div key={p.id} className="p-4 bg-slate-900/60 rounded-xl border border-slate-800 space-y-3 hover:border-slate-700 transition-colors">
                <div className="flex items-center justify-between">
                  <h4 className="font-semibold text-sm text-white">{p.name}</h4>
                  <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-950 text-emerald-400 border border-emerald-800/50">
                    {p.status}
                  </span>
                </div>
                <div className="flex items-center space-x-4 text-xs text-gray-400">
                  <span>Datasets: <strong className="text-gray-200">{p.datasets}</strong></span>
                  <span>Models: <strong className="text-gray-200">{p.models}</strong></span>
                </div>
                <div className="text-[10px] text-gray-500 pt-2 border-t border-slate-800">Created: {p.created}</div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
