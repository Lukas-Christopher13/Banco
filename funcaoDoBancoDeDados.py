import sqlite3
from datetime import datetime

#funções do SQL ou banco de dados.

#tabelas
    #Clientes
    #ContaConjunta
    #Historico
    #Transacoes
    #Emprestimo
    #Agendamento

#Faz a conecção com o banco de dados sqlite
def conectar():
    con = sqlite3.connect('banco14.db')
    cur = con.cursor()
    #cur.execute('''CREATE TABLE Agendamento
    #(Data Text, Remetente Text, CPFR Text, Destinatario Text ,CPFD Text, valor Real)''')
    return (cur, con)

#Verifica a existencia de um intem qulaquer em uma tabela qualquer de banco
#retornando True se o mesmo for encontrado.
def checar(tabela,intem): 
    cur, con = conectar()

    for i in cur.execute('SELECT * FROM  %s' % (tabela)):
        if intem in i:           
            con.close()
            return True
    con.close
    return False

#Recebe com parametros uma tabela qualquer e um intem para retorna a uma lina da base de dados
def RetornarLinha(tabela,intem):
    cur, con = conectar()

    for i in cur.execute('SELECT * FROM  %s' % (tabela)):
        if intem in i:           
            con.close()
            return i

#Retorna todos os dados de uma tabela em uma matriz
def RetornarTodosOsDados(tabela):
    cur, con = conectar()
    matriz = []

    for i in cur.execute('SELECT * FROM  %s' % (tabela)):
        matriz.append(i)

    con.close()
    return matriz

#seleciona uma linha de uma tabela com base no CPF
def selecionar(tabela, coluna, cpf):
    cur, con = conectar()

    cur.execute("SELECT * FROM %s WHERE %s = %s " % (tabela, coluna, cpf))
    return cur.fetchall()

#adiciona ou subitrai valor dinhairo na conta
#Essa função tambem utiliza a função 'selecionar' para poder realizar depositos e transferencia
def atualizarValor(tabela, coluna, cpf, posicao, valorAdicionado):
    #Parametros: 

    #tabela: recebe uma tabela do banco.
    #coluna: O nome de uma coluna de uma tabela, exe: CPF, nome ou montante.
    #cpf: um cpf.
    #posicao. recebe o indice do valor que queremos atualizar
    #valorAdicionado: o valor a ser adicionado a conta.

    cur, con = conectar()

    valorAtual = selecionar(tabela, coluna, cpf)
    montante = valorAtual[0]
    
    valorAtualizado = montante[posicao] + valorAdicionado

    cur.execute("UPDATE %s SET Montante = '%f' WHERE %s = %s " % (tabela, valorAtualizado, coluna, cpf))
    con.commit()
    con.close()

#subitrai um valor da tabela, seu modo de funcionamento e semalhante ao da função 'atualizar'
#com a diferança que essa função foca em subitrair um valor da tabela, referente ao saque por
#exemplo.
def Subitrair(tabela, coluna, cpf, posicao, valorAdicionado):
    cur, con = conectar()

    valorAtual = selecionar(tabela, coluna, cpf)
    montante = valorAtual[0]
    
    #Impede o valor armazenado na tabela fique negativo
    if  0 > montante[posicao] - valorAdicionado:
        return True
        
    valorAtualizado = montante[posicao] - valorAdicionado

    cur.execute("UPDATE %s SET Montante = '%f' WHERE %s = %s " % (tabela, valorAtualizado, coluna, cpf))
    con.commit()
    con.close()

#Grava os dados na tabela para o historico de Transacoes
def GravarNaTabelaTransacoes(nome1, cpf1, nome2, cpf2, valor):
    cur, con = conectar()
    Data = datetime.now()
    
    Dados = (Data, nome1, cpf1, nome2, cpf2, valor)
    
    cur.execute("INSERT INTO Transacoes VALUES (?,?,?,?,?,?)",Dados)
    con.commit()
    con.close()

#grava os dados pra o registro na tabela clientes 
def GravarNoBancoClientes(Dados):
    cur, con = conectar()

    cur.execute("INSERT INTO Clientes VALUES (?,?,?,?,?,?,?)", Dados)
    con.commit()
    con.close()

#grava os dados na tabela da conta conjunta
def GravarNoBancoContaConjunta(Dados):
    cur, con = conectar()

    cur.execute("INSERT INTO ContaConjunta VALUES (?,?,?,?)", Dados)
    con.commit()
    con.close()

#grava os dados para que o gerente os veja na tabela Emprestimo.
def GravarNaTabelaImprestimo(Dados):
    cur, con = conectar()

    cur.execute("INSERT INTO Emprestimo VALUES (?,?,?)", Dados)
    con.commit()
    con.close()

#Grava os dados na tabela agendamento para que o gerenteo os veja
def GravarNaTabelaAgendamento(Dados):
    cur, con = conectar()

    cur.execute("INSERT INTO Agendamento VALUES (?,?,?,?,?,?)", Dados)
    con.commit()
    con.close()

#Apos o gerente aprovar ou não o emprestimo essa função deleta os dados da tabela 
#Emprestimo 
def DeletarRegistroDoEmprestimo(cpf):
    cur, con = conectar()

    cur.execute("DELETE FROM Emprestimo WHERE CPF = %s" % (cpf))
    con.commit()
    con.close()

#Quando a data do agendamento do deposito chega, o gerente realiza a tranzação com...
#as informações da tabela e em seguida deleta o registro da tabela Agendamento.
def DeletarRegistroDoAgendamento(cpf):
    cur, con = conectar()

    cur.execute("DELETE FROM Agendamento WHERE CPFR = %s" % (cpf))
    con.commit()
    con.close()