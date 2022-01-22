import re
import imaplib
from PySide2.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QPushButton, QDialog
from PySide2.QtGui import QPixmap, QImage, QFont

from inbox import Inbox

imap_list = {
    "gmail.com":   ["imap.gmail.com",        993],
    "outlook.com": ["imap-mail.outlook.com", 993],
    "yahoo.com":   ["imap.mail.yahoo.com",   993],
    "zoho.com":    ["imap.zoho.com",         993]
}

class Login(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("NexMail Login")

        self.w = None

        h_box = QHBoxLayout()
        v_box = QVBoxLayout()

        icon = QLabel()
        icon_img = QImage('images/nexmail_main.png')
        icon.setStyleSheet("margin :55px;")
        icon.setPixmap(QPixmap(icon_img.scaledToWidth(250)))
        h_box.addWidget(icon)

        self.username_edit = QLineEdit()
        self.password_edit = QLineEdit()

        self.error_message = QLabel();


        fontsize = 12
        font = "arial"
        self.username_edit.setFont(QFont(font, fontsize))
        self.password_edit.setFont(QFont(font, fontsize))     

        self.username_edit.setPlaceholderText("Email")
        self.username_edit.setStyleSheet("padding: 3px 3px 3px 10px solid black;")
        self.password_edit.setPlaceholderText("Password")
        self.password_edit.setStyleSheet("padding: 3px 3px 3px 10px solid black;")

        self.password_edit.setEchoMode(QLineEdit.Password)

        self.username_edit.setFixedWidth(320)
        self.password_edit.setFixedWidth(320)

        login = QPushButton("L O G I N")
        login.clicked.connect(self.login_button_pressed)

        v_box.addWidget(self.username_edit)
        v_box.addWidget(self.password_edit)
        v_box.addWidget(self.error_message)
        v_box.addWidget(login)
        v_box.setContentsMargins(0, 70, 70, 70)

        h_box.addLayout(v_box)

        self.setLayout(h_box)

    def open_that_window(self):
        if self.w is None:
            self.w = Inbox()
            self.w.show()
            self.close()

    def login_button_pressed(self):
        self.error_message.setText("Loading...")
        username = self.username_edit.text()
        password = self.password_edit.text()

        try:
            #temp_regex = re.search("@.*$", username)
            #service = temp_regex.string[temp_regex.start()+1: temp_regex.end()]
            #imap = imaplib.IMAP4_SSL(imap_list[service][0])
            #imap.login(username, password)
            self.error_message.setText("Login Successful, Loading...")
            print("AUTH Success: ", username)
            self.open_that_window()

        except Exception as e:
            self.password_edit.setText("")
            self.error_message.setText("Login Error, Try Again")
            print("ERROR::", e)
