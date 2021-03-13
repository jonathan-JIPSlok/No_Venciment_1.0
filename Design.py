def Dark_Theme():
    Theme = """QWidget {
        background-color: rgb(80, 80, 80);
    }
    QLineEdit {
        background-color: rgb(200, 200, 200);
        font-size: 13px;
        border: 1px solid rgb(0, 200, 0);
        border-radius: 10px;
        padding: 3px
    }
    QTableWidget {
        border: 1px solid blue;
        border-radius: 20px;
        font: bold;
        font-size: 12px;
    }
    QPushButton {
        background-color: rgb(120, 120, 120);
        border: 1px solid rgb(0, 255, 0);
        border-radius: 5px;
        padding: 4px;
        font: bold;
        font-size: 14px;
    }
    QPushButton:hove:!pressed {
        background-color: rgb(200, 200, 200);
    }
    """
    return Theme

alternativo = """QMainWindow {background-color: rgb(50, 50, 50)}\
		QPushButton {border-radius: 10px; padding: 5px; background-color: rgb(100, 100, 100); border: 1px solid rgb(150, 150, 150)}\
			QPushButton:hover:!pressed {background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgb(40, 40, 40), stop: 1 rgb(100, 100, 100)); border-style: outset} \
			QWidget {font-size: 15px; font: bold; color: rgb(200, 200, 200); background-color: rgb(50, 50, 50)}\
				QLineEdit {background: rgb(70,70,70); border-radius: 10px; padding: 3px}\
					QComboBox {border-radius: 10px; padding: 2px; background: rgb(100, 100, 100); color: rgb(200, 200, 200)}\
						QComboBox:hover:!pressed {background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgb(40, 40, 80), stop: 1 rgb(100, 100, 180)); border-style: outset}
                            QTabBar::tab:Selected {background-color: gray; color: rgb(0, 255, 0)}
                                QTabBar::tab {background-color: rgb(100,100,100)}
                                    QTableWidget::item {background-color: rgb(100,100,100)}
                                        QTableWidget::item:selected {color: rgb(0,255,0)}"""
	