from fastmcp import FastMCP
from ..client import RaindropClient


def register(mcp: FastMCP, client: RaindropClient) -> None:
    @mcp.tool()
    async def search_raindrops(query: str, collection_id: int = 0, page: int = 0, per_page: int = 25) -> dict:
        """Search bookmarks using Raindrop search syntax. collection_id 0 = search all. Supports #tag, word, \"phrase\", type:article, etc. Maximum per_page is 50."""
        return await client.list_raindrops(collection_id, page=page, per_page=per_page, search=query)
