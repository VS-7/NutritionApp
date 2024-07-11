import pandas as pd
import sqlite3

# Passo 1: Ler o arquivo CSV
file_path = 'TACO.csv'  # substitua pelo caminho do seu arquivo
df = pd.read_csv(file_path, delimiter=',')  # ajuste o delimitador conforme necessário

# Passo 2: Tratar os dados
# Converter valores com vírgula para ponto decimal nas colunas numéricas
numeric_columns = df.columns[2:]  # pular 'id' e 'alimento'
for column in numeric_columns:
    df[column] = df[column].astype(str).str.replace(',', '.')

# Substituir valores "NA", "Tr", e valores em branco por None
df.replace({'NA': None, 'Tr': None, '': None}, inplace=True)

# Converter tipos de dados apropriados nas colunas numéricas
for column in numeric_columns:
    df[column] = pd.to_numeric(df[column], errors='coerce')

# Renomear colunas para corresponder aos nomes na tabela SQLite
df.columns = [
    'id', 'alimento', 'Umidade', 'Caloria_kcal', 'Caloria_kJ', 'Proteina', 'Lipideos',
    'Colesterol', 'Carboidrato', 'Fibra_Alimentar', 'Cinzas', 'Calcio', 'Magnesio',
    'Manganes', 'Fosforo', 'Ferro', 'Sodio', 'Potassio', 'Cobre', 'Zinco', 'Retinol',
    'RE', 'RAE', 'Tiamina', 'Riboflavina', 'Piridoxina', 'Niacina', 'Vitamina_C'
]

# Passo 3: Criar e popular a tabela no SQLite
conn = sqlite3.connect('tabela_alimentos.db')
cursor = conn.cursor()

# Criação da tabela
cursor.execute('''
    CREATE TABLE IF NOT EXISTS alimentos (
        id INTEGER PRIMARY KEY,
        alimento TEXT,
        Umidade REAL,
        Caloria_kcal REAL,
        Caloria_kJ REAL,
        Proteina REAL,
        Lipideos REAL,
        Colesterol REAL,
        Carboidrato REAL,
        Fibra_Alimentar REAL,
        Cinzas REAL,
        Calcio REAL,
        Magnesio REAL,
        Manganes REAL,
        Fosforo REAL,
        Ferro REAL,
        Sodio REAL,
        Potassio REAL,
        Cobre REAL,
        Zinco REAL,
        Retinol REAL,
        RE REAL,
        RAE REAL,
        Tiamina REAL,
        Riboflavina REAL,
        Piridoxina REAL,
        Niacina REAL,
        Vitamina_C REAL
    )
''')

# Inserção dos dados
df.to_sql('alimentos', conn, if_exists='append', index=False)

# Fechar a conexão
conn.close()
