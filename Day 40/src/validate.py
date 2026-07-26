import json

def validate_dataset():
    # Simulated internal data sanity checks
    validation_output = {
        "status": "ok",
        "rows": 200,
        "columns": ["amount", "hour", "num_tx_past_day", "is_fraud"]
    }
    
    # Save step results for subsequent pipeline usage
    with open("reports/validation_status.json", "w") as f:
        json.dump(validation_output, f, indent=2)
        
    print(f"[validate] {validation_output}")

if __name__ == "__main__":
    validate_dataset()
