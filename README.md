# Rainkeeper

A public, self-hostable MCP server that exposes the full [Raindrop.io](https://raindrop.io) API as Claude tools.

**Why this exists:** the community Raindrop MCP (v2.4.5) has a silent bug — collection moves do nothing. The Raindrop API requires `{"collection": {"$id": n}}`, not a flat `collectionId` field. Rainkeeper fixes that, adds proper sub-collection support, and is designed for sweep workflows: inbox triage, filing, tagging at scale.

---

## Tools

### Collections
| Tool | What it does |
|---|---|
| `list_collections` | All collections and sub-collections with ids |
| `get_collection` | Single collection detail |
| `create_collection` | New collection, optionally nested under a parent |
| `update_collection` | Rename, recolour, toggle public |
| `delete_collection` | Delete (contents go to Unsorted) |

### Bookmarks
| Tool | What it does |
|---|---|
| `list_raindrops` | Bookmarks in a collection, paginated |
| `get_raindrop` | Single bookmark detail |
| `create_raindrop` | Save a URL |
| `update_raindrop` | Edit title, tags, collection, note |
| `move_raindrop` | Move to a collection (named for clarity) |
| `delete_raindrop` | Delete permanently |

### Bulk
| Tool | What it does |
|---|---|
| `bulk_move_raindrops` | Move many bookmarks to a target collection |
| `bulk_tag_raindrops` | Apply tags to many bookmarks |
| `bulk_mark_important` | Star/unstar many bookmarks |
| `bulk_delete_raindrops` | Delete many bookmarks |

### Search
| Tool | What it does |
|---|---|
| `search_raindrops` | Full-text and syntax search (supports #tag, type:article, etc.) |

### Tags
| Tool | What it does |
|---|---|
| `list_tags` | All tags, optionally scoped to a collection |
| `rename_tag` | Rename a tag across all bookmarks |
| `delete_tags` | Delete tags from all bookmarks |

---

## Setup

### 1. Get a Raindrop test token

Sign in to Raindrop.io → Settings → Integrations → **For Developers** → create an app → copy the **Test token**. This works on free accounts.

### 2. Install

```bash
git clone https://github.com/simonives/rainkeeper.git
cd rainkeeper
pip install -e .   # or: uv pip install -e .
```

### 3. Configure

```bash
cp .env.example .env
# Edit .env and set RAINDROP_ACCESS_TOKEN=your_token
```

### 4. Register with Claude

**Claude Desktop** (`~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "rainkeeper": {
      "command": "python",
      "args": ["-m", "rainkeeper.server"],
      "cwd": "/path/to/rainkeeper",
      "env": {
        "RAINDROP_ACCESS_TOKEN": "your_token_here"
      }
    }
  }
}
```

**Claude CLI:**

```bash
claude mcp add rainkeeper -- python -m rainkeeper.server
```

---

## The collection move fix

The Raindrop API uses a nested object for collection references:

```json
PUT /raindrop/123
{"collection": {"$id": 456}}   ✓ correct
{"collectionId": 456}          ✗ silently ignored
```

Rainkeeper enforces the correct format in `RaindropClient` — tools never pass raw integers to the API.

---

## Architecture

```
src/rainkeeper/
├── server.py        FastMCP app, tool registrations
├── client.py        RaindropClient — thin async wrapper around the REST API
├── config.py        env vars, base URL, auth header
└── tools/
    ├── collections.py
    ├── raindrops.py
    ├── bulk.py
    ├── search.py
    └── tags.py
```

All HTTP lives in `RaindropClient`. Tools are thin wrappers that import the client and call methods — no `httpx` in tool files. This keeps API mapping testable independently of the MCP layer.

---

MIT License
