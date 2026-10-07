# Network Attack Detection

A machine learning project that flags suspicious network traffic as "normal" or "attack", served through a fast API.

## Dataset
NSL-KDD (KDDTrain+ and KDDTest+). About 126,000 training records and 22,500 test records.
The test set includes attack types that never appear in training, so it is a hard, realistic test.

## What I did
1. Loaded and explored the data (47% of the training records are attacks).
2. Converted text columns to numbers with one-hot encoding.
3. Trained a baseline (Logistic Regression), then Random Forest and XGBoost.
4. Tested ways to handle rare attacks: class weights and SMOTE.
5. Evaluated with recall, precision, F1, false alarm rate and PR-AUC.
6. Saved the best model and served it with FastAPI.

## Results (on KDDTest+)

| Model | Attack recall | Attack precision | False alarm rate |
|---|---|---|---|
| Logistic Regression (baseline) | 0.624 | 0.917 | 0.074 |
| Random Forest | 0.608 | 0.967 | 0.027 |
| XGBoost | 0.659 | 0.968 | 0.028 |
| XGBoost, threshold 0.1 | 0.707 | 0.969 | 0.030 |

- XGBoost PR-AUC: 0.968
- XGBoost missed 4,380 attacks, compared with 4,828 for the baseline, and cut false alarms from 7.4% to 2.8%.
- Lowering the decision threshold to 0.1 caught more attacks (recall 0.707) with only a small rise in false alarms.
- Class weights and SMOTE gave only small gains on this dataset.
- API speed: average XX ms per request, 95% of requests under XX ms (tested on a laptop).

## Run it yourself
```
pip install -r requirements.txt
python download_data.py
uvicorn app:app --reload
```
Then open http://127.0.0.1:8000/docs to try the API.

## Files
- `attack_detection.ipynb`: data exploration, training and evaluation
- `app.py`: FastAPI service
- `models/`: saved model, column order and a sample request
- `download_data.py`: downloads the dataset

## Limitations
NSL-KDD is an older benchmark, and the test set contains unseen attack types, so recall is limited. Real network traffic would need fresher data.