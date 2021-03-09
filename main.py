from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLabel
import sqlite3
import sys
from Design import *
from Functions import *

class Primary_Windows(QMainWindow): # Janela Princial
    def __init__(self):
        super().__init__()
        
        
        self.show()

if __name__ == '__main__':
    App = QApplication(sys.argv)
    Janela = Primary_Windows()
    sys.exit(App.exec_())
