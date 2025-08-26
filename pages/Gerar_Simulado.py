import streamlit as st

with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("🚧 Página em Construção")
st.image("em_construcao.jpg", caption="Estamos trabalhando nisso!", width=300)

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

# 🧭 Barra lateral personalizada
with st.sidebar:
    st.markdown("## 🧭 Navegação")
    if st.button("🤖 Ir para Chatbot", key="btn_chatbot"):
        st.switch_page("pages/chatbot.py")
    if st.button("🤖 Ir para Cadastrar_Respostas", key="btn_cadastrar_respostas"):
        st.switch_page("pages/Cadastrar_Respostas.py")
    if st.button("🤖 Ir para Cadastrar_Questões", key="btn_cadastrar"):
        st.switch_page("pages/Cadastrar_Questões.py")
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
