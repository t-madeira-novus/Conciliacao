import pandas as pd
from tqdm import tqdm


def _pega_numero(string):
    numero = [int(s) for s in string.split() if s.isdigit()]
    if numero != []:
        numero.sort(reverse = True)
        numero = str(numero[0])

        if len(numero) >= 6:
            numero = numero[-5:]

        return int(numero)
    else:
        return 'Sem número'
        # numero = string.split("-")[0]
        # numero = [int(s) for s in numero.split() if s.isdigit()]
        # numero = str(numero)
        # print (numero)
        #
        # if len(numero) >= 6:
        #     numero = numero[-5:]
        # try:
        #     return int(numero)
        # except IndexError:
        #     return -1
        # except ValueError:
        #     return -1


def _conciliar_impostos(df, app):
    path_df = df
    barra_index = path_df.rfind("/")
    path_to_save = path_df[:barra_index+1]
    df_name = path_df[barra_index+1:]
    ponto_index = df_name.rfind(".")
    df_resultado_name = df_name[:ponto_index] + "_resultado_imposto" + df_name[ponto_index:]
    path_to_save += df_resultado_name

    df = pd.read_excel(df)
    colunas_ficam = ["Data", "Histórico", "Débito", "Crédito"]
    colunas_saem = []
    for coluna in df.columns:
        if str(coluna) not in colunas_ficam:
            colunas_saem.append(coluna)

    # df = df.drop(['Unnamed: 1', 'Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4', 'Unnamed: 6', 'Unnamed: 7', 'Unnamed: 8',
    #               'Unnamed: 9', 'Unnamed: 10', 'Unnamed: 11', 'Unnamed: 12', 'Unnamed: 13', 'Cta.C.Part.',
    #               'Unnamed: 15', 'Unnamed: 16', 'Unnamed: 18', 'Unnamed: 20', 'Saldo', 'Unnamed: 22', 'Unnamed: 23',
    #                'Unnamed: 24', 'Saldo-Exercício'], axis=1, inplace=False)

    df = df.drop(colunas_saem, axis=1, inplace=False)

    indexes_to_drop = []
    for i in tqdm(df.index):
        if float(df.at[i, "Débito"]) > 0:
            for j in df.index:
                if float(df.at[j, "Crédito"]) > 0:
                    if float(df.at[i, "Débito"]) == float(df.at[j, "Crédito"]):
                        indexes_to_drop.append(i)
                        indexes_to_drop.append(j)

    df.drop(indexes_to_drop, inplace=True)

    app.infoBox("Fim", "Conciliação terminada. Planilha com históricos não conciliados salva no mesmo caminho da "
                       "planilha usada para a conciliação")

    df.to_excel(path_to_save, index=False)

def _conciliar_fornecedor_cliente(df, app):
    path_df = df
    barra_index = path_df.rfind("/")
    path_to_save = path_df[:barra_index+1]
    df_name = path_df[barra_index+1:]
    ponto_index = df_name.rfind(".")
    df_resultado_name = df_name[:ponto_index] + "_resultado_fornecedor_ou_cliente" + df_name[ponto_index:]
    path_to_save += df_resultado_name


    df = pd.read_excel(df)
    colunas_ficam = ["Data", "Histórico", "Débito", "Crédito"]
    colunas_saem = []
    for coluna in df.columns:
        if str(coluna) not in colunas_ficam:
            colunas_saem.append(coluna)

    # df = df.drop(['Unnamed: 1', 'Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4', 'Unnamed: 6', 'Unnamed: 7', 'Unnamed: 8',
    #               'Unnamed: 9', 'Unnamed: 10', 'Unnamed: 11', 'Unnamed: 12', 'Unnamed: 13', 'Cta.C.Part.',
    #               'Unnamed: 15', 'Unnamed: 16', 'Unnamed: 18', 'Unnamed: 20', 'Saldo', 'Unnamed: 22', 'Unnamed: 23',
    #                'Unnamed: 24', 'Saldo-Exercício'], axis=1, inplace=False)

    df = df.drop(colunas_saem, axis=1, inplace=False)

    dict = {}
    for i in tqdm(df.index):
        # if pd.isna(df.at[i, 'Histórico']) == False:
        historico = str(df.at[i, 'Histórico']).replace('-', ' ')
        df.at[i, 'Histórico'] = str(df.at[i, 'Histórico']) + " (" + str(_pega_numero(historico)) + ")"
        numero_nota = _pega_numero(historico)
        #print(str(historico) + ": " + str(numero_nota))
        # if numero_nota != [] :
        if numero_nota not in dict:
            dict[numero_nota] = [0, 0, []]
        if float (df.at[i, 'Débito']) > 0:
            dict[numero_nota][0] += float (df.at[i, 'Débito'])
            dict[numero_nota][2].append(i)
        elif float (df.at[i, 'Crédito']) > 0:
            dict[numero_nota][1] += float (df.at[i, 'Crédito'])
            dict[numero_nota][2].append(i)


    indexes_to_drop = []
    for nota in dict:
        if dict[nota][1] == dict[nota][0]:
            indexes_to_drop.append(dict[nota][2])
    flat_list = [item for sublist in indexes_to_drop for item in sublist]

    indexes_to_drop_2 = []
    for i in tqdm(df.index):
        if float(df.at[i, "Débito"]) > 0:
            for j in df.index:
                if float(df.at[j, "Crédito"]) > 0:
                    if float(df.at[i, "Débito"]) == float(df.at[j, "Crédito"]):
                        flat_list.append(i)
                        flat_list.append(j)

    flat_list = list(set(flat_list))

    print(dict)
    print(flat_list)

    df.drop(flat_list, inplace=True)
    # df.drop(indexes_to_drop_2, inplace=True)


    app.infoBox("Fim", "Conciliação terminada. Planilha com históricos não conciliados salva no mesmo caminho da "
                       "planilha usada para a conciliação")

    df.to_excel(path_to_save, index=False)

