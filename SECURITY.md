# Security

## Your Raindrop.io token

Rainkeeper authenticates with a **personal test token** from Raindrop.io. This token grants **full read and write access** to your account, including the ability to create, update, and permanently delete bookmarks, collections, and tags. Treat it as you would a password.

### Protect your token

**Never commit your token to version control.**

Rainkeeper's `.gitignore` already excludes `.env`. Before committing to any fork or derived repo, verify your token is not present in any tracked file:

```bash
git grep -r "RAINDROP" -- ':!.env.example' ':!SECURITY.md'
```

If this command returns any output, your token may be exposed.

### Where tokens live

| Location | File | Notes |
|---|---|---|
| Local development | `.env` | Git-ignored. Never commit. |
| Claude Desktop (macOS) | `~/Library/Application Support/Claude/claude_desktop_config.json` | Not in version control, but check before syncing dotfiles |
| Claude Desktop (Windows) | `%APPDATA%\Claude\claude_desktop_config.json` | Same caution applies |
| Claude CLI | `~/.claude.json` | Same caution applies |

If you sync any Claude config files with a backup or dotfile tool, confirm the token is masked or excluded.

### Token scope

Raindrop.io test tokens have no fine-grained permission scoping. There is no read-only option at the token level -- access control is your responsibility. Do not share your token.

### If your token is compromised

1. Go to **Raindrop.io -> Settings -> Integrations -> [your app] -> Regenerate token**
2. Update every location where the old token was stored (`.env`, Claude config files)
3. Check your Raindrop.io library for unexpected changes

Token regeneration is immediate. The old token stops working the moment a new one is issued.

---

## Security practices in the Rainkeeper codebase

| Practice | Implementation |
|---|---|
| No hardcoded secrets | Token read from `RAINDROP_ACCESS_TOKEN` env var only |
| No token in logs or output | `AUTH_HEADER` is set once at config load; never echoed in tool responses |
| No persistent state | Rainkeeper holds no data between tool calls -- thin proxy to the API only |
| Minimal dependencies | FastMCP, httpx, python-dotenv -- no unnecessary attack surface |
| Dependency monitoring | Dependabot watches for security updates weekly |

---

## Reporting a vulnerability in Rainkeeper

If you find a security vulnerability in the Rainkeeper codebase itself, **do not open a public GitHub issue**.

Email **simon@simonives.com** with the subject line `[Rainkeeper Security]`.

Please include:
- A description of the vulnerability
- Steps to reproduce
- Potential impact
- Any suggested fix (optional)

You can expect a response within 48 hours. Confirmed vulnerabilities will be fixed as a priority and credited in the changelog (unless you prefer to remain anonymous).
