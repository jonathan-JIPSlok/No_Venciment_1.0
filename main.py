from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLabel, QLineEdit, QGridLayout, QTabWidget
import sqlite3
import sys
import time
from Design import *
from Functions import *
import shelve

UserConfigs = shelve.open("Configs")
try:
    if len(UserConfigs['DisplayGeometry_Largura']) > 0 and len(UserConfigs['DisplayGeometry_Altura']) > 0:
        Display = (int(UserConfigs["DisplayGeometry_Largura"]), int(UserConfigs['DisplayGeometry_Altura']))
except:
    UserConfigs['DisplayGeometry_Largura'] = "620"
    UserConfigs['DisplayGeometry_Altura'] = "320"
    Display = (int(UserConfigs["DisplayGeometry_Largura"]), int(UserConfigs['DisplayGeometry_Altura']))


SQDB().Close()
displayConfigs = [(1280, 700), (1360, 720), (620, 320)]

class Primary_Windows(QMainWindow): # Janela Princial contera todos os QWidget com seus widgets
    def __init__(self):
        super().__init__()
        
        self.setCentralWidget(Widget_Primary())
        self.setGeometry(0, 0, Display[0], Display[1])
        
        self.show()

class Widget_Primary(QWidget):#Widget Principal 
    def __init__(self):
        super().__init__()
        
        self.Layout = QGridLayout(self)
        
        self.TabItems = QTabWidget(self)
        self.Layout.addWidget(self.TabItems)
        self.TabItems.addTab(WindowConfigs(), "Configurações")
        self.TabItems.addTab(Window_CadasterItems(), 'Cadastro')

class WindowConfigs(QWidget):
    def __init__(self):
        super().__init__()

        self.Layout = QGridLayout(self)

class Window_CadasterItems(QWidget):
    def __init__(self):
        super().__init__()

        self.Layout = QGridLayout(self)

        self.NameItem = QLineEdit(self) #Linha para Digitar nome do produto
        self.Layout.addWidget(self.NameItem, 1, 0, 1, 2)
        self.NameItem.setPlaceholderText('Nome Item')
        self.NameItem.returnPressed.connect(lambda : self.CodBarra.setFocus())
        
        self.CodBarra = QLineEdit(self)
        self.Layout.addWidget(self.CodBarra, 1, 2)
        self.CodBarra.setPlaceholderText("Codigo Barra")
        self.CodBarra.returnPressed.connect(lambda : self.DiaVencimento.setFocus())
        
        self.DiaVencimento = QLineEdit(self) #Dia que o produto vence
        self.Layout.addWidget(self.DiaVencimento, 1, 3)
        self.DiaVencimento.setFixedWidth(30)
        self.DiaVencimento.setPlaceholderText("Dia")
        self.DiaVencimento.returnPressed.connect(lambda : self.MesVencimento.setFocus())
        
        self.MesVencimento = QLineEdit(self) #mes que o produto vence
        self.Layout.addWidget(self.MesVencimento, 1, 4)
        self.MesVencimento.setFixedWidth(30)
        self.MesVencimento.setPlaceholderText("Mês")
        self.MesVencimento.returnPressed.connect(lambda : self.AnoVencimento.setFocus())
        
        self.AnoVencimento = QLineEdit(self) #Ano que o produto vence
        self.Layout.addWidget(self.AnoVencimento, 1, 5)
        self.AnoVencimento.setFixedWidth(40)
        self.AnoVencimento.setPlaceholderText("Ano")
        self.AnoVencimento.returnPressed.connect(self.CadButton_Func)

        self.CadasterButton = QPushButton('Cadastrar Produto', self)#Botao que Cadastra o Produto
        self.Layout.addWidget(self.CadasterButton, 1, 6)
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
