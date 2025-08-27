import streamlit as st
from streamlit_modal import Modal
from db_connection import DatabaseConnection

st.set_page_config(page_title="Simulado SAEB", page_icon="🧠", layout="wide")

# Estilo personalizado
try:
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    st.warning("⚠️ Arquivo de estilo não encontrado.")

# Conexão com o banco
db = DatabaseConnection()
db.connect()

if not db.conn:
    st.error("❌ Falha na conexão com o banco.")
    st.stop()

# Inicializa estado do modal
if "show_login_modal" not in st.session_state:
    st.session_state.show_login_modal = "usuario" not in st.session_state

# Função para listar usuários
def listar_usuarios():
    try:
        cursor = db.conn.cursor()
        cursor.execute("SELECT usuario FROM TB_010_USUARIOS ORDER BY usuario")
        return [row[0] for row in cursor.fetchall()]
    except Exception as e:
        st.error(f"Erro ao buscar usuários: {e}")
        return []

# Modal de login
modal = Modal("🔐 Portal de Acesso", key="login_modal", max_width=600)

if st.session_state.show_login_modal:
    modal.open()

if modal.is_open():
    with modal.container():
        usuarios = listar_usuarios()
        usuario = st.selectbox("Usuário", usuarios, key="usuario_modal")
        senha = st.text_input("Senha", type="password", key="senha_modal")

        if st.button("Entrar", key="btn_login_modal"):
            perfil = db.autenticar_usuario(usuario, senha)
            if perfil:
                st.session_state.perfil = perfil
                st.session_state.usuario = usuario
                st.session_state.show_login_modal = False
                st.success(f"✅ Bem-vindo, {usuario}!")
                st.rerun()
            else:
                st.error("❌ Usuário ou senha inválidos.")

# Conteúdo pós-login
if "usuario" in st.session_state:
    try:
        with open("assets/style.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass

    st.title("📚 Gerenciador de Perguntas do Simulado")

    # Estilização da barra lateral
    st.markdown("""
        <style>
            [data-testid="stSidebar"] {
               background: linear-gradient(#000000, #0000004c, #06080075);
               color: white;
               box-shadow: 0 0 10px rgba(0,0,0,0.5);
               padding: 20px;
               border-radius: 10px;
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
               justify-content: flex-start;
               align-items: center;
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
            st.switch_page("pages/gemini.py")
        st.markdown("---")
        st.markdown("## ⚙️   Cadastro")
        if st.button("🗂️   Questões", key="btn_cadastrar"):
            st.switch_page("pages/Cadastrar_Questões.py")
        if st.button("🗂️   Respostas", key="btn_cadastrar_respostas"):
            st.switch_page("pages/Cadastrar_Respostas.py")
        st.markdown("---")

        st.markdown("## 🚪   Sessão")
        if st.button("🚪   Sair", key="btn_logout"):
            for key in ["usuario", "perfil", "show_login_modal"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

        st.markdown("### 📞   Suporte")
        st.write("Email: suporte@meuapp.com")