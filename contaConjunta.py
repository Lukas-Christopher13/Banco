from funcaoDoBancoDeDados import *
from OperaçõesDeRegistro import *
import PySimpleGUI as sg

#notas....

#realizar o saque na conta conjunta
def saqueCojunto(cpf,tabela):
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
                if Subitrair(tabela, 'CPF1', cpf, 3, float(valor)):
                    sg.popup('Você não possui essa valor para Sacar!')                
                
                #caso o campo não seja fique em branco
                elif valor[0] == '':
                    sg.popup('Prencha o Campo Valor!')

                else:
                    #Se tudo for prenchido de forma correta o saque é realizado
                    sg.popup('Saque realizado com sucesso!')
                    janela.close()
                    valor = selecionar('ContaConjunta', 'CPF1', cpf)
                    montante = valor[0]

                    janela.close()
                    #retorna o valor após o saque para atulaizar o valor na interface
                    return montante

#Realiza o deposito na conta conjunta
def depositoConjunto(cpf,tabela):
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

            elif valor[0] == '':
                sg.popup('Prencha o Campo Valor!')

            else:
                #Se tudo for prenchido de forma correta o saque é realizado 
                atualizarValor(tabela, 'CPF1', cpf, 3, float(valor))
                sg.popup('Deposito realizado com sucesso!')
                janela.close()

                valor = selecionar('ContaConjunta', 'CPF1', cpf)
                montante = valor[0]
                #retorna o valor após o saque para atulaizar o valor na interface
                return montante

#interface para a conta conjunta
def contaConjunta(nome,cpf1,cpf2,valor):
    sg.theme('DarkAmber')
    
    montante = valor

    layout = [[sg.Text(('Conta: %s'% (nome)),size=(15,1))],
              [sg.Text('Valor :  %.2f' % (montante),key='-saldo-')],
              [sg.Text(('CPF 1: %s' % (cpf1)),size=(15,1))],
              [sg.Text(('CPF 1: %s' % (cpf2)),size=(15,1))],
              [sg.Button('Deposito'),sg.Button('Saque'),sg.Button('Cancelar')]]

    janela = sg.Window('Conta Conjunta', layout)

    while True:
        event, values = janela.read()
        if (event == sg.WIN_CLOSED) or event == 'Cancelar':
            janela.close()
            break

        elif event == 'Deposito':
            montante = depositoConjunto(cpf1,'ContaConjunta')
            #Atualiza o valor na interface
            if montante != None:
                #Quando um valor é digitado de forma icorreta ele retorna como
                #'None', esse trecho de codigo evita erros desencadeados
                #pelo ususario
               janela['-saldo-'].update("Saldo : R$  %.2f" % (montante[3]))

        elif event == 'Saque':
            montante = saqueCojunto(cpf1,'ContaConjunta')
            #Atualiza o valor na interface
            if montante != None:
                #Quando um valor é digitado de forma icorreta ele retorna como
                #'None', esse trecho de codigo evita erros desencadeados
                #pelo ususario
                janela['-saldo-'].update("Saldo : R$  %.2f" % (montante[3]))

#Realiza o registro de uma nova conta conjuta
def contaConjuntaRegis(cpf):
    sg.theme('DarkAmber')

    layout = [[sg.Text(('Nome da Conta:'),size=(15,1)), sg.InputText()],
              [sg.Text(('CPF 1: %s' % (cpf)),size=(15,1))],
              [sg.Text(('CPF 2:'),size=(15,1)), sg.InputText()],
              [sg.Button('Concluir'),sg.Button('Cancelar')]]
    
    janela = sg.Window('Criar conta corrente', layout)

    while True:
        event, values = janela.read()
        if (event == sg.WIN_CLOSED) or event == 'Cancelar':
            janela.close()
            #JanelaDeLogin()
            break
        elif(event == 'Concluir'):
            NomeDaconta = values[0]
            cpf1 = cpf
            cpf2 = values[1]

            #Checa se já existe um conta com esse cpf na tabela conta conjunta se sim retorna True
            #Isso é feito para que exita apenas uma conta conjunta por CPF
            if checar('ContaConjunta', cpf):
                sg.popup('Você so pode ter uma conta conjunta cadastrada')
            
            #Cadastra a conta
            elif ChecarDadosContaConjunta((NomeDaconta, cpf1, cpf2)):
                GravarNoBancoContaConjunta((NomeDaconta, cpf1, cpf2, 0)) #toda conta criada
                sg.popup('conta conjunta criada com sucesso!')           #tem 0 reais
                janela.close()
                    
#Interface pra acessar ou criar uma conta
def AcessesarOuCriar(cpf):
    sg.theme('DarkAmber')

    layout = [[sg.Text('Criar ou Acessar conta Conjunta')],
              [sg.Button('Acessar'), sg.Button('Criar')]]
    
    janela = sg.Window('Acessar ou Criar Conta Conjunta', layout)

    while True:
        event, values = janela.read()
        if (event == sg.WIN_CLOSED):
            janela.close()
            break
        elif event == 'Criar':
            janela.close()
            contaConjuntaRegis(cpf)
        elif event == 'Acessar':
            
            #checa se a pesso já tem conta cadastrada
            #se não tiver ela não pose acessar a conta
            if checar('ContaConjunta',cpf) == False:
                sg.popup('Você não Possui Conta Conjunta Cadastrada')

            else:
                Dados = RetornarLinha('ContaConjunta',cpf)
                contaConjunta(Dados[0], Dados[1], Dados[2], Dados[3])
