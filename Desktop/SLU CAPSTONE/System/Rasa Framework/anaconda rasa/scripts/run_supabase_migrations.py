#!/usr/bin/env python3
"""Run Supabase/Postgres SQL migration files from the local repo.

Usage:
    set DATABASE_URL=postgresql://...
    python scripts/run_supabase_migrations.py

Optional:
    python scripts/run_supabase_migrations.py scripts/create_rasa_trackers_table.sql
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import psycopg2


ROOT = Path(__file__).resolve().parent
DEFAULT_MIGRATIONS = [
    ROOT / "create_chat_history_tables.sql",
    ROOT / "create_rasa_trackers_table.sql",
    ROOT / "create_counseling_requests_table.sql",
]


def load_sql(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def run_migrations(database_url: str, migration_paths: list[Path]) -> None:
    with psycopg2.connect(database_url) as conn:
        conn.autocommit = False
        with conn.cursor() as cur:
            for path in migration_paths:
                print(f"[MIGRATE] Running {path.name}")
                cur.execute(load_sql(path))
        conn.commit()


def main() -> int:
    database_url = os.getenv("DATABASE_URL") or os.getenv("SUPABASE_DB_URL")
    if not database_url:
        print(
            "[ERROR] Set DATABASE_URL or SUPABASE_DB_URL to your Supabase Postgres connection string."
        )
        return 1

    paths = [Path(arg).resolve() for arg in sys.argv[1:]] if len(sys.argv) > 1 else DEFAULT_MIGRATIONS

    missing = [str(path) for path in paths if not path.exists()]
    if missing:
        print("[ERROR] Missing migration file(s):")
        for path in missing:
            print(f"  - {path}")
        return 1

    try:
        run_migrations(database_url, paths)
    except Exception as exc:
        print(f"[ERROR] Migration failed: {exc}")
        return 1

    print("[OK] Migrations completed successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
