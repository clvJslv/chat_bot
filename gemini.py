import streamlit as st
from db_connection import DatabaseConnection

# Estilo externo
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Configuração da página
st.set_page_config(page_title="Simulado SAEB", page_icon="🧠", layout="wide")

# Conexão com banco
db = DatabaseConnection()
db.connect()

if not db.conn:
    st.error("❌ Conexão com o banco falhou.")
    st.stop()

# Estilo adicional
st.markdown("""
    <style>
        .login-title {
            font-size: 24px;
            font-weight: bold;
            text-align: center;
            margin-bottom: 20px;
            color: #10b981;
        }

        div[data-testid="stSelectbox"] {
            width: 220px;
            margin-bottom: 10px;
        }

        div[data-testid="stSelectbox"] label {
            color: #10b981;
            font-weight: bold;
        }

        div[data-testid="stSelectbox"] .stSelectbox {
            background-color: #f9fafb;
            border: 2px solid #10b981;
            border-radius: 6px;
            padding: 6px 10px;
            color: #111827;
        }

        div[data-testid="stTextInput"] input {
            width: 220px;
            height: 32px;
            padding: 6px 10px;
            font-size: 14px;
            border: 2px solid #3b82f6;
            border-radius: 6px;
            background-color: #f3f4f6;
            color: #111827;
        }
    </style>
""", unsafe_allow_html=True)

# Se já estiver logado
if "perfil" in st.session_state:
    if st.button("🚪  Logout"):
        del st.session_state["perfil"]
        del st.session_state["usuario"]
        st.rerun()
else:
    st.markdown("<div class='login-title'>Login</div>", unsafe_allow_html=True)

    # Listar usuários cadastrados
    usuarios_cadastrados = db.listar_usuarios()

    if usuarios_cadastrados:
        usuario = st.selectbox("Selecione o usuário", usuarios_cadastrados)
        senha = st.text_input("Senha", type="password")

        if st.button("Entrar"):
            perfil = db.autenticar_usuario(usuario, senha)
            if perfil:
                st.session_state.perfil = perfil
                st.session_state.usuario = usuario
                st.success("✅ Login realizado com sucesso!")
                st.rerun()
            else:
                st.error("❌ Usuário ou senha inválidos.")
    else:
        st.warning("Nenhum usuário cadastrado no sistema.")

# Menu lateral
if "perfil" in st.session_state:
    perfil = st.session_state.perfil
    st.sidebar.markdown("## 🧭 Navegação")

    if st.sidebar.button("🎓   Chatbot"):
        st.switch_page("pages/chatbot.py")
    if st.sidebar.button("🖥️   Gerar Simulado"):
        st.switch_page("pages/Gerar_Simulado.py")
    if perfil == "Administrador" and st.sidebar.button("✅   Teste de Conexão"):
        st.switch_page("pages/conn_azure.py")
    if st.sidebar.button("↩️   Retornar"):
        st.switch_page("gemini.py")

    st.sidebar.markdown("---")
    st.sidebar.markdown("## ⚙️   Cadastro")

    if perfil in ["Professor", "Administrador"]:
        if st.sidebar.button("🗂️   Questões"):
            st.switch_page("pages/Cadastrar_Questões.py")
        if st.sidebar.button("🗂️   Respostas"):
            st.switch_page("pages/Cadastrar_Respostas.py")

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📞   Suporte")
    st.sidebar.write("Email: suporte@meuapp.com")

    st.markdown(f"### 👋 Olá, {st.session_state.usuario}! Você está logado como **{perfil}**.")

# Conteúdo principal
st.markdown("<h1 style='text-align: center; color: #4B8BBE;'>🎒 Aplicação para Avaliação de Alunos</h1>", unsafe_allow_html=True)

with st.expander("ℹ️ Sobre este portal"):
    st.markdown("""
        Este é um aplicativo que utiliza IA com consultas ao chatbot (GEMINI) para gerar simulados de acordo com descritores,
        apresentando sugestões de conteúdo para estudo das questões respondidas de forma errada.

        - 📚 [Documentação oficial do Streamlit](https://docs.streamlit.io/)
        - 🐞 [Reportar falhas ou bugs](https://github.com/streamlit/streamlit/issues)
    """)

st.divider()
st.markdown("### 🧪 Bem-vindo ao APP Simulado assistido por IA")
