from __future__ import annotations
from dataclasses import dataclass
import yfinance as yf


@dataclass
class LignePortefeuille:
    symbole: str
    quantite: float
    prix: float
    valeur: float
    variation_jour: float


def _fetch_price(symbole: str) -> tuple[float, float, float]:
    ticker = yf.Ticker(symbole)
    history = ticker.history(period="2d", auto_adjust=False)
    if history.empty:
        raise ValueError(f"Symbole invalide ou données indisponibles: {symbole}")
    close = float(history["Close"].iloc[-1])
    prev_close = float(history["Close"].iloc[0]) if len(history) > 1 else close
    variation = close - prev_close
    return close, prev_close, variation


def calculer_portefeuille(input_str: str) -> str:
    input_str = (input_str or "").strip()
    if not input_str:
        return "Format attendu : 'SYMBOLE:QUANTITE|SYMBOLE:QUANTITE'"

    lignes: list[LignePortefeuille] = []
    total = 0.0
    variation_totale = 0.0
    for item in input_str.split("|"):
        if ":" not in item:
            return "Format attendu : 'SYMBOLE:QUANTITE|SYMBOLE:QUANTITE'"
        symbole, quantite_txt = item.split(":", 1)
        symbole = symbole.strip().upper()
        try:
            quantite = float(quantite_txt.strip())
        except ValueError:
            return f"Quantité invalide pour {symbole}: {quantite_txt}"
        try:
            prix, prev_close, variation = _fetch_price(symbole)
        except Exception as exc:
            return str(exc)
        valeur = prix * quantite
        lignes.append(LignePortefeuille(symbole, quantite, prix, valeur, variation * quantite))
        total += valeur
        variation_totale += variation * quantite

    variation_pct = (variation_totale / (total - variation_totale) * 100) if (total - variation_totale) else 0.0
    result = ["Portefeuille :"]
    for ligne in lignes:
        result.append(
            f"  {ligne.symbole} x {ligne.quantite:g} | Cours : {ligne.prix:.2f} $ | Valeur : {ligne.valeur:.2f} $"
        )
    result.append(f"Valeur totale : {total:.2f} $")
    result.append(f"Variation globale du jour : {variation_totale:+.2f} $ ({variation_pct:+.2f}%)")
    return "\n".join(result)
