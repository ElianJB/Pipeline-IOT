import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
from sqlalchemy.sql import text
import streamlit as st

# Conexão com o banco de dados PostgreSQL
engine = create_engine('postgresql://postgres:6733@localhost:5432')

# Carregar dados do arquivo CSV
df = pd.read_csv('IOT-temp.csv')

# Função para criar ou substituir a tabela 'data'
def create_or_replace_table():
    with engine.connect() as conn:
        # Dropar a tabela 'data' caso exista
        conn.execute(text('DROP TABLE IF EXISTS data CASCADE;'))
        conn.commit()
        
        # Criar a tabela 'data' a partir do DataFrame
        df.to_sql('data', con=engine, if_exists='replace', index=False)
        conn.commit()

# Funções para criar ou substituir as novas views
def create_avg_temp_por_dispositivo():
    with engine.connect() as conn:
        conn.execute(text('''
        CREATE OR REPLACE VIEW avg_temp_por_dispositivo AS
        SELECT "room_id/id" as device_id, AVG(temp) as avg_temp
        FROM data
        GROUP BY "room_id/id";
        '''))
        conn.commit()

def create_leituras_por_hora():
    with engine.connect() as conn:
        conn.execute(text('''
        CREATE OR REPLACE VIEW leituras_por_hora AS
        SELECT EXTRACT(HOUR FROM TO_TIMESTAMP(noted_date, 'DD-MM-YYYY HH24:MI')) as hora, COUNT(*) as contagem
        FROM data
        GROUP BY hora;
        '''))
        conn.commit()

def create_temp_max_min_por_dia():
    with engine.connect() as conn:
        conn.execute(text('''
        CREATE OR REPLACE VIEW temp_max_min_por_dia AS
        SELECT DATE(TO_TIMESTAMP(noted_date, 'DD-MM-YYYY HH24:MI')) as data, 
               MAX(temp) as temp_max, 
               MIN(temp) as temp_min
        FROM data
        GROUP BY data;
        '''))
        conn.commit()

# Função para carregar dados de uma view
def load_data(view_name):
    with engine.connect() as conn:
        return pd.read_sql(text(f"SELECT * FROM {view_name}"), con=conn)

# Executar as funções para criar as tabelas e views no banco
create_or_replace_table()
create_avg_temp_por_dispositivo()
create_leituras_por_hora()
create_temp_max_min_por_dia()

# Título do dashboard
st.title('Dashboard de Temperaturas IoT')

# Gráfico 1: Média de temperatura por dispositivo (gráfico de pizza)
st.header('Média de Temperatura por Dispositivo')
df_avg_temp = load_data('avg_temp_por_dispositivo')
fig1 = px.pie(df_avg_temp, names='device_id', values='avg_temp', title="Média de Temperatura por Dispositivo")
st.plotly_chart(fig1)

# Gráfico 2: Leituras por hora do dia (gráfico de linha)
st.header('Leituras por Hora do Dia')
df_leituras_hora = load_data('leituras_por_hora')
fig2 = px.line(df_leituras_hora, x='hora', y='contagem', title="Leituras por Hora do Dia")
st.plotly_chart(fig2)

# Gráfico 3: Temperaturas máximas e mínimas por dia (gráfico de linha)
st.header('Temperaturas Máximas e Mínimas por Dia')
df_temp_max_min = load_data('temp_max_min_por_dia')
fig3 = px.line(df_temp_max_min, x='data', y=['temp_max', 'temp_min'], title="Temperaturas Máximas e Mínimas por Dia")
st.plotly_chart(fig3)
