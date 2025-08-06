from fastapi import FastAPI, HTTPException, Request, Depends
from pydantic import BaseModel
from typing import List
from inference import predict_label
from auth import verify_api_key
from rate_limiter import check_rate_limit
from logger import log_request

app = FastAPI(title="Zero-Day Threat Detection API")

class FeatureVector(BaseModel):
    features: List[float]

@app.get("/")
def root():
    return {"message": "Zero-Day Threat Detection API is running."}

@app.post("/predict")
def predict(
    data: FeatureVector,
    request: Request,
    _: None = Depends(verify_api_key),
    __: None = Depends(check_rate_limit)
):
    try:
        prediction = predict_label(data.features)
        label = "BENIGN" if prediction == 0 else "ATTACK"
        log_request(request.client.host, data.features, label)
        return {"prediction": prediction, "label": label}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
