import azure.functions as func
import logging
import os
import pyodbc
from datetime import datetime
import random

app = func.FunctionApp()

# --- CONFIGURAÇÕES ---
# A Connection String do Banco será lida da variável de ambiente SQL_CONNECTION_STRING
# que você configurará no local.settings.json (ou no Azure)
DB_CONNECTION_STRING = os.environ.get('SQL_CONNECTION_STRING') 

# -----------------------------------------------------------------------------
# FUNCTION 1: TIME TRIGGER (Simula Download da B3)
# Gatilho: Roda a cada 5 minutos (cron expression)
# -----------------------------------------------------------------------------
@app.schedule(schedule="0 */5 * * * *", arg_name="myTimer", run_on_startup=False, use_monitor=False) 
@app.blob_output(arg_name="outputblob", path="dados-brutos/cotacoes_{datetime}.txt", connection="AzureWebJobsStorage")
def download_b3_trigger(myTimer: func.TimerRequest, outputblob: func.Out[str]) -> None:
    logging.info('Simulando download B3 e criando arquivo...')
    
    data_hoje = datetime.now().strftime("%Y%m%d")
    linhas = []
    # Simula a extração de alguns ativos
    acoes = ['PETR4', 'VALE3', 'ITUB4', 'BBDC4', 'ABEV3']
    
    for acao in acoes:
        preco = random.uniform(10.0, 100.0)
        volume = random.randint(1000, 50000)
        # Formato de dados que será lido pelo Blob Trigger: DATA;ACAO;ABERTURA;FECHAMENTO;VOLUME
        linha = f"{data_hoje};{acao};{preco:.2f};{preco + 1.5:.2f};{volume}"
        linhas.append(linha)

    outputblob.set("\n".join(linhas))
    logging.info('Arquivo gerado e enviado ao Blob Storage. Isso irá disparar a Function de Carga.')

# -----------------------------------------------------------------------------
# FUNCTION 2: BLOB TRIGGER (Carga no Banco de Dados)
# Gatilho: Dispara AUTOMATICAMENTE quando um arquivo .txt cai em 'dados-brutos'
# -----------------------------------------------------------------------------
@app.blob_trigger(arg_name="myblob", path="dados-brutos/{name}.txt",
                  connection="AzureWebJobsStorage")
def processar_arquivo_blob(myblob: func.InputStream):
    logging.info(f"Novo arquivo detectado: {myblob.name}. Processando...")
    
    if not DB_CONNECTION_STRING:
        logging.error("Erro: Connection String do Banco não configurada (SQL_CONNECTION_STRING).")
        return

    try:
        # Lê o conteúdo do arquivo
        conteudo = myblob.read().decode('utf-8')
        linhas = conteudo.split('\n')

        # Conecta no Banco SQL Server
        conn = pyodbc.connect(DB_CONNECTION_STRING)
        cursor = conn.cursor()

        # Query de inserção na tabela Cotacoes
        query = "INSERT INTO Cotacoes (DataPregao, Ativo, Abertura, Fechamento, Volume) VALUES (?, ?, ?, ?, ?)"

        count = 0
        for linha in linhas:
            if not linha.strip(): continue
            
            partes = linha.split(';')
            if len(partes) >= 5:
                data_str = partes[0]
                data_pregao = f"{data_str[:4]}-{data_str[4:6]}-{data_str[6:]}" # Converte de YYYYMMDD para YYYY-MM-DD
                
                # Executa a inserção dos dados
                cursor.execute(query, data_pregao, partes[1], float(partes[2]), float(partes[3]), int(partes[4]))
                count += 1

        conn.commit()
        logging.info(f"Sucesso! {count} linhas inseridas na tabela Cotacoes.")

    except Exception as e:
        logging.error(f"Erro ao processar blob ou inserir no banco: {str(e)}")
    finally:
        if 'conn' in locals():
            conn.close()