"use client";

import React from "react";
import { Bell, ChevronDown, Search, User as UserIcon } from "lucide-react";

interface NavbarProps {
  workspaceName?: string;
  projectName?: string;
  userName?: string;
}

export const Navbar: React.FC<NavbarProps> = ({
  workspaceName = "Production-Workspace",
  projectName = "Customer-Churn-ML",
  userName = "Lead ML Engineer",
}) => {
  return (
    <header className="h-16 bg-dark-card border-b border-dark-border px-6 flex items-center justify-between">
      {/* Workspace & Project Scope Indicator */}
      <div className="flex items-center space-x-3">
        <div className="bg-slate-800 px-3 py-1.5 rounded-lg border border-slate-700/60 flex items-center space-x-2 text-xs">
          <span className="text-gray-400">Workspace:</span>
          <span className="font-semibold text-sky-400">{workspaceName}</span>
          <ChevronDown className="w-3.5 h-3.5 text-gray-400" />
        </div>
        <span className="text-gray-600">/</span>
        <div className="bg-slate-800 px-3 py-1.5 rounded-lg border border-slate-700/60 flex items-center space-x-2 text-xs">
          <span className="text-gray-400">Project:</span>
          <span className="font-semibold text-emerald-400">{projectName}</span>
          <ChevronDown className="w-3.5 h-3.5 text-gray-400" />
        </div>
      </div>

      {/* Global Search Bar */}
      <div className="relative w-72">
        <Search className="w-4 h-4 text-gray-400 absolute left-3 top-2.5" />
        <input
          type="text"
          placeholder="Search models, datasets, jobs..."
          className="w-full bg-slate-900 border border-slate-700 rounded-lg pl-9 pr-4 py-1.5 text-xs text-gray-200 placeholder-gray-500 focus:outline-none focus:border-sky-500 transition-colors"
        />
      </div>

      {/* Profile & Notifications */}
      <div className="flex items-center space-x-4">
        <button className="p-2 rounded-lg bg-slate-800 border border-slate-700/60 text-gray-400 hover:text-white transition-colors relative">
          <Bell className="w-4 h-4" />
          <span className="w-2 h-2 rounded-full bg-sky-500 absolute top-1.5 right-1.5"></span>
        </button>

        <div className="flex items-center space-x-3 pl-2 border-l border-slate-800">
          <div className="w-8 h-8 rounded-full bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center text-white font-bold text-xs shadow-md">
            ML
          </div>
          <div className="hidden md:block text-left">
            <div className="text-xs font-semibold text-gray-200">{userName}</div>
            <div className="text-[10px] text-gray-400">admin@mlcloudengine.com</div>
          </div>
        </div>
      </div>
    </header>
  );
};
