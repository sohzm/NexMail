from PySide2.QtWidgets import QMainWindow, QHBoxLayout, QVBoxLayout, QLabel, QWidget, QLineEdit
from PySide2.QtGui import QPixmap, QImage, QPalette, QColor, Qt

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
        tool_layout = QHBoxLayout()

        icon = QLabel()
        icon_img = QImage('images/nexmail_text.png')
        #icon.setStyleSheet("margin :55px;")
        icon.setPixmap(QPixmap(icon_img.scaledToWidth(250)))
        menu_layout.addWidget(icon)
        icon.setContentsMargins(40, 10, 10, 10)
        icon.setFixedHeight(140)

        main_menu = QWidget()

        search_bar = QLineEdit()
        font = search_bar.font()
        font.setPointSize(12) 
        search_bar.setFont(font)      
        search_bar.setPlaceholderText("Search Mail")
        search_bar.setContentsMargins(50, 55, 60, 10)
        search_bar.setFixedHeight(100)
        search_bar.setStyleSheet("padding: 0px 0px 0px 10px solid black;")
        menu_layout.addWidget(search_bar)

        label_inbox = QLabel("Inbox")
        label_inbox.setStyleSheet("margin: 30px 0px 0px 50px solid black;")
        menu_layout.addWidget(label_inbox)

        label_trash = QLabel("Trash")
        label_trash.setStyleSheet("margin: 30px 0px 0px 50px solid black;")
        menu_layout.addWidget(label_trash)
        
        font = label_trash.font()
        font.setPointSize(14) 
        label_trash.setFont(font)      
        label_inbox.setFont(font)      

        lhdd = QLabel("JJJJJJJJJJJJJJJJJJJJJj")
        lhdd.setFixedHeight(100)
        tool_layout.addWidget(lhdd)

        menu_layout.addWidget(main_menu)

        mail_layout.addLayout(tool_layout)
        mail_layout.addWidget(Color('red'))
        mail_layout.addWidget(Color('purple'))

        menu_layout.setAlignment(Qt.AlignTop)

        main_window.addLayout(menu_layout, 2)
        main_window.addLayout(mail_layout, 5)

        widget = QWidget()
        widget.setLayout(main_window)
        self.setCentralWidget(widget)
