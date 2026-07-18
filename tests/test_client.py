import pytest
from unittest.mock import patch
from rainkeeper.client import RaindropClient

@pytest.mark.asyncio
async def test_lazy_instantiation_no_token_crash():
    """Test that creating a client without a token does not crash instantly."""
    with patch("rainkeeper.config.RAINDROP_ACCESS_TOKEN", None):
        client = RaindropClient()
        # Should not crash on instantiation
        assert client._httpx_client is None

@pytest.mark.asyncio
async def test_lazy_instantiation_crash_on_request():
    """Test that it crashes on first request if token is missing."""
    with patch("rainkeeper.config.RAINDROP_ACCESS_TOKEN", None):
        client = RaindropClient()
        with pytest.raises(ValueError, match="RAINDROP_ACCESS_TOKEN is not set"):
            # Trigger property access which should raise ValueError
            _ = client.client

@pytest.mark.asyncio
async def test_lazy_instantiation_success():
    """Test that client initializes successfully when token is present."""
    with patch("rainkeeper.config.RAINDROP_ACCESS_TOKEN", "fake_token"):
        client = RaindropClient()
        assert client._httpx_client is None
        
        # Accessing the client property should initialize the httpx.AsyncClient
        httpx_client = client.client
        assert httpx_client is not None
        assert httpx_client.headers.get("Authorization") == "Bearer fake_token"
