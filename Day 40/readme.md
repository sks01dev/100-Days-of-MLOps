# Integrated End-to-End MLOps Pipeline Automation (Day 40)

An automated, declarative MLOps training orchestrator designed for **xFusionCorp Industries**. This project unifies fragmented ML lifecycle operations—data validation, hyperparameter optimization, metrics-driven model selection, model registry synchronization, and audit logging—behind a single, reliable build interface.

## 🎯 Core Intuition & Architecture

Executing ML lifecycle tasks as disconnected commands creates critical vulnerabilities. If a data validation step fails silently or code modifications drift from metrics tracking schemas, corrupted configurations or broken references can cascade into downstream production environments.

This pipeline eliminates manual handoffs by using a declarative `Makefile` to establish strict, sequential execution gates. The system guarantees that every registered model running under the `@staging` release lane has cleared every validation, tuning, and evaluation threshold, generating a verifiable audit trail (`training_report.json`) on every run.

```text
       ┌────────────────────────┐
       │   make train-pipeline  │
       └───────────┬────────────┘
                   │
                   ▼
     Stage 1: [validate_data.py]  ──► (Schema Validation & Integrity Check)
                   │
                   ▼
     Stage 2: [tune.py]           ──► (Hyperparameter Tuning via Optuna)
                   │
                   ▼
     Stage 3: [select_model.py]   ──► (Metric Realignment: f1_score Analysis)
                   │
                   ▼
     Stage 4: [register.py]       ──► (MLflow Model Registry @staging Promotion)
                   │
                   ▼
     Stage 5: [report.py]         ──► (Consolidated Audit Artifact Generation)
```

---

## 🛠️ Resolved Pipeline Vulnerabilities

1. **Metric Realignment (`src/select_model.py`)**: Corrected an upstream metric structural collision where downstream processing looked for an invalid `"metrics.accuracy"` string. Realigned lookup logic to extract `"metrics.f1_score"` emitted by the tuning stage.
2. **Release-Lane Target Synchronization (`src/register.py`)**: Automated model promotion workflows by explicitly mapping the active model tracking instance version directly to the `@staging` environment alias tag.
3. **Audit Schema Enforcement (`src/report.py`)**: Assembled a rigorous 5-key structured JSON output schema ensuring consistent down-stream operational auditing metrics.

---

## 🚀 Execution & Verification

### 1. Run the Complete Automation Pipeline
To clean past runs and trigger the automated workspace processing end-to-end, execute:
```bash
make clean && make train-pipeline
```

### 2. Expected Standard Output Log Trace
```text
[Pipeline] Stage 1/5: Executing Data Validation...
[validate] {'status': 'ok', 'rows': 200, 'columns': ['amount', 'hour', 'num_tx_past_day', 'is_fraud']}
[Pipeline] Stage 2/5: Commencing Hyperparameter Tuning...
[tune] 10 trials complete. best_value=0.4653 best_params={'max_depth': 5, 'model_type': 'RandomForest', 'n_estimators': 94}
[Pipeline] Stage 3/5: Running Top Model Selection Evaluation...
[select] {'run_id': 'f83a12...', 'model_type': 'RandomForest', 'f1_score': 0.4653417818740399}
[Pipeline] Stage 4/5: Registering Model to Central Registry...
[register] fraud-detector v1 registered and tagged as @staging
[Pipeline] Stage 5/5: Compiling Consolidated Audit Artifact...
[report] /root/code/fraud-detection/reports/training_report.json
[Pipeline] End-to-End Run Successfully Completed.
```

### 3. Consolidated Audit Artifact Output (`reports/training_report.json`)
```json
{
  "best_model": "RandomForest",
  "best_params": {
    "max_depth": "5",
    "n_estimators": "94"
  },
  "metrics": {
    "f1_score": 0.4653417818740399
  },
  "total_trials": 10,
  "validation_status": "ok"
}
```

---

## Main Idea
> **Automation pipelines rely on unified data interfaces.** When chaining pipeline stages via a orchestrator like `make`, verify that downstream consumer scripts process the exact data schemas emitted by upstream producers. Decouple pipeline configurations from explicit target strings by routing environmental updates through explicit tracking identifiers like `@staging`.
