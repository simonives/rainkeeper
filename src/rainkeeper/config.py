import os
from dotenv import load_dotenv

load_dotenv()

RAINDROP_ACCESS_TOKEN = os.environ.get("RAINDROP_ACCESS_TOKEN")
if not RAINDROP_ACCESS_TOKEN:
    raise ValueError(
        "RAINDROP_ACCESS_TOKEN is not set. "
        "Copy .env.example to .env and add your Raindrop.io test token. "
        "Get one at: https://app.raindrop.io/settings/integrations"
    )

BASE_URL = "https://api.raindrop.io/rest/v1"
AUTH_HEADER = {"Authorization": f"Bearer {RAINDROP_ACCESS_TOKEN}"}
