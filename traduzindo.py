import csv

# Função para remover tags HTML <i> e </i> dos nomes dos alimentos
def remover_tags(texto):
    return texto.replace('<i>', '').replace('</i>', '')

# Nome do arquivo CSV de entrada e saída
arquivo_entrada = 'TBCA.csv'
arquivo_saida = 'TBCA_PROCESSADA.csv'

# Abrir o arquivo de entrada e criar o arquivo de saída
with open(arquivo_entrada, 'r', encoding='utf-8') as csv_entrada, \
     open(arquivo_saida, 'w', newline='', encoding='utf-8') as csv_saida:

    leitor_csv = csv.reader(csv_entrada, delimiter=';')
    escritor_csv = csv.writer(csv_saida, delimiter=';')

    # Copiar cabeçalho
    cabecalho = next(leitor_csv)
    escritor_csv.writerow(cabecalho)

    # Processar cada linha de dados
    for linha in leitor_csv:
        # Remover tags <i> e </i> do nome do alimento na coluna 1 (índice 1)
        linha[1] = remover_tags(linha[1])
        
        # Escrever a linha processada no arquivo de saída
        escritor_csv.writerow(linha)

print(f'Processamento concluído. Arquivo salvo como "{arquivo_saida}"')
