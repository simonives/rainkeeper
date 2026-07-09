from fastmcp import FastMCP
from ..client import RaindropClient


def register(mcp: FastMCP, client: RaindropClient) -> None:
    @mcp.tool()
    async def list_collections() -> list[dict]:
        """List all Raindrop.io collections (root and sub-collections), with id, title, and parent_id."""
        return await client.list_collections()

    @mcp.tool()
    async def get_collection(collection_id: int) -> dict:
        """Get details of a single collection by id."""
        return await client.get_collection(collection_id)

    @mcp.tool()
    async def create_collection(title: str, parent_id: int | None = None, public: bool = False, color: str | None = None) -> dict:
        """Create a new collection. Pass parent_id to create a sub-collection."""
        return await client.create_collection(title, parent_id=parent_id, public=public, color=color)

    @mcp.tool()
    async def update_collection(collection_id: int, title: str | None = None, public: bool | None = None, color: str | None = None) -> dict:
        """Update a collection's title, visibility, or colour. color is a hex string e.g. '#ff0000'."""
        return await client.update_collection(collection_id, title=title, public=public, color=color)

    @mcp.tool()
    async def delete_collection(collection_id: int) -> dict:
        """Delete a collection. Contents move to Unsorted."""
        return await client.delete_collection(collection_id)
