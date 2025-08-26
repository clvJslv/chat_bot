import streamlit as st
import pyodbc
import pandas as pd

# 🎯 Configuração da página
st.set_page_config(page_title="📋 SimuladoPerguntas", layout="wide", page_icon="📘")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .block-container { padding-top: 2rem; }
    </style>
""", unsafe_allow_html=True)

st.title("📘 Visualização da Tabela SimuladoPerguntas")
st.caption("Explore os dados cadastrados no sistema de perguntas simuladas.")

# 🔌 Função de conexão
def conectar_banco():
    try:
        conexao = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=myfreesqldbserver-0101.database.windows.net;"
            "DATABASE=myFreeDB;"
            "UID=ivan;"
            "PWD=MigMat01#!;"
            "Encrypt=yes;"
            "TrustServerCertificate=no;"
            "Connection Timeout=30;"
        )
        return conexao
    except Exception as erro:
        st.error(f"❌ Erro ao conectar: {erro}")
        return None

# 📥 Função para buscar os dados
def carregar_dados():
    conexao = conectar_banco()
    if conexao:
        try:
            consulta = "SELECT * FROM [dbo].[SimuladoPerguntas]"
            df = pd.read_sql(consulta, conexao)
            return df
        except Exception as erro:
            st.error(f"❌ Erro ao carregar dados: {erro}")
            return None
        finally:
            conexao.close()

# 📊 Carregando os dados
dados = carregar_dados()

# 🔍 Filtros interativos
if dados is not None and not dados.empty:
    col1, col2 = st.columns(2)

    with col1:
        filtro_modulo = st.selectbox("🔎 Filtrar por Módulo", options=["Todos"] + sorted(dados["FK_MODULO"].unique().tolist()))
    with col2:
        filtro_texto = st.text_input("🔍 Buscar por palavra-chave na pergunta")

    # Aplicando filtros
    if filtro_modulo != "Todos":
        dados = dados[dados["FK_MODULO"] == filtro_modulo]

    if filtro_texto:
        dados = dados[dados["pergunta"].str.contains(filtro_texto, case=False, na=False)]

    # 🧾 Exibindo tabela
    st.markdown("### 📄 Resultados")
    st.dataframe(dados, use_container_width=True, height=500)
else:
    st.warning("⚠️ Nenhum dado encontrado ou erro na consulta.")