from fastmcp import FastMCP
from ..client import RaindropClient

_client = RaindropClient()


def register(mcp: FastMCP) -> None:
    @mcp.tool()
    async def search_raindrops(query: str, collection_id: int = 0, page: int = 0, per_page: int = 25) -> dict:
        """Search bookmarks using Raindrop search syntax. collection_id 0 = search all. Supports #tag, word, \"phrase\", type:article, etc."""
        return await _client.search(query, collection_id=collection_id, page=page, per_page=per_page)
