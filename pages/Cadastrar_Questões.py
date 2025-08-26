# app.py
import streamlit as st
from db_connection import DatabaseConnection

st.set_page_config(page_title="📚 CRUD Simulado", layout="wide")
st.title("📚 Gerenciador de Perguntas do Simulado")

db = DatabaseConnection()
db.connect()

# 🔍 Filtro por módulo
modulo_filtro = st.sidebar.number_input("🔎 Filtrar por módulo", min_value=0, step=1)
if modulo_filtro > 0:
    perguntas = db.get_perguntas(modulo_filtro)
else:
    perguntas = db.get_perguntas()

# 📋 Visualização
st.subheader("📋 Perguntas cadastradas")
if perguntas:
    for row in perguntas:
        with st.expander(f"ID {row.id} - Módulo {row.FK_MODULO}"):
            st.write(row.pergunta)
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"✏️ Editar {row.id}"):
                    st.session_state["edit_id"] = row.id
                    st.session_state["edit_pergunta"] = row.pergunta
                    st.session_state["edit_modulo"] = row.FK_MODULO
            with col2:
                if st.button(f"❌ Excluir {row.id}"):
                    db.delete_pergunta(row.id)
                    st.success(f"Pergunta {row.id} excluída.")
                    st.experimental_rerun()
else:
    st.info("Nenhuma pergunta encontrada.")

# ✏️ Formulário de edição/inserção
st.subheader("➕ Adicionar ou Editar Pergunta")
with st.form("form_crud"):
    id_edicao = st.session_state.get("edit_id", None)
    pergunta_input = st.text_area("Pergunta", value=st.session_state.get("edit_pergunta", ""))
    modulo_input = st.number_input("Módulo", min_value=1, step=1, value=st.session_state.get("edit_modulo", 1))
    enviar = st.form_submit_button("💾 Salvar")

if enviar:
    if not pergunta_input.strip():
        st.warning("⚠️ A pergunta não pode estar vazia.")
    else:
        if id_edicao:
            db.update_pergunta(id_edicao, pergunta_input, modulo_input)
            st.success("✅ Pergunta atualizada com sucesso!")
            st.session_state["edit_id"] = None
        else:
            db.insert_pergunta(pergunta_input, modulo_input)
            st.success("✅ Pergunta adicionada com sucesso!")
        st.session_state["edit_pergunta"] = ""
        st.session_state["edit_modulo"] = 1
        st.experimental_rerun()

db.close()