# Pipeline-IOT Dashboard de Temperaturas IoT
Este projeto cria um dashboard interativo usando Streamlit para visualizar dados de temperatura coletados por dispositivos IoT e armazenados em um banco de dados PostgreSQL. O dashboard oferece visualizações interativas de dados de temperatura por dispositivo, ambiente, hora do dia, entre outros, permitindo uma análise detalhada das leituras.

Funcionalidades
Visualização da média de temperatura por dispositivo.
Exibição das leituras de temperatura por hora do dia.
Gráfico com temperaturas máximas e mínimas por dia.
Análise de registros de temperatura por categoria (entrada/saída).
Tecnologias Utilizadas
Python: Linguagem de programação principal.
Streamlit: Framework para criação do dashboard interativo.
SQLAlchemy: ORM para interação com o banco de dados PostgreSQL.
Plotly: Para criar gráficos interativos.
PostgreSQL: Banco de dados relacional onde os dados de temperatura são armazenados.
Pré-requisitos
1. Python e Ambiente Virtual
Para garantir que todas as dependências sejam gerenciadas corretamente, é recomendado utilizar um ambiente virtual.

Criando o Ambiente Virtual:
Para criar um ambiente virtual, abra o terminal e execute o seguinte comando:

bash

python -m venv venv
Após criar o ambiente virtual, ative-o:

.\venv\Scripts\activate

2. Instalando Dependências
Com o ambiente virtual ativado, instale as dependências necessárias para o projeto com o comando:

bash

pip install -r requirements.txt
O arquivo requirements.txt contém todas as bibliotecas necessárias para o funcionamento do projeto.

3. Banco de Dados PostgreSQL
Rodando o PostgreSQL no Docker
Você pode rodar o PostgreSQL usando o Docker. Para isso, execute o seguinte comando no terminal:

bash

docker run --name postgres-iot -e POSTGRES_PASSWORD=(suasenha)-p 5432:5432 -d postgres
A conexão com o banco de dados será feita por meio da seguinte string de conexão:

python

engine = create_engine('postgresql://postgres:(suasenha)@localhost:5432')
4. Estrutura do Banco de Dados
Este projeto utiliza a tabela temperature_readings que contém os seguintes campos:

id: ID do dispositivo de leitura.
room_id/id: ID do ambiente onde a leitura foi realizada.
temp: Temperatura registrada.
out/in: Indica se a leitura é de dentro ou fora do ambiente.
noted_date: Data e hora da leitura.
Estrutura do Projeto
IOT-temp.csv: Arquivo CSV contendo os dados de temperatura.
app.py: Código principal do projeto, responsável pela criação do dashboard e interação com o banco de dados.
requirements.txt: Arquivo contendo todas as dependências necessárias.
Passos para Execução
1. Carregar os Dados para o Banco de Dados
O primeiro passo é carregar os dados do arquivo CSV (IOT-temp.csv) para o banco de dados PostgreSQL. O código utiliza a função create_or_replace_table para:


Criar uma nova tabela a partir do arquivo CSV.
2. Criação das Views no Banco de Dados
As seguintes views SQL são criadas para análise dos dados:

2.1. avg_temp_por_dispositivo
Essa view calcula a média de temperatura por dispositivo (ID), ignorando dispositivos com temperaturas inferiores a 20°C.

sql

CREATE OR REPLACE VIEW avg_temp_por_dispositivo AS
SELECT "room_id/id" as device_id, AVG(temp) as avg_temp
FROM temperature_readings
GROUP BY "room_id/id";
2.2. leituras_por_hora
Essa view conta o número de leituras feitas por hora, ajudando a identificar picos de atividade ao longo do dia.

sql

CREATE OR REPLACE VIEW leituras_por_hora AS
SELECT EXTRACT(HOUR FROM TO_TIMESTAMP(noted_date, 'DD-MM-YYYY HH24:MI')) as hora, COUNT(*) as contagem
FROM temperature_readings
GROUP BY hora;
2.3. temp_max_min_por_dia
Essa view calcula as temperaturas máxima e mínima registradas por dia.

sql

CREATE OR REPLACE VIEW temp_max_min_por_dia AS
SELECT DATE(TO_TIMESTAMP(noted_date, 'DD-MM-YYYY HH24:MI')) as data, MAX(temp) as temp_max, MIN(temp) as temp_min
FROM temperature_readings
GROUP BY data;
3. Executando o Dashboard
Com tudo configurado, você pode rodar o dashboard com o seguinte comando:

bash

streamlit run dashboard.py
Isso abrirá o dashboard no seu navegador, onde você poderá visualizar gráficos interativos de análise de temperatura.

Capturas de Tela
![Captura de tela 2024-09-19 072959](https://github.com/user-attachments/assets/c012cb8f-cde6-4a7e-bfa4-dfe24a8e231a)

![Captura de tela 2024-09-19 072949](https://github.com/user-attachments/assets/7fb4a71c-4a68-4d56-b814-474411d06ab2)

![Captura de tela 2024-09-19 072938](https://github.com/user-attachments/assets/fc356e62-2bea-4181-bfb8-8764f1213d3a)





Insights Obtidos
Com base nas visualizações oferecidas pelo dashboard, os seguintes insights podem ser extraídos dos dados:

Média de Temperatura por Dispositivo: Permite identificar quais dispositivos estão registrando temperaturas mais altas ou mais baixas, ajudando a monitorar possíveis falhas ou anomalias nos dispositivos.

Leituras por Hora do Dia: Mostra quais horários do dia há maior número de leituras, possibilitando identificar picos de atividade e horários críticos.

Temperaturas Máximas e Mínimas por Dia: Mostra a variação de temperatura ao longo do tempo, ajudando a identificar tendências e padrões diários de temperatura.
