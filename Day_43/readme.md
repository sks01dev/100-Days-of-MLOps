# Day 43: Online Feature Materialization & Low-Latency Retrieval with Feast

## Executive Summary
* **Problem:** The original `materialize.sh` script used an outdated or boundary-bound `END_DATE`. As a result, Feast synced **0 rows** into the online SQLite database (`data/online_store.db`), causing real-time feature retrieval calls (`get_online_features()`) to return `None` or null values during inference.
* **Solution:** Updated `END_DATE` in `materialize.sh` to `2026-01-01T00:00:00` (covering all source event timestamps), executed `./materialize.sh` to sync Parquet batch records into SQLite, and authored `fetch_features.py` to fetch low-latency features for customer IDs 1 through 5.

---

## Core Principles & Architecture

### 1. First Principles: Why Feast Exists
Machine Learning models require data in two distinct environments:
* **Offline Store:** Heavy, historical batch files (e.g., Parquet, S3, Snowflake) optimized for high-throughput model training without data leakage.
* **Online Store:** Ultra-low-latency key-value stores (e.g., SQLite, Redis, DynamoDB) optimized for millisecond-level live prediction lookups.

Feast acts as a unified feature store to keep both environments synchronized under identical schema definitions, completely eliminating training-serving skew.

### 2. Component Roles
* `features.py` **(The Blueprint):** Code declaration defining entity join keys (`customer_id`) and feature schemas (`amount`, `hour`, `num_tx_past_day`).
* `registry.db` **(The Catalog):** A compiled catalog produced by `feast apply` that Feast components read at runtime to discover feature views and entities.
* `transactions.parquet` **(Offline Archive):** Heavy historical batch source used strictly for point-in-time offline joins during training.
* `online_store.db` **(Online Database):** Lightweight SQLite database queried by live serving APIs during prediction.
* `materialize.sh` **(The Sync Engine):** Copies feature values from `transactions.parquet` into `online_store.db` up to `END_DATE`.
* `fetch_features.py` **(The Live App Simulator):** Simulates a production microservice querying `online_store.db` to serve real-time predictions.

---

## Execution Workflow

```bash
# 1. Navigate to the Feast feature repository directory
cd /root/code/fraud-detection/feature_repo/

# 2. Grant execution permissions and run online store materialization
chmod +x materialize.sh
./materialize.sh

# 3. Retrieve materialized online features and export to JSON
python3 fetch_features.py
```
---

# 📁 Code Files Associated with the Change

### 1. File: `fraud-detection/feature_repo/materialize.sh`
*(Save at `/root/code/fraud-detection/feature_repo/materialize.sh`)*

```bash
#!/bin/bash
# Local File Path: /root/code/fraud-detection/feature_repo/materialize.sh
# Lab Environment Path: /root/code/fraud-detection/feature_repo/materialize.sh
# Description: Shell script that triggers Feast materialization to sync offline 
#              Parquet transactions into the online SQLite database up to END_DATE.

set -euo pipefail

# Ensure script operates within its local directory context
cd "$(dirname "$0")"

# FIX: Set the ISO-8601 end date beyond all dataset event timestamps (>= 2024-01-01)
END_DATE="2026-01-01T00:00:00"

feast materialize-incremental "$END_DATE"
