"""Stage 4 — Register the selected model.

Reads the selection written by the previous stage, registers the
selected run's model as `fraud-detector` in the MLflow Model
Registry, and assigns the release-lane alias so the serving layer
can fetch the right version by name.
"""
import json
import os
import sys

import mlflow
from mlflow.tracking import MlflowClient

TRACKING_URI = "http://localhost:5000"
REPORTS_DIR = "/root/code/fraud-detection/reports"
SELECTION_JSON = os.path.join(REPORTS_DIR, "selection.json")

REGISTERED_MODEL_NAME = "fraud-detector"
# The release-lane alias the serving layer resolves by name. Per the
# release checklist, models promoted by this pipeline go to "staging".
RELEASE_ALIAS = "staging"


def main():
    if not os.path.exists(SELECTION_JSON):
        sys.exit(
            f"[register] {SELECTION_JSON} missing — the select stage "
            "has not produced a selection yet."
        )
    with open(SELECTION_JSON) as f:
        selection = json.load(f)

    mlflow.set_tracking_uri(TRACKING_URI)
    client = MlflowClient()

    model_uri = f"runs:/{selection['run_id']}/model"
    version = mlflow.register_model(model_uri, REGISTERED_MODEL_NAME)

    # TODO: assign the release-lane alias so the serving layer can fetch
    # this version by name. Point RELEASE_ALIAS at the just-registered
    # version using client.set_registered_model_alias(name, alias,
    # version) — pass REGISTERED_MODEL_NAME, RELEASE_ALIAS, and
    # version.version.
    client.set_registered_model_alias(REGISTERED_MODEL_NAME, RELEASE_ALIAS, version.version)

    print(
        f"[register] {REGISTERED_MODEL_NAME} v{version.version} "
        f"registered (assign the {RELEASE_ALIAS!r} alias in the TODO)"
    )


if __name__ == "__main__":
    main()
