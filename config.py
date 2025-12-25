import os
from dotenv import load_dotenv
import certifi

# Ensure SSL certificates are correctly resolved (Windows fix)
os.environ["SSL_CERT_FILE"] = certifi.where()

# Load environment variables
load_dotenv()

# Telegram bot token
TOKEN = os.getenv("TOKEN")

# JWT token used to authenticate against the backend
API_TOKEN = os.getenv("API_TOKEN")

# Base URL of the FastAPI backend
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

if not TOKEN or not API_TOKEN:
    raise RuntimeError("Missing required environment variables")
