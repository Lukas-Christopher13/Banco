import sqlite3

def conectar():
    con = sqlite3.connect('banco14.db')
    cur = con.cursor()
    #cur.execute('''CREATE TABLE Clientes 
    #(Nome Text, CPF Text, Sexo Text, Idade Int, Senha Text, Montante Real)''')
    return (cur, con)

def checar(tabela, intem):
    cur, con = conectar()

    for i in cur.execute("SELECT * FROM %s" % (tabela)):
        if intem in i:           
            con.close()
            return True
    con.close
    return False


def GravarNoBancoClientes(Dados):
    cur, con = conectar()

    cur.execute("INSERT INTO Clientes VALUES (?,?,?,?,?,?)", Dados)
    con.commit()
    con.close()

