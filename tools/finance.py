from __future__ import annotations

from functools import lru_cache

import yfinance as yf


@lru_cache(maxsize=64)
def _ticker_info(symbole: str) -> dict:
    ticker = yf.Ticker(symbole)
    info = getattr(ticker, "fast_info", None)
    if info is None:
        info = {}
    try:
        history = ticker.history(period="2d", auto_adjust=False)
    except Exception:
        history = None
    return {"ticker": ticker, "history": history, "fast_info": info}


def _format_stock(symbole: str, prix: float, change: float, change_pct: float, volume: int | None) -> str:
    tendance = "📈" if change >= 0 else "📉"
    vol_txt = f" | Volume : {volume:,}" if volume is not None else ""
    return f"{symbole.upper()} {tendance} : {prix:.2f} $ ({change:+.2f}, {change_pct:+.2f}%)" + vol_txt


def obtenir_cours_action(symbole: str) -> str:
    symbole = (symbole or "").strip().upper()
    if not symbole:
        return "Veuillez fournir un symbole d'action valide."
    try:
        payload = _ticker_info(symbole)
        ticker = payload["ticker"]
        history = payload["history"]
        if history is None or history.empty:
            return f"Action '{symbole}' non trouvée ou données indisponibles."
        last = history.tail(2)
        close = float(last["Close"].iloc[-1])
        prev_close = float(last["Close"].iloc[0]) if len(last) > 1 else close
        change = close - prev_close
        change_pct = (change / prev_close * 100) if prev_close else 0.0
        volume = None
        try:
            volume = int(last["Volume"].iloc[-1])
        except Exception:
            volume = None
        return _format_stock(symbole, close, change, change_pct, volume)
    except Exception:
        return f"Erreur lors de la récupération du cours de '{symbole}'."


def obtenir_cours_crypto(symbole: str) -> str:
    symbole = (symbole or "").strip().upper()
    if not symbole:
        return "Veuillez fournir un symbole de crypto valide."
    suffix = "-USD"
    return obtenir_cours_action(symbole + suffix)

