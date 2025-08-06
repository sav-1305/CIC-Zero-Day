from fastapi import Request, HTTPException
from time import time

# {IP: [timestamps]}
RATE_LIMIT_WINDOW = 60  # seconds
RATE_LIMIT_COUNT = 30   # max requests per window
access_log = {}

def check_rate_limit(request: Request):
    ip = request.client.host
    now = time()

    if ip not in access_log:
        access_log[ip] = []

    # Remove timestamps older than window
    access_log[ip] = [t for t in access_log[ip] if now - t < RATE_LIMIT_WINDOW]

    if len(access_log[ip]) >= RATE_LIMIT_COUNT:
        raise HTTPException(status_code=429, detail="Too Many Requests")

    access_log[ip].append(now)

