#PONTOS DE ATENÇÃO: EVENTOS COMEÇANDO EM DELTA ESÃO SENDO LANÇADOS CONSIDERANDO O VALOR DO SALDO INICIAL. A EMPRESA FIBX E EXIC POSSUEM DOIS CÓDIGOS DE CENTRO DE CUSTO (CONFERIR CADASTRO EMPRESAS) - ESTOU PEGANDO APENAS A PRIMEIRA OCORRÊNCIA, IGUAL O PROCV

import os
import pandas as pd
from datetime import datetime
from unidecode import unidecode
from importar import gerar_col_cta_sintet, gerar_col_cta_analitica, calcular_col_cta_subgrupo, calcular_movimentacao, calcular_col_saldo_inicial, calcular_col_saldo_final, processar_balancete
from gerar_painel import calcular_valor_lancamento, gera_painel_lancamentos, gerar_dicionario_hierarquia, gera_painel_lancamentos_v2
from gerar_sap import gerar_arquivo_sap, adicionar_campos_fixos

def listar_pastas():
    # Definir o caminho da pasta de entrada
    input_dir = os.path.join('Input', 'Balancetes', 'API')

    # Listar pastas no diretório
    pastas = [d for d in os.listdir(input_dir) if os.path.isdir(os.path.join(input_dir, d))]

    if not pastas:
        print("Não há pastas disponíveis.")
        return None

    # Mostrar as pastas disponíveis e solicitar ao usuário que escolha uma
    print("Pastas disponíveis:")
    for i, pasta in enumerate(pastas):
        print(f"{i + 1}: {pasta}")

    escolha = int(input("Escolha o número da pasta que deseja acessar: ")) - 1

    # Verificar se a escolha é válida
    if escolha < 0 or escolha >= len(pastas):
        print("Escolha inválida.")
        return None

    # Retornar o nome da pasta escolhida
    return pastas[escolha]

def listar_arquivos(pasta):
    # Definir o caminho da pasta escolhida
    input_dir = os.path.join('Input', 'Balancetes', 'API', pasta)

    # Listar arquivos .xlsx na pasta
    arquivos = [f for f in os.listdir(input_dir) if f.endswith('.xlsx')]
    
    if not arquivos:
        print("Não há arquivos Excel na pasta correspondente.")
        return None

    # Mostrar os arquivos disponíveis e solicitar ao usuário que escolha um
    print("Arquivos disponíveis:")
    for i, arquivo in enumerate(arquivos):
        print(f"{i + 1}: {arquivo}")
    
    escolha = int(input("Escolha o número do arquivo que deseja carregar: ")) - 1
    
    # Verificar se a escolha é válida
    if escolha < 0 or escolha >= len(arquivos):
        print("Escolha inválida.")
        return None
    
    # Retornar o caminho completo do arquivo escolhido
    return os.path.join(input_dir, arquivos[escolha])


##MACRO IMPORTAR----------------------

# Escolher passta
pasta_escolhida = listar_pastas()

if pasta_escolhida is not None:
    arquivo_escolhido = listar_arquivos(pasta_escolhida)

    if arquivo_escolhido is not None:
        print(f"O arquivo escolhido foi:\n{arquivo_escolhido}")
        df = pd.read_excel(arquivo_escolhido)

        # Normalizar os nomes das colunas, se necessário
        df.columns = df.columns.str.strip()  # Remove espaços em branco

        # Processar o balancete
        balancete_atual = processar_balancete(df)
        print('Balancete Processado!')


##MACRO GERAR PAINEL----------------------

# Carregar Cadastro Empresas
cad_emp = pd.read_excel('tb_aux.xlsx', 'Cadastro_Empresas', dtype={'Local Negócios Controladora': str})

#Limpar coluna Conta Ctp Investimento na Controladora
cad_emp['Conta Ctp Investimento na Controladora'] = cad_emp['Conta Ctp Investimento na Controladora']\
    .apply(lambda x: str(int(x)) if pd.notna(x) else '')
#Limpar coluna Centro de Custo Controladora
cad_emp['Centro de Custo Controladora'] = cad_emp['Centro de Custo Controladora']\
    .apply(lambda x: str(int(x)) if pd.notna(x) else '')

#Carregar Dividendos Desproporcionais
divi_den = pd.read_excel('tb_aux.xlsx', 'Dividendos_Desproporcionais')

#Carregar Cadastro Eventos Doador
cad_ev_doa = pd.read_excel('tb_aux.xlsx', 'Cadastro_Eventos_Doador')

#Carregar Cadastro Eventos Receptor
cad_ev_recep = pd.read_excel('tb_aux.xlsx', 'Cadastro_Eventos_Receptor', usecols='G').dropna()

#Carregar Grade Recep
grad_recep = pd.read_excel('tb_aux.xlsx', 'Grade_Receptora')

#Inserir coluna Chave Doador
grad_recep.insert(3, 'Chave Doador', grad_recep['Cod Empresa Controladora'] + "#" + grad_recep['Tipo de Evento Doador'])

#Inserir coluna Chave Receptor
grad_recep.insert(4, 'Chave Receptor', grad_recep['Cod Empresa Controladora'] + "#" + grad_recep['Tipo de Evento Receptor'])

#Preencher as contas no caso de Dividendos Desproporcionais
mapa_cta_ajuste = divi_den.set_index('Sigla')['Cta Ajuste Dividendos da Controladora (Lancto)'].to_dict()
grad_recep.loc[
    grad_recep['Tipo de Evento Doador'] == 'DIVI DESPROPORCIONAIS',
    'Conta Receptora da Controladora 1 - CRED'
] = grad_recep['Cod Empresa Controladora'].map(mapa_cta_ajuste).combine_first(
    grad_recep['Conta Receptora da Controladora 1 - CRED']
)
grad_recep[grad_recep['Tipo de Evento Doador'] == 'DIVI DESPROPORCIONAIS']

# Carregar Cadastro Participacao
cad_part = pd.read_excel('tb_aux.xlsx', 'Cadastro_Participacao', header=None)

# Preencher as células mescladas com o valor da célula superior (apenas para as colunas até a 10ª)
cad_part.iloc[0, :10] = cad_part.iloc[0, :10].fillna(method='ffill')

# Remove as colunas 10, 12 e 13 (índices 9, 11 e 12)
cad_part = cad_part.drop(cad_part.columns[[10, 12, 13]], axis=1)

# Preenche os valores NaN no cabeçalho superior com os valores correspondentes do cabeçalho inferior
cad_part.iloc[0, :] = cad_part.iloc[0, :].fillna(cad_part.iloc[1, :])

# Cria o novo cabeçalho combinando as duas linhas, mas verificando se são iguais ou diferentes
new_columns = [
    f"{cad_part.iloc[0, col]}_{cad_part.iloc[1, col]}" if cad_part.iloc[0, col] != cad_part.iloc[1, col] 
    else cad_part.iloc[0, col] for col in range(len(cad_part.columns))
]
# Atribui o novo cabeçalho ao DataFrame
cad_part.columns = new_columns
# Remove as primeiras duas linhas (usadas como cabeçalhos)
cad_part = cad_part.drop([0, 1]).reset_index(drop=True)


#Carregar Grade Doadora v0
grad_doa_v0 = pd.read_excel('tb_aux.xlsx', 'Grade_Doadora')


# Fazendo o merge com a cad_emp para trazer a coluna Nome da Empresa, Nível Controlada Conta Ctp Invest Controladora
grad_doa_v0 = grad_doa_v0.merge(cad_emp[['Cod Controlada SAP', 'Nome da Empresa', 'Nível Controlada', 'Conta Ctp Investimento na Controladora']], 
                                left_on='Cod Empresa', right_on='Cod Controlada SAP', 
                                how='left')
grad_doa_v0['Nome da Empresa'] = grad_doa_v0['Nome da Empresa'].str.upper()
grad_doa_v0.rename({'Nome da Empresa':'Empresa'}, axis=1, inplace=True)
grad_doa_v0['Nível Empresa'] = grad_doa_v0.apply(lambda row: row['Nível Controlada'] if pd.notna(row['Nível Controlada']) else "###Não cadastrada!##", axis=1)
grad_doa_v0['Conta Ctp Invest Controladora'] = grad_doa_v0.apply(lambda row: row['Conta Ctp Investimento na Controladora'] if pd.notna(row['Conta Ctp Investimento na Controladora']) else "###Não cadastrada!##", axis=1)



# Removendo a coluna 'Cod Controlada SAP', pois não é necessária
grad_doa_v0.drop('Cod Controlada SAP', axis=1, inplace=True)


#Inserindo a coluna Chave Doadora
grad_doa_v0.insert(4, 'Chave Doadora', grad_doa_v0['Cod Empresa'] + "#" + grad_doa_v0['Tipo de Evento Doador'])

# Inserindo a coluna Lança SAP
grad_doa_v0 = grad_doa_v0.merge(cad_ev_doa[['Tipo Evento', 'Lança SAP']], 
                                left_on='Tipo de Evento Doador', right_on='Tipo Evento', 
                                how='left')



# Aplicar a função para cada linha de grad_doa_v0
grad_doa_v1 = calcular_valor_lancamento(grad_doa_v0, balancete_atual, cad_part)

#Criar coluna Sinal Lançto
grad_doa_v1['Sinal Lançto'] = grad_doa_v1['Valor Lançamento'].apply(lambda x: "D" if x < 0 else "C")

grad_doa_v1.drop(['Nível Controlada', 'Conta Ctp Investimento na Controladora', 'Tipo Evento'], inplace=True, axis=1)

#Reordenar Dataframe
nova_ordem = [
    'Cod Empresa', 'Empresa', 'Origem', 'Tipo de Evento Doador', 'Chave Doadora', 
    'Lança SAP', 'Sinal Lançto', 'Valor Lançamento', 'Nível Empresa', 
    'Conta Ctp Invest Controladora', 'Conta Sintética da Controlada 1', 
    'Conta Sintética da Controlada 2', 'Conta Sintética da Controlada 3', 
    'Conta Subgrupo da Controlada 1', 'Conta Analítica da Controlada 1', 
    'Conta Analítica da Controlada 2', 'Conta Analítica da Controlada 3', 
    'Conta Analítica da Controlada 4', 'Conta Analítica da Controlada 5', 
    'Conta Analítica da Controlada 6', 'Conta Analítica da Controlada 7', 
    'Conta Analítica da Controlada 8', 'Conta Analítica da Controlada 9', 
    'Conta Analítica da Controlada 11', 'Conta Analítica da Controlada 9', 
    'Conta Analítica da Controlada 12'
]

# Reorganizando as colunas no DataFrame
grad_doa_v1 = grad_doa_v1[nova_ordem]


#Carregando o código de todas as empresas cadastradas para gerar o dicionario_hierarquia (Funcionará como Organograma)
organog = cad_emp[['Cod Controlada SAP']]

#Gerar Painel Lançamentos
painel_lancamentos = gera_painel_lancamentos(grad_doa_v1)

# Gerando o dicionário de hierarquia
dicionario_hierarquia = gerar_dicionario_hierarquia(organog, cad_emp, cad_part)


Tp_Recep_DividendoDesproporcional = cad_ev_recep.loc[0, 'Tipo Especial - Exceção']


#Adicionar campos fixos no Painel Lançamentos
painel_lancamentos_v2 = gera_painel_lancamentos_v2(painel_lancamentos, dicionario_hierarquia, Tp_Recep_DividendoDesproporcional, grad_recep, grad_doa_v1, cad_emp)


#MACRO GERAR SAP

arquivo_sap_cols = pd.read_excel('tb_aux.xlsx', sheet_name='Config_SAP', usecols='D')
arquivo_sap_val_fixos = pd.read_excel('tb_aux.xlsx', sheet_name='Config_SAP', usecols='A:B')
arquivo_sap_val_fixos_T = arquivo_sap_val_fixos.T.reset_index(drop=True).dropna(axis=1, how='all')
arquivo_sap_val_fixos_T.columns = arquivo_sap_val_fixos_T.iloc[0]
arquivo_sap_val_fixos_T = arquivo_sap_val_fixos_T.drop(0)
arquivo_sap_val_fixos_T.columns = [
    unidecode(col.strip().replace(' ', '_')) for col in arquivo_sap_val_fixos_T.columns
]


arquivo_sap = gerar_arquivo_sap(painel_lancamentos_v2, arquivo_sap_val_fixos_T, arquivo_sap_cols)
        
arquivo_sap_v2 = adicionar_campos_fixos(arquivo_sap, arquivo_sap_val_fixos_T)
arquivo_sap_v2.to_excel('plc_NFGR_NFHS_NFIS_NFLT.xlsx', index=False)

#TESTES
import os
caminho_base = 'Input/Balancetes/API/2025_04_08'
arquivo_entrada = 'Balancete_2025_04_08_20_36_32.xlsx'
caminho_entrada = os.path.join(caminho_base, arquivo_entrada)
df = pd.read_excel(caminho_entrada)
valores_filtrar = ['FIB3', 'NFPJ', 'NFMF']
df_filtrado = df[df['CompanyCode'].isin(valores_filtrar)]
nome_filtros = '_'.join(valores_filtrar)
arquivo_saida = f'{nome_filtros}.xlsx'
caminho_saida = os.path.join(caminho_base, arquivo_saida)
df_filtrado.to_excel(caminho_saida, index=False)


#cad_emp_dict_ccusto = cad_emp.set_index("Cod SAP Controladora")["Centro de Custo Controladora"].to_dict()
#cad_emp_dict_ccusto = (cad_emp.drop_duplicates(subset="Cod SAP Controladora", keep="first").set_index("Cod SAP Controladora")["Centro de Custo Controladora"].to_dict()) 

# Conta quantas vezes cada combinação empresa x centro de custo aparece
frequencia = (
    cad_emp
    .groupby(["Cod SAP Controladora", "Centro de Custo Controladora"])
    .size()
    .reset_index(name="Contagem")
)

# Seleciona o centro de custo com mais ocorrências por empresa
mais_frequente = (
    frequencia
    .sort_values("Contagem", ascending=False)
    .drop_duplicates(subset="Cod SAP Controladora", keep="first")
)

# Cria o dicionário
cad_emp_dict_ccusto = mais_frequente.set_index("Cod SAP Controladora")["Centro de Custo Controladora"].to_dict()

painel_lancamentos_v2["CCustoControladora"] = painel_lancamentos_v2["Empresa Destino"].map(cad_emp_dict_ccusto).fillna("ERRO")
cad_emp_dict_ccusto['EXIC']
cad_emp[cad_emp['Cod SAP Controladora'] == 'EXIC']