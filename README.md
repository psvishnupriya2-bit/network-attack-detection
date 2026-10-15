# Network Attack Detection (Real Traffic)

A machine learning project that checks whether a network flow looks **normal** or like an **attack**. It is trained on real recorded traffic from the CIC-IDS2017 dataset and served with FastAPI.

## Dataset
CIC-IDS2017: real network flows recorded over several days, labelled as BENIGN (normal) or as different attack types.

## What I did
1. Loaded and cleaned the CIC-IDS2017 data.
2. Trained an XGBoost model to tell normal flows from attacks.
3. Tested it on unseen real flows.
4. Saved the model and its column order.
5. Built a FastAPI app and a web page to check flows and show alarms.

## Project files
- `app.py`: FastAPI server
- `index.html`: web page (report and alarm panel)
- `real_data.ipynb`: notebook with training and testing
- `models/real_model.json`: trained model
- `models/real_columns.json`: column order used by the model
- `data/demo_flows.csv`: recorded flows used for the demo
- `requirements.txt`: Python packages

## How to run
```
pip install -r requirements.txt
uvicorn app:app --reload
```
Then open http://127.0.0.1:8000/ in your browser.

## How to use
1. Click **Load attack example** or **Load normal example**.
2. Click **Check Vulnerability** to see the result.
3. Click **Start demo traffic** to see the alarm panel update.
