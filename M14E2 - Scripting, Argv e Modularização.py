import pandas as pd
import matplotlib.pyplot as plt
import os
import sys

def plota_pivot_table(df, value, index, func, ylabel, xlabel, opcao='nada'):
    if opcao == 'nada':
        pd.pivot_table(df, values=value, index=index,
                       aggfunc=func).plot(figsize=[15, 5])
    elif opcao == 'sort':
        pd.pivot_table(df, values=value, index=index,
                       aggfunc=func).sort_values(value).plot(figsize=[15, 5])
    elif opcao == 'unstack':
        pd.pivot_table(df, values=value, index=index,
                       aggfunc=func).unstack().plot(figsize=[15, 5])
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)

def gera_graficos_para_mes(mes):
    caminho_entrada = f'input/SINASC_RO_2019_{mes}.csv'
    if not os.path.exists(caminho_entrada):
        print(f'[!] Arquivo não encontrado: {caminho_entrada}')
        return

    df = pd.read_csv(caminho_entrada)
    max_data = mes  # Simplesmente usamos o mês como identificador da pasta

    output_dir = f'output/figs/{max_data}'
    os.makedirs(output_dir, exist_ok=True)

    # Gráfico 1
    plota_pivot_table(df, 'IDADEMAE', ['DTNASC', 'SEXO'], 'mean',
                      'média idade mãe', 'data de nascimento', 'unstack')
    plt.title('Média de idade da mãe por sexo')
    plt.savefig(f'{output_dir}/media_idade_mae_por_sexo.png')
    plt.close()

    # Gráfico 2
    plota_pivot_table(df, 'PESO', ['DTNASC', 'SEXO'], 'mean',
                      'média peso bebê', 'data de nascimento', 'unstack')
    plt.title('Média de peso do bebê por sexo')
    plt.savefig(f'{output_dir}/media_peso_bebe_por_sexo.png')
    plt.close()

    # Gráfico 3
    plota_pivot_table(df, 'PESO', 'ESCMAE', 'median',
                      'peso médio do bebê', 'escolaridade da mãe', 'sort')
    plt.title('Peso médio do bebê por escolaridade da mãe')
    plt.savefig(f'{output_dir}/peso_medio_por_escolaridade_mae.png')
    plt.close()

    # Gráfico 4
    plota_pivot_table(df, 'APGAR1', 'GESTACAO', 'mean',
                      'APGAR1 médio', 'gestação', 'sort')
    plt.title('APGAR1 médio por tempo de gestação')
    plt.savefig(f'{output_dir}/apgar1_medio_por_gestacao.png')
    plt.close()

    # Gráfico 5
    plota_pivot_table(df, 'APGAR5', 'GESTACAO', 'mean',
                      'APGAR5 médio', 'gestação', 'sort')
    plt.title('APGAR5 médio por tempo de gestação')
    plt.savefig(f'{output_dir}/apgar5_medio_por_gestacao.png')
    plt.close()

    print(f'[✓] Gráficos gerados para {mes} em {output_dir}/')

# Execução
for mes in sys.argv[1:]:
    gera_graficos_para_mes(mes.upper())