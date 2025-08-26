# db_connection.py
import pyodbc
import streamlit as st

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