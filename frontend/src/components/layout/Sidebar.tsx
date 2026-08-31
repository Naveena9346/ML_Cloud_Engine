"use client";

import React from "react";
import {
  Activity,
  BarChart2,
  Cpu,
  Database,
  FileText,
  FolderGit2,
  Layers,
  LayoutDashboard,
  LogOut,
  ShieldCheck,
  Zap,
} from "lucide-react";

interface SidebarProps {
  currentTab: string;
  setCurrentTab: (tab: string) => void;
  userRole?: string;
}

export const Sidebar: React.FC<SidebarProps> = ({ currentTab, setCurrentTab, userRole = "ML_ENGINEER" }) => {
  const menuItems = [
    { id: "dashboard", label: "Executive Dashboard", icon: LayoutDashboard },
    { id: "workspaces", label: "Workspaces & Projects", icon: FolderGit2 },
    { id: "datasets", label: "Datasets & EDA Engine", icon: Database },
    { id: "training", label: "Training & Tuning", icon: Cpu },
    { id: "models", label: "Model Governance", icon: Layers },
    { id: "deployments", label: "Serving & Prediction APIs", icon: Zap },
    { id: "monitoring", label: "Drift & Telemetry", icon: Activity },
    { id: "audit", label: "Compliance & Audit Logs", icon: FileText },
  ];

  return (
    <aside className="w-64 bg-dark-card border-r border-dark-border min-h-screen flex flex-col justify-between p-4">
      <div>
        {/* Brand Header */}
        <div className="flex items-center space-x-3 px-2 py-4 mb-6 border-b border-dark-border">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-sky-500 to-indigo-600 flex items-center justify-center text-white shadow-lg shadow-sky-500/20">
            <Cpu className="w-6 h-6" />
          </div>
          <div>
            <h1 className="font-bold text-lg text-white tracking-wide leading-none">MLCloudEngine</h1>
            <span className="text-xs text-sky-400 font-medium">Enterprise ML Cloud</span>
          </div>
        </div>

        {/* User Role Badge */}
        <div className="mb-6 px-3 py-2 bg-slate-800/60 rounded-lg border border-slate-700/50 flex items-center space-x-2">
          <ShieldCheck className="w-4 h-4 text-emerald-400" />
          <div>
            <div className="text-[10px] text-gray-400 uppercase tracking-wider font-semibold">Active Access Role</div>
            <div className="text-xs font-semibold text-emerald-300">{userRole.replace("_", " ")}</div>
          </div>
        </div>

        {/* Navigation Menu */}
        <nav className="space-y-1">
          {menuItems.map((item) => {
            const Icon = item.icon;
            const isActive = currentTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setCurrentTab(item.id)}
                className={`w-full flex items-center space-x-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all duration-200 ${
                  isActive
                    ? "bg-sky-600 text-white shadow-md shadow-sky-600/30"
                    : "text-gray-400 hover:text-gray-200 hover:bg-slate-800/40"
                }`}
              >
                <Icon className={`w-5 h-5 ${isActive ? "text-white" : "text-gray-400"}`} />
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>
      </div>

      {/* Footer System Info */}
      <div className="pt-4 border-t border-dark-border text-xs text-gray-500 flex items-center justify-between">
        <span>Platform v1.0.0</span>
        <span className="flex items-center space-x-1 text-emerald-400">
          <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
          <span>Live</span>
        </span>
      </div>
    </aside>
  );
};
