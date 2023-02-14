import datetime
from datetime import date
import mysql.connector
con = mysql.connector.connect(host='localhost', db='banco', user='root', password='123456')
cursor = con.cursor()

def Verificar_login(cpf, senha):
    ''' Verifica se o CPF e a senha fornecidos correspondem a um registro no banco de dados. 
    
    Parametros:
    cpf (str): CPF do usuário a ser verificado.
    senha (str): Senha do usuário a ser verificado.   
    
    Returns:
        str: Retorna '0' caso o usuário não seja encontrado ou a senha esteja incorreta.
        Retorna '1' caso o usuário seja encontrado e a senha esteja correta.'''
    
    con = mysql.connector.connect(host='localhost', db='banco', user='root', password='123456')

    cursor = con.cursor()
    cursor.execute('SELECT * FROM teste1 WHERE cpf = %s AND senha = MD5(%s)', (cpf, senha))
    

    cont = '0'
    


    for c in cursor:
    
        if c != '':
            cont = '1'
    return cont


def Verifica_se_existe(cpf):
    ''' Verifica se um CPF existe no banco de dados.
    
    
    Esta função realiza uma busca em uma tabela chamada teste1 em um banco de dados chamado de banco, 
    para verificar se um CPF específico existe na tabela. Se existir, a função retorna True.
    Caso contrário, retorna None.
    
    Parametros:
        cpf (str): Uma string que representa o CPF a ser procurado.
    Returns:
    True se o CPF foi encontrado, None caso contrário.
    '''
    # conexão a um banco de dados
    con = mysql.connector.connect(host='localhost', db='banco', user='root', password='123456')
    # criado um cursor para a execução de comandos Sql
    cursor = con.cursor()
    # consulta para buscar todos os registros existentes na tabela teste1.
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
    # irá retornar verdadeiro caso o cpf seja encontrado
    else: 
        return None
    # retornado não existente caso não seja encontrado

def Armazenar(nome, cpf, endereco, nascimento, senha, limite, saldo):
    ''' Insere informações do cliente na tabela "teste1" do banco de dados MySQL.
    
    Parâmetros:
    nome (str): O nome do cliente.
    cpf (str): O CPF do cliente.
    endereco (str): O endereço do cliente.
    nascimento (str): A data de nascimento do cliente.
    senha (str): A senha do cliente, que será armazenada criptografada usando o algoritmo MD5.
    limite (str): O limite de crédito do cliente.
    saldo (str): O saldo do cliente.
    '''
    con = mysql.connector.connect(host='localhost', db='banco', user='root', password='123456')

    cursor = con.cursor()

    sql = """CREATE TABLE IF NOT EXISTS teste1 (id integer AUTO_INCREMENT PRIMARY KEY, nome text NOT NULL, cpf text NOT NULL, endereco text NOT NULL,nascimento text NOT NULL, senha VARCHAR(32) NOT NULL, limite text NOT NULL, saldo text NOT NULL);"""

    cursor.execute(sql)
    cursor.execute("INSERT INTO teste1(nome, cpf, endereco, nascimento, senha, limite, saldo) VALUES (%s, %s, %s, %s, MD5(%s), %s, %s)", (nome, cpf, endereco, nascimento, senha, limite, saldo))
    con.commit()
    # a função confirma as alterações no banco de dados 

def Linha(cpf):
    ''' definição de uma função chamada de linha
    
    Parametros:
    cpf(str): Uma string que representa o CPF a ser buscado.
    
    A função irá retornar a linha da tabela que contém o CPF passado como argumento,
    caso ela exista, ou retorna False caso contrário. '''
    
    con = mysql.connector.connect(host='localhost', db='banco', user='root', password='123456')
    cursor = con.cursor()
    cursor.execute("SELECT * FROM teste1")

    tupla = ''
    ''' variável que irá armazenar a linha da tabela que contém o CPF passado como
    argumento, caso exista '''
    for c in cursor:
        if cpf in c:
            tupla = c
    con.commit()
    con.close()

    if tupla == '':
        return False
    # irá ser retornado falso caso o cpf passado como argumento não seja encontrado na tabela de teste1
    else:
        return tupla
    # retornado a linha da tabela que contém o CPF passado como argumento


def Update_saldo(valor, onde):
    ''' Criado uma função para a definição da atualização de saldo
    
    Parametros:
    valor (str): valor de atualização de saldo
    onde (str): onde será consultado o saldo para atualização'''
    
    
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

