"""Build a point-in-time-correct training set from the Feast offline store.

A feature store's *offline* path is how you generate TRAINING data:
given an entity dataframe of `(id, event_timestamp)` rows,
`get_historical_features` joins each feature's value **as of** that
timestamp — so a training row never sees a feature value from the
future (no label leakage). This is the consistency guarantee that
makes the same feature definitions safe for both training and serving.
"""

import pandas as pd
from feast import FeatureStore

REPO = "/root/code/feature_repo/feature_repo"
store = FeatureStore(repo_path=REPO)

# 1. Build the entity dataframe from real (driver_id, event_timestamp) pairs
source = pd.read_parquet(f"{REPO}/data/driver_stats.parquet")
entity_df = source[["driver_id", "event_timestamp"]].head(10).reset_index(drop=True)

# 2. Build the point-in-time correct training set using Feast get_historical_features
training_df = store.get_historical_features(
    entity_df=entity_df,
    features=[
        "driver_hourly_stats:conv_rate",
        "driver_hourly_stats:acc_rate",
        "driver_hourly_stats:avg_daily_trips",
    ],
).to_df()

# 3. Save the generated offline dataset to Parquet
training_df.to_parquet("/root/code/training_set.parquet", index=False)

print(
    "wrote /root/code/training_set.parquet:",
    len(training_df),
    "rows, columns:",
    list(training_df.columns),
)
