import sqlite3
from pathlib import Path
from os.path import join as path_join
from random import randint

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
    
    def CreateTables(self):
        self.cursor.execute('CREATE TABLE IF NOT EXISTS Items(Codigo interger primary key, Codigo_Barras interger, Nome text, Data_Vencimento text)')
    
    def InsertItem(self, CodBarra, Nome, Data_Vencimento):
        self.cursor.execute('INSERT INTO Item(Codigo, Codigo_Barras, Nome, Data_Vencimento) VALUES(?, ?, ?, ?)', (randint(11111, 99999), int(CodBarra), Nome, Data_Vencimento))
        self.connection.commit()
