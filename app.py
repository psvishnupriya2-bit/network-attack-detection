import json
from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

BASE = Path(__file__).parent

app = FastAPI(
    title="Network Attack Detection API",
    description="Send one network connection and get back whether it looks "
                "like normal traffic or an attack.",
    version="1.0.0",
)

# Load the saved model and column order once, when the API starts
model = joblib.load(BASE / "models" / "attack_model.joblib")
with open(BASE / "models" / "columns.json") as f:
    columns = json.load(f)

TEXT_COLUMNS = ["protocol_type", "service", "flag"]


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def home():
    # The neat web page
    return (BASE / "index.html").read_text(encoding="utf-8")


@app.get("/health", tags=["Status"])
def health():
    return {"status": "ok", "message": "Network attack detection API is running"}


@app.post("/predict", tags=["Prediction"])
def predict(connection: dict):
    try:
        df = pd.DataFrame([connection])

        for c in df.columns:
            if c not in TEXT_COLUMNS:
                df[c] = pd.to_numeric(df[c], errors="coerce")

        text_cols = [c for c in TEXT_COLUMNS if c in df.columns]
        df = pd.get_dummies(df, columns=text_cols, dtype=int)
        df = df.reindex(columns=columns, fill_value=0).fillna(0)

        prob = float(model.predict_proba(df)[0, 1])
    except Exception:
        raise HTTPException(status_code=400,
                            detail="Could not read this connection. Check the values and try again.")

    is_attack = prob >= 0.5
    if prob >= 0.8:
        risk = "High"
    elif prob >= 0.3:
        risk = "Medium"
    else:
        risk = "Low"

    return {
        "prediction": "attack" if is_attack else "normal",
        "attack_probability": round(prob, 4),
        "confidence_percent": round((prob if is_attack else 1 - prob) * 100, 2),
        "risk_level": risk,
        "message": ("This connection looks like an attack. Flag it for the security team."
                    if is_attack else
                    "This connection looks like normal traffic."),
    }
