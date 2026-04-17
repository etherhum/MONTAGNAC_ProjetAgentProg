from __future__ import annotations

import os
import sqlite3
from pathlib import Path

CLIENTS = [
    ("C001", "Paul Montagnac", "paul.montagnac@epita.fr", "Paris", 15420.50, "Premium", "2026-03-18", 8750.00),
    ("C002", "Jean Marie", None, None, 3200.00, "Standard", None, None),
    ("C003", "Laurence Chalochet", None, None, 28900.00, "VIP", None, None),
    ("C004", "Claire Leroux", None, None, 750.00, "Standard", None, None),
]

PRODUITS = [
    ("P001", "Macbook Pro", 899.00, 45),
    ("P002", "Souris", 49.90, 120),
    ("P003", "Bureau", 350.00, 18),
    ("P004", "Casque", 129.00, 67),
    ("P005", "Écran 4K", 549.00, 30),
]


def get_db_path() -> Path:
    return Path(os.getenv("SQLITE_DB_PATH", "./database.db")).resolve()


def init_db(db_path: Path | None = None) -> Path:
    db_path = db_path or get_db_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id TEXT PRIMARY KEY,
            nom TEXT NOT NULL,
            email TEXT,
            ville TEXT,
            solde_compte REAL NOT NULL,
            type_compte TEXT NOT NULL,
            date_inscription TEXT,
            achats_total REAL
        )
        """)
        conn.execute("""
        CREATE TABLE IF NOT EXISTS produits (
            id TEXT PRIMARY KEY,
            nom TEXT NOT NULL,
            prix_ht REAL NOT NULL,
            stock INTEGER NOT NULL
        )
        """)
        conn.execute("DELETE FROM clients")
        conn.execute("DELETE FROM produits")
        conn.executemany("INSERT INTO clients VALUES (?, ?, ?, ?, ?, ?, ?, ?)", CLIENTS)
        conn.executemany("INSERT INTO produits VALUES (?, ?, ?, ?)", PRODUITS)
        conn.commit()
    return db_path


if __name__ == "__main__":
    path = init_db()
    print(f"Base SQLite init: {path}")