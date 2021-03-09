from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLabel, QLineEdit, QGridLayout
import sqlite3
import sys
import time
from Design import *
from Functions import *

SQDB()

class Primary_Windows(QMainWindow): # Janela Princial contera todos os QWidget com seus widgets
    def __init__(self):
        super().__init__()
        
        self.setCentralWidget(Widget_Primary())
        
        self.show()

class Widget_Primary(QWidget):#Widget Principal 
    def __init__(self):
        super().__init__()
        
        self.Layout = QGridLayout(self)
        
        self.NameItem = QLineEdit(self) #Linha para Digitar nome do produto
        self.Layout.addWidget(self.NameItem, 0, 0, 1, 2)
        
        self.CodBarra = QLineEdit(self)
        self.Layout.addWidget(self.CodBarra, 0, 2)
        
        self.DiaVencimento = QLineEdit(self) #Dia que o produto vence
        self.Layout.addWidget(self.DiaVencimento, 0, 3)
        
        self.MesVencimento = QLineEdit(self) #mes que o produto vence
        self.Layout.addWidget(self.MesVencimento, 0, 4)
        
        self.AnoVencimento = QLineEdit(self) #Ano que o produto vence
        self.Layout.addWidget(self.AnoVencimento, 0, 5)
        
        self.CadasterButton = QPushButton('Cadastrar Produto', self)#Botao que Cadastra o Produto
        self.Layout.addWidget(self.CadasterButton, 0, 6)
        self.CadasterButton.clicked.connect(self.CadButton_Func)
    
    def CadButton_Func(self):#Funcao efetuada apos clicar botao de cadastro, faz verificacao depois cadastra Item
        Data = (self.DiaVencimento.text(), self.MesVencimento.text(), self.AnoVencimento.text())
        if Data[0].isnumeric() and Data[1].isnumeric() and Data[2].isnumeric():
            if self.NameItem.text() != '' and self.NameItem.text() != ' ':
                Data = f'{Data[0]}.{Data[1]}.{Data[2]}'
                SQDB().InsertItem(self.CodBarra.text(), self.NameItem.text(), Data)

if __name__ == '__main__':
    App = QApplication(sys.argv)
    Janela = Primary_Windows()
    sys.exit(App.exec_())
