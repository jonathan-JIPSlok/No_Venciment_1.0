Dakt_Theme = """QMainWindow {
    background-color: rgb(50, 50, 50)
    }
    QWidget {
        font-size: 15px;
        font: bold;
        color: rgb(100, 200, 200);
        background-color: rgb(50, 50, 50)
    }
	QPushButton {
        border-radius: 10px;
        padding: 5px;
        background-color: rgb(80, 80, 80);
        border: 1px solid rgb(150, 150, 150)
    }
	QPushButton:hover:!pressed {
        background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgb(40, 40, 40), stop: 1 rgb(100, 100, 100));
        border-style: outset
    }
	QLineEdit {
        background: rgb(70,70,70);
        border-radius: 10px;
        padding: 3px
    }
	QComboBox {
        border-radius: 10px;
        padding: 2px;
        background: rgb(100, 100, 100);
        color: rgb(200, 200, 200)
    }
	QComboBox:hover:!pressed {
        background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgb(40, 40, 80), stop: 1 rgb(100, 100, 180));
        border-style: outset
    }
    QTabBar::tab:Selected {
        background-color: gray;
        color: rgb(0, 255, 0)
    }
    QTabBar::tab {
        background-color: rgb(100,100,100)
    }
    QTableWidget::item {
        background-color: rgb(100,100,100)
    }
    QTableWidget::item:selected {
        color: rgb(0,255,0)
    }"""

Light_Theme = """QMainWindow {
    background-color: rgb(250, 250, 250)
    }
    QWidget {
        font-size: 15px;
        font: bold;
        color: rgb(0, 0, 0);
        background-color: rgb(250, 250, 250)
    }
	QPushButton {
        border-radius: 10px;
        padding: 5px;
        background-color: rgb(200, 200, 200);
        border: 1px solid rgb(150, 150, 150)
    }
	QPushButton:hover:!pressed {
        background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgb(100, 100, 100), stop: 1 rgb(255, 255, 255));
        border-style: outset
    }
	QLineEdit {
        background: rgb(200,200,200);
        border-radius: 10px;
        padding: 3px
    }
    QLineEdit::hover:!focus {
        border: 2px solid blue;
    }
	QComboBox {
        border-radius: 10px;
        padding: 2px;
        background: rgb(200, 200, 200);
        color: rgb(0, 0, 0)
    }
	QComboBox:hover:!pressed {
        background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgb(100, 100, 100), stop: 1 rgb(255, 255, 255));
        border-style: outset
    }
    QTabBar::tab:Selected {
        background-color: rgb(150,150,150);
        color: rgb(0, 255, 0)
    }
    QTabBar::tab {
        background-color: rgb(180,180,180)
    }
    QTableWidget::item {
        background-color: rgb(200,200,200)
    }
    QTableWidget::item:selected {
        color: rgb(0,0,255)
    }"""