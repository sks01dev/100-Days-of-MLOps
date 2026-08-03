# Local File Path: /root/code/fraud-detection/feature_repo/fetch_features.py
# Lab Environment Path: /root/code/fraud-detection/feature_repo/fetch_features.py
# Description: Python script simulating a production service reading live materialized 
#              features from the Feast online store for customer entity keys 1 through 5.

import json
from feast import FeatureStore

# Initialize the Feast feature store using the current directory repo context
store = FeatureStore(repo_path=".")

# Fetch online features from online_store.db for customers 1 to 5
result = store.get_online_features(
    features=[
        "customer_transaction_features:amount",
        "customer_transaction_features:hour",
        "customer_transaction_features:num_tx_past_day",
    ],
    entity_rows=[{"customer_id": i} for i in range(1, 6)],
).to_dict()

# Save the materialized payload to JSON for inspection
with open("online_features.json", "w") as f:
    json.dump(result, f, indent=2, default=str)

print("wrote online_features.json:", result)
