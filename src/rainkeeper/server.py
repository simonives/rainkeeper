"""Rainkeeper MCP server entry point."""
from fastmcp import FastMCP
from .tools import collections, raindrops, bulk, search, tags

mcp = FastMCP(
    name="rainkeeper",
    instructions="Manage Raindrop.io bookmarks and collections. Use list_collections first to get collection IDs before moving or filing bookmarks.",
)

collections.register(mcp)
raindrops.register(mcp)
bulk.register(mcp)
search.register(mcp)
tags.register(mcp)


def main():
    mcp.run()


if __name__ == "__main__":
    main()
