# AGENTS.md — Rainkeeper

Rainkeeper is Simon's own open-source MCP server for Raindrop.io, described here for any agentic coding tool operating on this repo. It fixes two bugs in existing community alternatives: it works on free Raindrop accounts (the official MCP requires Pro), and collection moves actually work (correct `{"collection": {"$id": n}}` request body format). MIT licence.

**Language:** Python
**Framework:** FastMCP
**Repo:** `~/git/rainkeeper`
**Registered as:** `rainkeeper` in Claude Desktop and CLI (`mcp__rainkeeper__` tool prefix)

## Scope
This repo's delta over generic Python/FastMCP competence: the Raindrop-specific API bug fixes, and the mandatory Superpowers development methodology for this project. Generic Python/FastMCP/MCP-server knowledge is assumed, not repeated.

## Precedence
This file is authoritative for all rainkeeper work — no parent AGENTS.md exists inside this repo. Global developer and tool conventions apply where not overridden here; this file overrides defaults on rainkeeper-specific technical and process matters (e.g. mandatory TDD) regardless of recency.

## Instructions

**Commands:**
- Branch naming: `feat/`, `fix/`, `docs/`, `chore/`. All work on a feature branch, PR into `main` — never commit directly to `main`.
- Mandatory workflow for any new feature or significant change: `/brainstorming` (before any implementation, no exceptions for perceived simplicity) → `/writing-plans` (plan written to `docs/superpowers/specs/` and committed before coding) → `/test-driven-development` (no production code without a failing test first) → `/verification-before-completion` (before marking any task done) → `/finishing-a-development-branch` (before raising a PR).
- For bug fixes: write the failing test that reproduces the bug first, then fix. No exception.

**Conventions:**
- Always call `list_collections` first in any Raindrop session — all move/file operations require numeric collection IDs, not names.
- The Superpowers plugin methodology (referenced via `/brainstorming`, `/writing-plans`, `/test-driven-development`, `/verification-before-completion`, `/finishing-a-development-branch`) is mandatory for all work on this project.

## Negatives
Never skip a Superpowers hard gate without explicit instruction from Simon. Never write production code before a failing test exists — delete any code written before tests existed and start fresh, no exceptions. Exception: throwaway spikes for exploration/prototyping are exempt from TDD, but must be deleted before production implementation begins — do not adapt spike code into production code.

## Expiry
The critical Raindrop API fix (`{"collection": {"$id": n}}` required for moves; `{"collectionId": n}` returns 200 OK but silently does nothing) and the 19-tool count across collections/raindrops/bulk-operations/search/tags — owner: Simon, last-verified: 2026-07-25, refresh interval: whenever Raindrop's API changes or tools are added/removed. Connects to Simon's Raindrop.io account (`simon-ives-au`).

---
[[Rainkeeper]] · [[Side Projects CLAUDE]]
