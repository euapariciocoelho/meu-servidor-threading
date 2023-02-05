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
from dados import *


class Ui_Main(QtWidgets.QWidget):
    def setupUi(self, Main):
        Main.setObjectName('Main')
        Main.resize(640, 480)

        self.QtStack = QtWidgets.QStackedLayout()

        self.stack0 = QtWidgets.QMainWindow()
        self.stack1 = QtWidgets.QMainWindow()
        self.stack2 = QtWidgets.QMainWindow()
        self.stack3 = QtWidgets.QMainWindow()
        self.stack4 = QtWidgets.QMainWindow()
        self.stack5 = QtWidgets.QMainWindow()
        self.stack6 = QtWidgets.QMainWindow()
        self.stack7 = QtWidgets.QMainWindow()

        self.tela_inicial = Tela_inicial()
        self.tela_inicial.setupUi(self.stack0)

        self.tela_cadastro = Tela_cadastro()
        self.tela_cadastro.setupUi(self.stack1)

        self.tela_saque = Tela_saque()
        self.tela_saque.setupUi(self.stack2)

        self.tela_extrato = Tela_extrato()
        self.tela_extrato.setupUi(self.stack3)

        self.tela_depositar = Tela_depositar()
        self.tela_depositar.setupUi(self.stack4)

        self.tela_transacoes = Tela_transacoes()
        self.tela_transacoes.setupUi(self.stack5)

        self.tela_transferencia = Tela_transferencia()
        self.tela_transferencia.setupUi(self.stack6)

        self.login_efetuado = Login_efetuado()
        self.login_efetuado.setupUi(self.stack7)

        self.QtStack.addWidget(self.stack0)
        self.QtStack.addWidget(self.stack1)
        self.QtStack.addWidget(self.stack2)
        self.QtStack.addWidget(self.stack3)
        self.QtStack.addWidget(self.stack4)
        self.QtStack.addWidget(self.stack5)
        self.QtStack.addWidget(self.stack6)
        self.QtStack.addWidget(self.stack7)


class Main(QMainWindow, Ui_Main):
    def __init__(self):
        super(Main, self).__init__(None)
        self.setupUi(self)

        self.cad = Conta()

        self.tela_inicial.pushButton_3.clicked.connect(self.abrir_tela_login)
        self.tela_inicial.pushButton_2.clicked.connect(
            self.abrir_tela_cadastro)
        self.tela_inicial.pushButton_4.clicked.connect(self.botaoSair)

        self.tela_cadastro.pushButton.clicked.connect(self.botaoCadastrar)
        self.tela_cadastro.pushButton_2.clicked.connect(self.botaoVoltar)

        self.login_efetuado.pushButton_2.clicked.connect(self.abrir_tela_saque)
        self.login_efetuado.pushButton_3.clicked.connect(
            self.abrir_tela_depositar)

        self.login_efetuado.pushButton_4.clicked.connect(
            self.abrir_tela_extrato)
        self.login_efetuado.pushButton_5.clicked.connect(
            self.abrir_tela_transacoes)
        self.login_efetuado.pushButton_6.clicked.connect(
            self.abrir_tela_transferencia)
        self.login_efetuado.pushButton_7.clicked.connect(self.botaoVoltar)

        self.tela_saque.pushButton.clicked.connect(self.botaoSaque)
        self.tela_saque.pushButton_2.clicked.connect(self.botaoVoltarLogin)

        self.tela_extrato.pushButton.clicked.connect(self.botaoExtrato)
        self.tela_extrato.pushButton_2.clicked.connect(self.botaoVoltarLogin)

        self.tela_depositar.pushButton.clicked.connect(self.botaoDepositar)
        self.tela_depositar.pushButton_2.clicked.connect(self.botaoVoltarLogin)

        self.tela_transferencia.pushButton.clicked.connect(
            self.botaoTransferencia)
        self.tela_transferencia.pushButton_2.clicked.connect(
            self.botaoVoltarLogin)

        self.tela_transacoes.pushButton.clicked.connect(self.botaoTransacoes)
        self.tela_transacoes.pushButton_2.clicked.connect(
            self.botaoVoltarLogin)

    def botaoCadastrar(self):

        nome = self.tela_cadastro.lineEdit.text()
        cpf = self.tela_cadastro.lineEdit_2.text()
        endereco = self.tela_cadastro.lineEdit_3.text()
        nascimento = self.tela_cadastro.lineEdit_4.text()
        senha = self.tela_cadastro.lineEdit_5.text()
        limite = self.tela_cadastro.lineEdit_6.text()
        saldo = self.tela_cadastro.lineEdit_7.text()

        if not (nome == '' or endereco == '' or cpf == '' or nascimento == '' or senha == '' or limite == '' or saldo == ''):
           

            if self.cad.verifica_se_existe(cpf) == None:
                historico = f'Conta criada em {datetime.datetime.today()}'
                armazenar(nome, cpf, endereco, nascimento, senha, limite, saldo)
                con = mysql.connector.connect(host='localhost', db='banco', user='root', password='123456')

                cursor = con.cursor()

                sql = """CREATE TABLE IF NOT EXISTS transacoes (id integer AUTO_INCREMENT PRIMARY KEY, cpf_user text, transacoes text NULL);"""
                cursor.execute(sql)

                cursor.execute("INSERT INTO transacoes (cpf_user, transacoes) VALUES (%s, %s)", (cpf, historico))
                con.commit()
                
                QMessageBox.information(
                    None, 'POOII', 'Cadastro realizado com sucesso')
                self.tela_cadastro.lineEdit.setText('')
                self.tela_cadastro.lineEdit_2.setText('')
                self.tela_cadastro.lineEdit_3.setText('')
                self.tela_cadastro.lineEdit_4.setText('')
                self.tela_cadastro.lineEdit_5.setText('')
                self.tela_cadastro.lineEdit_6.setText('')
                self.tela_cadastro.lineEdit_7.setText('')
                self.QtStack.setCurrentIndex(0)

            else:
                QMessageBox.information(
                    None, 'POOII', 'O cpf informado já está cadastrado')
                self.tela_cadastro.lineEdit.setText('')
                self.tela_cadastro.lineEdit_2.setText('')
                self.tela_cadastro.lineEdit_3.setText('')
                self.tela_cadastro.lineEdit_4.setText('')
                self.tela_cadastro.lineEdit_5.setText('')
                self.tela_cadastro.lineEdit_6.setText('')
                self.tela_cadastro.lineEdit_7.setText('')
        else:
            QMessageBox.information(
                None, 'POOII', 'Todos os valores devem estar preenchidos')

    def botaoExtrato(self):
        cpf = self.tela_inicial.lineEdit.text()

        con = mysql.connector.connect(host='localhost', db='banco', user='root', password='123456')
        cursor = con.cursor()
        cursor.execute("SELECT * FROM teste1")
        for c in cursor:
            if cpf in c:
                tupla = c
        con.commit()
        con.close()
        self.tela_extrato.lineEdit_3.setText(tupla[1])
        self.tela_extrato.lineEdit_4.setText(tupla[2])
        self.tela_extrato.lineEdit_5.setText(tupla[7])

        con = mysql.connector.connect(host='localhost', db='banco', user='root', password='123456')

        cursor = con.cursor()

        # sql = """CREATE TABLE IF NOT EXISTS transacoes (id integer AUTO_INCREMENT PRIMARY KEY, cpf_user text, transacoes text NULL);"""
        # cursor.execute(sql)
        historico = f'Extrato tirado em {datetime.datetime.today()}'

        cursor.execute("INSERT INTO transacoes (cpf_user, transacoes) VALUES (%s, %s)", (cpf, historico))
        con.commit()


    def botaoSaque(self):

        valor = self.tela_saque.lineEdit.text()

        cpf = self.tela_inicial.lineEdit.text()
        if not (valor == ''):
            con = mysql.connector.connect(host='localhost', db='banco', user='root', password='123456')
            cursor = con.cursor()
            cursor.execute("SELECT * FROM teste1")

            for c in cursor:
                if cpf in c:
                    tupla = c
            con.commit()
            con.close()

            va = float(valor)
            saque = float(tupla[7])
            limite = float(tupla[6])
            
            if va <= saque:
                saque -= va
                saque = str(saque)
                
                con = mysql.connector.connect(host='localhost', db='banco', user='root', password='123456')
                cursor = con.cursor()
                cursor.execute("UPDATE teste1 SET saldo = " + saque + "WHERE id = " + str(tupla[0]))
                
                con.commit()

                con = mysql.connector.connect(host='localhost', db='banco', user='root', password='123456')

                cursor = con.cursor()

                # sql = """CREATE TABLE IF NOT EXISTS transacoes (id integer AUTO_INCREMENT PRIMARY KEY, cpf_user text, transacoes text NULL);"""
                # cursor.execute(sql)

                historico = f'Saque realizado em {datetime.datetime.today()}'
                cursor.execute("INSERT INTO transacoes (cpf_user, transacoes) VALUES (%s, %s)", (cpf, historico))
                con.commit()
                    

                QMessageBox.information(None, 'POOII', 'Saque realizado com sucesso.')
            else:
                QMessageBox.information(
                    None, 'POOII', 'Não é possivel realizar saque')
        else:
            QMessageBox.information(None, 'POOII', 'Preencha o campo')


    def botaoTransacoes(self):
        cpf = self.tela_inicial.lineEdit.text()
        self.tela_transacoes.listWidget.clear()
        destino = self.tela_transferencia.lineEdit_2.text()
        con = mysql.connector.connect(host='localhost', db='banco', user='root', password='123456')
        cursor = con.cursor()
        cursor.execute("SELECT * FROM transacoes")

        for c in cursor:
            if cpf in c:
                self.tela_transacoes.listWidget.addItem(c[2])
        

    def botaoDepositar(self):
        valor = self.tela_depositar.lineEdit.text()
        cpf = self.tela_inicial.lineEdit.text()

        con = mysql.connector.connect(host='localhost', db='banco', user='root', password='123456')
        cursor = con.cursor()
        cursor.execute("SELECT * FROM teste1")

        for c in cursor:
            if cpf in c:
                tupla = c
        con.commit()
        con.close()

        valor = float(valor)
        limite = float(tupla[6])
        saldo = float(tupla[7])
        total = valor + saldo
        if total <= limite:
            con = mysql.connector.connect(host='localhost', db='banco', user='root', password='123456')
            cursor = con.cursor()
            cursor.execute("UPDATE teste1 SET saldo = " + str(total) + "WHERE id = " + str(tupla[0]))
            con.commit()

            con = mysql.connector.connect(host='localhost', db='banco', user='root', password='123456')

            cursor = con.cursor()

            sql = """CREATE TABLE IF NOT EXISTS transacoes (id integer AUTO_INCREMENT PRIMARY KEY, cpf_user text, transacoes text NULL);"""
            cursor.execute(sql)

            historico = f'Deposito realizado em {datetime.datetime.today()}'
           # cursor.execute("INSERT INTO transacoes (cpf_user, transacoes) VALUES (%s, %s)", (cpf, historico))
           # con.commit()
            QMessageBox.information(None, 'POOII', 'Deposito realizado com sucesso')
            self.tela_cadastro.lineEdit.setText('')

        else:
            QMessageBox.information(None, 'POOII', 'Limite insuficiente')
            

    def botaoTransferencia(self):
        cpf = self.tela_inicial.lineEdit.text()
        con = mysql.connector.connect(host='localhost', db='banco', user='root', password='123456')
        cursor = con.cursor()
        cursor.execute("SELECT * FROM teste1")

        for c in cursor:
            if cpf in c:
                tupla = c
        con.commit()
        con.close()

        valor = self.tela_transferencia.lineEdit.text()
        destino = self.tela_transferencia.lineEdit_2.text()
        con = mysql.connector.connect(host='localhost', db='banco', user='root', password='123456')
        cursor = con.cursor()
        cursor.execute("SELECT * FROM teste1")

        for c in cursor:
            if destino in c:
                destino_dados = c
        if valor == '' or destino == '':
            QMessageBox.information(None, 'POOII', 'Preencha todos os campos')
        elif destino_dados == '':
            QMessageBox.information(None, 'POOII', 'Conta para transferencia não encontrada')
        else:
            
            saque = float(tupla[7]) - float(valor)
            # ajeitar aqui
            con = mysql.connector.connect(host='localhost', db='banco', user='root', password='123456')
            cursor = con.cursor()
            cursor.execute("UPDATE teste1 SET saldo = " + str(saque) + "WHERE id = " + str(tupla[0]))
            con.commit()


            destino_atualizado = float(destino_dados[7]) + float(valor)
            con = mysql.connector.connect(host='localhost', db='banco', user='root', password='123456')
            cursor = con.cursor()
            cursor.execute("UPDATE teste1 SET saldo = " + str(destino_atualizado) + "WHERE id = " + str(destino_dados[0]))
            con.commit()

            con = mysql.connector.connect(host='localhost', db='banco', user='root', password='123456')

            cursor = con.cursor()

            #sql = """CREATE TABLE IF NOT EXISTS transacoes (id integer AUTO_INCREMENT PRIMARY KEY, cpf_user text, transacoes text NULL);"""
            #cursor.execute(sql)

            historico = f'Transferencia de {valor} para {destino_dados[1]} em {datetime.datetime.today()}'
            cursor.execute("INSERT INTO transacoes (cpf_user, transacoes) VALUES (%s, %s)", (cpf, historico))
            historico = f'Transferencia recebida em {datetime.datetime.today()} de {tupla[1]}'
            cursor.execute("INSERT INTO transacoes (cpf_user, transacoes) VALUES (%s, %s)", (destino, historico))
            con.commit()
            QMessageBox.information(None, 'POOII', 'Transferência concluida')
            self.tela_transferencia.lineEdit.setText('')
            self.tela_transferencia.lineEdit_2.setText('')

    def botaoSair(self):
        con.close()
        sys.exit()

    def botaoVoltarLogin(self):
        self.QtStack.setCurrentIndex(7)

    def botaoVoltar(self):
        self.tela_inicial.lineEdit.setText('')
        self.tela_inicial.lineEdit_2.setText('')
        self.tela_extrato.lineEdit_3.setText('')
        self.tela_extrato.lineEdit_4.setText('')
        self.tela_extrato.lineEdit_5.setText('')
        self.QtStack.setCurrentIndex(0)

    def abrir_tela_cadastro(self):
        self.QtStack.setCurrentIndex(1)

    def abrir_tela_saque(self):
        self.QtStack.setCurrentIndex(2)

    def abrir_tela_extrato(self):
        self.tela_extrato.lineEdit_3.setText('')
        self.tela_extrato.lineEdit_4.setText('')
        self.tela_extrato.lineEdit_5.setText('')
        self.QtStack.setCurrentIndex(3)

    def abrir_tela_depositar(self):
        self.QtStack.setCurrentIndex(4)

    def abrir_tela_transacoes(self):
        self.tela_transacoes.listWidget.clear()
        self.QtStack.setCurrentIndex(5)

    def abrir_tela_transferencia(self):
        self.QtStack.setCurrentIndex(6)

    def abrir_tela_login(self):
        cpf = self.tela_inicial.lineEdit.text()
        senha = self.tela_inicial.lineEdit_2.text()
        if cpf == '' or senha == '':
            QMessageBox.information(None, 'POOII', 'Preencha todos os campos')
        else:
            con = mysql.connector.connect(host='localhost', db='banco', user='root', password='123456')
            cursor = con.cursor()
            cursor.execute('SELECT * FROM teste1 WHERE cpf = %s AND senha = MD5(%s)', (cpf, senha))

            cont = 0
            for c in cursor:
                if c != '':
                    cont = 1
            if cont == 1:
                self.QtStack.setCurrentIndex(7)
            else:
                QMessageBox.information(None, 'POOII', 'ALGO DEU ERRADO =(')
            
            con.commit()
            con.close()


        '''cpf = self.tela_inicial.lineEdit.text()
        senha = self.tela_inicial.lineEdit_2.text()
        existe = self.verificar_login(cpf, senha)
        if cpf == '' or senha == '':
            QMessageBox.information(None, 'POOII', 'Preencha todos os campos')
        else:
            if existe:
                self.QtStack.setCurrentIndex(7)
            elif existe == False:
                QMessageBox.information(None, 'POOII', 'Senha invalida')
                self.tela_inicial.lineEdit.setText('')
                self.tela_inicial.lineEdit_2.setText('')
            else:
                QMessageBox.information(None, 'POOII', 'CPF não cadastrado')
                self.tela_inicial.lineEdit.setText('')
                self.tela_inicial.lineEdit_2.setText('')'''


if __name__ == '__main__':
    app = QApplication(sys.argv)
    show_main = Main()
    sys.exit(app.exec_())
