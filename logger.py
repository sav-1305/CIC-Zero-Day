import logging

# Configure logger
logger = logging.getLogger("api_logger")
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler("api_requests.log")
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

def log_request(ip: str, data: dict, result: str):
    logger.info(f"IP: {ip}, Input: {data}, Prediction: {result}")
