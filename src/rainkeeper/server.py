"""Rainkeeper MCP server entry point."""
import asyncio
from fastmcp import FastMCP
from .client import RaindropClient
from .tools import collections, raindrops, bulk, search, tags

mcp = FastMCP(
    name="rainkeeper",
    instructions="Manage Raindrop.io bookmarks and collections. Use list_collections first to get collection IDs before moving or filing bookmarks.",
)

_client = RaindropClient()

collections.register(mcp, _client)
raindrops.register(mcp, _client)
bulk.register(mcp, _client)
search.register(mcp, _client)
tags.register(mcp, _client)


def main():
    mcp.run()


if __name__ == "__main__":
    main()
