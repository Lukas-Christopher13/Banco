import PySimpleGUI as sg
from funcaoB import *

def OpreacaoDeCadastro(Dados):

    # Tratamento de erros que podem ser cometidos durante o cadastro.
    if CamposEmBranco(Dados):
        sg.popup("Prencha Todos os Campos!")        
        return False
    else:
        for Id in Dados:
            ChecarError(Dados.index(Id),Id)
            break
    
def ChecarError(Id, Parametro):
    
    def Nomeinvalido(Parametro):
        nums = ['0','1','2','3','4','5','6','7','8','9']

        for i in nums:
            if i in Parametro:
                sg.popup('Apenas Caracteres Alfabeticos no Campo Nome!')
                return False

    def CpfInvalido(Paramerto):
        
        pass

    


    if Id == 0:
       return Nomeinvalido(Parametro)
    

def CamposEmBranco(campos):
    for i in campos:
        if i == '':
            return True
    return False

    
            

