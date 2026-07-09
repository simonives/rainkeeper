from fastmcp import FastMCP
from ..client import RaindropClient

_client = RaindropClient()


def register(mcp: FastMCP) -> None:
    @mcp.tool()
    async def list_tags(collection_id: int | None = None) -> list[dict]:
        """List all tags. Pass collection_id to scope to a collection."""
        return await _client.list_tags(collection_id)

    @mcp.tool()
    async def rename_tag(old_tag: str, new_tag: str) -> dict:
        """Rename a tag across all bookmarks."""
        return await _client.rename_tag(old_tag, new_tag)

    @mcp.tool()
    async def delete_tags(tags: list[str]) -> dict:
        """Delete one or more tags from all bookmarks."""
        return await _client.delete_tags(tags)
