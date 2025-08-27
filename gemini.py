# app.py
import streamlit as st
from streamlit_modal import Modal
from db_connection import DatabaseConnection

# 🎨 Configuração inicial
st.set_page_config(page_title="Simulado SAEB", page_icon="🧠", layout="wide")

# 🔧 Estilo personalizado
try:
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    st.warning("⚠️ Arquivo de estilo não encontrado.")

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

# 🔐 Login com Modal
modal = Modal("🔐 Portal de Acesso", key="login_modal", max_width=600)

st.title("📚 Gerenciador de Perguntas do Simulado")
st.markdown("---")
st.markdown("""
Este é um aplicativo que utiliza IA com consultas ao chatbot (GEMINI) para gerar simulados de acordo com descritores,
apresentando sugestões de conteúdo para estudo das questões respondidas de forma errada.

- 📚 [Documentação oficial do Streamlit](https://docs.streamlit.io/)
- 🐞 [Reportar falhas ou bugs](https://github.com/streamlit/streamlit/issues)
""")
st.markdown("### 🧪 Bem-vindo ao APP Simulado assistido por IA")
st.markdown("---")

# 🧠 Autenticação
if "usuario" not in st.session_state:
    if st.button("Fazer Login"):
        modal.open()

    if modal.is_open():
        with modal.container():
            usuarios = listar_usuarios()
            usuario = st.selectbox("Usuário", usuarios, key="usuario_modal")
            senha = st.text_input("Senha", type="password", key="senha_modal")

            if st.button("Entrar", key="btn_login_modal"):
                auth = db.autenticar_usuario(usuario, senha)
                if auth:
                    st.session_state.usuario = usuario
                    st.session_state.perfil = auth["perfil"]
                    st.session_state.usuario_id = auth["id"]
                    st.success(f"✅ Bem-vindo, {usuario}!")
                    modal.close()
                    st.rerun()
                else:
                    st.error("❌ Credenciais inválidas.")

# 📂 Conteúdo após login
if "usuario" in st.session_state:
    # 🎨 Estilização da barra lateral
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
           padding-left: 12px;
        }
    </style>
    """, unsafe_allow_html=True)

    # 🧭 Barra lateral
    with st.sidebar:
        st.markdown(f"""
        👋 Olá, **{st.session_state.usuario}**  
        🔐 Perfil: **{st.session_state.perfil}**
        """)
        st.markdown("## 🧭 Navegação")

        usuario_id = st.session_state.usuario_id

        # 🔁 Função utilitária para acesso
        def acesso_modulo(nome, caminho, chave):
            if db.usuario_tem_acesso(usuario_id, nome):
                if st.button(f"🔹  {nome}", key=chave):
                    st.switch_page(caminho)

        # 📁 Módulos disponíveis
        modulos = {
            "Chatbot": "pages/chatbot.py",
            "Gerar Simulado": "pages/Gerar_Simulado.py",
            "Teste de Conexão": "pages/conn_azure.py",
            "Retornar": "gemini.py",
            "Questões": "pages/Cadastrar_Questões.py",
            "Respostas": "pages/Cadastrar_Respostas.py",
            "Cadastrar Usuários": "pages/Cadastrar_Usuarios.py"
        }

        for nome, caminho in modulos.items():
            acesso_modulo(nome, caminho, f"btn_{nome.replace(' ', '_').lower()}")

        st.markdown("---")
        st.markdown("### 📞   Suporte")
        st.write("Email: suporte@meuapp.com")

        if st.button("🚪 Sair"):
            for key in ["usuario", "perfil", "usuario_id"]:
                st.session_state.pop(key, None)
            st.rerun()

    # 🧠 Conteúdo principal
    st.title("📚 Simulado SAEB")
    st.markdown("Escolha uma opção na barra lateral para começar.")