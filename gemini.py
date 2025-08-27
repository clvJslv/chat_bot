import streamlit as st
from db_connection import DatabaseConnection

# 🔌 Conexão com o banco
db = DatabaseConnection()
conn = db.connect()

# 🎨 Estilo customizado
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ⚙️ Configuração da página
st.set_page_config(
    page_title="Simulado SAEB",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 🔐 Autenticação
def autenticar_usuario(usuario, senha):
    cursor = conn.cursor()
    cursor.execute("SELECT perfil FROM usuarios WHERE usuario=? AND senha=?", (usuario, senha))
    resultado = cursor.fetchone()
    return resultado[0] if resultado else None

# 🧾 Login
st.title("🔐 Portal de Autenticação")
usuario = st.text_input("Usuário")
senha = st.text_input("Senha", type="password")

if st.button("Entrar"):
    perfil = autenticar_usuario(usuario, senha)
    if perfil:
        st.success(f"Bem-vindo, {usuario} ({perfil})")
        st.session_state.perfil = perfil
        st.session_state.usuario = usuario
    else:
        st.error("Usuário ou senha inválidos")

# 🧭 Menu lateral baseado na matriz
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

    # 👋 Saudação
    st.markdown(f"### 👋 Olá, {st.session_state.usuario}! Você está logado como **{perfil}**.")

# 🧠 Conteúdo principal
st.markdown(
    "<h1 style='text-align: center; color: #4B8BBE;'>🎒 Aplicação para Avaliação de Alunos</h1>",
    unsafe_allow_html=True
)

with st.expander("ℹ️ Sobre este portal"):
    st.markdown("""
        Este é um aplicativo que utiliza IA com consultas ao chatbot (GEMINI) para gerar simulados de acordo com descritores,
        apresentando sugestões de conteúdo para estudo das questões respondidas de forma errada.

        - 📚 [Documentação oficial do Streamlit](https://docs.streamlit.io/)
        - 🐞 [Reportar falhas ou bugs](https://github.com/streamlit/streamlit/issues)
    """)

st.divider()
st.markdown("### 🧪 Bem-vindo ao APP Simulado assistido por IA")