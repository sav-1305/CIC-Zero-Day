import os
from dotenv import load_dotenv
from fastapi import Header, HTTPException

# Load variables from .env file
load_dotenv()

# Fetch the API key
API_KEY = os.getenv("API_KEY")

if API_KEY is None:
    raise RuntimeError("API_KEY environment variable not set.")

def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
