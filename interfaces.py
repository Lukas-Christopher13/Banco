import PySimpleGUI as sg
from funcaoDoBancoDeDados import *
from OperaçõesDeRegistro import *
from TelaPrincipal import *

#janela de login e suas funções
def JanelaDeLogin():
    sg.theme('DarkAmber')

    layout = [[sg.Text('CPF', key= '-user-')],
              [sg.InputText()],
              [sg.Text('Senha')],
              [sg.InputText()],
              [sg.Button('Logar'), sg.Button('Registrar')]]
    
    janela = sg.Window('Banco14 Login/Registro', layout)

    while True:
        event, values = janela.read()
        if event == sg.WIN_CLOSED:
            break
        
        elif event == 'Registrar':
            janela.close()
            TelaDeCadastro()
        
        elif event == 'Logar':
            cpf = values[0]
            senha = values[1]

            if CamposEmBranco((cpf,senha)):
                sg.popup("Prencha Todos os Campos!")
            
            elif checar('Clientes',cpf):
                DadosDoCliente = RetornarLinha('Clientes',cpf)
                if senha == DadosDoCliente[4]:
                    janela.close()
                    
                    if DadosDoCliente[5] == 'cliente':
                        janela_principal(DadosDoCliente[0], DadosDoCliente[1], DadosDoCliente[6])
                    
                    else:
                        janelaDoGerente(DadosDoCliente[0], DadosDoCliente[1], DadosDoCliente[2])

                else:
                    sg.popup('Senha incorreta!')
            else:
                sg.popup('CPF incorreto ou não cadastrado!')
        
#tela de cadastro e suas funçoes
def TelaDeCadastro():
    sg.theme('DarkAmber')

    layout = [[sg.Text(('Nome Completo:'),size=(15,1)), sg.InputText()],
              [sg.Text(('CPF:'),size=(15,1)), sg.InputText()],
              [sg.Text(('Seu Sexo:'),size=(15,1)), sg.Combo(('Masculino', 'Feminino', 'Outro'), size=(10,1)), sg.Text('Idade:'),sg.InputText(size=(10,1))],
              [sg.Text(('Senha:'),size=(15,1)), sg.InputText()],
              [sg.Text(('Confimar Senha:'),size=(15,1)), sg.InputText()],
              [sg.Button('Concluir'),sg.Button('Cancelar'),]]
    
    janela = sg.Window('Banco14 Registro', layout)

    while True:
        event, values = janela.read()
        if (event == sg.WIN_CLOSED) or event == 'Cancelar':
            janela.close()
            JanelaDeLogin()
            break

        elif event == 'Concluir':
            Nome = values[0]
            Cpf = values[1]
            Sexo = values[2]
            Idade = values[3]
            Senha = values[4]
            ConfirmarSenha = values [5]

            Dados = (Nome, Cpf, Sexo, Idade, Senha, ConfirmarSenha)

            if ChecagemDecamposRegis(Dados):

                GravarNoBancoClientes((Nome, Cpf, Sexo, Idade, Senha, 'cliente', 0))

                sg.popup("Conta Registrada com Sucesso!")
                janela.close()
                JanelaDeLogin()
           
def executarAplicao():
    JanelaDeLogin()
