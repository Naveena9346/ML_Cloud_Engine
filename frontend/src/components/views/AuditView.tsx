"use client";

import React from "react";
import { FileText, Shield, Search } from "lucide-react";

export const AuditView: React.FC = () => {
  const mockAuditLogs = [
    { id: "log-101", user: "lead.mle@company.com", action: "MODEL_STAGE_PROMOTED", resource: "Customer_Churn_Classifier v1 -> PRODUCTION", ip: "192.168.1.45", time: "2026-08-31 20:15:22" },
    { id: "log-102", user: "data.sci@company.com", action: "TRAINING_JOB_LAUNCHED", resource: "Churn_XGBoost_BayesianOpt", ip: "192.168.1.88", time: "2026-08-31 19:40:10" },
    { id: "log-103", user: "data.eng@company.com", action: "DATASET_CLEANED", resource: "Customer_Churn_Features_v1.csv", ip: "192.168.1.12", time: "2026-08-31 18:22:05" },
    { id: "log-104", user: "admin@company.com", action: "USER_ROLE_ASSIGNED", resource: "Granted ML_ENGINEER role to user dev@company.com", ip: "192.168.1.01", time: "2026-08-31 16:10:00" },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-2xl font-bold text-white tracking-tight">Compliance & Audit Trails</h2>
        <p className="text-xs text-gray-400 mt-1">Immutable security log history tracking user actions, permissions & model governance events</p>
      </div>

      {/* Audit Log Table */}
      <div className="bg-dark-card border border-dark-border rounded-xl p-5 space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-base font-semibold text-white flex items-center space-x-2">
            <FileText className="w-4 h-4 text-sky-400" />
            <span>Audit Action Log History</span>
          </h3>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-900 text-gray-400 uppercase font-semibold border-b border-dark-border">
              <tr>
                <th className="py-3 px-4">Timestamp</th>
                <th className="py-3 px-4">User</th>
                <th className="py-3 px-4">Action</th>
                <th className="py-3 px-4">Resource Target</th>
                <th className="py-3 px-4">IP Address</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-dark-border text-gray-300">
              {mockAuditLogs.map((log) => (
                <tr key={log.id} className="hover:bg-slate-800/40 transition-colors">
                  <td className="py-3 px-4 font-mono text-gray-400">{log.time}</td>
                  <td className="py-3 px-4 font-medium text-white">{log.user}</td>
                  <td className="py-3 px-4">
                    <span className="px-2 py-0.5 rounded bg-slate-800 border border-slate-700 font-mono text-[10px] text-sky-400 font-semibold">
                      {log.action}
                    </span>
                  </td>
                  <td className="py-3 px-4 text-gray-300">{log.resource}</td>
                  <td className="py-3 px-4 font-mono text-gray-500">{log.ip}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
