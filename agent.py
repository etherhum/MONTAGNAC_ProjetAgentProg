from __future__ import annotations

import os

from langchain_classic.tools import Tool
from langchain_openai import ChatOpenAI

from tools.api_publique import convertir_devise, obtenir_taux_du_jour
from tools.calculs import calculer_interets_composes, calculer_marge, calculer_mensualite_pret, calculer_tva
from tools.database import lister_tous_les_clients, rechercher_client, rechercher_produit
from tools.finance import obtenir_cours_action, obtenir_cours_crypto
from tools.portefeuille import calculer_portefeuille
from tools.recommandation import recommander_produits
from tools.text import convertir_majuscules_minuscules, extraire_mots_cles, formater_rapport, resumer_texte


# ATTENTION SECURITE : cet outil exécute du code arbitraire.
# Ne jamais l'utiliser en production sans sandbox, contrôle d'accès et limites strictes.
python_repl = None
try:
    from langchain_experimental.tools import PythonREPLTool

    python_repl = PythonREPLTool()
    python_repl.description = (
        "Exécute du code Python pour des calculs complexes ou traitements de données non couverts par les autres outils. "
        "Entrée : code Python valide sous forme de chaîne."
    )
except Exception:
    python_repl = None


tools = [
    Tool(name="rechercher_client", func=rechercher_client,
         description="Recherche un client par nom ou ID (ex: C001). Retourne solde, type de compte, historique achats."),
    Tool(name="rechercher_produit", func=rechercher_produit,
         description="Recherche un produit par nom ou ID. Retourne prix HT, TVA, prix TTC, stock."),
    Tool(name="lister_tous_les_clients", func=lister_tous_les_clients,
         description="Liste tous les clients de la base de données."),
    Tool(name="cours_action", func=obtenir_cours_action,
         description="Cours boursier réel d'une action. Entrée : symbole ex AAPL, MSFT, TSLA, LVMH, AIR."),
    Tool(name="cours_crypto", func=obtenir_cours_crypto,
         description="Cours réel d'une crypto. Entrée : symbole ex BTC, ETH, SOL, BNB, DOGE."),
    Tool(name="calculer_tva", func=calculer_tva,
         description="Calcule TVA et prix TTC. Entrée : prix_ht,taux ex 100,20."),
    Tool(name="calculer_interets", func=calculer_interets_composes,
         description="Intérêts composés. Entrée : capital,taux_annuel,années ex 10000,5,3."),
    Tool(name="calculer_marge", func=calculer_marge,
         description="Marge commerciale. Entrée : prix_vente,cout_achat ex 150,80."),
    Tool(name="calculer_mensualite", func=calculer_mensualite_pret,
         description="Mensualité prêt. Entrée : capital,taux_annuel,mois ex 200000,3.5,240."),
    Tool(name="convertir_devise", func=convertir_devise,
         description="Conversion de devises en temps réel. Entrée : montant,DEV_SOURCE,DEV_CIBLE ex 100,USD,EUR."),
    Tool(name="taux_du_jour", func=obtenir_taux_du_jour,
         description="Affiche les taux de change du jour pour une devise base. Entrée : EUR, USD, GBP..."),
    Tool(name="resumer_texte", func=resumer_texte,
         description="Résume un texte et donne des statistiques. Entrée : texte complet."),
    Tool(name="formater_rapport", func=formater_rapport,
         description="Formate en rapport. Entrée : Cle1:Val1|Cle2:Val2."),
    Tool(name="extraire_mots_cles", func=extraire_mots_cles,
         description="Extrait les mots-clés d'un texte. Entrée : texte complet."),
    Tool(name="convertir_casse", func=convertir_majuscules_minuscules,
         description="Transforme la casse d'un texte. Entrée : mode,texte."),
    Tool(name="recommander_produits", func=recommander_produits,
         description="Recommandations produits. Entrée : budget,categorie,type_compte ex 300,Informatique,Premium."),
    Tool(name="calculer_portefeuille", func=calculer_portefeuille,
         description="Calcule la valeur d'un portefeuille. Entrée : SYMBOLE:QUANTITE|SYMBOLE:QUANTITE."),
]

if python_repl is not None:
    tools.append(python_repl)

try:
    from langchain_community.tools import TavilySearchResults

    tools.append(TavilySearchResults(max_results=3))
except Exception:
    pass


def creer_agent():
    """Crée et retourne un agent LangChain configuré."""
    from langchain_classic.agents import AgentExecutor, create_openai_tools_agent
    from langchain_classic import hub
    from langchain_classic.memory import ConversationBufferMemory

    llm = ChatOpenAI(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        temperature=0,
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    prompt = hub.pull("hwchase17/openai-tools-agent")
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    agent = create_openai_tools_agent(llm=llm, tools=tools, prompt=prompt)
    return AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        max_iterations=10,
        handle_parsing_errors=True,
        memory=memory,
    )


def interroger_agent(agent, question: str):
    print(f"\n{'='*60}")
    print(f"Question : {question}")
    print('='*60)
    result = agent.invoke({"input": question})
    print(f"\nRéponse finale : {result['output']}")
    return result

