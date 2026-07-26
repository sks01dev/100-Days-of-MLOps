# ==============================================================================
# xFusionCorp Industries - MLOps Pipeline Automation Orchestrator
# ==============================================================================

.PHONY: train-pipeline clean help

# Default target when running 'make' without arguments
help:
	@echo "Available commands:"
	@echo "  make train-pipeline  : Execute complete end-to-end ML lifecycle"
	@echo "  make clean           : Purge generated model binaries and reports"

train-pipeline:
	@echo "[Pipeline] Stage 1/5: Executing Data Validation..."
	python3 src/validate_data.py
	
	@echo "[Pipeline] Stage 2/5: Commencing Hyperparameter Tuning..."
	python3 src/tune.py
	
	@echo "[Pipeline] Stage 3/5: Running Top Model Selection Evaluation..."
	python3 src/select_model.py
	
	@echo "[Pipeline] Stage 4/5: Registering Model to Central Registry..."
	python3 src/register.py
	
	@echo "[Pipeline] Stage 5/5: Compiling Consolidated Audit Artifact..."
	python3 src/report.py
	@echo "[Pipeline] End-to-End Run Successfully Completed."

clean:
	@echo "Purging localized artifact directories..."
	rm -rf models/ reports/
	mkdir -p reports/ && touch reports/.gitkeep
