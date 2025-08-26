import streamlit as st

def render():
    st.markdown("<h1 style='text-align: center; color: #4B8BBE;'>🔮 Aplicativos de Detecção de Faces e Objetos</h1>", unsafe_allow_html=True)
    with st.expander("ℹ️ Sobre este portal"):
        st.markdown("""
            Este é um hub de aplicativos de rede neural baseados em **YOLO (You Only Look Once)** para detecção de objetos e rostos em tempo real.

            - 📚 [Documentação oficial do Streamlit](https://docs.streamlit.io/)
            - 🐞 [Reportar falhas ou bugs](https://github.com/streamlit/streamlit/issues)
        """)
    st.divider()
    st.markdown("### 🧪 Escolha um aplicativo na barra lateral para começar.")