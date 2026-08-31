"use client";

import React, { useState } from "react";
import { Sidebar } from "../components/layout/Sidebar";
import { Navbar } from "../components/layout/Navbar";
import { DashboardView } from "../components/views/DashboardView";
import { WorkspacesView } from "../components/views/WorkspacesView";
import { DatasetsView } from "../components/views/DatasetsView";
import { TrainingView } from "../components/views/TrainingView";
import { ModelRegistryView } from "../components/views/ModelRegistryView";
import { DeploymentsView } from "../components/views/DeploymentsView";
import { MonitoringView } from "../components/views/MonitoringView";
import { AuditView } from "../components/views/AuditView";

export default function Home() {
  const [currentTab, setCurrentTab] = useState("dashboard");

  const renderActiveView = () => {
    switch (currentTab) {
      case "dashboard":
        return <DashboardView />;
      case "workspaces":
        return <WorkspacesView />;
      case "datasets":
        return <DatasetsView />;
      case "training":
        return <TrainingView />;
      case "models":
        return <ModelRegistryView />;
      case "deployments":
        return <DeploymentsView />;
      case "monitoring":
        return <MonitoringView />;
      case "audit":
        return <AuditView />;
      default:
        return <DashboardView />;
    }
  };

  return (
    <div className="flex min-h-screen bg-dark-bg">
      {/* Platform Navigation Sidebar */}
      <Sidebar currentTab={currentTab} setCurrentTab={setCurrentTab} userRole="ML_ENGINEER" />

      {/* Main Content Workspace */}
      <div className="flex-1 flex flex-col min-w-0">
        <Navbar workspaceName="Production-Workspace" projectName="Customer-Churn-ML" userName="Lead ML Engineer" />

        <main className="flex-1 p-6 overflow-y-auto">
          {renderActiveView()}
        </main>
      </div>
    </div>
  );
}
