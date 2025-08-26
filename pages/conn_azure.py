import streamlit as st
import pyodbc


# Função de conexão
def conectar_banco():
    try:
        conexao = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=myfreesqldbserver-0101.database.windows.net;"
            "DATABASE=myFreeDB;"
            "UID=ivan;"  # substitua pelo seu usuário real
            "PWD=MigMat01#!;"  # substitua pela sua senha real
            "Encrypt=yes;"
            "TrustServerCertificate=no;"
            "Connection Timeout=30;"
        )
        return conexao
    except Exception as erro:
        st.error(f"❌ Erro ao conectar: {erro}")
        return None

# Função para gerar um único INSERT fixo
def gerar_insert_fixo():
    id = 9999
    pergunta = "Qual é a capital de Pernambuco?"
    fk_modulo = 101
    sql = f"INSERT INTO [dbo].[SimuladoPerguntas] ([id], [pergunta], [FK_MODULO]) VALUES ({id}, '{pergunta}', {fk_modulo});"
    return sql

# Interface Streamlit
st.set_page_config(page_title="Conexão com Banco", page_icon="🗄️", layout="centered")
st.title("🗄️ Conexão com SQL Server")

st.markdown("Clique no botão abaixo para conectar e listar as tabelas disponíveis:")

if st.button("🔌 Conectar ao Banco"):
    conexao = conectar_banco()
    
    if conexao:
        st.success("✅ Conexão bem-sucedida com o banco de dados!")
        try:
            cursor = conexao.cursor()
            cursor.execute("SELECT name FROM sys.tables")
            tabelas = cursor.fetchall()

            if tabelas:
                st.subheader("📂 Tabelas encontradas:")
                for tabela in tabelas:
                    st.markdown(f"- **{tabela.name}**")

                # Geração de INSERT fixo
                st.subheader("🧪 Gerar um único INSERT fixo para SimuladoPerguntas")
                if st.button("📌 Gerar INSERT fixo"):
                    insert_sql = gerar_insert_fixo()
                    st.code(insert_sql, language="sql")
            else:
                st.info("Nenhuma tabela encontrada no banco.")
        except Exception as erro:
            st.error(f"Erro ao buscar dados: {erro}")
        finally:
            conexao.close()
    else:
        st.warning("Não foi possível estabelecer conexão.")