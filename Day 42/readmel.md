# Day 42: Custom Entities & Feature Views in Feast

### Problem Statement

The feature repository at `/root/code/fraud-detection/feature_repo/` contained a draft `features.py` with an incorrect join key (`id`) and placeholder data types (`STRING`). Re-author `features.py` to match `data/transactions.parquet`, re-apply the registry using `feast apply`, and confirm the updated definitions in the Feast UI.

---

### 📁 Repository File Changes

#### 1. File: `fraud-detection/feature_repo/features.py`

```python
"""Feature definitions for the fraud detection feature store."""

from datetime import timedelta
from feast import Entity, FeatureView, Field, FileSource
from feast.types import Float32, Int64

# 1. Source mapping
source = FileSource(
    name="transactions_source",
    path="data/transactions.parquet",
    timestamp_field="event_timestamp",
)

# 2. Customer Entity definition
customer = Entity(
    name="customer",
    join_keys=["customer_id"],
    description="Customer ID for fraud detection feature lookup",
)

# 3. Feature View with matching schema
customer_transaction_features = FeatureView(
    name="customer_transaction_features",
    entities=[customer],
    ttl=timedelta(days=1),
    schema=[
        Field(name="amount", dtype=Float32),
        Field(name="hour", dtype=Int64),
        Field(name="num_tx_past_day", dtype=Int64),
    ],
    online=True,
    source=source,
    tags={"team": "fraud_detection"},
)

```

---

### Execution Commands

```bash
# 1. Navigate to feature repository
cd /root/code/fraud-detection/feature_repo/

# 2. Apply updated definitions to Feast registry
feast apply

```
---

### Major Idea

> **Match `Field` dtypes directly to source file types, and never include target labels (e.g., `is_fraud`) inside a `FeatureView`.**

---
