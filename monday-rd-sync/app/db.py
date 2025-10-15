import aiosqlite
import os

SQLITE_PATH = os.getenv("SQLITE_PATH", "/data/state.db")

INIT_SQL = """
CREATE TABLE IF NOT EXISTS processed_items (
  monday_item_id TEXT PRIMARY KEY,
  monday_updated_at TEXT,
  processed_at TEXT DEFAULT (datetime('now'))
);
"""

async def init_db():
    conn = await aiosqlite.connect(SQLITE_PATH)
    await conn.execute(INIT_SQL)
    await conn.commit()
    return conn

async def has_been_processed(conn, item_id: str, updated_at: str) -> bool:
    # Se já vimos o item com o mesmo updated_at, é duplicado
    async with conn.execute(
        "SELECT 1 FROM processed_items WHERE monday_item_id=? AND monday_updated_at=?",
        (item_id, updated_at),
    ) as cur:
        return await cur.fetchone() is not None

async def mark_processed(conn, item_id: str, updated_at: str):
    await conn.execute(
        "INSERT OR REPLACE INTO processed_items (monday_item_id, monday_updated_at) VALUES (?, ?)",
        (item_id, updated_at),
    )
    await conn.commit()
