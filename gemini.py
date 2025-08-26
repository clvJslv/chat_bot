import streamlit as st
from app import home, chatbot, cadastrar_questoes, gerar_simulado, conn_azure

st.set_page_config(page_title="Portal YOLO", page_icon="🧠", layout="wide")

with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

if "pagina_atual" not in st.session_state:
    st.session_state.pagina_atual = "home"

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
    st.selectbox("Modo de exibição", ["Claro", "Escuro", "Automático"])
    st.slider("Sensibilidade do modelo", 0.0, 1.0, 0.5)
    st.markdown("---")
    st.write("📞 suporte@meuapp.com")

match st.session_state.pagina_atual:
    case "home": home.render()
    case "chatbot": chatbot.render()
    case "cadastrar_questoes": cadastrar_questoes.render()
    case "gerar_simulado": gerar_simulado.render()
    case "conn_azure": conn_azure.render()