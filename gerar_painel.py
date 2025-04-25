import pandas as pd

def calcular_valor_lancamento(df, balancete_atual, cad_part):
    """
    Gera a coluna 'Valor Lançamento' no DataFrame baseado nas colunas 'Tipo de Evento Doador' e 'Cod Empresa'.
    
    Args:
    df (pd.DataFrame): O DataFrame que contém as colunas 'Tipo de Evento Doador', 'Cod Empresa', 'Conta Sintética da Controlada 1', 
                       'Conta Sintética da Controlada 2', 'Conta Sintética da Controlada 3', e 'Conta Subgrupo da Controlada 1'.
    balancete_atual (pd.DataFrame): O DataFrame que contém as colunas 'ChaveCtaSintetica', 'ChaveCtaAnalitica' e 'SaldoInicial'.
    cad_participacao (pd.DataFrame): O DataFrame que contém as colunas 'Sigla' e '(D) Part'.
    
    Returns:
    pd.DataFrame: O DataFrame com a nova coluna 'Valor Lançamento'.
    """
    
    # Criar a coluna 'Valor Lançamento'
    def calcular_lancamento(row):
        tipo_evento = row['Tipo de Evento Doador']
        cod_empresa = row['Cod Empresa']
        conta_sintetica_1 = row['Conta Sintética da Controlada 1']
        conta_sintetica_2 = row['Conta Sintética da Controlada 2']
        conta_sintetica_3 = row['Conta Sintética da Controlada 3']
        conta_subgrupo_1 = int(row['Conta Subgrupo da Controlada 1']) if pd.notna(row['Conta Subgrupo da Controlada 1']) else 0
        conta_analitica_1 = int(row['Conta Analítica da Controlada 1']) if pd.notna(row['Conta Analítica da Controlada 1']) else 0
        conta_analitica_2 = int(row['Conta Analítica da Controlada 2']) if pd.notna(row['Conta Analítica da Controlada 2']) else 0
        conta_analitica_3 = int(row['Conta Analítica da Controlada 3']) if pd.notna(row['Conta Analítica da Controlada 3']) else 0
        conta_analitica_4 = int(row['Conta Analítica da Controlada 4']) if pd.notna(row['Conta Analítica da Controlada 4']) else 0
        conta_analitica_5 = int(row['Conta Analítica da Controlada 5']) if pd.notna(row['Conta Analítica da Controlada 5']) else 0
        conta_analitica_6 = int(row['Conta Analítica da Controlada 6']) if pd.notna(row['Conta Analítica da Controlada 6']) else 0
        conta_analitica_7 = int(row['Conta Analítica da Controlada 7']) if pd.notna(row['Conta Analítica da Controlada 7']) else 0
        conta_analitica_8 = int(row['Conta Analítica da Controlada 8']) if pd.notna(row['Conta Analítica da Controlada 8']) else 0
        conta_analitica_9 = int(row['Conta Analítica da Controlada 9']) if pd.notna(row['Conta Analítica da Controlada 9']) else 0
        conta_analitica_10 = int(row['Conta Analítica da Controlada 10']) if pd.notna(row['Conta Analítica da Controlada 10']) else 0
        conta_analitica_11 = int(row['Conta Analítica da Controlada 11']) if pd.notna(row['Conta Analítica da Controlada 11']) else 0
        conta_analitica_12 = int(row['Conta Analítica da Controlada 12']) if pd.notna(row['Conta Analítica da Controlada 12']) else 0

        # Inicializa o valor de lançamento
        valor_lancamento = 0

        # Verifica se o tipo de evento começa com "DELTA"
        if tipo_evento.startswith("DELTA"):
            # Somar valores da coluna 'SaldoInicial' para ChaveCtaSintetica
            for conta in [conta_sintetica_1, conta_sintetica_2, conta_sintetica_3]:
                chave = f"{cod_empresa}#{conta}"
                saldo = balancete_atual.loc[balancete_atual['ChaveCtaSintetica'] == chave, 'SaldoInicial'].sum()
                valor_lancamento += saldo
        
                # Printar o valor adicionado e a chave
                if saldo != 0:  # Apenas printar se existir
                    print(f"[{tipo_evento}] - Adicionando {saldo} à variável valor_lancamento para a chave '{chave}'")

            # Verificar a conta analítica 1 na ChaveCtaAnalitica
            chave_analitica = f"{cod_empresa}#{conta_analitica_1}"
            saldo_analitico = balancete_atual.loc[balancete_atual['ChaveCtaAnalitica'] == chave_analitica, 'SaldoInicial'].sum()
            valor_lancamento += saldo_analitico
    
            # Printar o valor adicionado e a chave analítica
            if saldo_analitico != 0:  # Apenas printar se existir
                print(f"[{tipo_evento}] - Adicionando {saldo_analitico} à variável valor_lancamento para a chave '{chave_analitica}'")

            # Multiplicar pelo valor da participação
            participacao = cad_part.loc[cad_part['Sigla'] == cod_empresa, '(D) Part'].values
            if participacao.size > 0:  # Verifica se a participação foi encontrada
                valor_lancamento *= participacao[0]  # Multiplica pelo primeiro valor encontrado
        else:
            # Somar valores da coluna 'Movimentação' para ChaveCtaSintetica
            for conta in [conta_sintetica_1, conta_sintetica_2, conta_sintetica_3, conta_subgrupo_1]:
                chave = f"{cod_empresa}#{conta}"
                movimentacao = balancete_atual.loc[balancete_atual['ChaveCtaSintetica'] == chave, 'Movimentação'].sum()
                valor_lancamento += movimentacao
                
                # Printar o valor adicionado e a chave
                if movimentacao != 0:  # Apenas printar se existir
                    print(f"[{tipo_evento}]- Adicionando {movimentacao} à variável valor_lancamento para a chave '{chave}'")
             # Somar valores da coluna 'Movimentação' para ChaveCtaAnalitica
            for conta in [conta_analitica_1, conta_analitica_2, conta_analitica_3, conta_analitica_4,
                conta_analitica_5, conta_analitica_6, conta_analitica_7, conta_analitica_8,
                conta_analitica_9, conta_analitica_10, conta_analitica_11, conta_analitica_12]:

                if conta != 0:  # Verifica se a conta existe
                    chave = f"{cod_empresa}#{conta}"
                    movimentacao = balancete_atual.loc[balancete_atual['ChaveCtaAnalitica'] == chave, 'Movimentação'].sum()
                    valor_lancamento += movimentacao
                    if movimentacao != 0:  # Apenas printar se existir
                        print(f"[{tipo_evento}]- Adicionando {movimentacao} à variável valor_lancamento para a chave '{chave}'")

        return valor_lancamento

    # Aplicar a função calcular_lancamento a cada linha do DataFrame
    df['Valor Lançamento'] = df.apply(calcular_lancamento, axis=1)
    
    return df

def gera_painel_lancamentos(grad_doa_v1):
    # Lista para armazenar as linhas do painel
    linhas = []

    # Percorre todas as linhas da Grade Doadora (grad_doa_v1)
    for linha_entrada in range(len(grad_doa_v1)):
        valor_lancto = round(abs(grad_doa_v1.loc[linha_entrada, 'Valor Lançamento']), 2)
        
        if valor_lancto > 0:  # Existe valor a lançar
            empresa_origem = grad_doa_v1.loc[linha_entrada, 'Cod Empresa']
            tipo_origem = grad_doa_v1.loc[linha_entrada, 'Tipo de Evento Doador']
            nivel_empresa = int(grad_doa_v1.loc[linha_entrada, 'Nível Empresa'])
            tipo_lancto = grad_doa_v1.loc[linha_entrada, 'Sinal Lançto']
            
            # Garantir que o Nível Destino não seja menor que 1
            for i in range(nivel_empresa - 1):
                nivel_destino = nivel_empresa - 1 - i  # Garantir que Nível Destino seja >= 1

                if nivel_destino < 1:
                    break
                
                nova_linha = {
                    "Empresa Origem": empresa_origem,
                    "Nível Destino": nivel_destino,  # Nível de destino não pode ser 0
                    "Tipo Origem": tipo_origem,
                    "Valor Origem": valor_lancto,
                    "Tipo Lancto Dest": tipo_lancto,
                    "Nível Origem": nivel_empresa,
                }
                
                # Adiciona a nova linha na lista de linhas
                linhas.append(nova_linha)

    # Converte a lista de dicionários em um DataFrame
    painel_lancamentos = pd.DataFrame(linhas)

    # O dataframe `painel_lancamentos` já contém os dados processados
    return painel_lancamentos



def gerar_dicionario_hierarquia(organog, cad_emp, cad_part):
    # Limpeza da coluna Controlada (remover valores vazios e 'Preencher')
    organog_clean = organog[organog['Cod Controlada SAP'].notna() & (organog['Cod Controlada SAP'] != 'Preencher')]

    # Dicionário para armazenar a hierarquia das empresas
    hierarquia_dict = {}

    # Iterando sobre cada código de empresa no DataFrame organog
    for empresa in organog_clean['Cod Controlada SAP']:
        hierarquia = []  # Lista para armazenar a hierarquia de controladoras
        empresa_atual = empresa  # Variável para armazenar a empresa controladora atual
        hierarquia.append(empresa_atual)  # Adiciona a empresa de origem na hierarquia

        # Loop para buscar a hierarquia das controladoras
        while True:
            controladora = cad_emp[cad_emp['Cod Controlada SAP'] == empresa_atual]['Cod SAP Controladora'].values
            
            if len(controladora) == 0 or pd.isna(controladora[0]):
                break  # Interrompe o loop se não houver controladora
            
            empresa_atual = controladora[0]  # Atualiza para a nova controladora
            hierarquia.append(empresa_atual)

        # Inverte a hierarquia para começar da controladora mais alta
        hierarquia.reverse()

        # Construindo a hierarquia numerada com os dicionários exigidos
        hierarquia_numerada = {}
        percentual_indireto = 0  # Inicializa o percentual indireto da última empresa
        percentuais = []  # Lista auxiliar para armazenar os percentuais de controle

        for i in range(len(hierarquia)):
            if i == len(hierarquia) - 1:
                percentual = 0  # A última empresa sempre tem percentual 0
            else:
                percentual = cad_part[cad_part['Sigla'] == hierarquia[i + 1]].iloc[:, 9].values
                percentual = percentual[0] if len(percentual) > 0 else 1
            
            percentuais.append(percentual)
        
        # Calculando os percentuais indiretos de trás para frente
        for i in range(len(hierarquia) - 1, -1, -1):
            if i == len(hierarquia) - 1:
                percentual_indireto = 0  # O mais baixo da hierarquia tem 0
            elif i == len(hierarquia) - 2:
                percentual_indireto = percentuais[i]  # O próximo da hierarquia recebe ele mesmo
            else:
                percentual_indireto = percentuais[i] * percentual_indireto  # Multiplicação acumulada
            
            hierarquia_numerada[i + 1] = {
                'Empresa': hierarquia[i],
                '%_Controlador_na_Controlada': percentuais[i] if i < len(percentuais) else 0,
                '%_Indireta': percentual_indireto
            }

        #Ordena a hierarquia 
        hierarquia_numerada = dict(sorted(hierarquia_numerada.items()))
        # Adiciona ao dicionário final
        hierarquia_dict[empresa] = hierarquia_numerada

    return hierarquia_dict

def gera_painel_lancamentos_v2(painel_lancamentos_v0, dicionario_hierarquia, Tp_Recep_DividendoDesproporcional, grad_recep, grade_doa, cad_emp):
    # Iniciar painel_lancamentos_v2 como uma cópia do painel_lancamentos_v0
    painel_lancamentos_v2 = painel_lancamentos_v0.copy()
    
    # 1. Gerar a coluna "Empresa Destino"
    painel_lancamentos_v2['Empresa Destino'] = painel_lancamentos_v2.apply(
        lambda row: dicionario_hierarquia.get(row['Empresa Origem'], {}).get(row['Nível Destino'], {}).get('Empresa', None),
        axis=1
    )

    # 2. Calcular "Tipo Destino"
    grad_recep_dict = grad_recep.set_index("Chave Doador")["Tipo de Evento Receptor"].to_dict()
    
    def calcular_tipo_destino(row):
        if row["Tipo Origem"] == "DIVI DESPROPORCIONAIS" and row["Nível Destino"] == 1:
            return Tp_Recep_DividendoDesproporcional
        
        chave_busca = f"{row['Empresa Destino']}#{row['Tipo Origem']}"
        return grad_recep_dict.get(chave_busca, "ERRO")
    
    painel_lancamentos_v2["Tipo Destino"] = painel_lancamentos_v2.apply(calcular_tipo_destino, axis=1)
    
    # 3. Calcular "% Destino"
    def calcular_percentual_destino(row):
        # Verifica a condição especial
        if row["Tipo Origem"] in ["DIVI DESPROPORCIONAIS", "DELTA APORTE"] and \
           (row["Nível Origem"] - row["Nível Destino"]) == 1:
            return 1
        
        # Busca o percentual indireto no dicionário de hierarquia
        return dicionario_hierarquia.get(row['Empresa Origem'], {}).get(row['Nível Destino'], {}).get('%_Indireta', None)
    
    painel_lancamentos_v2["% Destino"] = painel_lancamentos_v2.apply(calcular_percentual_destino, axis=1)
    # 4. Calcular "Valor Destino"
    painel_lancamentos_v2["Valor Destino"] = (painel_lancamentos_v2["% Destino"] * painel_lancamentos_v2["Valor Origem"]).round(2)

    #5. Criando a ChaveLancto 
    painel_lancamentos_v2['ChaveLancto'] = painel_lancamentos_v2.apply(
        lambda row: "RESULTADO DE EQUIVALÊNCIA" if row['Tipo Origem'] == "DIVI DESPROPORCIONAIS" else row['Tipo Destino'], axis=1
    )
    

    # 6. Calcular Conta Destino
    grad_recep_dict_conta_cred = grad_recep.set_index("Chave Receptor")["Conta Receptora da Controladora 1 - CRED"].to_dict()
    grad_recep_dict_conta_deb = grad_recep.set_index("Chave Receptor")["Conta Receptora da Controladora 2 - DEB"].to_dict()
    
    def calcular_conta_destino(row):
        empresa_destino = dicionario_hierarquia.get(row['Empresa Origem'], {}).get(row['Nível Destino'] + 1, {}).get('Empresa', None)
        if empresa_destino is None:
            return "ERRO"
        
        chave_receptor = f"{empresa_destino}#{row['ChaveLancto']}"
        
        if row["Tipo Lancto Dest"] == "D":
            conta = grad_recep_dict_conta_deb.get(chave_receptor, "ERRO")
        else:
            conta = grad_recep_dict_conta_cred.get(chave_receptor, "ERRO")

        if pd.isna(conta):
            return ""
        
            # Converte para string e remove parte decimal, se houver
        try:
            conta_str = str(conta).split('.')[0]  # remove qualquer parte decimal
            if not conta_str.isdigit():
                return "ERRO"
            return conta_str
        except Exception:
            return "ERRO"
    
    painel_lancamentos_v2["Conta Destino"] = painel_lancamentos_v2.apply(calcular_conta_destino, axis=1)


    # 7. Calcular Conta Ctp Invest
    grad_doa_dict_ctp_invest = grade_doa.set_index("Cod Empresa")["Conta Ctp Invest Controladora"].to_dict()
    
    def calcular_conta_ctp_invest(row):
        nivel_proximo = row['Nível Destino'] + 1
        
        empresa_nivel_proximo = dicionario_hierarquia.get(row['Empresa Origem'], {}).get(nivel_proximo, {}).get('Empresa', None)
        if empresa_nivel_proximo is None:
            return "ERRO"
        
        return grad_doa_dict_ctp_invest.get(empresa_nivel_proximo, "ERRO")
    
    painel_lancamentos_v2["Conta Ctp Invest"] = painel_lancamentos_v2.apply(calcular_conta_ctp_invest, axis=1)

    # 8. Calcular Tipo Lancto Ctpt
    painel_lancamentos_v2['Tipo Lancto Ctpt'] = painel_lancamentos_v2['Tipo Lancto Dest'].apply(lambda x: 'D' if x == 'C' else 'C')

    # 9. Criar Lança SAP
    grad_doa_dict_lanca_sap = grade_doa.set_index("Chave Doadora")["Lança SAP"].to_dict()
    
    def calcular_lanca_sap(row):
        chave_doadora = f"{row['Empresa Origem']}#{row['Tipo Origem']}"
        return grad_doa_dict_lanca_sap.get(chave_doadora, "ERRO")
    
    painel_lancamentos_v2["Lança SAP"] = painel_lancamentos_v2.apply(calcular_lanca_sap, axis=1)


    # 10. Criar coluna CCustoControladora (Usando a ocorrencia do Centro de Custo que mais se repete para cada COD SAP Controladora)
    #cad_emp_dict_ccusto = cad_emp.set_index("Cod SAP Controladora")["Centro de Custo Controladora"].to_dict()
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
    
    # 11. Criar coluna LocalNegControladora
    def calcular_local_negocio_controladora(row):
        filtro = cad_emp[
            (cad_emp["Cod Controlada SAP"] == row["Empresa Origem"]) &
            (cad_emp["Cod SAP Controladora"] == row["Empresa Destino"])
        ]
        
        if not filtro.empty:
            valor = filtro["Local Negócios Controladora"].values[0]
            return valor if pd.notna(valor) and valor != "" else 0 # Pega o primeiro resultado encontrado
        else:
            return 0  # Retorna 0 caso não encontre correspondência

    painel_lancamentos_v2["LocalNegControladora"] = painel_lancamentos_v2.apply(calcular_local_negocio_controladora, axis=1)

    # 13. Criar Divisão Controladora
    def calcular_divisao_controladora(row):
        filtro = cad_emp[
            (cad_emp["Cod Controlada SAP"] == row["Empresa Origem"]) &
            (cad_emp["Cod SAP Controladora"] == row["Empresa Destino"])
        ]
        
        if not filtro.empty:
            valor = filtro["Divisão Controladora"].values[0]
            return valor if pd.notna(valor) and valor != "" else 0  # Retorna o valor encontrado ou 0 se estiver vazio
        else:
            return 0  # Retorna 0 caso não encontre correspondência

    painel_lancamentos_v2["DivControladora"] = painel_lancamentos_v2.apply(calcular_divisao_controladora, axis=1)

    #Ordenar colunas
    colunas_ordenadas = [
    "Empresa Origem", "Nível Destino", "Empresa Destino", "Tipo Origem", "Tipo Destino",
    "Valor Origem", "% Destino", "Valor Destino", "Conta Destino", "Tipo Lancto Dest",
    "Conta Ctp Invest", "Tipo Lancto Ctpt", "Lança SAP", "CCustoControladora",
    "Nível Origem", "ChaveLancto", "LocalNegControladora", "DivControladora"
    ]

    painel_lancamentos_v2 = painel_lancamentos_v2[colunas_ordenadas]

    return painel_lancamentos_v2