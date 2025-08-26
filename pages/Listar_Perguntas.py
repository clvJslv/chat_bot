import streamlit as st
import pyodbc
import pandas as pd

# Função de conexão
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

# Função para buscar os dados da tabela
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

# Interface Streamlit
st.set_page_config(page_title="Visualização de Perguntas", layout="wide")
st.title("📋 Visualização da Tabela SimuladoPerguntas")

dados = carregar_dados()

if dados is not None and not dados.empty:
    st.dataframe(dados, use_container_width=True)
else:
    st.warning("⚠️ Nenhum dado encontrado ou erro na consulta.")