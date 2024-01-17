import pandas as pd


def processa_aposentadoria(planilha_path):
    # Carrega a planilha
    df_servidores = pd.read_excel(planilha_path, sheet_name="Servidores")

    # Tentativa de conversão da coluna 'datanascimento' com diferentes formatos
    try:
        df_servidores['datanascimento'] = pd.to_datetime(
            df_servidores['datanascimento'], format='%Y%m%d')
    except ValueError:
        df_servidores['datanascimento'] = pd.to_datetime(
            df_servidores['datanascimento'], errors='coerce')

    # Calcula a idade com base na data de nascimento
    df_servidores['idade'] = (pd.to_datetime(
        'now') - df_servidores['datanascimento']).dt.total_seconds() / (365.25 * 24 * 3600)

    # Aplica a regra para determinar se é aposentável
    df_servidores['aposentável'] = (
        (df_servidores['codsexo'] == 'F') & (df_servidores['idade'] > 60) |
        (df_servidores['codsexo'] == 'M') & (df_servidores['idade'] > 65)
    )

    # Formata a coluna 'datanascimento' para o formato desejado
    df_servidores['datanascimento'] = df_servidores['datanascimento'].dt.strftime(
        '%Y-%m-%d')

    # Seleciona apenas as colunas necessárias
    df_resultado = df_servidores[[
        'nome', 'codsexo', 'datanascimento', 'aposentável']]

    return df_resultado


# Caminho do arquivo da planilha
arquivo_planilha = 'Estudo_de_Caso_PGFN.xlsx'

# Processa a aposentadoria e exibe o resultado
resultado = processa_aposentadoria(arquivo_planilha)
print(resultado)
