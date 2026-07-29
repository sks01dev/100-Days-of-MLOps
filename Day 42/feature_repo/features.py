"""Feature definitions for the fraud detection feature store.

Defines:
  1. FileSource: Reading raw parquet transaction records.
  2. Entity: customer (keyed on `customer_id`).
  3. FeatureView: customer_transaction_features serving amount, hour,
     and num_tx_past_day features.
"""

from datetime import timedelta
from feast import (
    Entity,
    FeatureView,
    Field,
    FileSource,
)
from feast.types import Float32, Int64

# 1. Declare the data source mapping
source = FileSource(
    name="transactions_source",
    path="data/transactions.parquet",
    timestamp_field="event_timestamp",
)

# 2. Define the Customer Entity with matching join key
customer = Entity(
    name="customer",
    join_keys=["customer_id"],
    description="Customer ID for fraud detection feature lookup",
)

# 3. Define the Feature View with source-matching schema types
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
