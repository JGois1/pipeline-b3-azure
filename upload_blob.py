import os
from azure.storage.blob import BlobServiceClient

def upload_to_blob():
    """
    Conecta-se ao Azure Storage Account e faz o upload de um arquivo.
    """
    try:

        connect_str = "AZURE_STORAGE_KEY"

        container_name = "dados-brutos"

        local_file_path = "cotacoes_exemplo.txt"

        blob_name = "cotacoes_exemplo.txt"

        print("Conectando ao Azure Blob Storage...")
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)

        print(f"Fazendo upload do arquivo '{local_file_path}' para o contêiner '{container_name}'...")


        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)


        with open(local_file_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)

        print("Upload concluído com sucesso!")

    except FileNotFoundError:
        print(f"ERRO: O arquivo de exemplo '{local_file_path}' não foi encontrado.")
        print("Por favor, baixe um arquivo da B3 e salve-o com este nome na pasta do projeto.")
    except Exception as ex:
        print(f"Ocorreu um erro inesperado: {ex}")

if name == "main":
    upload_to_blob()