from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLabel, QLineEdit, QGridLayout, QTabWidget, QComboBox, QTableWidget, QTableWidgetItem, QMessageBox, QDateEdit
from PyQt5.QtCore import QDateTime
import sqlite3
import sys
import time
import Design
from Design import *
from Functions import *
from datetime import date
import shelve

UserConfigs = shelve.open("Configs")

try: #Configuracoes do programa
    if len(UserConfigs['DisplayGeometry_Largura']) >= 0 and len(UserConfigs['DisplayGeometry_Altura']) >= 0:
        Display = (int(UserConfigs["DisplayGeometry_Largura"]), int(UserConfigs['DisplayGeometry_Altura']))
except:
    UserConfigs['DisplayGeometry_Largura'] = "750"
    UserConfigs['DisplayGeometry_Altura'] = "320"
    UserConfigs['Thema'] = 'Dark_Theme'
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
        self.setStyle()
        self.setWindowTitle("AntiVenciment")
        self.show()
    
    def setStyle(self):
        UserConfigs = shelve.open("Configs")
        if UserConfigs["Thema"] == 'Dark_Theme':
            self.setStyleSheet(Design.Dark_Theme)
        elif UserConfigs["Thema"] == "Light_Theme":
            self.setStyleSheet(Design.Light_Theme)

class Widget_Primary(QWidget):#Widget Principal 
    def __init__(self):
        super().__init__()
        
        self.Layout = QGridLayout(self)
        self.Lista_ItemsTot = Tabelas()
        self.Lista_PertoVencimento = Tabelas(Type = 'Perto')
        self.Lista_Vencidos = Tabelas(Type = 'Vencido')
        self.Informacoes = Window_Informations([self.Lista_ItemsTot, self.Lista_PertoVencimento, self.Lista_Vencidos])
        
        self.TabItems = QTabWidget(self)
        self.Layout.addWidget(self.TabItems)
        
        self.TabItems.addTab(self.Informacoes, "Informações")
        self.TabItems.addTab(Window_CadasterItems(), 'Cadastro')
        self.TabItems.addTab(self.Lista_ItemsTot, "Lista")
        self.TabItems.addTab(self.Lista_PertoVencimento, "Perto do Vencimento")
        self.TabItems.addTab(self.Lista_Vencidos, "Items Vencidos")
        self.TabItems.addTab(WindowConfigs(), "Configurações")

class Window_Informations(QWidget):
    def __init__(self, Janela):
        super().__init__()
        self.Layout = QGridLayout(self)
        self.Janela = Janela
        Data = self.ColetinData()

        self.LabelTot = QLabel(Data[0], self)
        self.LabelPerto = QLabel(Data[1], self)
        self.LabelVencido = QLabel(Data[2], self)

        TotItems = QLabel('Total de items:', self)
        self.Layout.addWidget(TotItems,0,0)
        self.Layout.addWidget(self.LabelTot, 0, 1)

        ItemsPerto_Vencimento = QLabel("Items perto de vencer:", self)
        self.Layout.addWidget(ItemsPerto_Vencimento, 1,0)
        self.Layout.addWidget(self.LabelPerto, 1, 1)

        ItemsVencidos = QLabel("Items Vencidos:", self)
        self.Layout.addWidget(ItemsVencidos, 2, 0)
        self.Layout.addWidget(self.LabelVencido, 2, 1)

    def ColetinData(self):
        lista = []
        lista.append(str(self.Janela[0].RowCountTot))
        lista.append(str(self.Janela[1].RowCountTot))
        lista.append(str(self.Janela[2].RowCountTot))
        return lista

    def Atualizar(self):
        self.LabelTot.setText(str(self.ColetinData()[0]))
        self.LabelPerto.setText(str(self.ColetinData()[1]))
        self.LabelVencido.setText(str(self.ColetinData()[2]))

class WindowConfigs(QWidget):
    def __init__(self):
        super().__init__()

        self.Layout = QGridLayout(self)

        self.LabeDisplay_Configure = QLabel("Display", self) #Label de display
        self.LabeDisplay_Configure.setMaximumWidth(60) #Tamanho da label/Widget

        self.Display_ConfigureLargura = QLineEdit(str(Display[0]), self) #largura desejada da tela
        self.Display_ConfigureLargura.setMaximumWidth(50)
        self.Display_ConfigureAltura = QLineEdit(str(Display[1]), self) #Altura desejada da tela
        self.Display_ConfigureAltura.setMaximumWidth(50)

        self.Layout.addWidget(self.LabeDisplay_Configure, 0, 0)#Adcinionado widgest a tela
        self.Layout.addWidget(self.Display_ConfigureLargura, 0, 1)
        self.Layout.addWidget(self.Display_ConfigureAltura, 0, 2)

        self.ResetButton_Items = QPushButton("Resetar items cadastrados", self) #Reseta o banco de dados
        self.Layout.addWidget(self.ResetButton_Items, 0, 3)
        self.ResetButton_Items.clicked.connect(self.Verify_Reset)
        self.ResetButton_Items.clicked.connect(lambda : Janela.WidgetPrincipal.Lista_ItemsTot.ResetTable())
        self.ResetButton_Items.clicked.connect(lambda : Janela.WidgetPrincipal.Lista_Vencidos.ResetTable())
        self.ResetButton_Items.clicked.connect(lambda : Janela.WidgetPrincipal.Lista_PertoVencimento.ResetTable())
        self.ResetButton_Items.clicked.connect(lambda : Janela.WidgetPrincipal.Informacoes.Atualizar())

        self.SetTheme_Button = QComboBox(self)
        self.SetTheme_Button.addItems(['Dark-Theme', "Light-Theme"])
        self.SetTheme_Button.activated[str].connect(self.SetTheme)
        self.Layout.addWidget(self.SetTheme_Button, 1, 0, 1, 3)

        self.SaveButton = QPushButton("Salvar", self)
        self.Layout.addWidget(self.SaveButton, 5, 0, 1, 4)
        self.SaveButton.clicked.connect(self.SaveConfigs)

    def SaveConfigs(self): #Salva as configuracoes no arquivo configs
        UserConfigs = shelve.open("Configs")
        if self.Display_ConfigureLargura.text().isnumeric() and self.Display_ConfigureAltura.text().isnumeric():
            UserConfigs.__setitem__('DisplayGeometry_Largura', self.Display_ConfigureLargura.text())
            UserConfigs.__setitem__('DisplayGeometry_Altura', self.Display_ConfigureAltura.text())
            UserConfigs.close()
            Janela.setGeometry(10,30,int(self.Display_ConfigureLargura.text()), int(self.Display_ConfigureAltura.text()))
        else: 
            MSG = QMessageBox()
            MSG.setIcon(QMessageBox.Information)
            MSG.setWindowTitle("Problema!")
            MSG.setText("Apenas números no tamanho do Display!")
            MSG.exec_()

    def Verify_Reset(self):
        MSG = QMessageBox(QMessageBox.Question, "Alerta", "Deseja mesmo Resetar os Dados?", QMessageBox.StandardButton(QMessageBox.Yes | QMessageBox.No))
        button = MSG.exec_()
        if button == QMessageBox.Yes:
            SQDB().Reset()
    
    def SetTheme(self):
        UserConfigs = shelve.open("Configs")
        if self.SetTheme_Button.currentText() == 'Dark-Theme':
            UserConfigs.__setitem__("Thema", "Dark_Theme")
            Janela.setStyleSheet(Design.Dark_Theme)
        elif self.SetTheme_Button.currentText() == "Light-Theme":
            UserConfigs.__setitem__("Thema", "Light_Theme")
            Janela.setStyleSheet(Design.Light_Theme)
        UserConfigs.close()

class Window_CadasterItems(QWidget):
    def __init__(self):
        super().__init__()

        self.Layout = QGridLayout(self)

        self.NameItem = QLineEdit(self) #Linha para Digitar nome do produto
        self.Layout.addWidget(self.NameItem, 1, 0, 1, 2)
        self.NameItem.setPlaceholderText('Nome Item')
        self.NameItem.returnPressed.connect(lambda : self.CodBarra.setFocus())
        
        self.CodBarra = QLineEdit(self)
        self.Layout.addWidget(self.CodBarra, 2, 0, 1, 2)
        self.CodBarra.setPlaceholderText("Codigo Barra")
        self.CodBarra.returnPressed.connect(lambda : self.DateVencimento.setFocus())

        self.DateVencimento = QLabel('Vencimento:' ,self) #Dia que o produto vence
        self.Layout.addWidget(self.DateVencimento, 3, 0, 1, 1)
        self.DateVencimento.setFixedWidth(100)

        self.Date = QDateEdit()
        datetimetext = QDateTime(date.today().year, date.today().month, date.today().day, 0, 0)
        self.Date.setDateTime(datetimetext)
        self.Layout.addWidget(self.Date, 3, 1, 1, 1)
        
        self.CadasterButton = QPushButton('Cadastrar Produto', self)#Botao que Cadastra o Produto
        self.Layout.addWidget(self.CadasterButton, 4, 0, 1, 2)
        self.CadasterButton.clicked.connect(self.CadButton_Func)

    def CadButton_Func(self):#Funcao efetuada apos clicar botao de cadastro, faz verificacao depois cadastra Item
        Data = str(self.Date.date().toPyDate())
        if self.NameItem.text() != '' and self.NameItem.text() != ' ':
            Data = f'{Data[8:10]}.{Data[5:7]}.{Data[0:4]}'
            SQDB().InsertItem(self.CodBarra.text(), self.NameItem.text().upper(), Data)
            self.CodBarra.setText('')
            self.NameItem.setText("")
            #Atualizando Tabela!
            Janela.WidgetPrincipal.Lista_ItemsTot.ResetTable()
            Janela.WidgetPrincipal.Lista_Vencidos.ResetTable()
            Janela.WidgetPrincipal.Lista_PertoVencimento.ResetTable()
            Janela.WidgetPrincipal.Informacoes.Atualizar()
        else:
            MSG = QMessageBox()
            MSG.setIcon(QMessageBox.Information)
            MSG.setWindowTitle("Problema!")
            MSG.setText("Preencha todos os campos!")
            MSG.exec_()

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
        self.RowCountTot = 0

        for lista in Data: #Cada lista detro de Data
            self.Tabela.insertRow(self.Tabela.rowCount()) #Adiciona uma nova linha
            self.RowCountTot += 1
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
                try:
                    if items.isSelected() == True: #Verifica se o Objeto foi selecionado
                        Key = Item.keys() #Obtem os dados da linha na qual o Usuario selecionou
                        Data = []
                        for Dados in Key: #Extraindo Dados Da Key Item
                            Data.append(Dados)
                        Janela.setCentralWidget(Window_InformationSelected(Data))
                except RuntimeError: pass

class Window_InformationSelected(QWidget):
    def __init__(self, Data):
        super().__init__()

        self.Layout = QGridLayout(self)

        LabelCodigo = QLabel("Codigo: ", self)
        self.Layout.addWidget(LabelCodigo,0,0)
        self.Layout.addWidget(QLabel(str(Data[0]), self), 0, 1)

        LabelBarra = QLabel("Codigo Barra: ", self)
        self.Layout.addWidget(LabelBarra,1,0)
        self.Layout.addWidget(QLabel(str(Data[1]), self), 1, 1)

        LabelNome = QLabel("Nome: ", self)
        self.Layout.addWidget(LabelNome,2,0)
        self.Layout.addWidget(QLabel(str(Data[2]), self), 2, 1)

        LabelVencimento = QLabel("Vencimento: ", self)
        self.Layout.addWidget(LabelVencimento,3,0)
        self.Layout.addWidget(QLabel(str(Data[3]), self), 3, 1)

        voltarButton = QPushButton("Voltar", self)
        voltarButton.clicked.connect(lambda : self.Voltar())
        self.Layout.addWidget(voltarButton, 4, 0,1,2)

        DellItems = QPushButton("Deletar", self)
        self.Layout.addWidget(DellItems, 5, 0, 1, 2)
        DellItems.clicked.connect(lambda : SQDB().DellItem(Data[0]))
        DellItems.clicked.connect(lambda : self.Voltar())

        self.show()

    def Voltar(self):
        Janela.WidgetPrincipal = Widget_Primary()
        Janela.setCentralWidget(Janela.WidgetPrincipal)

if __name__ == '__main__':
    App = QApplication(sys.argv)
    Janela = Primary_Windows()
    sys.exit(App.exec_())
