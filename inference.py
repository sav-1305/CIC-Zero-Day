import numpy as np
import tensorflow as tf
import xgboost as xgb
import joblib

# Load models and scaler
scaler = joblib.load("scaler.pkl")
encoder = tf.keras.models.load_model("ae_encoder.keras")
xgb_model = xgb.XGBClassifier()
xgb_model.load_model("xgb_model.json")

def predict_label(input_features):
    # Reshape input
    input_array = np.array(input_features).reshape(1, -1)
    
    # Scale input
    scaled = scaler.transform(input_array)
    
    # Get encoded features
    latent = encoder.predict(scaled)
    
    # Predict class
    prediction = xgb_model.predict(latent)[0]
    return int(prediction)
