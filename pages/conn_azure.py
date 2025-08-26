import pyodbc

def conectar_banco():
    try:
        conexao = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=myfreesqldbserver-0101.database.windows.net;"
            "DATABASE=myFreeDB;"
            "UID=ivan;"  # substitua pelo seu usuário real
            "PWD=MigMat01#!;"    # substitua pela sua senha real
            "Encrypt=yes;"
            "TrustServerCertificate=no;"
            "Connection Timeout=30;"
        )
        print("✅ Conexão bem-sucedida com o banco de dados!")
        return conexao
    except Exception as erro:
        print("❌ Erro ao conectar:", erro)

# Teste de conexão
conexao = conectar_banco()

if conexao:
    cursor = conexao.cursor()
    cursor.execute("SELECT name FROM sys.tables")
    tabelas = cursor.fetchall()
    print("📂 Tabelas encontradas:")
    for tabela in tabelas:
        print("-", tabela.name)
    conexao.close()