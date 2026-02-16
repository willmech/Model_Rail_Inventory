from __future__ import annotations

import sqlite3
from pathlib import Path

DB_FILENAME = "inventory.db"


def get_repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def get_data_dir() -> Path:
    data_dir = get_repo_root() / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir


def get_images_dir() -> Path:
    img_dir = get_data_dir() / "images"
    (img_dir / "locomotives").mkdir(parents=True, exist_ok=True)
    (img_dir / "rolling_stock").mkdir(parents=True, exist_ok=True)
    return img_dir


def get_db_path() -> Path:
    return get_data_dir() / DB_FILENAME


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(get_db_path())
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def _column_exists(conn: sqlite3.Connection, table: str, column: str) -> bool:
    rows = conn.execute(f"PRAGMA table_info({table});").fetchall()
    return any(r["name"] == column for r in rows)


def _migrate_locomotives(conn: sqlite3.Connection) -> None:
    # Add columns safely for existing DBs
    if not _column_exists(conn, "locomotives", "model_manufacturer"):
        conn.execute("ALTER TABLE locomotives ADD COLUMN model_manufacturer TEXT;")
    if not _column_exists(conn, "locomotives", "prototype_manufacturer"):
        conn.execute("ALTER TABLE locomotives ADD COLUMN prototype_manufacturer TEXT;")
    if not _column_exists(conn, "locomotives", "control_type"):
        conn.execute(
            "ALTER TABLE locomotives ADD COLUMN control_type TEXT NOT NULL DEFAULT 'DC';"
        )
    if not _column_exists(conn, "locomotives", "decoder_id"):
        conn.execute("ALTER TABLE locomotives ADD COLUMN decoder_id TEXT;")

    # Enforce rule: DC should not have decoder_id
    conn.execute("UPDATE locomotives SET decoder_id = NULL WHERE control_type = 'DC';")


def initialize_database() -> None:
    # Ensure folders exist (DB + images)
    get_images_dir()

    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS locomotives (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                road_name TEXT NOT NULL,
                locomotive_number TEXT NOT NULL,
                model_manufacturer TEXT,
                prototype_manufacturer TEXT,
                control_type TEXT NOT NULL DEFAULT 'DC',
                decoder_id TEXT,
                horsepower INTEGER,
                notes TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            );
            """
        )

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS locomotive_photos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                locomotive_id INTEGER NOT NULL,
                file_path TEXT NOT NULL,
                caption TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(locomotive_id) REFERENCES locomotives(id) ON DELETE CASCADE
            );
            """
        )

        # Rolling stock table placeholder (we’ll build later)
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS rolling_stock (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL,
                notes TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            );
            """
        )

        _migrate_locomotives(conn)
