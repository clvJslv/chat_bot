import streamlit as st

# Barra lateral personalizada
with st.sidebar:
    st.markdown("## 🧭 Navegação")
    if st.button("🤖 Ir para Chatbot"):
        st.switch_page("app/chatbot.py")
    if st.button("🤖 Ir para Cadastrar_Questões"):
        st.switch_page("app/Cadastrar_Questões.py")
    if st.button("🤖 Ir para Gerar_Simulado"):
        st.switch_page("app/Gerar_Simulado.py")
    if st.button("🤖 Ir para conn_azure"):
        st.switch_page("app/conn_azure.py")
    
    if st.button("🤖 Retornar"):
        st.switch_page("gemini.py")
    

    st.markdown("---")
    st.markdown("## ⚙️ Configurações")
    st.selectbox("Modo de exibição", ["Claro", "Escuro", "Automático"])
    st.slider("Sensibilidade do modelo", 0.0, 1.0, 0.5)

    st.markdown("---")
    st.markdown("### 📞 Suporte")
    st.write("Email: suporte@meuapp.com")
    
st.title("🚧 Página em Construção")
st.image("em_construcao.jpg", caption="Estamos trabalhando nisso!", width=300)
