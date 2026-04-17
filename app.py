from __future__ import annotations

import streamlit as st
from dotenv import load_dotenv
from agent import creer_agent, tools

load_dotenv()
st.set_page_config(page_title="Agent TP", page_icon="💬", layout="wide")
st.title("Agent LangChain TP")

if "agent" not in st.session_state:
    st.session_state.agent = creer_agent()
if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.header("Outils disponibles")
    for tool in tools:
        st.markdown(f"- **{tool.name}** : {tool.description}")
    if st.button("Réinitialiser la conversation"):
        st.session_state.messages = []
        st.session_state.agent = creer_agent()
        st.rerun()

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

question = st.chat_input("Posez votre question ici...")
if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)
    with st.chat_message("assistant"):
        st.write("Réflexion en cours...")
        result = st.session_state.agent.invoke({"input": question})
        answer = result.get("output", "")
        st.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})
