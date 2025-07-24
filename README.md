# PredChem MVP (Stub)

This repository contains a minimal skeleton implementation of the PredChem MVP as described in the design document. It exposes four FastAPI endpoints:

- `/api/planner` – returns a dummy two-step route graph for any text prompt
- `/api/simulate` – given reaction SMILES strings, returns placeholder product and yield predictions
- `/api/safety` – checks provided SMILES against a small blocked list and reports status
- `/api/export` – renders a simple PDF of the route

The code is located in `backend/main.py`. This is **not** a production-ready implementation; it serves only as a lightweight demonstration of the intended API shape.

## Running

```bash
pip install fastapi uvicorn fpdf2
uvicorn backend.main:app --reload
```

The application will start on `http://localhost:8000` and provide an interactive Swagger UI at `/docs`.
