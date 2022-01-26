import re
import time
import imaplib
from PySide6.QtWidgets import (
        QHBoxLayout, 
        QVBoxLayout, 
        QLabel, 
        QLineEdit, 
        QPushButton, 
        QDialog
    )
from PySide6.QtGui import (
        QPixmap, 
        QImage, 
        QFont
    )

from PySide6.QtCore import QObject, QThread, Signal
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
        self.ret = 8
        self.load_layout()


    def load_layout(self):
        self.setWindowTitle("NexMail Login")

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

        #rt: add view/hide password option
        self.password_edit.setEchoMode(QLineEdit.Password)

        self.username_edit.setFixedWidth(320)
        self.password_edit.setFixedWidth(320)

        self.login = QPushButton("L O G I N")
        self.login.clicked.connect(self.login_button_pressed)

        v_box.addWidget(self.username_edit)
        v_box.addWidget(self.password_edit)
        v_box.addWidget(self.error_message)
        v_box.addWidget(self.login)
        v_box.setContentsMargins(0, 70, 70, 70)

        h_box.addLayout(v_box)
        self.setLayout(h_box)


    def login_button_pressed(self):
        print("after login button pressed")
        self.error_message.setText("Loading...")
        self.username = self.username_edit.text()
        self.password = self.password_edit.text()

        try:
            temp_regex = re.search("@.*$", self.username)
            self.service = temp_regex.string[temp_regex.start()+1: temp_regex.end()]
            self.sr = imap_list[self.service][0]
            self.start_new_thread()

        except Exception as e:
            self.password_edit.setText("")
            self.error_message.setText("Login Error, Try Again")
            print("ERROR::", e)

    def start_new_thread(self):
        self.thread = Worker(self.username, self.password, self.sr)
        self.thread.task.connect(self.open_that_window)
        self.thread.error.connect(self.return_error)
        self.login.setEnabled(False)
        self.thread.start()

    def open_that_window(self, val):
        print("AUTH::open")
        inbox = Inbox(self.username, self.password, self.sr)
        inbox.show()
        self.close()

    def return_error(self, val):
        print("AUTH::errr")
        self.login.setEnabled(True)
        self.error_message.setText("Login Error, Try Again")
        self.password_edit.setText("")

    #rt: add loading animation

    def update_message(self):
        self.permission_to_run = True
        i = 0
        while(self.permission_to_run):
            self.error_message.setText("Loading" + ("."*(i%3)))
            time.sleep(1)
            i += 1


class Worker(QThread):

    error = Signal(int)
    task = Signal(int)

    def __init__(self, usr, pss, imp) -> None:
        super().__init__()
        self.usr = usr
        self.pss = pss
        self.imp = imp

    def run(self):
        try:
            imap = imaplib.IMAP4_SSL(self.imp)
            imap.login(self.usr, self.pss)
            print("AUTH::SUCCESS")
            self.task.emit(7)
        except:
            print("AUTH::ERROR")
            self.error.emit(1)
