# Day 38: Parallel Computational Execution and Hardware Scaling Optimization

### Problem Statement

The xFusionCorp Industries multi-core training pipeline script at `/root/code/fraud-detection/src/models/train_parallel.py` contains incorrect parameters: it hardcodes execution parameters to a single worker core grid (`[1, 1]`) and hardcodes telemetry values (`"all"`), resulting in an inability to track parallel speedup metrics. Reconfigure the script to unlock multi-core execution (`-1`), map the telemetry properties dynamically, and record the parallelization speedup metrics.

---

### The Code Fix

Open `/root/code/fraud-detection/src/models/train_parallel.py` and modify the worker core constraints, the dynamic logging statement, and the metric calculation block:

```python
# FIX 1: Set the list to execute first sequentially (1) and then across all cores (-1)
N_JOBS_VALUES = [1, -1]

def main():
    # ... (Data loading scaffolding blocks remain identical) ...

    last_model = None
    times = {} 
    for n_jobs in N_JOBS_VALUES:
        run_name = "serial" if n_jobs == 1 else "parallel"
        with mlflow.start_run(run_name=run_name):
            # FIX 2: Log the actual numeric parameter variable instead of a hardcoded string
            mlflow.log_param("n_jobs", n_jobs)
            mlflow.log_param("n_estimators", N_ESTIMATORS)

            model = RandomForestClassifier(
                n_estimators=N_ESTIMATORS,
                random_state=RANDOM_STATE,
                n_jobs=n_jobs,
            )
            start = time.perf_counter()
            model.fit(X, y)
            elapsed = time.perf_counter() - start

            mlflow.log_metric("training_time_seconds", elapsed)
            times[n_jobs] = elapsed
            # ... (Print scaffolding remains intact) ...
            last_model = model

    # FIX 3: Open the final summary run block to calculate and log the speedup factor
    with mlflow.start_run(run_name="speedup-summary"):
        mlflow.log_metric(key="speedup", value=(times[1] / times[-1]))

```

---

### The Terminal Solution

Run this command inside your terminal interface to execute the parallel training bake-off script:

```bash
python3 /root/code/fraud-detection/src/models/train_parallel.py

```

---

### MLFlow UI

<img width="1366" height="645" alt="image" src="https://github.com/user-attachments/assets/22377b0f-c098-4e85-aa68-9eb69c474642" />

---

<img width="1366" height="647" alt="image" src="https://github.com/user-attachments/assets/9eddcd0e-b88e-4de8-91fa-ed6ba7ba8d90" />


---

### Rule for Instant Recall

> **`n_jobs=1` locks computation to a single core; `n_jobs=-1` scales across all available hardware cores.** When measuring hardware acceleration improvements, verify that your dataset is sufficiently large (e.g., thousands of rows) to offset the minor system memory overhead associated with spawning parallel subprocess threads.
