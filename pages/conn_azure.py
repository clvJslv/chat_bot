import streamlit as st
import pyodbc

with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
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

# Barra lateral personalizada
with st.sidebar:
    st.markdown("## 🧭 Navegação")
    if st.button("🤖 Ir para Chatbot"):
        st.switch_page("pages/chatbot.py")
    if st.button("🤖 Ir para Cadastrar_Questões"):
        st.switch_page("pages/Cadastrar_Questões.py")
    if st.button("🤖 Ir para Gerar_Simulado"):
        st.switch_page("pages/Gerar_Simulado.py")
    if st.button("🤖 Ir para conn_azure"):
        st.switch_page("pages/conn_azure.py")
    
    if st.button("🤖 Retornar"):
        st.switch_page("gemini.py")
    

    st.markdown("---")
    st.markdown("## ⚙️ Configurações")
    st.selectbox("Modo de exibição", ["Claro", "Escuro", "Automático"])
    st.slider("Sensibilidade do modelo", 0.0, 1.0, 0.5)

    st.markdown("---")
    st.markdown("### 📞 Suporte")
    st.write("Email: suporte@meuapp.com")
    
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

# Executando dentro do Streamlit
def executar_insert():
    conexao = conectar_banco()
    if conexao:
        try:
            cursor = conexao.cursor()
            sql = "INSERT INTO [dbo].[SimuladoPerguntas] ([pergunta], [FK_MODULO]) VALUES ('quem descobriu a beringela', 1010);"
            cursor.execute(sql)
            conexao.commit()
            st.success("✅ INSERT executado com sucesso!")

            # Verificando se foi inserido
            cursor.execute("SELECT top 1 * FROM [dbo].[SimuladoPerguntas] order by id desc")
            resultado = cursor.fetchone()
            if resultado:
                st.write("📌 Resultado do SELECT:")
                st.write(resultado)
            else:
                st.warning("⚠️ Nenhum registro encontrado com id = 100")

        except Exception as erro:
            st.error(f"❌ Erro ao executar SQL: {erro}")
        finally:
            cursor.close()
            conexao.close()

# Botão para executar
if st.button("Executar INSERT"):
    executar_insert()
   
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