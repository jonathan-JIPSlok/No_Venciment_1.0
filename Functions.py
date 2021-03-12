import sqlite3
from pathlib import Path
from os.path import join as path_join
from random import randint
import datetime

class SQDB(): #Funcoes com o banco de dados
    def __init__(self):
        super().__init__()

        #Criando ou abrindo a pasta do banco de dados
        Pasta = Path.home() / path_join("MyAppPastaJP")
        try:
            pastinha = Pasta.mkdir()
        except:
            pass
        self.connection = sqlite3.connect(Pasta / 'AntVencimentApp.db')
        self.cursor = self.connection.cursor()
        
        self.CreateTables()
    
    def CreateTables(self): #Cria a tabela no banco de dados caso ela nao exista
        self.cursor.execute('CREATE TABLE IF NOT EXISTS Items(Codigo interger primary key, Codigo_Barras interger, Nome text, Data_Vencimento text)')
    
    def InsertItem(self, CodBarra, Nome, Data_Vencimento): #Insere um elemento no banco de dados
        self.cursor.execute('INSERT INTO Items(Codigo, Codigo_Barras, Nome, Data_Vencimento) VALUES(?, ?, ?, ?)', (randint(11111, 99999), (int(CodBarra) if CodBarra.isnumeric() else randint(111, 999)), Nome, Data_Vencimento))
        self.connection.commit()
        self.Close()

    def Close(self):
        self.connection.close()

    def DellItem(self, Cod):
        self.cursor.execute("DELETE FROM Items WHERE Codigo = ?", (int(Cod), ))
        self.connection.commit()
        self.Close()

    def Reset(self):
        self.cursor.execute("DELETE FROM Items")
        self.connection.commit()
        self.Close()

    def getItems(self, Type = "Geral"):
        Data = self.cursor.execute("SELECT * FROM Items").fetchall()
        DataAtual = (datetime.date.today().day, datetime.date.today().month, datetime.date.today().year)
        
        if Type == "Geral":
            self.connection.close()
            return Data

        if Type == "Perto":
            DataFinal = [] #Dados a serem retornados
            for Item in Data:
                DataItem = Item[3] # pegando o ano
                NewData = [] 
                Temporaria = ""
                for Caractere in DataItem: #Separando o dia, mes, ano
                    if Caractere.isnumeric():
                        Temporaria += str(Caractere)
                    else:
                        NewData.append(int(Temporaria))
                        Temporaria = ""
                    if len(Temporaria) > 3:
                        NewData.append(int(Temporaria))
                
                if len(NewData) == 3: #Decidindo o que entra na lista conforme a data
                    if NewData[2] == DataAtual[2]: #se for do mesmo ano 
                        if NewData[1] == DataAtual[1] and NewData[0] >= DataAtual[0]: #se for do mesmo mes
                            DataFinal.append(Item)
                        elif NewData[1] -1 == DataAtual[1]: #Se for de outro mes
                            DataFinal.append(Item)
                    elif NewData[2] - 1 == DataAtual[2]: #se for de outro ano
                        if NewData[1] == 1 and DataAtual[1] == 12:
                            DataFinal.append(Item)
            self.connection.close()
            return DataFinal
        
        if Type == 'Vencido':
            DataFinal = [] #Dados a serem retornados
            for Item in Data:
                DataItem = Item[3] # pegando o ano
                NewData = [] 
                Temporaria = ""
                for Caractere in DataItem: #Separando o dia, mes, ano
                    if Caractere.isnumeric():
                        Temporaria += str(Caractere)
                    else:
                        NewData.append(int(Temporaria))
                        Temporaria = ""
                    if len(Temporaria) > 3:
                        NewData.append(int(Temporaria))
                
                if len(NewData) == 3: #Decidindo o que entra na lista conforme a data
                    if NewData[2] == DataAtual[2]: #se for do mesmo ano 
                        if NewData[1] == DataAtual[1] and NewData[0] < DataAtual[0]: #se for do mesmo mes
                            DataFinal.append(Item)
                        elif NewData[1] < DataAtual[1]: #Se for de outro mes
                            DataFinal.append(Item)
                    elif NewData[2] < DataAtual[2]: #se for de outro ano
                        DataFinal.append(Item)
            self.connection.close()
            return DataFinal

if __name__ == '__main__':
    pass