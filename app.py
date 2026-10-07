import json
import joblib
import pandas as pd
from fastapi import FastAPI

app = FastAPI(title="Network Attack Detection API")

# Load the saved model and column order once, when the API starts
model = joblib.load("models/attack_model.joblib")
with open("models/columns.json") as f:
    columns = json.load(f)

TEXT_COLUMNS = ["protocol_type", "service", "flag"]


@app.get("/")
def home():
    return {"message": "Network attack detection API is running"}


@app.post("/predict")
def predict(connection: dict):
    # Turn the request into a one-row table
    df = pd.DataFrame([connection])

    # Make sure number columns are numbers
    for c in df.columns:
        if c not in TEXT_COLUMNS:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    # Same text-to-number conversion as in training
    text_cols = [c for c in TEXT_COLUMNS if c in df.columns]
    df = pd.get_dummies(df, columns=text_cols, dtype=int)

    # Match the exact columns the model was trained on
    df = df.reindex(columns=columns, fill_value=0).fillna(0)

    prob = float(model.predict_proba(df)[0, 1])
    return {
        "prediction": "attack" if prob >= 0.5 else "normal",
        "attack_probability": round(prob, 4),
    }