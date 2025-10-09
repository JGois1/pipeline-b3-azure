import pyodbc

def test_db_connection():
    """
    Tenta estabelecer uma conexão com o Azure SQL Database.
    """

    server = 'tcp:srv-b3-joao.database.windows.net,1433'
    database = 'db-b3-dados'
    username = 'adminjoao'
    password = 'M@pm1952'
    
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

    try:
        print("Tentando conectar ao Azure SQL Database...")
    
        with pyodbc.connect(connection_string) as cnxn:
            print("Conexão bem-sucedida!")
            
            cursor = cnxn.cursor()
            cursor.execute("SELECT @@VERSION;")
            row = cursor.fetchone()
            print(f"Versão do SQL Server: {row[0]}")

    except pyodbc.Error as ex:
        
        sqlstate = ex.args[0]
        if sqlstate == '28000':
            print("ERRO DE AUTENTICAÇÃO: Verifique se seu usuário e senha estão corretos.")
        elif sqlstate == '08001':
            print("ERRO DE CONEXÃO: Verifique o nome do servidor e se o seu IP foi liberado no firewall da Azure.")
        else:
            print(f"Ocorreu um erro de banco de dados: {ex}")
    except Exception as ex:
        print(f"Ocorreu um erro inesperado: {ex}")


if __name__ == '__main__':
    test_db_connection()

