import pandas as pd
from sqlalchemy import create_engine, text

# Caminho para o arquivo CSV
csv_path = 'alimentos.csv'

# Configurar a conexão com o PostgreSQL
postgres_url = 'postgresql://postgres.ocphuexqtlflnvylcpou:qNNMqRMUuSMkwGDB@aws-0-sa-east-1.pooler.supabase.com:6543/postgres'
engine = create_engine(postgres_url)

# Definir a estrutura da tabela no PostgreSQL
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

# Executar a consulta de criação da tabela
with engine.connect() as conn:
    conn.execute(text(create_table_query))

# Carregar os dados do CSV para um DataFrame do Pandas
df = pd.read_csv(csv_path)

# Importar os dados para a tabela 'alimentos' no PostgreSQL
df.to_sql('alimentos', engine, if_exists='replace', index=False)

print("Dados migrados com sucesso!")
