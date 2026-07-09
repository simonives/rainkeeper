from fastmcp import FastMCP
from ..client import RaindropClient

_client = RaindropClient()


def register(mcp: FastMCP) -> None:
    @mcp.tool()
    async def list_collections() -> list[dict]:
        """List all Raindrop.io collections (root and sub-collections), with id, title, and parent_id."""
        return await _client.list_collections()

    @mcp.tool()
    async def get_collection(collection_id: int) -> dict:
        """Get details of a single collection by id."""
        return await _client.get_collection(collection_id)

    @mcp.tool()
    async def create_collection(title: str, parent_id: int | None = None, public: bool = False, color: str | None = None) -> dict:
        """Create a new collection. Pass parent_id to create a sub-collection."""
        return await _client.create_collection(title, parent_id=parent_id, public=public, color=color)

    @mcp.tool()
    async def update_collection(collection_id: int, title: str | None = None, public: bool | None = None, color: str | None = None) -> dict:
        """Update a collection's title, visibility, or colour."""
        return await _client.update_collection(collection_id, title=title, public=public, color=color)

    @mcp.tool()
    async def delete_collection(collection_id: int) -> dict:
        """Delete a collection. Contents move to Unsorted."""
        return await _client.delete_collection(collection_id)
