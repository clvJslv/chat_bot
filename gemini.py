import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="Portal YOLO",
    page_icon="🧠",
    layout="wide",
)

# Estilização da barra lateral
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

# Inicializa a página atual
if "pagina_atual" not in st.session_state:
    st.session_state.pagina_atual = "home"

# Funções de cada “página”
def home():
    st.markdown(
        """<h1 style='text-align: center; color: #4B8BBE;'>🔮 Aplicativos de Detecção de Faces e Objetos</h1>""",
        unsafe_allow_html=True
    )
    with st.expander("ℹ️ Sobre este portal"):
        st.markdown("""
            Este é um hub de aplicativos de rede neural baseados em **YOLO (You Only Look Once)** para detecção de objetos e rostos em tempo real.

            - 📚 [Documentação oficial do Streamlit](https://docs.streamlit.io/)
            - 🐞 [Reportar falhas ou bugs](https://github.com/streamlit/streamlit/issues)
        """)
    st.divider()
    st.markdown("### 🧪 Escolha um aplicativo na barra lateral para começar.")

def chatbot():
    st.title("🤖 Chatbot")
    st.write("Aqui você pode conversar com o modelo de IA.")

def cadastrar_questoes():
    st.title("📝 Cadastro de Questões")
    st.write("Interface para cadastrar perguntas no sistema.")

def gerar_simulado():
    st.title("🧪 Gerar Simulado")
    st.write("Ferramenta para montar simulados personalizados.")

def conn_azure():
    st.title("🔗 Conexão com Azure")
    st.write("Configuração e testes de integração com Azure.")

# Barra lateral personalizada
with st.sidebar:
    st.markdown("## 🧭 Navegação")
    if st.button("🤖 Ir para Chatbot"):
        st.session_state.pagina_atual = "chatbot"
    if st.button("📝 Ir para Cadastrar Questões"):
        st.session_state.pagina_atual = "cadastrar_questoes"
    if st.button("🧪 Ir para Gerar Simulado"):
        st.session_state.pagina_atual = "gerar_simulado"
    if st.button("🔗 Ir para Conexão Azure"):
        st.session_state.pagina_atual = "conn_azure"
    if st.button("🏠 Retornar à Home"):
        st.session_state.pagina_atual = "home"

    st.markdown("---")
    st.markdown("## ⚙️ Configurações")
    st.selectbox("Modo de exibição", ["Claro", "Escuro", "Automático"])
    st.slider("Sensibilidade do modelo", 0.0, 1.0, 0.5)

    st.markdown("---")
    st.markdown("### 📞 Suporte")
    st.write("Email: suporte@meuapp.com")

# Renderiza a página atual
if st.session_state.pagina_atual == "home":
    home()
elif st.session_state.pagina_atual == "chatbot":
    chatbot()
elif st.session_state.pagina_atual == "cadastrar_questoes":
    cadastrar_questoes()
elif st.session_state.pagina_atual == "gerar_simulado":
    gerar_simulado()
elif st.session_state.pagina_atual == "conn_azure":
    conn_azure()