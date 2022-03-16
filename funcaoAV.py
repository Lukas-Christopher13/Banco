import PySimpleGUI as sg
from funcaoB import *

#Checar erros em campos mal prenchidos 
def ChecagemDecamposRegis(Dados):
    # Tratamento de erros que podem ser cometidos durante o prenchimento de quaisquer campos.
    if CamposEmBranco(Dados):
        sg.popup("Prencha Todos os Campos!")        
        return False
    
    elif ApenasLetras(Dados[0], 'Nome', (4,15)):
        return False

    elif ApenasNumero(Dados[1], 'CPF', (11,)):
        return False

    elif CpfsJaCadastradp(Dados[1], 'CPF'):
        return False
    
    elif ChecarSexo(Dados[2]):
        return False
 
    elif (ApenasNumero(Dados[3], 'Idade', (1,3))):
        return False

    elif (int(Dados[3]) < 18):
        sg.popup('Você deve ter mais de 18 anos para poder criar uma conta!')
        return False

    elif SenhasIguais(Dados[4],Dados[5], 'Senha',(9,18)):
        return False

    else:
        return True

#checa se há campos em branco
def CamposEmBranco(campos):
    for i in campos:
        if i == '':
            return True
    return False

#Verifica o tamanho de cada campo
def VerificarTamanho(nomeDoCampo, campo, Tamanho):
    if len(Tamanho) == 2:
        if (len(campo) < Tamanho[0]) or (len(campo) > Tamanho[1]):
            sg.popup('O campo %s dever ter no mininmo %d e no maximo %d caractres!' % (nomeDoCampo, Tamanho[0], Tamanho[1]))
            return True
    else:
        if (len(campo) != Tamanho[0]):
            sg.popup('O campo %s dever ter %d caracteres!' % (nomeDoCampo, Tamanho[0]))
            return True

#Funções para checar erros de prenchimentos... 
def ApenasLetras(Palavra, nomeDoCampo, Tamanho):
    nums = ('0','1','2','3','4','5','6','7','8','9')

    for i in nums:
        if i in Palavra:
            sg.popup('Apenas Caracteres Alfabeticos no Campo %s'%(nomeDoCampo))            
            return True
    
    if VerificarTamanho(nomeDoCampo, Palavra, Tamanho):
        return True

#Verifica se há letras em um campo só pra numeros!
def ApenasNumero(numero, nomeDoCampo, Tamanho):
    try:
        int(numero)
    except:
        sg.popup("Apenas Numeros no Campo %s" % (nomeDoCampo))
        return True
    
    if VerificarTamanho(nomeDoCampo, numero, Tamanho):
        return True

#Verifica no banco se o CPF em questão já está cadastrado
def CpfsJaCadastradp(cpf, nomeDoCampo):
    if checar('Clientes',cpf):
        sg.popup('Esse %s já foi cadastrado!' % (nomeDoCampo))
        return True

#Verifica se o usuario seleciono o sexo corrtamente!
def ChecarSexo(Sexo):
    if (Sexo == 'Feminino') or (Sexo == 'Masculino') or (Sexo == 'Outro'):
        return False
    else:   
        sg.popup('Insira a opção correta no campo Seu Sexo!')
        return True

#Verifica se as senha são iguais
def SenhasIguais(senha,confirmarSenha, nomeDoCampo, Tamanho):
    if senha != confirmarSenha:
        sg.popup('As senhas devem ser iguais!')
        return True
    
    if VerificarTamanho(nomeDoCampo, senha, Tamanho):
        return True