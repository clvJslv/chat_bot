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

# Função para gerar perguntas aleatórias
def gerar_inserts_aleatorios(qtd):
    perguntas_exemplo = [
        "Qual é a capital do Brasil?",
        "O que é um algoritmo?",
        "Quem descobriu o Brasil?",
        "O que significa HTML?",
        "Qual linguagem estiliza páginas web?",
        "O que é uma variável?",
        "Qual a função do comando SELECT?",
        "O que representa o número pi?",
        "Qual a diferença entre RAM e HD?",
        "Em que ano foi a independência do Brasil?"
    ]
    inserts = []
    for i in range(1, qtd + 1):
        pergunta = random.choice(perguntas_exemplo)
        pergunta = pergunta.replace("'", "''")  # Escapar aspas simples
        fk_modulo = random.randint(100, 105)
        sql = f"INSERT INTO [dbo].[SimuladoPerguntas] ([id], [pergunta], [FK_MODULO]) VALUES ({i}, '{pergunta}', {fk_modulo});"
        inserts.append(sql)
    return inserts

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

                # Geração de INSERTs aleatórios
                st.subheader("🧪 Gerar INSERTs aleatórios para SimuladoPerguntas")
                qtd = st.slider("Quantidade de INSERTs", 1, 20, 10)
                inserts = gerar_inserts_aleatorios(qtd)
                st.code("\n".join(inserts), language="sql")
            else:
                st.info("Nenhuma tabela encontrada no banco.")
        except Exception as erro:
            st.error(f"Erro ao buscar dados: {erro}")
        finally:
            conexao.close()
    else:
        st.warning("Não foi possível estabelecer conexão.")
