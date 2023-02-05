from mysql.connector.constants import ServerFlag
from bd import armazenar
import datetime
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
import socket
#alteracao do banco de dados
import mysql.connector
import threading
con = mysql.connector.connect(host='localhost', db='banco', user='root', password='123456')
cursor = con.cursor()
sql = """CREATE TABLE IF NOT EXISTS teste1 (id integer AUTO_INCREMENT PRIMARY KEY, nome text NOT NULL, cpf text NOT NULL, endereco text NOT NULL,nascimento text NOT NULL, senha VARCHAR(32) NOT NULL, limite text NOT NULL, saldo text NOT NULL);"""
cursor.execute(sql)
class ClienteThread(threading.Thread):
    def __init__(self, clientAddress, clientesocket, numero, aux: int, aux_id: int, sinc):
        threading.Thread.__init__(self)
        self.csocket = clientesocket
        self.numero = numero
        self.aux = aux
        self.aux_id = aux_id
        self.sinc = sinc
        print("Nova conexao: ",clientAddress)

    
    def run(self):
        print("Conectado de: ", ClientAddress)
        self.sinc.acquire()
        self.operacao()
        self.sinc.release()

    
    def verifica_se_existe(self, cpf):
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

    def operacao(self):
        recebe_operacao = self.csocket.recv(1024).decode()
        self.csocket.send('opcao recebida'.encode())

        
        if recebe_operacao == 'cadastrar':
            recebe = self.csocket.recv(1024).decode()
            nome = recebe
            self.csocket.send('nome recebido'.encode())
            recebe = self.csocket.recv(1024).decode()
            cpf = recebe
            self.csocket.send('cpf recebido'.encode())
            recebe = self.csocket.recv(1024).decode()
            endereco = recebe
            self.csocket.send('endereco recebido'.encode())
            recebe = self.csocket.recv(1024).decode()
            nascimento = recebe
            self.csocket.send('nascimento recebido'.encode())
            recebe = self.csocket.recv(1024).decode()
            senha = recebe
            self.csocket.send('senha recebido'.encode())
            recebe = self.csocket.recv(1024).decode()
            limite = recebe
            self.csocket.send('limite recebido'.encode())
            recebe = self.csocket.recv(1024).decode()
            saldo = recebe
            self.csocket.send('saldo recebido'.encode())
            
            
            if not (nome == '' or endereco == '' or cpf == '' or nascimento == '' or senha == '' or limite == '' or saldo == ''):
            

                if self.verifica_se_existe(cpf) == None:
                    historico = f'Conta criada em {datetime.datetime.today()}'
                    armazenar(nome, cpf, endereco, nascimento, senha, limite, saldo)
                    con = mysql.connector.connect(host='localhost', db='banco', user='root', password='123456')

                    cursor = con.cursor()

                    sql = """CREATE TABLE IF NOT EXISTS transacoes (id integer AUTO_INCREMENT PRIMARY KEY, cpf_user text, transacoes text NULL);"""
                    cursor.execute(sql)

                    cursor.execute("INSERT INTO transacoes (cpf_user, transacoes) VALUES (%s, %s)", (cpf, historico))
                    con.commit()
                    
                    
                    retorno = 'True'
                    self.csocket.send(retorno.encode())


                else:
                    retorno = 'False'
                    self.csocket.send(retorno.encode())
            else:
                retorno = 'None'
                self.csocket.send(retorno.encode())

        if recebe_operacao == 'sacar':
            valor = self.csocket.recv(1024).decode()
            self.csocket.send('valor recebido'.encode())
            cpf = self.csocket.recv(1024).decode()
            self.csocket.send('cpf recebido'.encode())

            print(valor, cpf)

                


if (__name__ == '__main__' ):
    host = '10.180.44.105'
    port = 1234
    addr = (host, port)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(addr)

    print("SERVIDOR INICIADO!")
    print("Aguardando nova conexao...")
    
    

    #alteracao do banco de dados
    
    server.listen(10)
    cont = 0

    aux = 0
    aux_id = 0

    aux_id+=1
    # cursor.execute('UPDATE contas_banco SET saldo = c.saldo WHERE id = 0')

    sinc = threading.Lock()
    numero = 0
    while True:
        numero+=1
        Clientesock, ClientAddress = server.accept()
        newthread = ClienteThread(ClientAddress, Clientesock, numero, aux, aux_id, sinc)
        newthread.start()