from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLabel, QLineEdit, QGridLayout, QTabWidget, QComboBox, QTableWidget, QTableWidgetItem
import sqlite3
import sys
import time
from Design import *
from Functions import *
import shelve

UserConfigs = shelve.open("Configs")

try: #Configuracoes do programa
    if len(UserConfigs['DisplayGeometry_Largura']) >= 0 and len(UserConfigs['DisplayGeometry_Altura']) >= 0:
        Display = (int(UserConfigs["DisplayGeometry_Largura"]), int(UserConfigs['DisplayGeometry_Altura']))
except:
    UserConfigs['DisplayGeometry_Largura'] = "620"
    UserConfigs['DisplayGeometry_Altura'] = "320"
    Display = (int(UserConfigs["DisplayGeometry_Largura"]), int(UserConfigs['DisplayGeometry_Altura']))
finally:
    UserConfigs.close()


SQDB().Close()

class Primary_Windows(QMainWindow): # Janela Princial contera todos os QWidget com seus widgets
    def __init__(self):
        super().__init__()
        
        self.WidgetPrincipal = Widget_Primary()
        self.setCentralWidget(self.WidgetPrincipal)
        self.setGeometry(0, 0, Display[0], Display[1])
        
        self.show()

class Widget_Primary(QWidget):#Widget Principal 
    def __init__(self):
        super().__init__()
        
        self.Layout = QGridLayout(self)
        self.Lista_ItemsTot = Tabelas()
        
        self.TabItems = QTabWidget(self)
        self.Layout.addWidget(self.TabItems)
        self.TabItems.addTab(WindowConfigs(), "Configurações")
        self.TabItems.addTab(Window_CadasterItems(), 'Cadastro')
        self.TabItems.addTab(self.Lista_ItemsTot, "Lista")

class WindowConfigs(QWidget):
    def __init__(self):
        super().__init__()

        self.Layout = QGridLayout(self)

        self.LabeDisplay_Configure = QLabel("Display", self) #Label de display
        self.LabeDisplay_Configure.setMaximumWidth(50) #Tamanho da label/Widget
        self.Display_ConfigureLargura = QLineEdit(str(Display[0]), self) #largura desejada da tela
        self.Display_ConfigureLargura.setMaximumWidth(50)
        self.Display_ConfigureAltura = QLineEdit(str(Display[1]), self) #Altura desejada da tela
        self.Display_ConfigureAltura.setMaximumWidth(50)
        self.Layout.addWidget(self.LabeDisplay_Configure, 0, 0)#Adcinionado widgest a tela
        self.Layout.addWidget(self.Display_ConfigureLargura, 0, 1)
        self.Layout.addWidget(self.Display_ConfigureAltura, 0, 2)

        self.SaveButton = QPushButton("Salvar", self)
        self.Layout.addWidget(self.SaveButton, 5, 0, 1, 3)
        self.SaveButton.clicked.connect(self.SaveConfigs)

    def SaveConfigs(self): #Salva as configuracoes no arquivo configs
        UserConfigs = shelve.open("Configs")
        UserConfigs.__setitem__('DisplayGeometry_Largura', self.Display_ConfigureLargura.text())
        UserConfigs.__setitem__('DisplayGeometry_Altura', self.Display_ConfigureAltura.text())
        UserConfigs.close()
        Janela.setGeometry(10,30,int(self.Display_ConfigureLargura.text()), int(self.Display_ConfigureAltura.text()))
class Window_CadasterItems(QWidget):
    def __init__(self):
        super().__init__()

        self.Layout = QGridLayout(self)

        self.NameItem = QLineEdit(self) #Linha para Digitar nome do produto
        self.Layout.addWidget(self.NameItem, 1, 0)
        self.NameItem.setPlaceholderText('Nome Item')
        self.NameItem.returnPressed.connect(lambda : self.CodBarra.setFocus())
        
        self.CodBarra = QLineEdit(self)
        self.Layout.addWidget(self.CodBarra, 2, 0)
        self.CodBarra.setPlaceholderText("Codigo Barra")
        self.CodBarra.returnPressed.connect(lambda : self.DiaVencimento.setFocus())
        
        self.DiaVencimento = QLineEdit(self) #Dia que o produto vence
        self.Layout.addWidget(self.DiaVencimento, 3, 0)
        self.DiaVencimento.setFixedWidth(30)
        self.DiaVencimento.setPlaceholderText("Dia")
        self.DiaVencimento.returnPressed.connect(lambda : self.MesVencimento.setFocus())
        
        self.MesVencimento = QLineEdit(self) #mes que o produto vence
        self.Layout.addWidget(self.MesVencimento, 4, 0)
        self.MesVencimento.setFixedWidth(30)
        self.MesVencimento.setPlaceholderText("Mês")
        self.MesVencimento.returnPressed.connect(lambda : self.AnoVencimento.setFocus())
        
        self.AnoVencimento = QLineEdit(self) #Ano que o produto vence
        self.Layout.addWidget(self.AnoVencimento, 5, 0)
        self.AnoVencimento.setFixedWidth(40)
        self.AnoVencimento.setPlaceholderText("Ano")
        self.AnoVencimento.returnPressed.connect(self.CadButton_Func)

        self.CadasterButton = QPushButton('Cadastrar Produto', self)#Botao que Cadastra o Produto
        self.Layout.addWidget(self.CadasterButton, 6, 0)
        self.CadasterButton.clicked.connect(self.CadButton_Func)

    def CadButton_Func(self):#Funcao efetuada apos clicar botao de cadastro, faz verificacao depois cadastra Item
        Data = (self.DiaVencimento.text(), self.MesVencimento.text(), self.AnoVencimento.text())
        if Data[0].isnumeric() and Data[1].isnumeric() and Data[2].isnumeric():
            if self.NameItem.text() != '' and self.NameItem.text() != ' ':
                Data = f'{Data[0]}.{Data[1]}.{Data[2]}'
                SQDB().InsertItem(self.CodBarra.text(), self.NameItem.text(), Data)
                self.CodBarra.setText('')
                self.NameItem.setText("")
                self.DiaVencimento.setText('')
                self.MesVencimento.setText("")
                self.AnoVencimento.setText("")
                Janela.WidgetPrincipal.Lista_ItemsTot.ResetTable()

class Tabelas(QWidget): #tabela com todos os items cadastrados no sistema
    def __init__(self, Type = 'Geral'):
        super().__init__()
        self.Type = Type
        self.Layout = QGridLayout(self)#Layout da tela

        self.Tabela = QTableWidget()#tabela
        self.Layout.addWidget(self.Tabela)

        self.Tabela.setColumnCount(4)
        self.AddRow()

        self.Tabela.show()

    def AddRow(self):
        Data = SQDB().getItems(self.Type)
        self.ItemsObject = []
        ItemAtual = {}
        itemCount = 0
        listaCount = 0

        for lista in Data: #Cada lista detro de Data
            self.Tabela.insertRow(self.Tabela.rowCount()) #Adiciona uma nova linha
            for item in lista: #Cada item dentro da lista
                Objeto = QTableWidgetItem(str(item)) #Objeto do item
                ItemAtual[item] = Objeto #Adiciona o objeto a uma lista para ser uzado mais tarde
                self.Tabela.setItem(self.Tabela.rowCount() - 1, itemCount, Objeto) #insere os items a tabela

                itemCount += 1
            itemCount = 0
            self.ItemsObject.append(ItemAtual)
            ItemAtual = {}
            listaCount += 1

        self.Tabela.cellDoubleClicked.connect(lambda : self.VerifiSelected(self.ItemsObject))

    def ResetTable(self): #Reseta a tabela
        while self.Tabela.rowCount() > 0:           
            self.Tabela.removeRow(self.Tabela.rowCount() - 1)
        self.AddRow()

    def VerifiSelected(self, Data):
        for Item in Data: #pega cada item (key e value)
            for items in Item.values(): #Pega apenas o Objeto
                print(items)
                try:
                    if items.isSelected() == True: #Verifica se o Objeto foi selecionado
                        Data = Item.keys() #Obtem os dados da linha na qual o Usuario selecionou
                        
                except RuntimeError: pass

if __name__ == '__main__':
    App = QApplication(sys.argv)
    Janela = Primary_Windows()
    sys.exit(App.exec_())
