from __future__ import annotations

import os
import sqlite3
from pathlib import Path

DB_PATH = Path(os.getenv("SQLITE_DB_PATH", "./database.db")).resolve()


def _connect() -> sqlite3.Connection:
    return sqlite3.connect(DB_PATH)


def _format_client_row(row) -> str:
    client_id, nom, email, ville, solde_compte, type_compte, date_inscription, achats_total = row
    parts = [f"Client : {nom}", f"ID : {client_id}", f"Solde : {solde_compte:.2f} €", f"Type de compte : {type_compte}"]
    if email:
        parts.append(f"Email : {email}")
    if ville:
        parts.append(f"Ville : {ville}")
    if date_inscription:
        parts.append(f"Inscription : {date_inscription}")
    if achats_total is not None:
        parts.append(f"Achats total : {achats_total:.2f} €")
    return " | ".join(parts)


def _format_produit_row(row) -> str:
    produit_id, nom, prix_ht, stock = row
    tva = prix_ht * 0.20
    prix_ttc = prix_ht + tva
    return (
        f"Produit : {nom} | ID : {produit_id} | Prix HT : {prix_ht:.2f} € | TVA : {tva:.2f} € "
        f"| Prix TTC : {prix_ttc:.2f} € | Stock : {stock}"
    )


def rechercher_client(query: str) -> str:
    query = (query or "").strip()
    if not query:
        return "Veuillez fournir un nom ou un identifiant de client."
    with _connect() as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        row = cur.execute(
            """
            SELECT id, nom, email, ville, solde_compte, type_compte, date_inscription, achats_total
            FROM clients
            WHERE UPPER(id) = UPPER(?) OR LOWER(nom) LIKE LOWER(?)
            LIMIT 1
            """,
            (query, f"%{query}%"),
        ).fetchone()
        if row:
            return _format_client_row(tuple(row))
    return f"Aucun client trouvé pour : '{query}'"


def rechercher_produit(query: str) -> str:
    query = (query or "").strip()
    if not query:
        return "Veuillez fournir un nom ou un identifiant de produit."
    with _connect() as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        row = cur.execute(
            """
            SELECT id, nom, prix_ht, stock
            FROM produits
            WHERE UPPER(id) = UPPER(?) OR LOWER(nom) LIKE LOWER(?)
            LIMIT 1
            """,
            (query, f"%{query}%"),
        ).fetchone()
        if row:
            return _format_produit_row(tuple(row))
    return f"Aucun produit trouvé pour : '{query}'"


def lister_tous_les_clients(query: str = "") -> str:
    with _connect() as conn:
        cur = conn.cursor()
        rows = cur.execute("SELECT id, nom, email, ville, solde_compte, type_compte, date_inscription, achats_total FROM clients ORDER BY id").fetchall()
    lignes = ["Liste des clients :"]
    for row in rows:
        lignes.append(f"  {row[0]} : {row[1]} | {row[5]} | Solde : {row[4]:.2f} €")
    return "\n".join(lignes)

