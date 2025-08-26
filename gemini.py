import streamlit as st

st.set_page_config(
    page_title="",
    page_icon="🔮",
    layout="wide",  # "centered",  ou "wide"
    initial_sidebar_state="expanded",  # "auto", "expanded" ou "collapsed"

)

st.write("# Aplicativos de Detecção de Faces e Objetos 🔮")

st.markdown(
    """
    **Ajuda:** [https://docs.streamlit.io/](https://docs.streamlit.io/)

    **Reportar falha:** [https://github.com/streamlit/streamlit/issues](https://github.com/streamlit/streamlit/issues) 

    **Descrição:** Portal de Aplicativos de Rede Neural baseados em YOLO.
"""
)
