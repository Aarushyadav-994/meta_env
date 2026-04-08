# Simple Reach Environment

Minimal submission-ready repository for the Meta PyTorch OpenEnv Hackathon.

## Run the validator

Point your OpenEnv validator at `openenv.yaml`.

## Run the service

```bash
uvicorn inference:app --host 0.0.0.0 --port 8000
```

## Run inference

Set `API_BASE_URL`, `MODEL_NAME`, and `HF_TOKEN`, then run:

```bash
python inference.py
```
