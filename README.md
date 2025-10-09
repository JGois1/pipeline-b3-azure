# 📊 Pipeline de Dados da B3 com Azure
Este projeto é um estudo prático sobre a construção de um pipeline de dados na nuvem Azure. O objetivo é automatizar a extração, transformação e carga (ETL) dos arquivos diários de cotações da B3 em um banco de dados SQL para futuras análises.

#### Alunos: João Gois de Otoni, Marcus Vinicius Azevedo Moreira

### 🚀 Tecnologias Utilizadas
Azure Blob Storage: Para armazenar os arquivos brutos (.txt) de cotações.

Azure SQL Database: Para guardar os dados já limpos, tratados e prontos para consulta.

Azure Data Factory: É o orquestrador do projeto, responsável por automatizar todo o fluxo de dados.

Python: Utilizado em scripts de apoio para testes de conexão e upload inicial de arquivos.

### ⚙️ Como Configurar o Projeto
Para executar os scripts Python (upload_blob.py e testar_conexao_db.py) localmente, é necessário criar um arquivo config.ini na raiz do projeto.

Este arquivo deve conter as chaves de acesso e senhas dos serviços da Azure. Por questões de segurança, ele é ignorado pelo Git e não deve ser enviado para o repositório.

### 📋 Status Atual
O projeto está em desenvolvimento. A infraestrutura base e o pipeline de cópia de dados foram concluídos.
