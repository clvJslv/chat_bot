import streamlit as st

st.set_page_config(
    page_title="🔮 Estilo Místico",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS para estilizar a sidebar
st.markdown("""
    <style>
    /* Estilo da barra lateral */
    [data-testid="stSidebar"] {
        font-size: 18px;
        font-family: 'Nunito', sans-serif;
        color: #333333;
        background-color: #f5f5f5;
        padding: 20px;
    }

    /* Título e cabeçalhos */
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        font-size: 24px;
        font-weight: bold;
        color: #6a1b9a;
    }

    /* Links e textos */
    [data-testid="stSidebar"] a {
        color: #6a1b9a;
        text-decoration: none;
    }

    /* Hover elegante */
    [data-testid="stSidebar"] a:hover {
        color: #9c27b0;
        text-decoration: underline;
    }
    </style>
""", unsafe_allow_html=True)

# Conteúdo da barra lateral
with st.sidebar:
    st.header("🔮 Navegação")
    st.write("Escolha uma opção:")
    st.button("Página Inicial")
    st.button("Cadastrar Questões")
    st.button("Configurações")