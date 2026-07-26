"""Stage 5 — Training report.

Aggregates every upstream stage's output into a single JSON report
at `reports/training_report.json`. Reads:
  - `reports/validation_status.json` produced by the validate stage.
  - `reports/selection.json` produced by the select stage.
  - the MLflow experiment's run count for the total trials figure.
"""
import json
import os

import mlflow

TRACKING_URI = "http://localhost:5000"
EXPERIMENT = "fraud-detection-tuning"
REPORTS_DIR = "/root/code/fraud-detection/reports"

VALIDATION_JSON = os.path.join(REPORTS_DIR, "validation_status.json")
SELECTION_JSON = os.path.join(REPORTS_DIR, "selection.json")
TRAINING_REPORT_JSON = os.path.join(REPORTS_DIR, "training_report.json")


def main():
    with open(VALIDATION_JSON) as f:
        validation = json.load(f)
    with open(SELECTION_JSON) as f:
        selection = json.load(f)

    mlflow.set_tracking_uri(TRACKING_URI)
    client = mlflow.MlflowClient()
    exp = client.get_experiment_by_name(EXPERIMENT)
    runs = mlflow.search_runs([exp.experiment_id], max_results=500) if exp else []
    total_trials = int(len(runs)) if hasattr(runs, "__len__") else 0

    run_id = selection["run_id"]
    client = mlflow.MlflowClient()
    run = client.get_run(run_id)
    best_params = {k: v for k, v in run.data.params.items()}
    best_metrics = {k: float(v) for k, v in run.data.metrics.items()}

    # TODO: assemble the consolidated training report from the upstream
    # artefacts gathered above. Build a dict with exactly these five keys
    # and bind it to `report`:
    #   "best_model"        -> selection's model_type (selection["model_type"])
    #   "best_params"       -> best_params
    #   "metrics"           -> best_metrics
    #   "total_trials"      -> total_trials
    #   "validation_status" -> validation's status (validation["status"])

    report = {
        "best_model": selection["model_type"],
        "best_params": best_params,
        "metrics": best_metrics,
        "total_trials": total_trials,
        "validation_status": validation["status"]
    }

    os.makedirs(REPORTS_DIR, exist_ok=True)
    with open(TRAINING_REPORT_JSON, "w") as f:
        json.dump(report, f, indent=2)
    print(f"[report] {TRAINING_REPORT_JSON}")


if __name__ == "__main__":
    main()
