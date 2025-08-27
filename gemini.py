import streamlit as st

with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# Configuração da página
st.set_page_config(
    page_title="Simulado IDEB",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilização da barra lateral
st.markdown("""
    <style>
        [data-testid="stSidebar"] {
           background: #00000024;
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
           background-color: #00000024;
           color: rgba(245, 245, 245, 0.477);
           border: none;
           border-radius: 8px;
           padding: 3px 5px;
           font-size: 16px;
           font-weight: bold;
           box-shadow: 0 4px 6px rgba(0,0,0,0.1);
           cursor: pointer;
           transition: background-color 0.3s ease-in-out;
        }
    </style>
""", unsafe_allow_html=True)

# 🧭 Barra lateral personalizada
with st.sidebar:
    st.markdown("## 🧭 Navegação")
    if st.button("🤖 Ir para Chatbot", key="btn_chatbot"):
        st.switch_page("pages/chatbot.py")
    if st.button("🤖 Ir para Cadastrar_Questões", key="btn_cadastrar"):
        st.switch_page("pages/Cadastrar_Questões.py")
    if st.button("🤖 Ir para Cadastrar_Respostas", key="btn_cadastrar_respostas"):
        st.switch_page("pages/Cadastrar_Respostas.py")
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

# Conteúdo principal
st.markdown(
    """
    <h1 style='text-align: center; color: #4B8BBE;'>🔮 Aplicação para Avaliação de Alunos</h1>
    """,
    unsafe_allow_html=True
)

with st.expander("ℹ️ Sobre este portal"):
    st.markdown(
        """
        Este é um hub de aplicativos de rede neural baseados em **YOLO (You Only Look Once)** para detecção de objetos e rostos em tempo real.

        - 📚 [Documentação oficial do Streamlit](https://docs.streamlit.io/)
        - 🐞 [Reportar falhas ou bugs](https://github.com/streamlit/streamlit/issues)
        """
    )

st.divider()
st.markdown("### 🧪 Escolha um aplicativo na barra lateral para começar.")