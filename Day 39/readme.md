# Day 39: Dynamic Device Management & Resumable Checkpoint Systems in PyTorch

### Problem Statement

The xFusionCorp Industries PyTorch trainer at `/root/code/fraud-detection/src/models/train_pytorch.py` contains rigid hardware assumptions and lacks checkpointing. Update the device selection to dynamically detect whether CUDA or CPU is available, log the runtime device to MLflow, and add per-epoch checkpointing every 10th epoch to save the model and optimizer state.

---

### The Code Fix

Open `/root/code/fraud-detection/src/models/train_pytorch.py` and implement dynamic device mapping along with path-based checkpoint serialization:

```python
def main():
    torch.manual_seed(SEED)
    np.random.seed(SEED)
    
    # FIX 1: Dynamically detect and assign the execution device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    mlflow.set_tracking_uri(TRACKING_URI)
    mlflow.set_experiment(EXPERIMENT)

    df = pd.read_csv(TRAIN_CSV)
    X = df[FEATURES].values.astype(np.float32)
    y = df[TARGET].values.astype(np.int64)

    # FIX 2: Bind input tensors and model weights to the target device
    X_t = torch.from_numpy(X).to(device)
    y_t = torch.from_numpy(y).to(device)

    model = FraudNet().to(device)

    optimizer = torch.optim.SGD(model.parameters(), lr=LR)
    loss_fn = nn.CrossEntropyLoss()

    os.makedirs(CHECKPOINT_DIR, exist_ok=True)

    with mlflow.start_run(run_name="fraud-mlp"):
        # Log the actual device type used ("cpu" or "cuda")
        mlflow.log_param("device", device.type)

        xb = X_t.to(device)
        yb = y_t.to(device)

        final_loss = None
        for epoch in range(EPOCHS):
            logits = model(xb)
            loss = loss_fn(logits, yb)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            final_loss = float(loss.item())
            print(f"epoch {epoch:02d}  loss={final_loss:.4f}")

            # FIX 3: Save full checkpoint dict with filename path every 10 epochs
            if epoch % 10 == 0:
                checkpoint = {
                    "epoch": epoch, 
                    "model_state_dict": model.state_dict(),
                    "optimizer_state_dict": optimizer.state_dict(),
                    "loss": final_loss
                }
                ckpt_path = os.path.join(CHECKPOINT_DIR, f"ckpt_epoch_{epoch}.pt")
                torch.save(checkpoint, ckpt_path)

        mlflow.log_metric("final_loss", final_loss)

        os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
        torch.save(model.state_dict(), MODEL_PATH)
        print(f"Model saved to {MODEL_PATH}")

```

---

### The Terminal Solution

Run this command inside your terminal workspace to execute the PyTorch training pass:

```bash
python3 /root/code/fraud-detection/src/models/train_pytorch.py

```

---

### UI Verification Checkpoint Placeholders

#### 1. Device Parameter Logging

<img width="1366" height="647" alt="image" src="https://github.com/user-attachments/assets/6a14abf2-f982-4b0b-9de1-d385943f9d52" />


#### 2. Saved Checkpoint File Layout

Verify in your terminal or file explorer directory view that state-dict files (`ckpt_epoch_0.pt`, `ckpt_epoch_10.pt`, `ckpt_epoch_20.pt`) are generated inside `/root/code/fraud-detection/checkpoints/`.
<img width="1366" height="640" alt="image" src="https://github.com/user-attachments/assets/1732bca3-c544-4874-bf49-86fc7db63d27" />

---

### Rule for Instant Recall

> **Always use `torch.device("cuda" if torch.cuda.is_available() else "cpu")` instead of bare `.cuda()` calls.** When saving state dicts for checkpointing, construct a explicit target filename path using `os.path.join()` so `torch.save()` writes to a file rather than attempting to overwrite a directory.
