from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLabel, QLineEdit, QGridLayout
import sqlite3
import sys
import time
from Design import *
from Functions import *

class Primary_Windows(QMainWindow): # Janela Princial contera todos os QWidget com seus widgets
    def __init__(self):
        super().__init__()
        
        self.setCentralWidget(Widget_Primary())
        
        self.show()

class Widget_Primary(QWidget):#Widget Principal 
    def __init__(self):
        super().__init__()
        
        self.Layout = QGridLayout(self)
        
        NameItem = QLineEdit(self) #Linha para Digitar nome do produto
        self.Layout.addWidget(NameItem, 0, 0, 1, 2)
        
        DiaVencimento = QLineEdit(self) #Dia que o produto vence
        self.Layout.addWidget(DiaVencimento, 0, 2)
        
        MesVencimento = QLineEdit(self) #mes que o produto vence
        self.Layout.addWidget(MesVencimento, 0, 3)
        
        AnoVencimento = QLineEdit(self) #Ano que o produto vence
        self.Layout.addWidget(AnoVencimento, 0, 4)
        
        CadasterButton = QPushButton('Cadastrar Produto', self)#Botao que Cadastra o Produto
        self.Layout.addWidget(CadasterButton, 0, 5)
        

if __name__ == '__main__':
    App = QApplication(sys.argv)
    Janela = Primary_Windows()
    sys.exit(App.exec_())
