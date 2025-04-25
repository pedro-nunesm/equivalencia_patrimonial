import pandas as pd

def gerar_arquivo_sap(painel_lancamentos_v2, arquivo_sap_val_fixos_T, arquivo_sap_cols):
    #Definindo nome das colunas da Arquivo SAP
    arquivo_sap_cols['Nomes de Campos - Arquivo SAP'] = arquivo_sap_cols['Nomes de Campos - Arquivo SAP'].str.replace('\xa0', ' ', regex=False)
    cols = arquivo_sap_cols['Nomes de Campos - Arquivo SAP'].values
    # Inicializando o DataFrame para o arquivo SAP com as colunas necessárias
    arquivo_sap = pd.DataFrame(columns=cols)

    # Iterando sobre as linhas do DataFrame painel_lancamentos_v2
    for index, row in painel_lancamentos_v2.iterrows():
        # Verifica se o registro deve ser lançado no SAP
        if row['Lança SAP'] == 'S' and row['CCustoControladora'] != 'ERRO':
            # Monta a descrição do lançamento
            ds_cabecalho = f"{row['Empresa Origem']} >> {row['Empresa Destino']} - {row['Tipo Origem'][:50]}"
            
            # Lançamento da conta de equivalência
            lancamento_equivalencia = {
                'Empresa': row['Empresa Destino'],
                'Referencia Cabeçalho': ds_cabecalho,
                'Conta': row['Conta Destino'],
                'Centro de Custo': row['CCustoControladora'] if str(row['Conta Destino']).startswith('8') else '',
                'Centro de Lucro': arquivo_sap_val_fixos_T['Clucro'][1] if str(row['Conta Destino']).startswith('7') else '',
                'Valor': row['Valor Destino'],
                'Debito_Credito': row['Tipo Lancto Dest'],  # 'D' ou 'C'
                'Local Negocios': row['LocalNegControladora'] if row['LocalNegControladora'] != 0 else '',
                'Divisão': row['DivControladora'] if row['DivControladora'] != 0 else ''
            }
            # Adiciona o lançamento de equivalência ao DataFrame
            arquivo_sap = pd.concat([arquivo_sap, pd.DataFrame([lancamento_equivalencia])], ignore_index=True)

            # Lançamento da contrapartida de investimento
            lancamento_contrapartida = {
                'Empresa': row['Empresa Destino'],
                'Referencia Cabeçalho': ds_cabecalho,
                'Conta': row['Conta Ctp Invest'],
                'Centro de Custo': row['CCustoControladora'] if str(row['Conta Ctp Invest']).startswith('8') else '',
                'Centro de Lucro': 'Clucro' if str(row['Conta Ctp Invest']).startswith('7') else '',
                'Valor': row['Valor Destino'],
                'Debito_Credito': row['Tipo Lancto Ctpt'],  # 'D' ou 'C'
                'Local Negocios': row['LocalNegControladora'] if row['LocalNegControladora'] != 0 else '',
                'Divisão': row['DivControladora'] if row['DivControladora'] != 0 else ''
            }
            # Adiciona o lançamento de contrapartida ao DataFrame
            arquivo_sap = pd.concat([arquivo_sap, pd.DataFrame([lancamento_contrapartida])], ignore_index=True)

    return arquivo_sap

def adicionar_campos_fixos(arquivo_sap, arquivo_sap_val_fixos_T):
    # Verifica se o DataFrame arquivo_sap tem mais de uma linha
    if len(arquivo_sap) > 0:
        # Preenchendo as colunas fixas
        arquivo_sap['Data lançamento'] = arquivo_sap_val_fixos_T.loc[1, 'Data lancamento']
        arquivo_sap['Tipo Documento'] = arquivo_sap_val_fixos_T.loc[1, 'Tipo Documento']
        arquivo_sap['Moeda'] = arquivo_sap_val_fixos_T.loc[1, 'Moeda']
                # Preenchendo o Texto Cabeçalho
        arquivo_sap['Texto Cabeçalho'] = arquivo_sap['Referencia Cabeçalho']

        # Preenchendo a coluna Item com a lógica especificada
        arquivo_sap['Item'] = 1  # Inicializa a coluna com 1
        for i in range(1, len(arquivo_sap)):
            if arquivo_sap.loc[i - 1, 'Item'] == 1:
                arquivo_sap.loc[i, 'Item'] = 2
            else:
                arquivo_sap.loc[i, 'Item'] = 1

        # Preenchendo o Texto do Item
        arquivo_sap['Texto do Item'] = arquivo_sap['Referencia Cabeçalho']

        # Preenchendo o Período Contábil
        arquivo_sap['Período contábil'] = arquivo_sap_val_fixos_T.loc[1, 'Periodo contabil']

        # Preenchendo a Data de Referência
        arquivo_sap['Data de Referencia'] = arquivo_sap_val_fixos_T.loc[1, 'Data lancamento']
    
        

    return arquivo_sap