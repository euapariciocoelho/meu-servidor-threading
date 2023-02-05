import mysql.connector

def armazenar(nome, cpf, endereco, nascimento, senha, limite, saldo):
    con = mysql.connector.connect(host='localhost', db='banco', user='root', password='123456')

    cursor = con.cursor()

    sql = """CREATE TABLE IF NOT EXISTS teste1 (id integer AUTO_INCREMENT PRIMARY KEY, nome text NOT NULL, cpf text NOT NULL, endereco text NOT NULL,nascimento text NOT NULL, senha VARCHAR(32) NOT NULL, limite text NOT NULL, saldo text NOT NULL);"""

    cursor.execute(sql)
    cursor.execute("INSERT INTO teste1(nome, cpf, endereco, nascimento, senha, limite, saldo) VALUES (%s, %s, %s, %s, MD5(%s), %s, %s)", (nome, cpf, endereco, nascimento, senha, limite, saldo))
    con.commit()

    


  