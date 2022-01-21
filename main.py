import sys
from PySide2.QtWidgets import QMainWindow, QHBoxLayout, QVBoxLayout, QLabel, QWidget, QLineEdit, QPushButton, QApplication
from PySide2.QtGui import QPixmap, QImage, QPalette, QColor, Qt

from login import Login

class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)

class Inbox(QMainWindow):

    def __init__(self):
        super(Inbox, self).__init__()

        self.setWindowTitle("Inbox")

        main_window = QHBoxLayout()
        menu_layout = QVBoxLayout()
        mail_layout = QVBoxLayout()

        icon = QLabel()
        icon_img = QImage('nexmail.png')
        #icon.setStyleSheet("margin :55px;")
        icon.setPixmap(QPixmap(icon_img.scaledToWidth(150)))
        menu_layout.addWidget(icon)
        icon.setContentsMargins(40, 10, 10, 10)
        icon.setFixedHeight(140)

        main_menu = QWidget()

        search_bar = QLineEdit()
        font = search_bar.font()
        font.setPointSize(12) 
        search_bar.setFont(font)      
        search_bar.setPlaceholderText("Search Mail")
        search_bar.setContentsMargins(50, 10, 60, 10)
        search_bar.setFixedHeight(55)
        search_bar.setStyleSheet("padding: 0px 0px 0px 10px solid black;")
        menu_layout.addWidget(search_bar)

        menu_layout.addWidget(main_menu, 1)

        mail_layout.addWidget(Color('red'))
        mail_layout.addWidget(Color('purple'))

        menu_layout.setAlignment(Qt.AlignTop)

        main_window.addLayout(menu_layout, 2)
        main_window.addLayout(mail_layout, 5)

        widget = QWidget()
        widget.setLayout(main_window)
        self.setCentralWidget(widget)

app = QApplication(sys.argv)

window = Login()
window.show()
window.setFixedSize(window.size());

app.exec_()
