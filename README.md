# MLCloudEngine — Enterprise Machine Learning Cloud Platform

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/Next.js-14.2-black)](https://nextjs.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16.0-blue)](https://www.postgresql.org/)

**MLCloudEngine** is a production-grade, enterprise-ready Machine Learning and Cloud Platform engineered to streamline the end-to-end machine learning lifecycle—from data ingestion, EDA, data cleaning, and feature engineering to automated model training, hyperparameter optimization, experiment tracking, model registry, real-time/batch prediction serving, and continuous model drift monitoring.

---

## 🌟 Key Features & Platform Capabilities

### 1. User & Access Governance
- **Role-Based Access Control (RBAC):** 7 granular user roles (`Super Admin`, `Admin`, `ML Engineer`, `Data Scientist`, `Data Engineer`, `Developer`, `Viewer`).
- **Multi-Tenancy Workspaces:** Isolated workspace environments with user invitations, project scoping, and audit logs.
- **Enterprise Security:** JWT bearer authentication, password hashing with Argon2/Bcrypt, session invalidation, and rate limiting.

### 2. Dataset Management & Data Engineering
- **Multi-Format Ingestion:** Support for CSV, TSV, JSON, JSONL, Parquet, and Arrow datasets.
- **Dataset Versioning:** Immutable dataset snapshots with SHA-256 integrity verification and S3/MinIO artifact storage.
- **Data Cleaning & Imputation:** Automated null value imputation, IQR/Z-score outlier detection, categorical encoding (One-Hot, Ordinal, Target), and feature scaling (Standard, MinMax, Robust).
- **Automated Exploratory Data Analysis (EDA):** Statistical profiling, distribution analytics, Pearson/Spearman correlation heatmaps, missing value maps, and skewness metrics.
- **Feature Store:** Centralized feature registry, feature set definition, point-in-time feature retrieval, and lineage mapping.

### 3. Model Training & Hyperparameter Tuning
- **Multi-Framework ML Support:** Built-in trainers for Scikit-learn, XGBoost, LightGBM, CatBoost, and PyTorch models.
- **Automated Hyperparameter Optimization:** Optuna-powered Bayesian optimization, Grid Search, and Random Search with parallel worker trial execution.
- **Evaluation Engine:** Classification (Accuracy, Precision, Recall, F1, ROC-AUC, PR-AUC, Confusion Matrices, Log-Loss) and Regression metrics (MSE, RMSE, MAE, R², MAPE, Residual plots).
- **Experiment Tracking:** Real-time logging of epoch loss curves, hyperparameter configurations, artifact tracking, and experiment side-by-side comparison matrices.

### 4. Model Registry & Deployment Strategy
- **Governance & Versioning:** State-machine lifecycle governance (`Draft` → `Staging` → `Production` → `Archived`) with rollback capabilities and signature validation.
- **Real-Time Prediction APIs:** Async REST endpoints with sub-50ms inference latency, dynamic container initialization, and request validation.
- **Batch Scoring Engine:** Asynchronous offline scoring pipelines for high-throughput batch predictions with results stored directly to S3/PostgreSQL.

### 5. Model Monitoring, Drift & Observability
- **Data & Concept Drift Detection:** Population Stability Index (PSI), Kolmogorov-Smirnov (KS) tests, and Wasserstein distance monitoring.
- **Performance Telemetry:** Prometheus metrics exporter tracking p95/p99 latency, request volume, error rates, and GPU/CPU utilization.
- **Automated Alerts & Audit Trails:** Real-time alert notifications for accuracy degradation, data drift, and hardware resource constraints; comprehensive immutable audit logs for compliance.

---

## 🏗️ High-Level Architecture Diagram

```
+-----------------------------------------------------------------------------------+
|                                  MLCloudEngine UI                                 |
|              (Next.js 14, React 18, TypeScript, Tailwind CSS, ECharts)            |
+-----------------------------------------+-----------------------------------------+
                                          |
                                          | HTTP / WebSockets / REST API
                                          v
+-----------------------------------------------------------------------------------+
|                               FastAPI API Gateway                                 |
|         (JWT Auth, RBAC Middleware, OpenAPI Documentation, Rate Limiter)          |
+-------------------+---------------------+--------------------+--------------------+
                    |                     |                    |
                    v                     v                    v
+-----------------------+ +-----------------------+ +-------------------------------+
|  PostgreSQL 16 RDBMS  | |   Redis Cache & Broker| | MinIO / S3 Object Storage     |
| (Users, Workspaces,   | | (Task Queues, Pub/Sub,| | (Datasets, Feature Sets,      |
| Metadata, Audits)     | |  Active Session DB) | |  Model Artifacts, Checkpoints)|
+-----------------------+ +-----------+-----------+ +---------------+---------------+
                                      |                             ^
                                      v                             | Read / Write
+-------------------------------------------------------------------+---------------+
|                            Celery Worker Processing Cluster                       |
|   (Data Cleaning, EDA Engine, Optuna Tuning, PyTorch Trainer, Drift Detector)    |
+-------------------------------------+---------------------------------------------+
                                      |
                                      v Dynamic Model Pull
+-----------------------------------------------------------------------------------+
|                        Prediction & Model Serving Engine                          |
|             (Real-Time REST Endpoints, Asynchronous Batch Scoring Workers)        |
+-----------------------------------------------------------------------------------+
```

---

## 🛠️ Technology Stack

| Layer | Technologies |
| :--- | :--- |
| **Frontend Framework** | Next.js 14, React 18, TypeScript, Tailwind CSS, Lucide Icons |
| **Data Visualization** | Apache ECharts, Recharts, Chart.js, D3-cloud |
| **Backend API Engine** | Python 3.11+, FastAPI, Pydantic v2, Async SQLAlchemy 2.0, Alembic |
| **Task Queue & Broker**| Celery, Redis Streams, RabbitMQ |
| **Machine Learning** | PyTorch, Scikit-learn, XGBoost, LightGBM, CatBoost, Optuna, Pandas, Polars, NumPy, SciPy |
| **Model Drift & Monitoring** | Evidently AI integration, Custom PSI & KS-Test Engines, Prometheus Client |
| **Databases & Storage**| PostgreSQL 16, Redis 7, MinIO / Amazon S3 SDK |
| **DevOps & Testing** | Docker, Docker Compose, Kubernetes, Helm, Pytest, Playwright, GitHub Actions |

---

## 📁 Repository Structure

```
MLCloudEngine/
├── backend/                  # FastAPI Application Core & Services
│   ├── app/                  # Application Modules (API, DB, ML Engine, Services, Workers)
│   └── requirements.txt      # Python Dependencies
├── frontend/                 # Next.js 14 Web Application
├── ml_pipelines/             # Standalone Reusable ML Pipeline Modules
├── tests/                    # Comprehensive Automated Test Suites
├── docs/                     # Platform Architecture & API Specs
├── infra/                    # Docker, Kubernetes & CI/CD Manifests
└── README.md                 # Project Overview & Setup Guide
```

---

## 🚀 Quick Setup & Local Development Guide

### Prerequisites
- Python 3.11+
- Node.js 18+ & npm / yarn / pnpm
- Docker & Docker Compose
- PostgreSQL 16 & Redis 7 (or run via Docker Compose)

### 1. Environment Setup
Clone the repository and prepare environment configuration files:
```bash
git clone https://github.com/Naveena9346/ML_Cloud_Engine.git
cd ML_Cloud_Engine
cp .env.example .env
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload --port 8000
```

### 3. Worker Setup (Async ML Tasks)
```bash
cd backend
celery -A app.workers.celery_app worker --loglevel=info
```

### 4. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

Visit `http://localhost:3000` to access the MLCloudEngine Platform UI, and `http://localhost:8000/docs` for the interactive OpenAPI documentation.

---

## 🧪 Testing Suite Execution

Run automated unit, integration, and ML pipeline tests:
```bash
cd backend
pytest ../tests -v --cov=app --cov-report=term-missing
```

---

## 📄 License & Contact

This project is open-source under the [MIT License](LICENSE).  
Maintained by **Naveena9346** and the MLCloudEngine Core Engineering Team.
