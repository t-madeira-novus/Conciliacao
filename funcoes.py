import pandas as pd
from tqdm import tqdm

def _conciliar_impostos(df, app):
    path_df = df
    barra_index = path_df.rfind("/")
    path_to_save = path_df[:barra_index+1]
    df_name = path_df[barra_index+1:]
    ponto_index = df_name.rfind(".")
    df_resultado_name = df_name[:ponto_index] + "_resultado_imposto" + df_name[ponto_index:]
    path_to_save += df_resultado_name

    df = pd.read_excel(df)
    df = df.drop(['Unnamed: 1', 'Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4', 'Unnamed: 6', 'Unnamed: 7', 'Unnamed: 8',
                  'Unnamed: 9', 'Unnamed: 10', 'Unnamed: 11', 'Unnamed: 12', 'Unnamed: 13', 'Cta.C.Part.',
                  'Unnamed: 15', 'Unnamed: 16', 'Unnamed: 18', 'Unnamed: 20', 'Saldo', 'Unnamed: 22', 'Unnamed: 23',
                   'Unnamed: 24', 'Saldo-Exercício'], axis=1, inplace=False)

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


    df.to_excel(path_to_save)

def _conciliar_fornecedor_cliente(df, app):
    path_df = df
    barra_index = path_df.rfind("/")
    path_to_save = path_df[:barra_index+1]
    df_name = path_df[barra_index+1:]
    ponto_index = df_name.rfind(".")
    df_resultado_name = df_name[:ponto_index] + "_resultado_fornecedor_ou_cliente" + df_name[ponto_index:]
    path_to_save += df_resultado_name

    df = df.drop(['Unnamed: 1', 'Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4', 'Unnamed: 6', 'Unnamed: 7', 'Unnamed: 8',
                  'Unnamed: 9', 'Unnamed: 10', 'Unnamed: 11', 'Unnamed: 12', 'Unnamed: 13', 'Cta.C.Part.',
                  'Unnamed: 15', 'Unnamed: 16', 'Unnamed: 18', 'Unnamed: 20', 'Saldo', 'Unnamed: 22', 'Unnamed: 23',
                   'Unnamed: 24', 'Saldo-Exercício'], axis=1, inplace=False)

    dict = {}
    for i in tqdm(df.index):
        current_object += 1
        # if pd.isna(df.at[i, 'Histórico']) == False:
        historico = str(df.at[i, 'Histórico'])
        numero_nota = [int(s) for s in historico.split() if s.isdigit()]
        if numero_nota != [] :
            # if numero_nota not in notas and numero_nota != []:
            # print(numero_nota)
            if numero_nota[0] not in dict:
                dict[numero_nota[0]] = [0, 0, []]
            if float (df.at[i, 'Débito']) > 0:
                dict[numero_nota[0]][0] += float (df.at[i, 'Débito'])
                dict[numero_nota[0]][2].append(i)
            elif float (df.at[i, 'Crédito']) > 0:
                dict[numero_nota[0]][1] += float (df.at[i, 'Crédito'])
                dict[numero_nota[0]][2].append(i)


    indexes_to_drop = []
    for nota in dict:
        if dict[nota][1] != dict[nota][0]:
            indexes_to_drop.append(dict[nota][2])
    flat_list = [item for sublist in indexes_to_drop for item in sublist]
    df.drop(flat_list, inplace=True)

    app.infoBox("Fim", "Conciliação terminada. Planilha com históricos não conciliados salva no mesmo caminho da "
                       "planilha usada para a conciliação")

    df.to_excel(path_to_save)

