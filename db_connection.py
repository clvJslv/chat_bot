import pyodbc
import streamlit as st

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
        try:
            self.conn = pyodbc.connect(self.connection_string)
        except Exception as e:
            raise ConnectionError(f"Erro ao conectar: {e}")

    def execute_merge(self, id_input, pergunta, modulo):
        cursor = self.conn.cursor()
        merge_sql = """
        MERGE INTO [dbo].[SimuladoPerguntas] AS destino
        USING (SELECT ? AS id) AS origem
        ON destino.id = origem.id
        WHEN MATCHED THEN
            UPDATE SET pergunta = ?, FK_MODULO = ?
        WHEN NOT MATCHED THEN
            INSERT (pergunta, FK_MODULO) VALUES (?, ?);
        """
        cursor.execute(
            merge_sql,
            id_input if id_input else None,
            pergunta,
            modulo,
            pergunta,
            modulo
        )
        self.conn.commit()
        cursor.close()

    def close(self):
        if self.conn:
            self.conn.close()