# Changelog

All notable changes to Rainkeeper are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Versioning follows [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [0.1.0] -- 2026-07-09

### Added

- `RaindropClient` -- async HTTP wrapper around Raindrop.io REST API v1 using `httpx`
- Collection tools: `list_collections`, `get_collection`, `create_collection`, `update_collection`, `delete_collection`
- Bookmark tools: `list_raindrops`, `get_raindrop`, `create_raindrop`, `update_raindrop`, `move_raindrop`, `delete_raindrop`
- Bulk tools: `bulk_move_raindrops`, `bulk_tag_raindrops`, `bulk_mark_important`, `bulk_delete_raindrops`
- Search: `search_raindrops` with full Raindrop search syntax support
- Tag tools: `list_tags`, `rename_tag`, `delete_tags`
- Sub-collection support: `list_collections` fetches root and child collections
- FastMCP server entry point; installable as `rainkeeper` CLI command

### Fixed

- Critical: collection move operations now use the correct `{"collection": {"$id": n}}` API format, fixing the silent failure in existing community MCP servers
- Critical: bulk move operations use the correct nested collection format, fixing "Resource not found" errors
