# app.py
import streamlit as st
from db_connection import DatabaseConnection

# 🔧 Estilo personalizado
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.set_page_config(page_title="📚 CRUD Simulado", layout="wide")
st.title("📚 Gerenciador de Perguntas do Simulado")

# Estilização da barra lateral
st.markdown("""
    <style>
        [data-testid="stSidebar"] {
           background: linear-gradient( #000000, #0000004c, #06080075);
           color: white;
           box-shadow: 0 0 10px rgba(0,0,0,0.5);
           padding: 20px;
           border-radius: 10px;
        }
       
        [data-testid="stSidebar"] {
           height: 100vh;
        overflow-y: auto;
}

        [data-testid="stSidebar"] h2 {
            color: #10b981;
        }
        [data-testid="stSidebar"] .stButton button {
           background-color: #0000004c;
           color: rgba(245, 245, 245, 0.849);
           text-align: left;
           padding-left: 12px;
           width: 240px;
           height: 40px;
           border: none;
           border-radius: 8px;
           font-size: 18px;
           font-weight: bold;
           box-shadow: 0 4px 6px rgba(0,0,0,0.1);
           cursor: pointer;
           transition: background-color 0.3s ease-in-out;
           display: flex;
           justify-content: flex-start;   /* Alinha conteúdo à esquerda */
           align-items: center;           /* Centraliza verticalmente */
           padding-left: 12px;            /* Espaço interno à esquerda */
           text-align: left;              /* Redundante, mas seguro */
        }
    </style>
""", unsafe_allow_html=True)

# 🧭 Barra lateral personalizada
with st.sidebar:
    st.markdown("## 🧭 Navegação")
    if st.button("🎓   Chatbot", key="btn_chatbot"):
       st.switch_page("pages/chatbot.py")
    if st.button("🖥️   Gerar Simulado", key="btn_simulado"):
        st.switch_page("pages/Gerar_Simulado.py")
    if st.button("✅   Teste de Conexão", key="btn_azure"):
        st.switch_page("pages/conn_azure.py")
    if st.button("↩️   Retornar", key="btn_retornar"):
        st.switch_page("gemini.py")
    st.markdown("---")
    st.markdown("## ⚙️   Cadastro")
    if st.button("🗂️   Questões", key="btn_cadastrar"):
        st.switch_page("pages/Cadastrar_Questões.py")
    if st.button("🗂️   Respostas", key="btn_cadastrar_respostas"):
        st.switch_page("pages/Cadastrar_Respostas.py")
        st.markdown("---")
    
    st.markdown("---")
    st.markdown("### 📞   Suporte")
    st.write("Email: suporte@meuapp.com")

# 🔌 Conexão com o banco
db = DatabaseConnection()
db.connect()

# 🔍 Filtro por módulo
modulo_filtro = st.sidebar.number_input("🔎 Filtrar por módulo", min_value=0, step=1, key="modulo_filtro")
if modulo_filtro > 0:
    perguntas = db.get_perguntas(modulo_filtro)
else:
    perguntas = db.get_perguntas()

# 📋 Visualização das perguntas
st.subheader("📋 Perguntas cadastradas")

if perguntas and len(perguntas) > 0:
   for row in perguntas:
    codigo = row['CO_PERGUNTA']
    descricao = row['DE_PERGUNTA']

    codigo_formatado = codigo.strip() if codigo else "Sem código"
    descricao_formatada = descricao.strip() if descricao else "Sem descrição"

    with st.expander(f"ID {row['PK_CO_PERGUNTA']} - Código {codigo_formatado}"):
        st.write(descricao_formatada)
        col1, col2 = st.columns(2)
        with col1:
            if st.button(f"✏️ Editar {row['PK_CO_PERGUNTA']}", key=f"editar_{row['PK_CO_PERGUNTA']}"):
                st.session_state["edit_id"] = row['PK_CO_PERGUNTA']
                st.session_state["edit_codigo"] = codigo_formatado
                st.session_state["edit_descricao"] = descricao_formatada
        with col2:
            if st.button(f"❌ Excluir {row['PK_CO_PERGUNTA']}", key=f"excluir_{row['PK_CO_PERGUNTA']}"):
                db.delete_pergunta(row['PK_CO_PERGUNTA'])
                st.success(f"Pergunta {row['PK_CO_PERGUNTA']} excluída.")
                st.rerun()
else:
    st.warning("⚠️ Nenhuma pergunta encontrada para o filtro atual.")

# ➕ Formulário de edição/inserção
st.subheader("➕ Adicionar ou Editar Pergunta")
with st.form("form_crud"):
    id_edicao = st.session_state.get("edit_id", None)
    codigo_input = st.text_input("Pergunta", value=st.session_state.get("edit_codigo", ""))
    descricao_input = st.text_area("Texto", value=st.session_state.get("edit_descricao", ""))
    
    enviar = st.form_submit_button("💾 Salvar")

if enviar:
    if not codigo_input.strip() or not descricao_input.strip():
        st.warning("⚠️ Código e descrição não podem estar vazios.")
    else:
        if id_edicao:
            db.update_pergunta(id_edicao, codigo_input, descricao_input)
            st.success("✅ Pergunta atualizada com sucesso!")
            st.session_state["edit_id"] = None
        else:
            db.insert_pergunta(codigo_input, descricao_input)
            st.success("✅ Pergunta adicionada com sucesso!")
        st.session_state["edit_codigo"] = ""
        st.session_state["edit_descricao"] = ""
        st.rerun()

# 🔒 Encerrando conexão
db.close()