from fastmcp import FastMCP
from ..client import RaindropClient


def register(mcp: FastMCP, client: RaindropClient) -> None:
    @mcp.tool()
    async def list_tags(collection_id: int | None = None) -> list[dict]:
        """List all tags. Pass collection_id to scope to a specific collection."""
        return await client.list_tags(collection_id)

    @mcp.tool()
    async def rename_tag(old_tag: str, new_tag: str) -> dict:
        """Rename a tag across all bookmarks."""
        return await client.rename_tag(old_tag, new_tag)

    @mcp.tool()
    async def delete_tags(tags: list[str]) -> dict:
        """Delete one or more tags from all bookmarks."""
        return await client.delete_tags(tags)
