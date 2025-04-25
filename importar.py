import os
import pandas as pd



def gerar_col_cta_sintet(df):
    """
    Gera a coluna 'ChaveCtaSintetica' no DataFrame baseado nas colunas 'CompanyCode' e 'GLAccount'.
    
    Args:
    df (pd.DataFrame): O DataFrame que contém as colunas 'CompanyCode' e 'GLAccount'.
    
    Returns:
    pd.DataFrame: O DataFrame com a nova coluna 'ChaveCtaSintetica'.
    """
   
    # Criar a coluna 'ChaveCtaSintetica' usando operações vetorizadas
    df['ChaveCtaSintetica'] = df['CompanyCode'].astype(str) + '#'
    
    # Verificar se GLAccount está vazia e preencher a coluna ChaveCtaSintetica
    df['ChaveCtaSintetica'] += df['GLAccount'].astype(str).apply(lambda x: f"Grupo#{x[0]}" if x else "ERRO")

    return df

def gerar_col_cta_analitica(df):
    """
    Gera a coluna 'ChaveCtaAnalitica' no DataFrame baseado nas colunas 'CompanyCode', 'GLAccountHierarchyName' e 'GLAccount'.
    
    Args:
    df (pd.DataFrame): O DataFrame que contém as colunas 'CompanyCode', 'GLAccountHierarchyName' e 'GLAccount'.
    
    Returns:
    pd.DataFrame: O DataFrame com a nova coluna 'ChaveCtaAnalitica'.
    """
    # Criar a coluna 'ChaveCtaAnalitica' usando a lógica descrita
    df['ChaveCtaAnalitica'] = df['CompanyCode'].astype(str) + '#' + df.apply(
        lambda row: str(row['GLAccount']) if pd.notna(row['GLAccount']) and str(row['GLAccount']) != '' else str(row['GLAccountHierarchyName']), axis=1
    )
    
    return df

def calcular_col_cta_subgrupo(df):
    """
    Gera a coluna 'ChaveCtaSubGrupo' no DataFrame baseado nas colunas 'CompanyCode' e 'GLAccount'.
    
    Args:
    df (pd.DataFrame): O DataFrame que contém as colunas 'CompanyCode' e 'GLAccount'.
    
    Returns:
    pd.DataFrame: O DataFrame com a nova coluna 'ChaveCtaSubGrupo'.
    """
    # Criar a coluna 'ChaveCtaSubGrupo' usando operações vetorizadas
    df['ChaveCtaSubGrupo'] = df['CompanyCode'].astype(str) + '#'
    
    # Verificar se GLAccount está vazia e preencher a coluna ChaveCtaSubGrupo
    df['ChaveCtaSubGrupo'] += df['GLAccount'].astype(str).apply(lambda x: f"SubGrupo#{x[:4]}" if pd.notna(x) and x != '' else "ERRO")
    
    return df

def calcular_movimentacao(df):
    """
    Gera a coluna 'Movimentação' no DataFrame baseado nas colunas 'Movimentacao_DC' e 'Movimentacao'.
    
    Args:
    df (pd.DataFrame): O DataFrame que contém as colunas 'Movimentacao_DC' e 'Movimentacao'.
    
    Returns:
    pd.DataFrame: O DataFrame com a nova coluna 'Movimentação'.
    """
    # Criar a coluna 'Movimentação' usando operações vetorizadas
    df['Movimentação'] = df.apply(
        lambda row: -row['Movimentacao'] if row['Movimentacao_DC'] == 'D' else row['Movimentacao'],
        axis=1
    )
    
    return df


def calcular_col_saldo_inicial(df):
    """
    Gera a coluna 'SaldoInicial' no DataFrame baseado nas colunas 'StartingBalanceAmtInCoCodeCrcy_DC' e 'StartingBalanceAmtInCoCodeCrcy'.
    
    Args:
    df (pd.DataFrame): O DataFrame que contém as colunas 'StartingBalanceAmtInCoCodeCrcy_DC' e 'StartingBalanceAmtInCoCodeCrcy'.
    
    Returns:
    pd.DataFrame: O DataFrame com a nova coluna 'SaldoInicial'.
    """
    # Criar a coluna 'SaldoInicial' usando operações vetorizadas
    df['SaldoInicial'] = df.apply(
        lambda row: -row['StartingBalanceAmtInCoCodeCrcy'] if row['StartingBalanceAmtInCoCodeCrcy_DC'] == 'D' else row['StartingBalanceAmtInCoCodeCrcy'],
        axis=1
    )
    
    return df

def calcular_col_saldo_final(df):
    """
    Gera a coluna 'SaldoFinal' no DataFrame baseado nas colunas 'EndingBalanceAmtInCoCodeCrcy_DC' e 'EndingBalanceAmtInCoCodeCrcy'.
    
    Args:
    df (pd.DataFrame): O DataFrame que contém as colunas 'EndingBalanceAmtInCoCodeCrcy_DC' e 'EndingBalanceAmtInCoCodeCrcy'.
    
    Returns:
    pd.DataFrame: O DataFrame com a nova coluna 'SaldoFinal'.
    """
    # Criar a coluna 'SaldoFinal' usando operações vetorizadas
    df['SaldoFinal'] = df.apply(
        lambda row: -row['EndingBalanceAmtInCoCodeCrcy'] if row['EndingBalanceAmtInCoCodeCrcy_DC'] == 'D' else row['EndingBalanceAmtInCoCodeCrcy'],
        axis=1
    )
    
    return df

def processar_balancete(df):
    # Chamar a função para gerar a coluna 'ChaveCtaSintetica'
    df = gerar_col_cta_sintet(df)
    
    # Chamar a função para calcular a coluna 'ChaveCtaAnlitica'
    df = gerar_col_cta_analitica(df)

    #Chama a função para calcular a coluna "ChaveCtaSubGrupo"
    df = calcular_col_cta_subgrupo(df)

    #Chama a função para calcular a coluna "Movimentação"
    df = calcular_movimentacao(df)

    #Chama a função para calcular a coluna "Saldo Inicial"
    df = calcular_col_saldo_inicial(df)

    #Chama a função para calcular a coluna "Saldo Final"
    df = calcular_col_saldo_final(df)

    # Definir a ordem das colunas
    nova_ordem = [
        'CompanyCode', 'GLAccount', 'GLAccountHierarchyName',
        'StartingBalanceAmtInCoCodeCrcy', 'StartingBalanceAmtInCoCodeCrcy_DC',
        'DebitAmountInCoCodeCrcy', 'DebitAmountInCoCodeCrcy_DC',
        'CreditAmountInCoCodeCrcy', 'CreditAmountInCoCodeCrcy_DC',
        'Movimentacao', 'Movimentacao_DC', 
        'EndingBalanceAmtInCoCodeCrcy', 'EndingBalanceAmtInCoCodeCrcy_DC',
        'ChaveCtaSintetica', 'Movimentação', 'SaldoInicial', 'SaldoFinal',
        'ChaveCtaAnalitica', 'ChaveCtaSubGrupo'
    ]

    # Reorganizar as colunas conforme a nova ordem
    df = df[nova_ordem]
    return df