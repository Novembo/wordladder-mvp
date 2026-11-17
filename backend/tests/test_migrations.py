import os
import sqlite3
import subprocess
import sys
from pathlib import Path


def test_match_uuid_migration_preserves_existing_archive(tmp_path):
    backend = Path(__file__).resolve().parents[1]
    database = tmp_path / "prior-schema.db"
    database_url = f"sqlite+aiosqlite:///{database.as_posix()}"
    environment = os.environ.copy()
    environment.update(
        {
            "WL_DATABASE_URL": database_url,
            "WL_REDIS_ENABLED": "false",
            "PYTHONPATH": str(backend),
        }
    )
    alembic = [
        sys.executable,
        "-m",
        "alembic",
        "-c",
        str(backend / "alembic.ini"),
        "upgrade",
    ]

    subprocess.run(
        [*alembic, "36a7f11c9e02"], cwd=backend, env=environment, check=True
    )
    with sqlite3.connect(database) as connection:
        connection.execute(
            """INSERT INTO match_records
            (id, lang, level, mode, scores, winner, total_moves, created_at,
             finished_at, user_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            ("deadbeef", "en", "basic", "duo", "[1,0]", 0, 4,
             "2026-11-17 00:00:00", "2026-11-17 00:01:00", None),
        )

    subprocess.run([*alembic, "head"], cwd=backend, env=environment, check=True)
    with sqlite3.connect(database) as connection:
        match = connection.execute(
            "SELECT id, scores FROM match_records WHERE id = 'deadbeef'"
        ).fetchone()
        match_id_type = {
            row[1]: row[2] for row in connection.execute("PRAGMA table_info(match_records)")
        }
        move_id_type = {
            row[1]: row[2] for row in connection.execute("PRAGMA table_info(move_records)")
        }

    assert match == ("deadbeef", "[1,0]")
    assert match_id_type["id"] == "VARCHAR(32)"
    assert move_id_type["match_id"] == "VARCHAR(32)"
