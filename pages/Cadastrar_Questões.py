# app.py
import streamlit as st
from db_connection import DatabaseConnection

st.set_page_config(page_title="🔄 Merge de Perguntas", layout="centered")
st.title("🔄 Atualizar ou Inserir Pergunta no Simulado")

with st.form("form_merge"):
    id_input = st.text_input("ID da pergunta (deixe vazio para inserir nova)", "")
    pergunta_input = st.text_area("Texto da pergunta")
    modulo_input = st.number_input("ID do módulo", min_value=1, step=1)
    enviar = st.form_submit_button("🔁 Executar MERGE")

if enviar:
    if not pergunta_input.strip():
        st.warning("⚠️ A pergunta não pode estar vazia.")
    else:
        db = DatabaseConnection()
        try:
            db.connect()
            db.execute_merge(id_input, pergunta_input, modulo_input)
            st.success("✅ MERGE executado com sucesso!")
        except Exception as erro:
            st.error(f"Erro: {erro}")
        finally:
            db.close()