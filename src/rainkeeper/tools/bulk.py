from fastmcp import FastMCP
from ..client import RaindropClient

_client = RaindropClient()


def register(mcp: FastMCP) -> None:
    @mcp.tool()
    async def bulk_move_raindrops(ids: list[int], source_collection_id: int, target_collection_id: int) -> dict:
        """Move multiple bookmarks to a target collection in one call. Uses correct nested collection format."""
        return await _client.bulk_move(source_collection_id, ids, target_collection_id)

    @mcp.tool()
    async def bulk_tag_raindrops(ids: list[int], collection_id: int, tags: list[str]) -> dict:
        """Apply tags to multiple bookmarks. Merges with existing tags."""
        return await _client.bulk_tag(collection_id, ids, tags)

    @mcp.tool()
    async def bulk_mark_important(ids: list[int], collection_id: int, important: bool = True) -> dict:
        """Flag multiple bookmarks as important (starred)."""
        return await _client.bulk_mark_important(collection_id, ids, important)

    @mcp.tool()
    async def bulk_delete_raindrops(ids: list[int], collection_id: int) -> dict:
        """Permanently delete multiple bookmarks."""
        return await _client.bulk_delete(collection_id, ids)
