import PySimpleGUI as sg
from funcaoDoBancoDeDados import *
from tkinter.font import BOLD
from turtle import position
from contaConjunta import *
#tela principal 

#função para o saque
def sacar(tabela,cpf):
    sg.theme('DarkAmber')

    layout = [[sg.Text('Valor :'),sg.Input()],
              [sg.Button('Sacar'), sg.Button('Sair')]]
    
    janela = sg.Window('Sacar', layout)

    while True:
        event, values = janela.read()
        if (event == sg.WIN_CLOSED) or event == 'Sair':
            janela.close()
            break
            
        elif event == 'Sacar':
            valor = values[0]
            if ApenasNumero(valor, 'Valor', (1,4)):
                pass

            elif float(valor) < 0:
                sg.popup('Você não pode inserir um valor negativo!')
            
            else: 
                if Subitrair(tabela, 'CPF', cpf, 6, float(valor)):
                    sg.popup('Você não possui essa valor para Sacar!')                
                
                #caso o campo fique em branco
                elif valor[0] == '':
                    sg.popup('Prencha o Campo Valor!')

                else:
                    #Se tudo for prenchido de forma correta o saque é realizado
                    sg.popup('Saque realizado com sucesso!')
                    janela.close()
                    valor = selecionar('Clientes', 'CPF', cpf)

                    janela.close()
                    

#Interface para que o gerente possa efetuar a transferencia por agendamento
def transferirAgendado():
    
    sg.theme('DarkAmber')

    layout = [[sg.Text(('Valor:'),size=(5,1)), sg.InputText()],
              [sg.Text('=======================================================')],
              [sg.Text('Nome Remetente:')],
              [sg.InputText()],
              [sg.Text('CPF Remetente'),sg.InputText()],
              [sg.Text('=======================================================')],
              [sg.Text('Nome destinatário:')],
              [sg.InputText()],
              [sg.Text('CPF destinatário:'),sg.InputText()],
              [sg.Button('Cancelar'),sg.Button('Transferir', key='-transferir-')]]
              

    janela = sg.Window('Painel de transferência',layout)

    while True:
        event, values = janela.read()
        
        if (event == sg.WIN_CLOSED) or event=='Cancelar':
            janela.close()
            break
        
        elif(event == '-transferir-'):
            valor = values[0]
            NomeRemetente = values[1]
            CpfRemetente = values[2]
            NomeDestinatario = values[3]
            CpfDestinatario = values[4]
            
            #Faz a checagem para que tudo ocorra dentro do previsto
            if checar('Clientes', NomeDestinatario):
                if checar('Clientes', CpfDestinatario):
                    #subitrai de um conta para adicionar em outra!
                    if Subitrair('Clientes', 'CPF', CpfRemetente, 6, float(valor)):
                        sg.popup('Saldo insuficiente')
                    else:
                        #Se tudo ocorrer bem a transferencia é efetuada

                        atualizarValor('Clientes', 'CPF', CpfDestinatario, 6, float(valor))
                        GravarNaTabelaTransacoes(NomeRemetente, CpfRemetente, NomeDestinatario, CpfDestinatario, valor)
                        sg.popup('Transferencia realizada!')
                        #Deleta da agendamento da tabela 'Agemdameto' após o gerente efetuar
                        #Transferencia
                        DeletarRegistroDoAgendamento(CpfRemetente)
                        
                        janela.close()
                         
                else:
                    sg.popup('O CPF não consta no banco')
            else:
                sg.popup('O nome não consta no banco')
             
#Trata da parte do agendamento.
#Quando apertamos o botão 'Agendar Transferéncia' essa interface abre, e recebe todos os
#dados da função 'janela_transferir' paraj gravar tudo na tebela Agendamento.  
def agendarData(NomeR, Cpf1 ,NomeD, Cpf2, valor):
    sg.theme('DarkAmber')

    layout = [
            [sg.Text('Ano:'), sg.Input(size=(12)),sg.Text('Mês:'), sg.Input(size=(12)),sg.Text('Dia:'), sg.Input(size=(12))],
            [sg.Button('Solicitar', size=(7,0))], [sg.Button('Cancelar', size=(7,0))]
        ]
    
    janela = sg.Window('Agendar', layout)

    while True:
        event, values = janela.read()
        if (event == sg.WIN_CLOSED) or event == 'Cancelar':
            janela.close()
            break

        elif event == 'Solicitar':
            linha = selecionar('Agendamento','CPFR', Cpf1)
            linhAgendamento = linha[0]

            if (values[0] == '') or (values[1] == '') or (values[2] == ''):
                sg.popup('Prencha Todos os Campos!')
            
            elif ApenasNumero(values[0], 'Ano', (4,)):
                pass
            elif ApenasNumero(values[1], 'mês', (1,2)):
                pass
            elif ApenasNumero(values[2], 'Dia', (1,2)):
                pass
            
            elif linhAgendamento[2] == Cpf1:
                sg.popup('Você já agendou uma transferencia!')

            else:
                Data = ('%s-%s-%s' % (values[0],values[1],values[2]))
                GravarNaTabelaAgendamento((Data, NomeR, Cpf1, NomeD, Cpf2, valor))
                sg.popup('Agendamento Realizado!')
                
                janela.close()

#Função responsavel para solicitar o emprestimo
def emprestimo(nome,cpf):

    sg.theme('DarkAmber')

    layout = [
            [sg.Text('Valor do empréstimo:',size=(20,0)), sg.Input(size=(12))],
            [sg.Button('Solicitar', size=(7,0))], [sg.Button('Cancelar', size=(7,0))]
        ]
    
    janela = sg.Window('Emprestimo', layout)

    while True:
        event, values = janela.read()
        if (event == sg.WIN_CLOSED) or event == 'Cancelar':
            janela.close()
            break

        elif event == 'Solicitar':
            if values[0] == '':
                sg.popup('Preencha Todos os Campos!')
            elif ApenasNumero(values[0], 'Valor do empréstimo', (1,5)):
                pass
            elif checar('Emprestimo',cpf):
                sg.popup('Você já solicitou um emprestimo!\n Aguarde...')
            else:
                GravarNaTabelaImprestimo((nome,cpf,values[0]))
                sg.popup('Pedido realizado!\n Aguarde até que o gerente aprove o emprestimo')
                janela.close()

#Função para realizar o deposito
def deposito(cpf,tabela):
    sg.theme('DarkAmber')

    layout = [[sg.Text('Valor :'),sg.Input()],
              [sg.Button('Depositar'), sg.Button('Sair')]]
    
    janela = sg.Window('Depositar', layout)

    while True:
        event, values = janela.read()
        if (event == sg.WIN_CLOSED) or event == 'Sair':
            janela.close()
            break
        
        elif event == 'Depositar':
            valor = values[0]
            if ApenasNumero(valor, 'Valor', (1,4)):
                pass
            
            elif float(valor) < 0:
                sg.popup('Você não pode inserir um valor negativo!')

            else:
                if valor == '':
                    sg.popup('Prencha o Campo Valor!')
                
                else:
                    atualizarValor(tabela, 'CPF', cpf, 6, float(valor))
                    sg.popup('Deposito realizado com sucesso!')
                    janela.close()
                    break
        
#janela principal, para acessar as demais funções do banco!
def janela_principal(nome,cpf,saldo):
    sg.theme("Reddit")

    montante = saldo

    layout = [
        [sg.Text("Bem Vindo %s!" % (nome), font=("Arial", 20))],  # 
        [
            sg.Text(
                "Conta Bancária",
                size=(30, 1),
                font=("Helvetica", 25, BOLD),
                text_color="black",
            )
        ],
        [sg.Text("Saldo : R$  %.2f" % (montante), font=("Arial", 18, BOLD),key='-saldo-')],
        [sg.Button("Transferência", size=(11, 2))],
        [sg.Button("Depósito", size=(11, 2))],
        [sg.Button("Sacar", size=(11, 2))],
        [sg.Button("Empréstimo", size=(11, 2))],
        [sg.Button("Conta conjunta", size=(11, 2))],
        [sg.Button("Sair", size=(5, 2))],
    ]
    janela = sg.Window("Banco", layout=layout, finalize=True)

    while True:
        event, values = janela.read()
        if (event == sg.WIN_CLOSED) or event == 'Sair':
            janela.close()
            break

        elif event == 'Depósito':
            deposito(cpf,'Clientes')
            valor = selecionar('Clientes', 'CPF', cpf)
            montante = valor[0]
            janela['-saldo-'].update("Saldo : R$  %.2f" % (montante[6]))

        elif event == 'Transferência':
            janela_transferir(nome , cpf)
            valor = selecionar('Clientes', 'CPF', cpf)
            montante = valor[0]
            janela['-saldo-'].update("Saldo : R$ %.2f" % (montante[6]))

        elif event == 'Sacar':
            sacar('Clientes', cpf)
            valor = selecionar('Clientes', 'CPF', cpf)
            montante = valor[0]
            janela['-saldo-'].update("Saldo : R$ %.2f" % (montante[6]))

        elif event == 'Conta conjunta':
            AcessesarOuCriar(cpf)

        elif event == "Empréstimo":
            emprestimo(nome, cpf)

#Interface para a transferencia
def janela_transferir(nome, cpf):
    sg.theme('DarkAmber')

    layout = [[sg.Text(('Valor:'),size=(5,1)), sg.InputText()],
              [sg.Text('=======================================================')],
              [sg.Text('Nome remetente: %s' % (nome))],
              [sg.Text('CPF remetente: %s' % (cpf))],
              [sg.Text('=======================================================')],
              [sg.Text('Nome destinatário:')],
              [sg.InputText()],
              [sg.Text('CPF destinatário:'),sg.InputText()],
              [sg.Text('=======================================================')],
              [sg.Button('Agendar Transferéncia')],
              [sg.Text('=======================================================')],
              [sg.Button('Cancelar'),sg.Button('Transferir', key='-transferir-')]]
              

    janela = sg.Window('Painel de transferência',layout)

    while True:
        event, values = janela.read()
        
        if (event == sg.WIN_CLOSED) or event=='Cancelar':
            janela.close()
            break
        
        elif(event == '-transferir-'):
            valor = values[0]
            NomeDestinatario = values[1]
            CpfDestinatario = values[2]

            if ApenasNumero(valor, 'Valor', (1,6)):
                pass

            elif float(valor) < 0:
                sg.popup('Você não pode inserir um valor negativo!')
        
            elif checar('Clientes', NomeDestinatario):
                if checar('Clientes', CpfDestinatario):
                    #subitrai de um conta para adicionar em outra!
                    if Subitrair('Clientes', 'CPF', cpf, 6, float(valor)):
                        sg.popup('Saldo insuficiente')
                    else:
                        #se tudo for prenchido de forma correta a opração procede
                        atualizarValor('Clientes', 'CPF', CpfDestinatario, 6, float(valor))
                        GravarNaTabelaTransacoes(nome, cpf, NomeDestinatario, CpfDestinatario, valor)
                        janela.close()
                         
                else:
                    sg.popup('O CPF não consta no banco')
            else:
                sg.popup('O nome não consta no banco')
             
        elif(event == 'Agendar Transferéncia'):
            valor = values[0]
            NomeDestinatario = values[1]
            CpfDestinatario = values[2]

            if checar('Clientes', NomeDestinatario):
                if checar('Clientes', CpfDestinatario):
                    agendarData(nome,cpf,NomeDestinatario,CpfDestinatario,valor)
                         
                else:
                    sg.popup('O CPF não consta no banco')
            else:
                sg.popup('O nome não consta no banco')
            
                   
#Funções referentes a tela do gerente...

#Função em que o gerente permite ou não o emprestimo
def permitirEmprestimo():
    sg.theme('DarkAmber')

    layout = [[sg.Text('CPF :'),sg.Input()],
              [sg.Button('Pemitir'), sg.Button('Recusar'), sg.Button('Sair')]]
    
    janela = sg.Window('Aprovar Emprestimo', layout)

    while True:
        event, values = janela.read()
        if (event == sg.WIN_CLOSED) or event == 'Sair':
            janela.close()
            break
        
        elif event == 'Pemitir':
            if values[0] == '':
                sg.popup('Prencha o Campo CPF!')
            
            elif ApenasNumero(values[0], 'Emprestimo', (11,)):
                pass
            elif checar('Emprestimo',values[0]) == False:
                sg.popup('Não há solicitação de emprestimo nesse CPF!')

            else:
                Dados = RetornarLinha('Emprestimo',values[0])
                atualizarValor('Clientes', 'CPF', values[0], 6, Dados[2])
                DeletarRegistroDoEmprestimo(values[0])

                sg.popup('Emprestimo Aprovado')
                janela.close()
        
        elif event == 'Recusar':
            if values[0] == '':
                sg.popup('Prencha o Campo CPF!')
            
            elif ApenasNumero(values[0], 'Emprestimo', (11,)):
                pass
            elif checar('Emprestimo',values[0]) == False:
                sg.popup('Não há solicitação de emprestimo nesse CPF!')

            else:
                DeletarRegistroDoEmprestimo(values[0])

                sg.popup('Emprestimo Recusado!')
                janela.close()

#Função pra printar na tela os dados da tabela agendamento
def DadosDoAgendamento():
    Dados = RetornarTodosOsDados('Agendamento')
    sg.Print('Transações Agendadas\n',font=('Arial',12))
    for i in Dados:
        sg.Print('|DATA: %s\t |DE: %s \t%s\t |PARA: %s \t%s|NO VALOR DE: \t%s' %(i[0],i[1],i[2],i[3],i[4],i[5]),font=('Arial',12))

#Função pra printar na tela os dados da tabela Emprestimo
def DadosDosEmprestimos():
    Dados = RetornarTodosOsDados('Emprestimo')
    sg.Print('Pedidos de Emprestimo\n',font=('Arial',12))
    for i in Dados:
        sg.Print('|NOME: %s\t |CPF: %s|NO VALOR DE: \t%s' %(i[0],i[1],i[2]),font=('Arial',12))

#Função pra printar na tela os dados da tabela das Transações
def DadosDasTransacoes():
    Dados = RetornarTodosOsDados('Transacoes')
    sg.Print('Histórico de Transações\n',font=('Arial',12))
    for i in Dados:
        sg.Print('|DATA: %s\t |DE: %s \t%s\t |PARA: %s \t%s|NO VALOR DE: \t%s' %(i[0],i[1],i[2],i[3],i[4],i[5]),font=('Arial',12))

#Função pra printar na tela os dados da tabela Contaconjunta
def DadosDaContaConjunta():
    Dados = RetornarTodosOsDados('ContaConjunta')
    sg.Print('NOME\t          |CPF1            \t|CPF2           \t|MONTANTE\n', font=('Arial',15))
    for i in Dados:
        sg.Print('|%s\t|%s\t|%s\t|     %s     ' %(i[0],i[1],i[2],i[3]),font=('Arial',15))

#Função pra printar na tela os dados da tabela Clientes
def DadosDosClientes():
    Dados = RetornarTodosOsDados('Clientes')
    sg.Print('NOME\t|CPF\t       |SEXO      \t|IDADE\t   |USUARIO\t    |MONTANTE\n', font=('Arial',15))
    for i in Dados:
        sg.Print('|%s\t|%s\t|%s\t|     %s     |   \t%s      \t|     %s' %(i[0],i[1],i[2],i[3],i[5],i[6]),font=('Arial',15))

#função para a janela do gerente 
def janelaDoGerente(nome, cpf, sexo):
    sg.theme('DarkAmber')

    layout = [[sg.Text(('Bem Vindo: %s ' %(nome)),size=(15,1))],
              [sg.Text(('CPF: %s ' % (cpf)),size=(15,1))],
              [sg.Text(('Sexo: %s ' % (sexo)),size=(15,1))],
              [sg.Button('Ver Dados dos Clientes'),sg.Button('Historico De Transações')],
              [sg.Button('Pedidos de Emprestimo'),sg.Button('Permitir Emprestimo')],
              [sg.Button('Ver Depositos Agendados'),sg.Button('Realizar Transferencia')]]

    janela = sg.Window('Banco14 Registro', layout)

    while True:
        event, values = janela.read()
        if (event == sg.WIN_CLOSED) or event == 'Cancelar':
            janela.close()
            break
        
        elif event == 'Ver Dados dos Clientes':
           sg.Print('CONTAS',font=('Arial',15))
           DadosDosClientes()
           sg.Print('\nCONTAS CONJUNTAS',font=('Arial',15))
           DadosDaContaConjunta()
        
        elif event == 'Historico De Transações':
            DadosDasTransacoes()
        
        elif event == 'Pedidos de Emprestimo':
            DadosDosEmprestimos()
        
        elif event == 'Permitir Emprestimo':
            permitirEmprestimo()

        elif event == 'Ver Depositos Agendados':
            DadosDoAgendamento()

        elif event == 'Realizar Transferencia':
            transferirAgendado()