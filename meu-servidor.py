import socket, threading
from bd import armazenar
import mysql.connector
con = mysql.connector.connect(host='localhost', db='banco', user='root', password='123456')
cursor = con.cursor()
sql = """CREATE TABLE IF NOT EXISTS teste1 (id integer AUTO_INCREMENT PRIMARY KEY, nome text NOT NULL, cpf text NOT NULL, endereco text NOT NULL,nascimento text NOT NULL, senha VARCHAR(32) NOT NULL, limite text NOT NULL, saldo text NOT NULL);"""
cursor.execute(sql)
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
import datetime
from datetime import date
from tela_inicial import Tela_inicial
from tela_cadastro import Tela_cadastro
from tela_saque import Tela_saque
from tela_extrato import Tela_extrato
from tela_depositar import Tela_depositar
from tela_transacoes import Tela_transacoes
from tela_transferencia import Tela_transferencia
from login_efetuado import Login_efetuado
from dados import Verifica_se_existe, Armazenar, Linha, Update_saldo, Transacoes, Verificar_login
from dados import *



class ClientThread(threading.Thread):
    def __init__(self, clientAddress, clientsocket):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        #self.nome = ''
        print('Nova conexao: ', clientAddress)
    
    def run(self):
        #self.name = self.csocket.recv(1024).decode()
        #print(self.name, " se conectou!")
        msg = ''
        flag = 0
        while True:
            # data = self.csocket.recv(1024)
            data = self.csocket.recv(1024)
            recebe = data.decode()
            if recebe == 'bye':
                break
            print("from ", self.name+": ",recebe)
            # recebe = con.recv(1024)
    
            if recebe == 'entrar' or flag == 1:
                if recebe == 'entrar':
                
                    print('mensagem recebida: '+ recebe)
                    enviar = 'entrar recebido'
                    cpf = ''
                    senha = ''
                    flag = 1
                    self.csocket.send(enviar.encode())
                  
                else:
                    if cpf == '':
                        print('mensagem recebida: '+ recebe)
                        cpf = recebe
                        enviar = 'cpf recebido'
                        self.csocket.send(enviar.encode())
                    elif senha == '':
                        print('mensagem recebida: '+ recebe)
                        senha = recebe
                        flag = 0
                        if Verificar_login(cpf, senha) == '1':
                            enviar = 'True'
                            self.csocket.send(enviar.encode())
                        else:
                            enviar = 'False'
                            self.csocket.send(enviar.encode())
            elif recebe == 'cadastrar' or flag == 2:
                if recebe == 'cadastrar':
                
                    print('mensagem recebida: '+ recebe)
                    enviar = 'cadastrar recebido'
                
                    nome = ''
                    cpf = ''
                    endereco = ''
                    nascimento = ''
                    senha = ''
                    limite = ''
                    saldo = ''
                    flag = 2
                    self.csocket.send(enviar.encode())
                else:
                    if nome == '':
                        print('mensagem recebida: '+ recebe)
                        nome = recebe
                        enviar = 'nome recebido'
                        self.csocket.send(enviar.encode())
                    elif cpf == '':
                        print('mensagem recebida: '+ recebe)
                        cpf = recebe
                        enviar = 'cpf recebido'
                        self.csocket.send(enviar.encode())
                    elif endereco == '':
                        print('mensagem recebida: '+ recebe)
                        endereco = recebe
                        enviar = 'endereco recebido'
                        self.csocket.send(enviar.encode())
                    elif nascimento == '':
                        print('mensagem recebida: '+ recebe)
                        nascimento = recebe
                        enviar = 'nascimento recebido'
                        self.csocket.send(enviar.encode())
                    elif senha == '':
                        print('mensagem recebida: '+ recebe)
                        senha = recebe
                        enviar = 'senha recebido'
                        self.csocket.send(enviar.encode())
                    elif limite == '':
                        print('mensagem recebida: '+ recebe)
                        limite = recebe
                        enviar = 'limite recebido'
                        self.csocket.send(enviar.encode())
                    elif saldo == '':
                        print('mensagem recebida: '+ recebe)
                        saldo = recebe
                        flag = 0
                        if Verifica_se_existe(cpf):
                            enviar = 'True' # eh p ja existe e nao pode cadastrar de novo
                            self.csocket.send(enviar.encode())
                        else:
                            Armazenar(nome, cpf, endereco, nascimento, senha, limite, saldo)
                            historico = f'Conta criada em {datetime.datetime.today()}'
                            Gravar_transacoes(cpf, historico)
                            enviar = 'False'
                            self.csocket.send(enviar.encode())
            elif recebe == 'sacar' or flag == 3:
                if recebe == 'sacar':
                    print('mensagem recebida: '+ recebe)
                    enviar = 'sacar recebido'
                
                    valor = ''
                    cpf = ''
                    flag = 3
                    self.csocket.send(enviar.encode())
              
                else:
                    if valor == '':
                        valor = recebe
                        print('mensagem recebida: '+ recebe)
                        enviar = 'Valor recebido'
                        self.csocket.send(enviar.encode())
                    elif cpf == '':
                        flag = 0
                        cpf = recebe
                        print('mensagem recebida: '+ recebe)
                        resposta = Linha(cpf)

                        if resposta:
                            va = float(valor)
                            saque = float(resposta[7])
                            limite = float(resposta[6])
                    
                            if va <= saque:
                                saque -= va
                                saque = str(saque)
                                historico = f'Saque realizado em {datetime.datetime.today()}'
                                Gravar_transacoes(cpf, historico)
                                Update_saldo(saque, resposta[0])
                            
                            
                                enviar = 'True'
                                self.csocket.send(enviar.encode())
                            else:
                                enviar = 'False'
                                self.csocket.send(enviar.encode())
                        else:
                            enviar = 'None'
                            self.csocket.send(enviar.encode())
            elif recebe == 'depositar' or flag == 7:
                if recebe == 'depositar':
                    print('mensagem recebida: '+ recebe)
                    enviar = 'depositar recebido'
                
                    valor = ''
                    cpf = ''
                    flag = 7
                    self.csocket.send(enviar.encode())
                else:
                    if valor == '':
                        valor = recebe
                        print('mensagem recebida: '+ recebe)
                        enviar = 'Valor recebido'
                        self.csocket.send(enviar.encode())
                    elif cpf == '':
                        flag = 0
                        cpf = recebe
                        print('mensagem recebida: '+ recebe)
                    

                        dados_cpf = Linha(cpf)

                        va = float(valor)
                        saldo = float(dados_cpf[7])
                        total = va + saldo

                        Update_saldo(total, dados_cpf[0])
                    
                        historico = f'Deposito de {valor} em {datetime.datetime.today()}'
                        Gravar_transacoes(cpf, historico)

                        enviar = 'True'
                        self.csocket.send(enviar.encode())
                    
            elif recebe == 'transferir' or flag == 4:
                if recebe == 'transferir':
                    print('mensagem recebida: '+ recebe)
                    enviar = 'transferir recebido'
                
                    valor = ''
                    destino = ''
                    cpf = ''
                    flag = 4
                    self.csocket.send(enviar.encode())
                else:
                    if valor == '':
                        valor = recebe
                        print('mensagem recebida: '+ recebe)
                        enviar = 'Valor recebido'
                        self.csocket.send(enviar.encode())
                    elif destino == '':
                        destino = recebe
                        print('mensagem recebida: '+ recebe)
                        enviar = 'destino recebido'
                        self.csocket.send(enviar.encode())
                    elif cpf == '':
                        cpf = recebe
                        flag = 0
                        print('mensagem recebida: '+ recebe)
                        
                        dados_cpf = Linha(cpf)
                        dados_destino = Linha(destino)

                        if dados_destino == False:
                            enviar = 'None'
                            self.csocket.send(enviar.encode())

                        if float(dados_cpf[7]) >= float(valor):
                            saque = float(dados_cpf[7]) - float(valor)
                            Update_saldo(saque, dados_cpf[0])

                            destino_recebeu = float(dados_destino[7]) + float(valor)
                            Update_saldo(destino_recebeu, dados_destino[0])
                            historico = f'Transferencia de {valor} para {destino} em {datetime.datetime.today()}'
                            Gravar_transacoes(cpf, historico)

                            historico = f'Transferencia recebida de {valor} de {dados_cpf[1]} em {datetime.datetime.today()}'
                            Gravar_transacoes(dados_destino[2], historico)

                            enviar = 'True'
                            self.csocket.send(enviar.encode())
                        else:
                            enviar = 'False'
                            self.csocket.send(enviar.encode())

            elif recebe == 'transacoes' or flag == 5:
                if recebe == 'transacoes':
                
                    print('mensagem recebida: '+ recebe)
                    enviar = 'transacoes recebido'
                
                    cpf = ''
                    flag = 5
                    self.csocket.send(enviar.encode())
                else:
                    if cpf == '':
                        flag = 0
                        cpf = recebe
                        dados_cpf = Transacoes(cpf)
                        
                    
                        if dados_cpf != '':
                            enviar = str(dados_cpf)
                            self.csocket.send(enviar.encode())
                        else:
                            enviar = False
                            self.csocket.send(enviar.encode())


            elif recebe == 'extrato' or flag == 6:
                if recebe == 'extrato':
                
                    print('mensagem recebida: '+ recebe)
                    enviar = 'extrato recebido'
                
                    cpf = ''
                    flag = 6
                    #enviar = 'extrato recebido'
                    
                    self.csocket.send(enviar.encode())
                    #con.send(enviar.encode())
                else:
                    if cpf == '':
                        flag = 0
                        cpf = recebe
                        dados_cpf = Linha(cpf)
                    
                    
                        if dados_cpf:
                            print(dados_cpf)
                            historico = f'Extrato tirado em {datetime.datetime.today()}'
                            Gravar_transacoes(cpf, historico)
                            enviar = str(dados_cpf[1] + ' ' + dados_cpf[7])
                            
                            self.csocket.send(enviar.encode())
                        else:
                            
                            enviar = 'None'
                            self.csocket.send(enviar.encode())
                            #con.send(enviar.encode())
            elif recebe == 'sair':
                enviar = 'sair'
                self.csocket.send(enviar.encode())
        print("Client at ", clientAddress , " disconnected...")

if __name__ == '__main__':
    LOCALHOST = '192.168.1.4'
    PORT = 1235
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADOR, 1)
    server.bind((LOCALHOST, PORT))
    print("Servidor iniciado!")
    print("Aguardando nova conexao...")
    while True:
        server.listen(1)
        clientsock, clientAddress = server.accept()
        newthread = ClientThread(clientAddress, clientsock)
        newthread.start()