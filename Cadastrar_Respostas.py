import streamlit as st
from db_connection import DatabaseConnection

st.title("📝 Cadastro de Respostas")

db = DatabaseConnection()
db.connect()

# 🔍 Selecionar pergunta existente
perguntas = db.get_perguntas()
pergunta_opcoes = {f"{p['PK_CO_PERGUNTA']} - {p['CO_PERGUNTA'].strip()}": p['PK_CO_PERGUNTA'] for p in perguntas}
pergunta_selecionada = st.selectbox("Pergunta relacionada", list(pergunta_opcoes.keys()))
pergunta_id = pergunta_opcoes[pergunta_selecionada]

# 📋 Listar respostas existentes
respostas = db.get_respostas(pergunta_id)
st.subheader("📋 Respostas cadastradas")
for r in respostas:
    with st.expander(f"ID {r['CO_RESPOSTA']} - {r['NO_RESPOSTA'].strip()}"):
        st.write(f"✔️ Correta: {'Sim' if r['CO_RESPOSTA_CORRETA'] else 'Não'}")
        col1, col2 = st.columns(2)
        with col1:
            if st.button(f"✏️ Editar {r['CO_RESPOSTA']}", key=f"edit_{r['CO_RESPOSTA']}"):
                st.session_state["edit_id"] = r['CO_RESPOSTA']
                st.session_state["edit_texto"] = r['NO_RESPOSTA'].strip()
                st.session_state["edit_correta"] = r['CO_RESPOSTA_CORRETA']
        with col2:
            if st.button(f"❌ Excluir {r['CO_RESPOSTA']}", key=f"del_{r['CO_RESPOSTA']}"):
                db.delete_resposta(r['CO_RESPOSTA'])
                st.success("Resposta excluída com sucesso.")
                st.rerun()

# ➕ Formulário de inserção/edição
st.subheader("➕ Adicionar ou Editar Resposta")
with st.form("form_resposta"):
    id_edicao = st.session_state.get("edit_id", None)
    texto = st.text_input("Texto da Resposta", value=st.session_state.get("edit_texto", ""))
    correta = st.checkbox("É a resposta correta?", value=st.session_state.get("edit_correta", False))
    enviar = st.form_submit_button("💾 Salvar")

if enviar:
    if not texto.strip():
        st.warning("⚠️ O texto da resposta não pode estar vazio.")
    else:
        if id_edicao:
            db.update_resposta(id_edicao, texto, pergunta_id, correta)
            st.success("✅ Resposta atualizada com sucesso!")
            st.session_state["edit_id"] = None
        else:
            db.insert_resposta(texto, pergunta_id, correta)
            st.success("✅ Resposta adicionada com sucesso!")
        st.session_state["edit_texto"] = ""
        st.session_state["edit_correta"] = False
        st.rerun()

db.close()