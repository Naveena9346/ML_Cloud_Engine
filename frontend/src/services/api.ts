import axios from "axios";
import {
  AuditLog,
  DashboardSummary,
  Dataset,
  DatasetVersion,
  DriftReport,
  ModelDeployment,
  ModelRegistry,
  ModelVersion,
  PredictionResponse,
  Project,
  TrainingJob,
  User,
  Workspace,
} from "../types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Interceptor to attach Bearer JWT Token if logged in
apiClient.interceptors.request.use((config) => {
  if (typeof window !== "undefined") {
    const token = localStorage.getItem("mlengine_token");
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }
  }
  return config;
});

export const api = {
  // Auth & User Profile
  async login(formData: FormData) {
    const res = await apiClient.post("/auth/login", formData, {
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
    });
    return res.data;
  },

  async register(data: any) {
    const res = await apiClient.post("/auth/register", data);
    return res.data;
  },

  async getProfile(): Promise<User> {
    const res = await apiClient.get("/auth/me");
    return res.data;
  },

  // Dashboard Overview
  async getDashboardSummary(): Promise<DashboardSummary> {
    const res = await apiClient.get("/dashboard/summary");
    return res.data;
  },

  // Workspaces & Projects
  async listWorkspaces(): Promise<Workspace[]> {
    const res = await apiClient.get("/workspaces/");
    return res.data;
  },

  async createWorkspace(data: { name: string; description?: string }): Promise<Workspace> {
    const res = await apiClient.post("/workspaces/", data);
    return res.data;
  },

  async listProjects(workspaceId: string): Promise<Project[]> {
    const res = await apiClient.get(`/projects/?workspace_id=${workspaceId}`);
    return res.data;
  },

  async createProject(data: { workspace_id: string; name: string; description?: string }): Promise<Project> {
    const res = await apiClient.post("/projects/", data);
    return res.data;
  },

  // Datasets & Preprocessing
  async listDatasets(projectId: string): Promise<Dataset[]> {
    const res = await apiClient.get(`/datasets/?project_id=${projectId}`);
    return res.data;
  },

  async uploadDataset(formData: FormData): Promise<Dataset> {
    const res = await apiClient.post("/datasets/upload", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
    return res.data;
  },

  async previewDataset(datasetId: string, limit: number = 50) {
    const res = await apiClient.get(`/datasets/${datasetId}/preview?limit=${limit}`);
    return res.data;
  },

  async cleanDataset(datasetId: string, options: any): Promise<DatasetVersion> {
    const res = await apiClient.post(`/preprocessing/clean/${datasetId}`, options);
    return res.data;
  },

  async runEDA(datasetVersionId: string) {
    const res = await apiClient.get(`/eda/${datasetVersionId}`);
    return res.data;
  },

  // Training & Experiments
  async createTrainingJob(data: any): Promise<TrainingJob> {
    const res = await apiClient.post("/training/jobs", data);
    return res.data;
  },

  async listTrainingJobs(projectId: string): Promise<TrainingJob[]> {
    const res = await apiClient.get(`/training/jobs?project_id=${projectId}`);
    return res.data;
  },

  // Model Registry & Lifecycle
  async registerModel(data: any): Promise<ModelVersion> {
    const res = await apiClient.post("/models/register", data);
    return res.data;
  },

  async listModelRegistries(projectId: string): Promise<ModelRegistry[]> {
    const res = await apiClient.get(`/models/registry?project_id=${projectId}`);
    return res.data;
  },

  async updateModelStage(versionId: string, targetStage: string): Promise<ModelVersion> {
    const res = await apiClient.put(`/models/versions/${versionId}/stage`, { target_stage: targetStage });
    return res.data;
  },

  // Deployments & Predictions
  async createDeployment(data: any): Promise<ModelDeployment> {
    const res = await apiClient.post("/deployments/", data);
    return res.data;
  },

  async listDeployments(projectId: string): Promise<ModelDeployment[]> {
    const res = await apiClient.get(`/deployments/?project_id=${projectId}`);
    return res.data;
  },

  async invokePrediction(endpointName: string, features: Record<string, any>): Promise<PredictionResponse> {
    const res = await apiClient.post(`/predictions/realtime/${endpointName}`, { features });
    return res.data;
  },

  // Monitoring & Audit Logs
  async calculateDrift(deploymentId: string): Promise<DriftReport> {
    const res = await apiClient.post(`/monitoring/drift/${deploymentId}`);
    return res.data;
  },

  async listDriftReports(deploymentId: string): Promise<DriftReport[]> {
    const res = await apiClient.get(`/monitoring/reports/${deploymentId}`);
    return res.data;
  },

  async listAuditLogs(): Promise<AuditLog[]> {
    const res = await apiClient.get("/audit/");
    return res.data;
  },
};
