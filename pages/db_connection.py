# db_connection.py
import pyodbc

class DatabaseConnection:
    def __init__(self):
        self.connection_string = (
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=myfreesqldbserver-0101.database.windows.net;"
            "DATABASE=myFreeDB;"
            "UID=ivan;"
            "PWD=MigMat01#!;"
            "Encrypt=yes;"
            "TrustServerCertificate=no;"
            "Connection Timeout=30;"
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