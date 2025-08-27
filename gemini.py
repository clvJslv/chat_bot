import streamlit as st
from db_connection import DatabaseConnection

# Configuração da página
st.set_page_config(page_title="Login", page_icon="🔐", layout="centered")

# Conexão com o banco
db = DatabaseConnection()
db.connect()

if not db.conn:
    st.error("❌ Falha na conexão com o banco.")
    st.stop()

# Função para listar usuários
def listar_usuarios():
    try:
        cursor = db.conn.cursor()
        cursor.execute("SELECT usuario FROM TB_010_USUARIOS ORDER BY usuario")
        return [row[0] for row in cursor.fetchall()]
    except Exception as e:
        st.error(f"Erro ao buscar usuários: {e}")
        return []

# Título da página
st.markdown("<h2 style='text-align:center; color:#10b981;'>🔐 Acesso ao Portal</h2>", unsafe_allow_html=True)

# Botão para abrir o modal
if st.button("Fazer login"):
    with st.modal("🔐 Login de Usuário", padding=30):
        st.markdown("### Selecione o usuário e digite a senha")

        usuarios = listar_usuarios()
        usuario = st.selectbox("Usuário", usuarios)
        senha = st.text_input("Senha", type="password")

        if st.button("Entrar"):
            perfil = db.autenticar_usuario(usuario, senha)
            if perfil:
                st.session_state.perfil = perfil
                st.session_state.usuario = usuario
                st.success("✅ Login realizado com sucesso!")
                st.switch_page("home.py")
            else:
                st.error("❌ Usuário ou senha inválidos.")