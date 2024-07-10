import sqlite3
import pandas as pd
from sqlalchemy import create_engine

# Caminho para o arquivo SQLite
sqlite_db_path = 'tabela_alimentos.db'

# Conectar ao banco de dados SQLite e exportar os dados
sqlite_conn = sqlite3.connect(sqlite_db_path)
query = "SELECT * FROM alimentos"
df = pd.read_sql_query(query, sqlite_conn)
sqlite_conn.close()

# Salvar os dados em um arquivo CSV
csv_path = 'alimentos.csv'
df.to_csv(csv_path, index=False)

# Configurar a conexão com o PostgreSQL
postgres_url = 'postgres://default:bHJ0dtgYQ9RS@ep-black-night-a46gt28n.us-east-1.aws.neon.tech:5432/verceldb?sslmode=require'
engine = create_engine(postgres_url)

# Criar a tabela no PostgreSQL
create_table_query = """
CREATE TABLE IF NOT EXISTS alimentos (
    id SERIAL PRIMARY KEY,
    alimento VARCHAR(255),
    energia_kcal INT,
    proteina_g FLOAT,
    lipideos_g FLOAT,
    carboidrato_g FLOAT,
    fibra_g FLOAT,
    calcio_mg FLOAT,
    magnesio_mg FLOAT,
    manganes_mg FLOAT,
    fosforo_mg FLOAT,
    ferro_mg FLOAT,
    sodio_mg FLOAT,
    potassio_mg FLOAT,
    cobre_mg FLOAT,
    zinco_mg FLOAT,
    retinol_mcg FLOAT,
    tiamina_mg FLOAT,
    riboflavina_mg FLOAT,
    piridoxina_mg FLOAT,
    niacina_mg FLOAT,
    vitamina_c_mg FLOAT
);
"""
with engine.connect() as conn:
    conn.execute(create_table_query)

# Importar os dados do CSV para o PostgreSQL
df.to_sql('alimentos', engine, if_exists='replace', index=False)

print("Dados migrados com sucesso!")
