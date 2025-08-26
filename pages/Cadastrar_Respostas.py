import streamlit as st
from db_connection import DatabaseConnection

# 🔧 Estilo personalizado
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
    st.title("📝 Cadastro de Respostas")
    
# 🎨 Estilização da barra lateral
st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            background-color: #1f2937;
            color: white;
        }
        [data-testid="stSidebar"] h2 {
            color: #10b981;
        }
        [data-testid="stSidebar"] .stButton button {
            background-color: #10b981;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# 🧭 Barra lateral personalizada
with st.sidebar:
    st.markdown("## 🧭 Navegação")
    if st.button("🤖 Ir para Chatbot", key="btn_chatbot"):
        st.switch_page("pages/chatbot.py")
    if st.button("🤖 Ir para Cadastrar_Respostas", key="btn_cadastrar_respostas"):
        st.switch_page("pages/Cadastrar_Respostas.py")
    if st.button("🤖 Ir para Cadastrar_Questões", key="btn_cadastrar"):
        st.switch_page("pages/Cadastrar_Questões.py")
    if st.button("🤖 Ir para Gerar_Simulado", key="btn_simulado"):
        st.switch_page("pages/Gerar_Simulado.py")
    if st.button("🤖 Ir para conn_azure", key="btn_azure"):
        st.switch_page("pages/conn_azure.py")
    if st.button("🤖 Retornar", key="btn_retornar"):
        st.switch_page("gemini.py")

    st.markdown("---")
    st.markdown("## ⚙️ Configurações")
    st.selectbox("Modo de exibição", ["Claro", "Escuro", "Automático"], key="modo_exibicao")
    st.slider("Sensibilidade do modelo", 0.0, 1.0, 0.5, key="sensibilidade")

    st.markdown("---")
    st.markdown("### 📞 Suporte")
    st.write("Email: suporte@meuapp.com")


# 🔌 Conexão com o banco
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