import datetime
from datetime import date
import mysql.connector
con = mysql.connector.connect(host='localhost', db='banco', user='root', password='123456')
cursor = con.cursor()

def Verificar_login(cpf, senha):
    con = mysql.connector.connect(host='localhost', db='banco', user='root', password='123456')
    cursor = con.cursor()
    cursor.execute('SELECT * FROM teste1 WHERE cpf = %s AND senha = MD5(%s)', (cpf, senha))

    cont = '0'
    for c in cursor:
        if c != '':
            cont = '1'
    return cont

def Verifica_se_existe(cpf):
    con = mysql.connector.connect(host='localhost', db='banco', user='root', password='123456')
    cursor = con.cursor()
    cursor.execute("SELECT * from teste1")
    existe = False
    for c in cursor:
        if cpf in c:
            tupla = c
            existe = True
    con.commit()
    con.close()

    if existe:
        return True
    else: 
        return None
   
def Armazenar(nome, cpf, endereco, nascimento, senha, limite, saldo):
    con = mysql.connector.connect(host='localhost', db='banco', user='root', password='123456')

    cursor = con.cursor()

    sql = """CREATE TABLE IF NOT EXISTS teste1 (id integer AUTO_INCREMENT PRIMARY KEY, nome text NOT NULL, cpf text NOT NULL, endereco text NOT NULL,nascimento text NOT NULL, senha VARCHAR(32) NOT NULL, limite text NOT NULL, saldo text NOT NULL);"""

    cursor.execute(sql)
    cursor.execute("INSERT INTO teste1(nome, cpf, endereco, nascimento, senha, limite, saldo) VALUES (%s, %s, %s, %s, MD5(%s), %s, %s)", (nome, cpf, endereco, nascimento, senha, limite, saldo))
    con.commit()

def Linha(cpf):
    con = mysql.connector.connect(host='localhost', db='banco', user='root', password='123456')
    cursor = con.cursor()
    cursor.execute("SELECT * FROM teste1")

    tupla = ''
    for c in cursor:
        if cpf in c:
            tupla = c
    con.commit()
    con.close()

    if tupla == '':
        return False
    else:
        return tupla


def Update_saldo(valor, onde):
    con = mysql.connector.connect(host='localhost', db='banco', user='root', password='123456')
    cursor = con.cursor()
    cursor.execute("UPDATE teste1 SET saldo = " + str(valor) + "WHERE id = " + str(onde))
                    
    con.commit()

    con = mysql.connector.connect(host='localhost', db='banco', user='root', password='123456')

    cursor = con.cursor()
    con.commit()
    con.close()

def Gravar_transacoes(cpf, historico):
    con = mysql.connector.connect(host='localhost', db='banco', user='root', password='123456')
    cursor = con.cursor()
    sql = """CREATE TABLE IF NOT EXISTS transacoes (id integer AUTO_INCREMENT PRIMARY KEY, cpf_user text NOT NULL, transacoes text NOT NULL);"""

    cursor.execute(sql)
    cursor.execute("INSERT INTO transacoes (cpf_user, transacoes) VALUES (%s, %s)", (cpf, historico))
    con.commit()
    con.close()

def Transacoes(cpf):
    con = mysql.connector.connect(host='localhost', db='banco', user='root', password='123456')
    cursor = con.cursor()
    cursor.execute("SELECT * FROM transacoes")

    tupla = ''
    for c in cursor:
        if cpf in c:
            tupla += c[2]
            tupla += ','
    con.commit()
    con.close()

    return tupla # retornando apenas a coluna transacoes na tabela transacoes

def Entrar():
    print('entrou')


   