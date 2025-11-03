from dotenv import load_dotenv
import os
load_dotenv()
BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000")
DEFAULT_TIMEOUT = float(os.getenv("DEFAULT_TIMEOUT", "10"))
