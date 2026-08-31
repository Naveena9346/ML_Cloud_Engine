# MLCloudEngine — API Reference Documentation

All API endpoints are prefixed with `/api/v1` and generate interactive documentation at `/docs` (Swagger UI) and `/redoc` (ReDoc).

---

## 🔐 Authentication & Profile Routes (`/api/v1/auth`)

| Method | Endpoint | Description | Request Payload | Response |
| :--- | :--- | :--- | :--- | :--- |
| `POST` | `/auth/register` | Register new platform user | `UserCreate` | `UserResponse` |
| `POST` | `/auth/login` | OAuth2 password login & token issuance | `OAuth2PasswordRequestForm` | `Token` |
| `GET` | `/auth/me` | Get profile of logged-in user | Header: `Bearer <token>` | `UserResponse` |

---

## 📁 Datasets & Preprocessing Routes (`/api/v1/datasets`, `/api/v1/preprocessing`, `/api/v1/eda`)

| Method | Endpoint | Description | Request Payload | Response |
| :--- | :--- | :--- | :--- | :--- |
| `POST` | `/datasets/upload` | Ingest dataset file snapshot | Multipart Form (`file`, `name`) | `DatasetResponse` |
| `GET` | `/datasets/` | List datasets for project | `?project_id=<id>` | `List[DatasetResponse]` |
| `GET` | `/datasets/{id}/preview` | Preview N dataset rows | `?limit=50` | `DatasetPreview` |
| `POST` | `/preprocessing/clean/{id}` | Execute data cleaner pipeline | `DataCleaningOptions` | `DatasetVersionResponse` |
| `GET` | `/eda/{version_id}` | Generate statistical EDA profile | None | `EDAProfileSummary` |

---

## 🤖 Model Training & Governance Routes (`/api/v1/training`, `/api/v1/models`)

| Method | Endpoint | Description | Request Payload | Response |
| :--- | :--- | :--- | :--- | :--- |
| `POST` | `/training/jobs` | Launch training & Optuna tuning job | `TrainingJobCreate` | `TrainingJobResponse` |
| `GET` | `/training/jobs` | List training jobs for project | `?project_id=<id>` | `List[TrainingJobResponse]` |
| `POST` | `/models/register` | Register model version snapshot | `ModelRegisterRequest` | `ModelVersionResponse` |
| `GET` | `/models/registry` | List model registries and versions | `?project_id=<id>` | `List[ModelRegistryResponse]` |
| `PUT` | `/models/versions/{id}/stage`| Promote model stage (`STAGING` $\rightarrow$ `PRODUCTION`) | `ModelStageUpdateRequest` | `ModelVersionResponse` |

---

## ⚡ Deployment, Prediction & Monitoring Routes (`/api/v1/deployments`, `/api/v1/predictions`, `/api/v1/monitoring`)

| Method | Endpoint | Description | Request Payload | Response |
| :--- | :--- | :--- | :--- | :--- |
| `POST` | `/deployments/` | Deploy model version endpoint | `ModelDeploymentCreate` | `ModelDeploymentResponse` |
| `GET` | `/deployments/` | List active endpoints | `?project_id=<id>` | `List[ModelDeploymentResponse]` |
| `POST` | `/predictions/realtime/{endpoint_name}` | Invoke real-time REST inference API | `RealTimePredictionRequest` | `PredictionResponse` |
| `POST` | `/monitoring/drift/{deployment_id}` | Calculate PSI & KS drift metrics | None | `DriftReportResponse` |
| `GET` | `/audit/` | Retrieve system compliance audit logs | `?limit=100` | `List[AuditLogResponse]` |
