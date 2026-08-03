# Day 43: Online Feature Materialization & Low-Latency Retrieval with Feast

### Quick Summary
* **Problem:** `materialize.sh` used an outdated `END_DATE`, syncing 0 rows to `online_store.db` and causing live inference calls (`get_online_features`) to return `None`.
* **Solution:** Updated `END_DATE` in `materialize.sh` to `2026-01-01T00:00:00`, ran `./materialize.sh` to sync batch features to SQLite, and authored `fetch_features.py` to retrieve live features for customers 1–5.

---

### Core Principles & Architecture
* **Why Feast Exists:** ML models require data in two environments: **Offline** (slow historical files for training) and **Online** (fast key-value stores for instant predictions). Feast keeps both environments in sync to eliminate training-serving skew.
* **Component Roles:**
  * `features.py`: Schema blueprint for entity keys and feature fields.
  * `registry.db`: Catalog compiled via `feast apply`.
  * `transactions.parquet`: Heavy offline historical source for model training.
  * `online_store.db`: Fast SQLite store for live serving lookups.
  * `materialize.sh`: Syncs records from Parquet into SQLite up to `END_DATE`.
  * `fetch_features.py`: Queries `online_store.db` to simulate real-time production inference.

---

### Key Execution Commands

```bash
cd /root/code/fraud-detection/feature_repo/
chmod +x materialize.sh
./materialize.sh
python3 fetch_features.py
