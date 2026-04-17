# Cet outil effectue des calculs financiers 
# courants : TVA, intérêts composés, marge commerciale, et mensualités de prêt.
# Il accepte des paramètres séparés par des virgules.




def calculer_tva(input_str: str) -> str:
    """Calcule TVA et prix TTC. Entrée : "prix_ht,taux_tva" ex: "100,20" """
    parties = input_str.strip().split(',')
    prix_ht, taux_tva = float(parties[0]), float(parties[1])
    montant_tva = prix_ht * (taux_tva / 100)
    prix_ttc = prix_ht + montant_tva
    return f"HT: {prix_ht:.2f}€  TVA({taux_tva}%): {montant_tva:.2f}€  TTC: {prix_ttc:.2f}€"


def calculer_interets_composes(input_str: str) -> str:
    """Intérêts composés. Entrée : "capital,taux_annuel,duree_annees" """
    c, t, n = input_str.strip().split(',')
    capital, taux, duree = float(c), float(t), int(n)
    capital_final = capital * ((1 + taux/100) ** duree)
    return f"Capital final : {capital_final:,.2f}€ (gain : {capital_final-capital:,.2f}€)"


def calculer_marge(input_str: str) -> str:
    """Marge commerciale. Entrée : "prix_vente,cout_achat" """
    parties = [p.strip() for p in input_str.strip().split(',') if p.strip()]
    if len(parties) < 2:
        return "Entrée invalide. Format attendu : prix_vente,cout_achat"

    pv = parties[0]
    ca = parties[1]

    # Permet de tolérer les entrées du type "1200,prix_achat"
    # en récupérant le coût d'achat dans la valeur absolue si elle est fournie plus tard.
    try:
        prix_vente = float(pv)
    except ValueError:
        return "Entrée invalide. Le prix de vente doit être un nombre."

    try:
        cout_achat = float(ca)
    except ValueError:
        if len(parties) >= 3:
            try:
                cout_achat = float(parties[2])
            except ValueError:
                return "Entrée invalide. Le coût d'achat doit être un nombre."
        else:
            return "Entrée invalide. Le coût d'achat doit être un nombre."

    marge = prix_vente - cout_achat
    taux_marge = (marge / cout_achat) * 100 if cout_achat else 0
    return f"Marge : {marge:.2f}€ | Taux de marge : {taux_marge:.1f}%"


def calculer_mensualite_pret(input_str: str) -> str:
    """Mensualité de prêt. Entrée : "capital,taux_annuel,duree_mois" """
    c, t, d = input_str.strip().split(',')
    K, r, n = float(c), float(t)/100/12, int(d)
    M = K * (r * (1+r)**n) / ((1+r)**n - 1)
    return f"Mensualité : {M:.2f}€/mois | Coût total : {M*n:,.2f}€"
