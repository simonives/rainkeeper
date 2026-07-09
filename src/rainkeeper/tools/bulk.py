from fastmcp import FastMCP
from ..client import RaindropClient


def register(mcp: FastMCP, client: RaindropClient) -> None:
    @mcp.tool()
    async def bulk_move_raindrops(ids: list[int], source_collection_id: int, target_collection_id: int) -> dict:
        """Move multiple bookmarks to a target collection. ids must be non-empty and all from source_collection_id — ids from other collections are silently skipped by the API."""
        result = await client.bulk_move(source_collection_id, ids, target_collection_id)
        modified = result.get("modified", 0)
        if modified < len(ids):
            result["warning"] = f"Only {modified} of {len(ids)} bookmarks were moved. Ensure all ids belong to source_collection_id={source_collection_id}."
        return result

    @mcp.tool()
    async def bulk_tag_raindrops(ids: list[int], collection_id: int, tags: list[str]) -> dict:
        """Apply tags to multiple bookmarks. Merges with existing tags. WARNING: passing tags=[] will remove all tags from the targeted bookmarks."""
        return await client.bulk_tag(collection_id, ids, tags)

    @mcp.tool()
    async def bulk_mark_important(ids: list[int], collection_id: int, important: bool = True) -> dict:
        """Flag multiple bookmarks as important (starred). ids must be non-empty."""
        return await client.bulk_mark_important(collection_id, ids, important)

    @mcp.tool()
    async def bulk_delete_raindrops(ids: list[int], collection_id: int) -> dict:
        """Permanently delete multiple bookmarks. ids must be non-empty."""
        return await client.bulk_delete(collection_id, ids)
