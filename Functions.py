import sqlite3
from pathlib import Path
from os.path import join as path_join

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