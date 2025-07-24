from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import random
from fpdf import FPDF
import io

app = FastAPI(title="PredChem MVP")


class PlannerRequest(BaseModel):
    prompt: str


class SimulateRequest(BaseModel):
    reactions: List[str]


class SafetyRequest(BaseModel):
    smiles: List[str]


class ExportRequest(BaseModel):
    route: Dict


@app.post("/api/planner")
def plan_route(req: PlannerRequest):
    """Return a dummy 2-step route graph for the given prompt."""
    if not req.prompt:
        raise HTTPException(status_code=400, detail="Prompt required")
    route = {
        "nodes": [
            {"id": "step1", "smiles": "CCO", "label": "Start"},
            {"id": "step2", "smiles": "CCN", "label": "Product"},
        ],
        "edges": [{"source": "step1", "target": "step2"}],
    }
    return {"route": route}


@app.post("/api/simulate")
def simulate(req: SimulateRequest):
    """Return placeholder product predictions and random yield."""
    results = []
    for r in req.reactions:
        product = r.split(">>")[-1] if ">>" in r else "C"
        yield_est = round(random.uniform(0.5, 0.95), 2)
        results.append({"input": r, "product_smiles": product, "yield_est": yield_est})
    return {"results": results}


BLOCKED_SMILES = {"CCOC(=O)Cl"}  # dummy list


@app.post("/api/safety")
def safety(req: SafetyRequest):
    flagged = [s for s in req.smiles if s in BLOCKED_SMILES]
    status = "red" if flagged else "green"
    return {"status": status, "flagged": flagged}


@app.post("/api/export")
def export(req: ExportRequest):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="PredChem Route", ln=True)
    pdf.multi_cell(0, 10, txt=str(req.route))
    buf = io.BytesIO()
    pdf.output(buf)
    return {"file": buf.getvalue().hex()}
