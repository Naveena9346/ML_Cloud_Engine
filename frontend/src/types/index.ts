export type UserRole = 
  | "SUPER_ADMIN"
  | "ADMIN"
  | "ML_ENGINEER"
  | "DATA_SCIENTIST"
  | "DATA_ENGINEER"
  | "DEVELOPER"
  | "VIEWER";

export interface User {
  id: string;
  email: string;
  full_name: string;
  role: UserRole;
  job_title?: string;
  organization?: string;
  avatar_url?: string;
  is_active: boolean;
  is_superuser: boolean;
  created_at: string;
}

export interface Workspace {
  id: string;
  name: string;
  slug: string;
  description?: string;
  owner_id: string;
  created_at: string;
}

export interface Project {
  id: string;
  workspace_id: string;
  name: string;
  slug: string;
  description?: string;
  status: "ACTIVE" | "ARCHIVED" | "DELETED";
  created_at: string;
}

export interface DatasetVersion {
  id: string;
  dataset_id: string;
  version_number: number;
  file_path: string;
  file_size_bytes: number;
  row_count: number;
  column_count: number;
  sha256_checksum?: string;
  schema_json?: Record<string, string>;
  eda_summary?: any;
  cleaned_status: "RAW" | "PROCESSING" | "CLEANED";
  created_at: string;
}

export interface Dataset {
  id: string;
  project_id: string;
  name: string;
  description?: string;
  data_type: string;
  file_format: string;
  current_version: number;
  created_at: string;
  latest_version?: DatasetVersion;
}

export interface ExperimentRun {
  id: string;
  training_job_id: string;
  run_name: string;
  run_number: number;
  status: string;
  parameters?: Record<string, any>;
  metrics?: Record<string, number | any>;
  artifacts?: Record<string, string>;
  duration_seconds?: number;
  created_at: string;
}

export interface TrainingJob {
  id: string;
  project_id: string;
  dataset_version_id: string;
  name: string;
  algorithm: string;
  target_column: string;
  model_type: string;
  status: "PENDING" | "RUNNING" | "COMPLETED" | "FAILED" | "CANCELLED";
  hyperparameters?: Record<string, any>;
  execution_time_seconds?: number;
  error_message?: string;
  created_at: string;
  experiments?: ExperimentRun[];
}

export interface ModelVersion {
  id: string;
  model_registry_id: string;
  experiment_run_id?: string;
  version_number: number;
  stage: "DRAFT" | "STAGING" | "PRODUCTION" | "ARCHIVED";
  artifact_path: string;
  signature_schema: Record<string, string>;
  metrics?: Record<string, any>;
  tags?: Record<string, string>;
  created_at: string;
}

export interface ModelRegistry {
  id: string;
  project_id: string;
  name: string;
  description?: string;
  model_type: string;
  framework: string;
  created_at: string;
  versions?: ModelVersion[];
}

export interface ModelDeployment {
  id: string;
  project_id: string;
  model_version_id: string;
  endpoint_name: string;
  deployment_type: "REAL_TIME" | "BATCH";
  status: "ACTIVE" | "INACTIVE" | "FAILED";
  replicas: number;
  total_requests: number;
  avg_latency_ms: number;
  created_at: string;
  model_version?: ModelVersion;
}

export interface PredictionResponse {
  prediction: any;
  probabilities?: Record<string, number>;
  latency_ms: number;
  model_version: number;
  endpoint_name: string;
}

export interface DriftReport {
  id: string;
  deployment_id: string;
  drift_score: number;
  drift_detected: "TRUE" | "FALSE";
  feature_drift_details?: Record<string, any>;
  samples_analyzed: number;
  created_at: string;
}

export interface AuditLog {
  id: string;
  user_id?: string;
  action: string;
  resource_type: string;
  resource_id?: string;
  ip_address?: string;
  details?: Record<string, any>;
  timestamp: string;
}

export interface DashboardSummary {
  total_projects: number;
  total_datasets: number;
  active_training_jobs: number;
  completed_training_jobs: number;
  failed_training_jobs: number;
  registered_models: number;
  deployed_models: number;
  total_api_requests: number;
  avg_model_accuracy: number;
  system_cpu_usage_pct: number;
  system_memory_usage_pct: number;
}
