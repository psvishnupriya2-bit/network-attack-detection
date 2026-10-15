import json
from pathlib import Path

import numpy as np
import pandas as pd
import xgboost as xgb
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

BASE = Path(__file__).parent

app = FastAPI(
    title="Network Attack Detection: Real Traffic Replay",
    description="Score recorded network flows (CIC-IDS2017 format) as normal or attack.",
    version="2.0.0",
)

# Load the trained model and its column order once, when the API starts
booster = xgb.Booster()
booster.load_model(str(BASE / "models" / "real_model.json"))
with open(BASE / "models" / "real_columns.json") as f:
    columns = json.load(f)

MAX_ROWS = 1000


def score(rows):
    df = pd.DataFrame(rows)
    df.columns = df.columns.astype(str).str.strip()
    df = df.loc[:, ~df.columns.duplicated()]
    df = df.reindex(columns=columns)
    df = df.apply(pd.to_numeric, errors="coerce")
    df = df.replace([np.inf, -np.inf], np.nan)
    return booster.predict(xgb.DMatrix(df))


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def home():
    return (BASE / "index.html").read_text(encoding="utf-8")


@app.get("/health", tags=["Status"])
def health():
    return {"status": "ok", "message": "Real traffic detection API is running"}


@app.get("/api/demo", tags=["Demo"])
def demo():
    path = BASE / "models" / "demo_flows.csv"
    if not path.exists():
        raise HTTPException(status_code=404, detail="Demo file not found")
    df = pd.read_csv(path)
    return {"rows": json.loads(df.to_json(orient="records"))}


@app.post("/api/score", tags=["Prediction"])
def score_rows(payload: dict):
    rows = payload.get("rows")
    if not isinstance(rows, list) or not rows:
        raise HTTPException(status_code=400, detail="Send a list of rows.")
    if len(rows) > MAX_ROWS:
        raise HTTPException(status_code=400, detail="Too many rows in one request.")
    try:
        probs = score(rows)
    except Exception:
        raise HTTPException(status_code=400,
                            detail="Could not read these rows. Check the column names.")
    return {"n": len(rows), "probabilities": [round(float(p), 4) for p in probs]}
