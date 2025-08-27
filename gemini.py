import streamlit as st
from db_connection import DatabaseConnection

# ✅ Configuração da página (chamada única e no topo)
st.set_page_config(page_title="Simulado SAEB", page_icon="🧠", layout="wide")

# 🔧 Estilo personalizado
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# 🔌 Conexão com o banco
db = DatabaseConnection()
db.connect()

if not db.conn:
    st.error("❌ Falha na conexão com o banco.")
    st.stop()

# 🔍 Função para listar usuários
def listar_usuarios():
    try:
        cursor = db.conn.cursor()
        cursor.execute("SELECT usuario FROM TB_010_USUARIOS ORDER BY usuario")
        return [row[0] for row in cursor.fetchall()]
    except Exception as e:
        st.error(f"Erro ao buscar usuários: {e}")
        return []

# 🔐 Login
st.markdown("<h2 style='text-align:center;'>🔐 Portal de Acesso</h2>", unsafe_allow_html=True)

with st.expander("Clique para fazer login", expanded=True):
    usuarios = listar_usuarios()
    usuario = st.selectbox("Usuário", usuarios)
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        perfil = db.autenticar_usuario(usuario, senha)
        if perfil:
            st.session_state.perfil = perfil
            st.session_state.usuario = usuario
            st.success(f"✅ Bem-vindo, {usuario}!")
        else:
            st.error("❌ Usuário ou senha inválidos.")

# 🔓 Conteúdo após login
if "usuario" in st.session_state:
    st.markdown("---")
    st.markdown(f"👋 Olá, **{st.session_state.usuario}**! Seu perfil é **{st.session_state.perfil}**.")
    st.markdown("Você agora tem acesso ao conteúdo do portal Gemini.")

    # 🧭 Barra lateral personalizada
    with st.sidebar:
        st.markdown("## 🧭 Navegação")
        if st.button("🎓   Chatbot", key="btn_chatbot"):
            st.switch_page("pages/Chatbot")
        if st.button("🖥️   Gerar Simulado", key="btn_simulado"):
            st.switch_page("Gerar Simulado")
        if st.button("✅   Teste de Conexão", key="btn_azure"):
            st.switch_page("Teste de Conexão")
        if st.button("↩️   Retornar", key="btn_retornar"):
            st.switch_page("Gemini")
        st.markdown("---")
        st.markdown("## ⚙️   Cadastro")
        if st.button("🗂️   Questões", key="btn_cadastrar"):
            st.switch_page("Cadastrar Questões")
        if st.button("🗂️   Respostas", key="btn_cadastrar_respostas"):
            st.switch_page("Cadastrar Respostas")
        st.markdown("---")
        st.markdown("### 📞   Suporte")
        st.write("Email: suporte@meuapp.com")

    # 🎒 Conteúdo principal
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