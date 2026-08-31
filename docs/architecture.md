# MLCloudEngine — Architecture Documentation

## 1. System High-Level Architecture

MLCloudEngine follows a modular microservice and event-driven architecture designed for high scalability, fault tolerance, and secure multi-tenancy.

```
                                  +---------------------------------------+
                                  |            Next.js 14 UI              |
                                  | (React 18, Tailwind CSS, Recharts)   |
                                  +-------------------+-------------------+
                                                      |
                                                      | HTTP / REST API / WebSockets
                                                      v
                                  +---------------------------------------+
                                  |          FastAPI API Gateway          |
                                  |   (Auth, RBAC, Middleware, OpenAPI)   |
                                  +---------+-------------------+---------+
                                            |                   |
                     +----------------------+                   +-----------------------+
                     | DB Queries                                                       | Task Enqueue
                     v                                                                  v
+------------------------------------------+                      +------------------------------------------+
|          PostgreSQL 16 Database           |                      |              Redis Queue                 |
| (Users, Workspaces, Metadata, Audit Logs)|                      |     (Celery Task Broker & Caching)       |
+------------------------------------------+                      +--------------------+---------------------+
                                                                                       | Task Dispatch
                                                                                       v
                                                                  +------------------------------------------+
                                                                  |        Celery ML Worker Cluster          |
                                                                  |  (Data Cleaning, Training, Tuning, EDA)  |
                                                                  +--------------------+---------------------+
                                                                                       | S3 Write
                                                                                       v
                                                                  +------------------------------------------+
                                                                  |        MinIO / S3 Object Storage         |
                                                                  |     (Raw Data, Features, Model Files)    |
                                                                  +--------------------+---------------------+
                                                                                       | Model Load
                                                                                       v
                                                                  +------------------------------------------+
                                                                  |      Inference & Prediction Engine       |
                                                                  |  (Real-Time Endpoints, Batch Scoring)    |
                                                                  +------------------------------------------+
```

## 2. Core Service Boundaries
- **API Gateway (`backend/app/main.py`):** Serves as central request router, JWT bearer validator, rate limiter, and OpenAPI doc generator.
- **Data Engineering & Preprocessing (`ml_pipelines/preprocessing/`):** Handles multi-format data ingestion (CSV/Parquet/JSON), missing value imputation, outlier clipping (IQR/Z-Score), encoding, scaling, and EDA profiling.
- **Model Training & Tuning (`ml_pipelines/training/`):** Universal trainer supporting Scikit-Learn, XGBoost, LightGBM, and PyTorch models with Optuna Bayesian hyperparameter search.
- **Model Registry & Governance (`backend/app/api/v1/models.py`):** Enforces staging state machine (`Draft` → `Staging` → `Production` → `Archived`).
- **Real-Time Prediction Serving (`backend/app/api/v1/predictions.py`):** Low-latency REST endpoints for live inference with telemetry logging.
- **Model Telemetry & Drift Engine (`ml_pipelines/monitoring/`):** Population Stability Index (PSI) and Kolmogorov-Smirnov (KS) drift testing.

---

## 3. RBAC Security Matrix

| Role | Workspace | Datasets & EDA | Training & Tuning | Model Registry | Deployments | Audit Logs |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Super Admin** | Full Access | Full Access | Full Access | Full Access | Full Access | Full Access |
| **Admin** | Full Access | Full Access | Full Access | Full Access | Full Access | Read |
| **ML Engineer** | Read/Create | Full Access | Full Access | Full Access | Full Access | Read |
| **Data Scientist** | Read/Create | Full Access | Full Access | Register | View/Invoke | Read |
| **Data Engineer** | Read | Full Access | View | View | View/Invoke | Read |
| **Developer** | Read | Read | View | View | Deploy/Invoke | Read |
| **Viewer** | Read | Read | View | View | View | Read |
