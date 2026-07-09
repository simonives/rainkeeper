```
  ·  ·    ·  ·    ·  ·    ·    ·  ·    ·  ·    ·   ·  ·    ·  ·
    ·    ·    ·  ·     ·    · ·     ·    ·    ·  ·     ·  ·    ·

 ____      _    ___ _   _ _  _______ _____ _____ ____  _____ ____
|  _ \    / \  |_ _| \ | | |/ / ____| ____|  ___|  _ \| ____| __ \
| |_) |  / _ \  | ||  \| | ' /|  _| |  _| | |_  | |_) |  _| |    /
|  _ <  / ___ \ | || |\  | . \| |___| |___|  _| |  __/| |___|  _ \
|_| \_\/_/   \_\___|_| \_|_|\_\_____|_____|_|   |_|   |_____|_| \_\

    ·    ·    ·  ·     ·    · ·     ·    ·    ·  ·     ·  ·    ·
  ·  ·    ·  ·    ·  ·    ·    ·  ·    ·  ·    ·   ·  ·    ·  ·
```

<div align="center">

**The Raindrop.io MCP Server that works on free accounts — and actually moves bookmarks.**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-3776ab?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![FastMCP](https://img.shields.io/badge/FastMCP-powered-22c55e?style=flat-square)](https://github.com/jlowin/fastmcp)
[![License: MIT](https://img.shields.io/badge/license-MIT-f59e0b?style=flat-square)](LICENSE)
[![Raindrop.io API v1](https://img.shields.io/badge/Raindrop.io-API%20v1-2563eb?style=flat-square)](https://developer.raindrop.io)

</div>

---

## What is Raindrop.io?

[Raindrop.io](https://raindrop.io) is the bookmark manager that makes the web collectible. Save anything — articles, videos, PDFs, images, links — organise it into collections and sub-collections, tag it, annotate it, and surface it exactly when you need it. It runs on every platform, syncs everywhere, and has a free tier that covers everything most people ever need.

If you've ever lost a link, abandoned browser bookmarks, or wished your read-later queue could talk back — Raindrop is the answer.

Rainkeeper connects Raindrop to Claude, giving you natural-language control over your entire library.

---

## Why Rainkeeper?

Two problems with the existing MCP options:

**The official Raindrop.io MCP server requires a Pro subscription** (~$3/month). If you're on the free tier — which covers the vast majority of Raindrop's feature set — you cannot use it.

**The community alternative ([adeze/raindrop-mcp](https://github.com/adeze/raindrop-mcp)) has a silent critical bug:** collection moves do nothing. Ask Claude to file a bookmark into a collection, and the API call returns 200 OK — while the bookmark sits exactly where it was. The root cause is a malformed request body that the Raindrop API silently ignores. The same bug breaks all bulk move operations.

Rainkeeper fixes both.

| | Rainkeeper | Official MCP | Community MCP |
|---|:---:|:---:|:---:|
| Free account | ✅ | ❌ Pro only | ✅ |
| Collection moves work | ✅ | ✅ | ❌ Silent fail |
| Sub-collection support | ✅ | — | ❌ |
| Bulk operations | ✅ | — | ✅ (broken) |
| Self-hostable | ✅ | ✅ | ✅ |
| Open source (MIT) | ✅ | — | ✅ |

---

## The Fix

The Raindrop.io REST API uses a nested object for all collection references. Sending a flat integer is accepted without error — and silently ignored.

```json
// ✅ Correct — what Rainkeeper sends
PUT /raindrop/123
{"collection": {"$id": 456}}

// ❌ Silently ignored — what the community MCP sends
PUT /raindrop/123
{"collectionId": 456}
```

The same applies to bulk operations:

```json
// ✅ Correct
PUT /raindrops/0
{"ids": [111, 222], "collection": {"$id": 456}}

// ❌ Returns 404 or silently fails
PUT /raindrops/0
{"ids": [111, 222], "collectionId": 456}
```

`RaindropClient` enforces the correct format at the HTTP layer. Tools never pass raw integer IDs to the API. One rule, one place, always correct.

---

## Quick Start

### 1. Get your token

Raindrop.io → **Settings → Integrations → For Developers** → create an app → copy the **Test token**. Free accounts included. Takes 30 seconds.

### 2. Install

```bash
git clone https://github.com/simonives/rainkeeper.git
cd rainkeeper
pip install -e .    # or: uv pip install -e .
```

### 3. Configure

```bash
cp .env.example .env
# Open .env — set RAINDROP_ACCESS_TOKEN=your_token_here
```

### 4. Register with Claude

<details>
<summary><strong>Claude Desktop (macOS / Windows)</strong></summary>

Add to `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "rainkeeper": {
      "command": "python",
      "args": ["-m", "rainkeeper.server"],
      "cwd": "/absolute/path/to/rainkeeper",
      "env": {
        "RAINDROP_ACCESS_TOKEN": "your_token_here"
      }
    }
  }
}
```

Restart Claude Desktop after saving.
</details>

<details>
<summary><strong>Claude CLI</strong></summary>

```bash
claude mcp add rainkeeper -- python -m rainkeeper.server
```

Make sure your `.env` is in the `rainkeeper` directory and contains your token.
</details>

### 5. Verify

Ask Claude: *"List my Raindrop collections."*

You should see your collections within a few seconds. If you get an auth error, verify the token in your config matches what's in Raindrop Settings → Integrations.

---

## Tools

Rainkeeper exposes **17 tools** across five domains. Claude selects the right tool automatically — docstrings are tuned for tool selection accuracy.

> **Start every session with `list_collections`.** You need collection IDs to move or file bookmarks, and Raindrop doesn't use predictable names as identifiers.

### Collections

| Tool | What it does |
|---|---|
| `list_collections` | All collections and sub-collections — id, title, parent_id, count |
| `get_collection` | Single collection detail |
| `create_collection` | New collection; pass `parent_id` to nest inside an existing one |
| `update_collection` | Rename, recolour, or toggle public visibility |
| `delete_collection` | Delete a collection — contents move to Unsorted |

### Bookmarks

| Tool | Key parameters | Notes |
|---|---|---|
| `list_raindrops` | `collection_id`, `page`, `per_page`, `sort` | `0` = All, `-1` = Unsorted |
| `get_raindrop` | `raindrop_id` | Full detail: tags, note, type, domain |
| `create_raindrop` | `link`, `collection_id`, `title`, `tags`, `note` | Saves to Unsorted by default |
| `update_raindrop` | `raindrop_id` + any field | Pass `collection_id` to move |
| `move_raindrop` | `raindrop_id`, `target_collection_id` | Explicit move — better tool selection than update |
| `delete_raindrop` | `raindrop_id` | Permanent |

### Bulk Operations

| Tool | What it does |
|---|---|
| `bulk_move_raindrops` | Move a list of bookmark IDs to a target collection |
| `bulk_tag_raindrops` | Apply tags to a list of bookmarks (merges with existing) |
| `bulk_mark_important` | Star or unstar a list of bookmarks |
| `bulk_delete_raindrops` | Permanently delete a list of bookmarks |

### Search

| Tool | Notes |
|---|---|
| `search_raindrops` | Searches all bookmarks by default (`collection_id=0`). Full Raindrop search syntax supported. |

**Search syntax:**

| Syntax | Example | Finds |
|---|---|---|
| Word | `python` | Bookmarks containing "python" |
| Phrase | `"machine learning"` | Exact phrase match |
| Tag | `#ai` | Bookmarks tagged "ai" |
| Type | `type:article` | Articles only (`article`, `video`, `image`, `document`, `audio`) |
| Exclude | `-draft` | Excludes the word "draft" |
| Domain | `site:github.com` | From a specific domain |
| Untagged | `#` | Bookmarks with no tags |
| Unsorted | `collection:unsorted` | Items in Unsorted |
| Starred | `important:true` | Starred / important bookmarks |

### Tags

| Tool | What it does |
|---|---|
| `list_tags` | All tags across your library; pass `collection_id` to scope |
| `rename_tag` | Rename a tag everywhere it appears |
| `delete_tags` | Remove one or more tags from all bookmarks |

---

## Sweep Workflows

Rainkeeper is built for inbox-zero sweeps: work through Unsorted, tag and file everything, leave nothing behind.

```
"List everything in my Unsorted collection and suggest a collection for each."

"Move all bookmarks tagged #read-later to my Reading collection."

"Search for everything tagged #ai from the last 30 days and list titles and URLs."

"Rename the tag 'ai-tools' to 'ai' across my whole library."

"File the 20 most recent bookmarks into the right collections based on their titles."

"Delete everything in Unsorted older than 6 months."
```

---

## Architecture

```
rainkeeper/
├── src/
│   └── rainkeeper/
│       ├── server.py          FastMCP app · registers all tools
│       ├── client.py          RaindropClient · all HTTP lives here
│       ├── config.py          RAINDROP_ACCESS_TOKEN · BASE_URL · headers
│       └── tools/
│           ├── collections.py   5 tools — list · get · create · update · delete
│           ├── raindrops.py     6 tools — list · get · create · update · move · delete
│           ├── bulk.py          4 tools — move · tag · star · delete (batch)
│           ├── search.py        1 tool  — full-text + Raindrop syntax
│           └── tags.py          3 tools — list · rename · delete
├── .env.example               token template — copy to .env, never commit .env
├── pyproject.toml             installable package · rainkeeper CLI entrypoint
└── README.md
```

**Design rule:** `RaindropClient` owns all HTTP. Tools are thin wrappers — no `httpx` in tool files. The API mapping (including the collection move fix) is enforced in one place and testable independently of the MCP layer.

---

## Known Limitations

The following Raindrop.io API capabilities are not yet exposed. Open a [feature request](https://github.com/simonives/rainkeeper/issues/new?template=feature_request.md) if any matter to your workflow, or start an [idea in Discussions](https://github.com/simonives/rainkeeper/discussions).

- **Highlights** — create and read highlights within a bookmark
- **User profile** — `GET /user` (handy for verifying auth is working)
- **Imports / exports** — bulk HTML bookmark import, export to file
- **Sharing** — shared collection management
- **OAuth 2.0** — multi-user auth; currently personal test token only

---

## Contributing

Rainkeeper is maintained by [@simonives](https://github.com/simonives). See [CONTRIBUTING.md](CONTRIBUTING.md) for how to raise bugs, propose features, and fork the project.

---

## License

MIT — see [LICENSE](LICENSE).

---

<div align="center">
<sub>Built with <a href="https://github.com/jlowin/fastmcp">FastMCP</a> · <a href="https://developer.raindrop.io">Raindrop.io REST API v1</a></sub>
</div>
