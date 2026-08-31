# MLCloudEngine — Machine Learning Pipeline Documentation

The MLCloudEngine pipeline automates the end-to-end machine learning lifecycle from raw file upload to continuous drift monitoring.

---

## 🔄 ML Lifecycle Stages

```
 +---------------+     +---------------+     +---------------+     +---------------+
 | Data Ingest   | --> | Preprocess &  | --> | Model Train & | --> |  Evaluation & |
 | & Versioning  |     | EDA Profiling |     | Optuna Tuning |     | Metric Benchmark
 +---------------+     +---------------+     +---------------+     +---------------+
                                                                           |
                                                                           v
 +---------------+     +---------------+     +---------------+     +---------------+
 | Retraining    | <-- | Drift & Tele- | <-- | Real-time REST| <-- | Model Registry|
 | Trigger       |     | metry Monitor |     | API Serving   |     | Staging (Prod)|
 +---------------+     +---------------+     +---------------+     +---------------+
```

### Stage 1: Data Ingestion & Immutability
- Uploads CSV, Parquet, TSV, or JSON datasets with chunked processing.
- Computes SHA-256 hash digest for immutable dataset version snapshots.
- Stores metadata in PostgreSQL and raw files in MinIO/S3 object storage.

### Stage 2: Automated Cleaning & EDA Engine
- **Null Value Handling:** Impute mean, median, mode, or drop rows.
- **Outliers:** IQR factor clipping ($1.5 \times \text{IQR}$) or Z-score bounds ($3.0 \times \sigma$).
- **Encoding:** One-Hot Encoding or Ordinal Encoding.
- **Scaling:** StandardScaler, MinMaxScaler, or RobustScaler.
- **EDA Profiling:** Distribution stats, null percentage heatmaps, Pearson/Spearman correlations.

### Stage 3: Training & Optuna Tuning
- **Algorithms:** Scikit-learn (Random Forest, Gradient Boosting, Logistic Regression), XGBoost, LightGBM, PyTorch Neural Networks.
- **Hyperparameter Optimization:** Optuna Bayesian search with parallel 3-fold cross-validation scoring.

### Stage 4: Governance & Model Serving
- **Staging Transitions:** `Draft` → `Staging` → `Production` → `Archived`.
- **Real-Time Prediction APIs:** Async REST endpoints with sub-30ms inference latency and JSON input signature validation.

### Stage 5: Telemetry & Drift Monitoring
- **Population Stability Index (PSI):**
  $$\text{PSI} = \sum \left( \% \text{Actual} - \% \text{Expected} \right) \times \ln\left( \frac{\% \text{Actual}}{\% \text{Expected}} \right)$$
  - $\text{PSI} < 0.1$: No Drift / Stable Population.
  - $0.1 \le \text{PSI} < 0.2$: Moderate Drift Warning.
  - $\text{PSI} \ge 0.2$: Significant Drift Alert.
- **Kolmogorov-Smirnov (KS) Test:** Two-sample non-parametric goodness-of-fit test ($p < 0.05$ indicates distribution shift).
