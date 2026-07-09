import os
from dotenv import load_dotenv

load_dotenv()

RAINDROP_ACCESS_TOKEN = os.environ.get("RAINDROP_ACCESS_TOKEN")

BASE_URL = "https://api.raindrop.io/rest/v1"


def get_auth_header() -> dict:
    """Return the auth header, raising if the token is missing."""
    token = RAINDROP_ACCESS_TOKEN
    if not token:
        raise ValueError(
            "RAINDROP_ACCESS_TOKEN is not set. "
            "Copy .env.example to .env and add your Raindrop.io test token. "
            "Get one at: https://app.raindrop.io/settings/integrations"
        )
    return {"Authorization": f"Bearer {token}"}
