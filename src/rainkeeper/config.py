import os
from dotenv import load_dotenv

load_dotenv()

RAINDROP_ACCESS_TOKEN: str = os.environ["RAINDROP_ACCESS_TOKEN"]
BASE_URL = "https://api.raindrop.io/rest/v1"
AUTH_HEADER = {"Authorization": f"Bearer {RAINDROP_ACCESS_TOKEN}"}
