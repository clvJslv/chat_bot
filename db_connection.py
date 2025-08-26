# db_connection.py
import pyodbc
import streamlit as st

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

# Conexão com a base de dados
class DatabaseConnection:
    def __init__(self):
        db = st.secrets["database"]
        self.connection_string = (
            f"DRIVER={{{db['driver']}}};"
            f"SERVER={db['server']};"
            f"DATABASE={db['database']};"
            f"UID={db['uid']};"
            f"PWD={db['pwd']};"
            f"Encrypt={db['encrypt']};"
            f"TrustServerCertificate={db['trust_cert']};"
            f"Connection Timeout={db['timeout']};"
        )
        self.conn = None

    def connect(self):
        self.conn = pyodbc.connect(self.connection_string)

    def close(self):
        if self.conn:
            self.conn.close()

    def get_perguntas(self, filtro_modulo=None):
        cursor = self.conn.cursor()
        if filtro_modulo:
            cursor.execute("SELECT PK_CO_PERGUNTA, CO_PERGUNTA,  DE_PERGUNTA FROM smulado.dbo.TB_007_PERGUNTAS WHERE PK_CO_PERGUNTA = ?", filtro_modulo)
        else:
            cursor.execute("SELECT PK_CO_PERGUNTA, CO_PERGUNTA,  DE_PERGUNTA FROM smulado.dbo.TB_007_PERGUNTAS")
        rows = cursor.fetchall()
        cursor.close()
        return rows

    def insert_pergunta(self, pergunta, modulo):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO smulado.dbo.TB_007_PERGUNTAS (CO_PERGUNTA, DE_PERGUNTA) VALUES (?, ?)", pergunta, modulo)
        self.conn.commit()
        cursor.close()

    def update_pergunta(self, id, pergunta, modulo):
        cursor = self.conn.cursor()
        cursor.execute("UPDATE smulado.dbo.TB_007_PERGUNTAS SET CO_PERGUNTA = ?, DE_PERGUNTA = ? WHERE PK_CO_PERGUNTA = ?", pergunta, modulo, id)
        self.conn.commit()
        cursor.close()

    def delete_pergunta(self, id):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM smulado.dbo.TB_007_PERGUNTAS WHERE PK_CO_PERGUNTA = ?", id)
        self.conn.commit()
        cursor.close()