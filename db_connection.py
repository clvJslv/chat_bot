# db_connection.py
import pyodbc
import streamlit as st

with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
# Estilização da barra lateral
st.markdown("""
    <style>
        [data-testid="stSidebar"] {
           background: linear-gradient( #000000, #0000004c, #06080075);
           color: white;
           box-shadow: 0 0 10px rgba(0,0,0,0.5);
           padding: 20px;
           border-radius: 10px;
        }
       
        [data-testid="stSidebar"] {
           height: 100vh;
        overflow-y: auto;
}

        [data-testid="stSidebar"] h2 {
            color: #10b981;
        }
        [data-testid="stSidebar"] .stButton button {
           background-color: #0000004c;
           color: rgba(245, 245, 245, 0.849);
           text-align: left;
           padding-left: 12px;
           width: 240px;
           height: 40px;
           border: none;
           border-radius: 8px;
           font-size: 18px;
           font-weight: bold;
           box-shadow: 0 4px 6px rgba(0,0,0,0.1);
           cursor: pointer;
           transition: background-color 0.3s ease-in-out;
           display: flex;
           justify-content: flex-start;   /* Alinha conteúdo à esquerda */
           align-items: center;           /* Centraliza verticalmente */
           padding-left: 12px;            /* Espaço interno à esquerda */
           text-align: left;              /* Redundante, mas seguro */
        }
    </style>
""", unsafe_allow_html=True)

# 🧭 Barra lateral personalizada
with st.sidebar:
    st.markdown("## 🧭 Navegação")
    if st.button("🎓   Chatbot", key="btn_chatbot"):
       st.switch_page("pages/chatbot.py")
    if st.button("🖥️   Gerar Simulado", key="btn_simulado"):
        st.switch_page("pages/Gerar_Simulado.py")
    if st.button("✅   Teste de Conexão", key="btn_azure"):
        st.switch_page("pages/conn_azure.py")
    if st.button("↩️   Retornar", key="btn_retornar"):
        st.switch_page("gemini.py")
    st.markdown("---")
    st.markdown("## ⚙️   Cadastro")
    if st.button("🗂️   Questões", key="btn_cadastrar"):
        st.switch_page("pages/Cadastrar_Questões.py")
    if st.button("🗂️   Respostas", key="btn_cadastrar_respostas"):
        st.switch_page("pages/Cadastrar_Respostas.py")
        st.markdown("---")
    
    st.markdown("---")
    st.markdown("### 📞   Suporte")
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
            cursor.execute(
            "SELECT PK_CO_PERGUNTA, CO_PERGUNTA, DE_PERGUNTA FROM TB_007_PERGUNTAS WHERE PK_CO_PERGUNTA = ?",
            filtro_modulo
        )
        else:
            cursor.execute("SELECT PK_CO_PERGUNTA, CO_PERGUNTA, DE_PERGUNTA FROM TB_007_PERGUNTAS")

        columns = [column[0] for column in cursor.description]
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
        cursor.close()
        return rows

    def insert_pergunta(self, codigo, descricao):
        cursor = self.conn.cursor()
        cursor.execute(
        "INSERT INTO TB_007_PERGUNTAS (CO_PERGUNTA, DE_PERGUNTA) VALUES (?, ?)",
        codigo, descricao
    )
        self.conn.commit()
        cursor.close()

    def update_pergunta(self, id, codigo, descricao):
        cursor = self.conn.cursor()
        cursor.execute(
        "UPDATE TB_007_PERGUNTAS SET CO_PERGUNTA = ?, DE_PERGUNTA = ? WHERE PK_CO_PERGUNTA = ?",
        codigo, descricao, id
    )
        self.conn.commit()
        cursor.close()


    def delete_pergunta(self, id):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM TB_007_PERGUNTAS WHERE PK_CO_PERGUNTA = ?", id)
        self.conn.commit()
        cursor.close()
        
# Respostas
    def get_respostas(self, pergunta_id=None):
        cursor = self.conn.cursor()
        if pergunta_id:
            cursor.execute("""
                SELECT CO_RESPOSTA, NO_RESPOSTA, FK_CO_PERGUNTA, CO_RESPOSTA_CORRETA
                FROM TB_008_RESPOSTAS WHERE FK_CO_PERGUNTA = ?
            """, pergunta_id)
        else:
            cursor.execute("SELECT CO_RESPOSTA, NO_RESPOSTA, FK_CO_PERGUNTA, CO_RESPOSTA_CORRETA FROM TB_008_RESPOSTAS")
        columns = [col[0] for col in cursor.description]
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
        cursor.close()
        return rows

    def insert_resposta(self, texto_resposta, pergunta_id, resposta_correta):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO TB_008_RESPOSTAS (NO_RESPOSTA, FK_CO_PERGUNTA, CO_RESPOSTA_CORRETA)
            VALUES (?, ?, ?)
        """, texto_resposta, pergunta_id, resposta_correta)
        self.conn.commit()
        cursor.close()

    def update_resposta(self, resposta_id, texto_resposta, pergunta_id, resposta_correta):
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE TB_008_RESPOSTAS
            SET NO_RESPOSTA = ?, FK_CO_PERGUNTA = ?, CO_RESPOSTA_CORRETA = ?
            WHERE CO_RESPOSTA = ?
        """, texto_resposta, pergunta_id, resposta_correta, resposta_id)
        self.conn.commit()
        cursor.close()

    def delete_resposta(self, resposta_id):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM TB_008_RESPOSTAS WHERE CO_RESPOSTA = ?", resposta_id)
        self.conn.commit()
        cursor.close()
    
    # 🔐 Autenticação
    def autenticar_usuario(self,usuario, senha):
        cursor = self.conn.cursor()
        cursor.execute("SELECT perfil FROM TB_010_USUARIOS WHERE usuario=? AND senha=?", (usuario, senha))
        resultado = cursor.fetchone()
        return resultado[0] if resultado else None
    
    def listar_usuarios(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT usuario FROM TB_010_USUARIOS ORDER BY usuario")
            return [row[0] for row in cursor.fetchall()]
        except Exception as e:
            print(f"Erro ao listar usuários: {e}")
            return []