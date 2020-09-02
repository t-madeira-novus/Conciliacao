from appJar import gui
from funcoes import _conciliar_impostos, _conciliar_fornecedor_cliente

def _ajuda(submenu):
    aux = 'Este sistema é capaz de realizar a conciliação entre débito e crédito das contas de impostos, fornecedores e' \
          'clientes, através do relatório \"Razão\" extraído da Domínio.\n\n' \
          'Como usar:\n' \
          'i) Excluir as 6 primeiras linhas do relatório gerada pela Domínio, de modo que a primeira linha seja o nome ' \
          'das colunas (Data, Histórico, Débito, Crédito, etc.)\n\n'\
          'ii) Selecionar o tipo de planilha, se é referente a impostos ou cliente/fornecedor. Se selecionar errado, ' \
          'o sistema não apresenta erro. Mas o resultado gerado estará errado.\n\n' \
          'iii) O sistema gera como resultado uma planilha no mesmo caminho da planilha original, contendo apenas os ' \
          'históricos que não foram conciliados. '

    if submenu == 'Como usar':
        app.infoBox('Como usar', aux)
    elif submenu == 'Versão':
        app.infoBox('Versão', 'Versão 1.0')

def _thread_conferir():
    df = app.openBox(title=None, dirName=None, fileTypes=None, asFile=False, parent=None, multiple=False, mode='r')
    tipo = app.getOptionBox("Tipo: ")

    if tipo == "Impostos":
        _conciliar_impostos (df, app)

    else:
        _conciliar_fornecedor_cliente(df, app)
        # print(df.columns)
        # return 0

# Criando a interface Gráfica
app = gui("Conciliação de Lançamentos")
app.setFont(10)
app.addMenuList("Ajuda", ["Como usar", "Versão"], _ajuda)


#######################################################################################################################
coluna = 0
linha = 0

app.addLabelOptionBox("Tipo: ", ["- Tipo -", "Cliente ou Fornecedor", "Impostos"],  row=linha, column=coluna)
linha += 1
app.addButton("Conferir", _thread_conferir, row=linha, column=coluna)
linha += 1

#######################################################################################################################

# start the GUI
app.go()

