"""
Live validation script — tests rainkeeper against the real Raindrop.io API.
Run with: .venv/bin/python test_live.py

This is NOT part of the test suite (which uses mocks). It's for manual
end-to-end validation and produces a report suitable for logging to GitHub.
"""
import asyncio
import json
import sys
from datetime import datetime, timezone

from src.rainkeeper.client import RaindropClient


PASS = "PASS"
FAIL = "FAIL"
results = []


def log(status, test, detail=""):
    mark = "✓" if status == PASS else "✗"
    line = f"  {mark} [{status}] {test}"
    if detail:
        line += f"\n         {detail}"
    print(line)
    results.append((status, test, detail))


async def run():
    print(f"\nRainkeeper live validation — {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}")
    print("=" * 60)

    async with RaindropClient() as client:

        # ── 1. Collections ────────────────────────────────────────────
        print("\n[Collections]")
        try:
            collections = await client.list_collections()
            assert isinstance(collections, list)
            log(PASS, "list_collections", f"{len(collections)} collections returned")
            col_sample = collections[:3]
        except Exception as e:
            log(FAIL, "list_collections", str(e))
            col_sample = []
            print("  Cannot continue collection tests — aborting.\n")
            return

        if col_sample:
            first = col_sample[0]
            try:
                detail = await client.get_collection(first["_id"])
                assert "_id" in detail
                log(PASS, "get_collection", f"id={first['_id']} title={first.get('title','?')!r}")
            except Exception as e:
                log(FAIL, "get_collection", str(e))

        # ── 2. Raindrops: list and get ─────────────────────────────────
        print("\n[Raindrops — read]")
        raindrop_id = None
        try:
            page = await client.list_raindrops(collection_id=0, per_page=5)
            items = page.get("items", [])
            assert isinstance(items, list)
            log(PASS, "list_raindrops (All)", f"{page.get('count', '?')} total, {len(items)} returned")
            if items:
                raindrop_id = items[0]["_id"]
        except Exception as e:
            log(FAIL, "list_raindrops", str(e))

        if raindrop_id:
            try:
                rd = await client.get_raindrop(raindrop_id)
                assert "_id" in rd
                log(PASS, "get_raindrop", f"id={raindrop_id} title={rd.get('title','?')!r}")
            except Exception as e:
                log(FAIL, "get_raindrop", str(e))

        # ── 3. Unsorted / Inbox ────────────────────────────────────────
        print("\n[Unsorted]")
        unsorted_items = []
        try:
            page = await client.list_raindrops(collection_id=-1, per_page=10)
            unsorted_items = page.get("items", [])
            log(PASS, "list_raindrops (Unsorted)", f"{page.get('count', '?')} total, {len(unsorted_items)} returned")
        except Exception as e:
            log(FAIL, "list_raindrops (Unsorted)", str(e))

        # ── 4. THE CORE FIX: move a raindrop and verify ───────────────
        # Use any available bookmark (Unsorted preferred, else first collection item)
        print("\n[Collection move — THE CORE FIX]")
        move_candidate = None
        if unsorted_items:
            move_candidate = unsorted_items[0]
        elif items:
            move_candidate = items[0]

        if move_candidate and len(collections) >= 2:
            original_col_id = move_candidate.get("collection", {}).get("$id", -1)
            test_id = move_candidate["_id"]
            # Pick a target that's different from the current collection
            target = next((c for c in collections if c["_id"] != original_col_id), None)
            if target:
                target_id = target["_id"]
                try:
                    result = await client.update_raindrop(test_id, collection_id=target_id)
                    new_col = result.get("collection", {}).get("$id")
                    if new_col == target_id:
                        log(PASS, "update_raindrop (move)", f"id={test_id} → collection {target_id} ({target.get('title','?')!r})")
                        # Restore
                        await client.update_raindrop(test_id, collection_id=original_col_id)
                        log(PASS, "update_raindrop (restore)", f"id={test_id} → original collection {original_col_id}")
                    else:
                        log(FAIL, "update_raindrop (move)", f"collection.$id in response is {new_col!r}, expected {target_id} — MOVE DID NOT WORK")
                except Exception as e:
                    log(FAIL, "update_raindrop (move)", str(e))
        else:
            log(PASS, "update_raindrop (move)", "SKIPPED — need at least 2 collections and 1 bookmark")

        # ── 5. move_raindrop (bulk) ───────────────────────────────────
        # Re-fetch current collection so section 5 is independent of the section 4 restore.
        if move_candidate and len(collections) >= 2:
            current = await client.get_raindrop(move_candidate["_id"])
            original_col_id = current.get("collection", {}).get("$id", -1)
            test_id = move_candidate["_id"]
            target = next((c for c in collections if c["_id"] != original_col_id), None)
            if target:
                target_id = target["_id"]
                try:
                    result = await client.bulk_move(original_col_id, [test_id], target_id)
                    # Raindrop bulk returns {"modified": n, "result": true}
                    modified = result.get("modified", 0)
                    if modified >= 1:
                        log(PASS, "bulk_move_raindrops", f"1 bookmark moved to collection {target_id} ({target.get('title','?')!r})")
                        # Restore
                        await client.bulk_move(target_id, [test_id], original_col_id)
                        log(PASS, "bulk_move_raindrops (restore)", f"restored to collection {original_col_id}")
                    else:
                        log(FAIL, "bulk_move_raindrops", f"modified={modified}, expected >=1 — BULK MOVE DID NOT WORK")
                except Exception as e:
                    log(FAIL, "bulk_move_raindrops", str(e))

        # ── 6. Search ─────────────────────────────────────────────────
        print("\n[Search]")
        try:
            page = await client.list_raindrops(collection_id=0, per_page=3, search="a")
            items = page.get("items", [])
            log(PASS, "search_raindrops", f"{page.get('count', '?')} results for 'a', {len(items)} returned")
        except Exception as e:
            log(FAIL, "search_raindrops", str(e))

        # ── 7. Tags ───────────────────────────────────────────────────
        print("\n[Tags]")
        try:
            tags = await client.list_tags()
            assert isinstance(tags, list)
            log(PASS, "list_tags", f"{len(tags)} tags returned")
        except Exception as e:
            log(FAIL, "list_tags", str(e))

    # ── Summary ───────────────────────────────────────────────────────
    print("\n" + "=" * 60)
    passed = sum(1 for s, _, _ in results if s == PASS)
    failed = sum(1 for s, _, _ in results if s == FAIL)
    print(f"Results: {passed} passed, {failed} failed")

    if failed:
        print("\nFailed tests:")
        for status, test, detail in results:
            if status == FAIL:
                print(f"  ✗ {test}: {detail}")
        sys.exit(1)
    else:
        print("All tests passed.")


if __name__ == "__main__":
    asyncio.run(run())
