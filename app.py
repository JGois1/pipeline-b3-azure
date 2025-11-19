from flask import Flask, jsonify
from flask_cors import CORS
import pyodbc
import configparser

app = Flask(__name__)
CORS(app)  # Permite que o Frontend acesse este Backend

# Ler configurações do arquivo config.ini (O MESMO QUE VOCÊ JÁ TEM)
config = configparser.ConfigParser()
config.read('config.ini')

# Configuração do Banco
server = config['AZURE_SQL']['SERVER']
database = config['AZURE_SQL']['DATABASE']
username = config['AZURE_SQL']['USERNAME']
password = config['AZURE_SQL']['PASSWORD']
driver = '{ODBC Driver 17 for SQL Server}'

def get_db_connection():
    conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    return pyodbc.connect(conn_str)

@app.route('/')
def home():
    return "<h1>Backend da B3 Online! 🚀</h1><p>Acesse <a href='/api/ativos'>/api/ativos</a> para ver as cotações.</p>"

@app.route('/api/ativos', methods=['GET'])
def listar_ativos():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Pega as 100 últimas cotações
        cursor.execute("SELECT TOP 100 DataPregao, Ativo, Fechamento, Volume FROM Cotacoes ORDER BY DataPregao DESC")
        
        columns = [column[0] for column in cursor.description]
        resultados = []
        
        for row in cursor.fetchall():
            resultados.append(dict(zip(columns, row)))
            
        conn.close()
        return jsonify(resultados)
        
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

if __name__ == '__main__':
    # Roda localmente na porta 5000
    app.run(debug=True, host='0.0.0.0', port=5000)