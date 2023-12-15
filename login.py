from PyQt5 import uic, QtWidgets
import mysql.connector
from config import DB_CONFIG

def chamaSegundaTela():
  primeira_tela.label_4.setText("")
  nome_usuario = primeira_tela.lineEdit.text()
  senha = primeira_tela.lineEdit_2.text()
  banco = mysql.connector.connect(**DB_CONFIG)
  cursor = banco.cursor()
  try:
    cursor.execute("SELECT senha FROM cadastro WHERE login = '{}'".format(nome_usuario))
    senha_bd = cursor.fetchall()
    print(senha_bd[0][0])
    banco.close()
  except:
    print("Erro ao validar o login")
  
  if senha==senha_bd[0][0]:
    primeira_tela.close()
    segunda_tela.show()
  else:
    primeira_tela.label_4.setText("Dados de login incorretos!")


def logout():
  segunda_tela.close()
  primeira_tela.show()


def abreTelaCadastro():
    tela_cadastro.show()


def cadastrar():
  nome = tela_cadastro.lineEdit.text()
  login = tela_cadastro.lineEdit_2.text()
  senha = tela_cadastro.lineEdit_3.text()
  c_senha = tela_cadastro.lineEdit_4.text()

  if (senha == c_senha):
    try:
      banco = mysql.connector.connect(**DB_CONFIG)
      cursor = banco.cursor()
      cursor.execute("CREATE TABLE IF NOT EXISTS cadastro (nome VARCHAR (100), login VARCHAR(50), senha VARCHAR(50))")
      cursor.execute("INSERT INTO cadastro VALUES (%s, %s, %s)", (nome, login, senha))

      banco.commit()
      banco.close()
      tela_cadastro.label.setText("Usuário cadastrado com sucesso")

    except mysql.Error as error:
      print("Erro ao inserir os dados ", error)
    finally:
      banco.close()
  else:
    tela_cadastro.label.setText("AS senhas digitadas são difernetes")




app=QtWidgets.QApplication([])
primeira_tela=uic.loadUi("primeira_tela.ui")
segunda_tela=uic.loadUi("segunda_tela.ui")
tela_cadastro = uic.loadUi("tela_cadastro.ui")
primeira_tela.pushButton.clicked.connect(chamaSegundaTela)
segunda_tela.pushButton.clicked.connect(logout)
primeira_tela.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
primeira_tela.pushButton_2.clicked.connect(abreTelaCadastro)
tela_cadastro.pushButton.clicked.connect(cadastrar)

primeira_tela.show()
app.exec()