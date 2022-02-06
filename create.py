from PySide6.QtWidgets import (
    QHBoxLayout, QVBoxLayout, QLabel, QWidget,
    QPlainTextEdit, QPushButton, QLineEdit
)
from PySide6.QtGui     import QFont
from PySide6.QtCore    import QThread, Signal

import smtplib

class MCreateTab(QWidget):
    def __init__(self, usr, pss) -> None:
        super().__init__()

        self.usr = usr
        self.pss = pss

        self.title = "Create New Mail"

        self.layout = QVBoxLayout()
        self.top_bar = QVBoxLayout()
        self.bottom_bar = QHBoxLayout()

        ### TO
        self.success_msg = QLabel("Mail Sent Successfully")
        self.success_msg.setFont(QFont("arial", 14))
        self.success_msg.hide()
        self.top_bar.addWidget(self.success_msg)

        self.to_layout = QHBoxLayout()
        self.to_label = QLabel("To")
        self.to_layout.addWidget(self.to_label)
        self.to_edit = QLineEdit()
        self.to_label.setFont(QFont("arial", 12))
        self.to_edit.setFont(QFont("arial", 12))
        self.to_layout.addWidget(self.to_edit)
        self.to_label.setFixedWidth(80)

        self.subject_layout = QHBoxLayout()
        self.subject_label = QLabel("Subject")
        self.subject_layout.addWidget(self.subject_label)
        self.subject_edit = QLineEdit()
        self.subject_edit.setFont(QFont("arial", 12))
        self.subject_label.setFont(QFont("arial", 12))
        self.subject_layout.addWidget(self.subject_edit)
        self.subject_label.setFixedWidth(80)

        self.top_bar.addLayout(self.to_layout)
        self.top_bar.addLayout(self.subject_layout)

        self.input_field = QPlainTextEdit()
        self.input_field.setPlaceholderText("Type your email here.")
        self.input_field.setFont(QFont("arial", 12))

        self.send_button = QPushButton("SEND MAIL")
        self.bottom_bar.addWidget(self.send_button)
        self.send_button.clicked.connect(self.send_mail)

        self.layout.addLayout(self.top_bar)
        self.layout.addWidget(self.input_field)
        self.layout.addLayout(self.bottom_bar)
        self.setLayout(self.layout)
        self.setStyleSheet(
            """
            """
        )

    def send_mail(self):
        self.send_button.setEnabled(False)
        self.to = self.to_edit.text()
        self.sub = self.subject_edit.text()
        self.body = self.input_field.toPlainText()
        self.send_thread = MSendWorker(self.usr, self.pss, self.to, self.sub, self.body)
        self.send_thread.mail_sent.connect(self.mail_sent_bro)
        self.send_thread.start()

    def mail_sent_bro(self):
        self.success_msg.show()
        print("Sent successfully")

class MSendWorker(QThread):

    mail_sent = Signal()

    def __init__(self, usr, pss, to, sub, body) -> None:
        super().__init__()
        self.usr = usr
        self.pss = pss
        self.to = [to]
        self.sub = sub
        self.body = body

    def run(self):
        try:
            """
            Add more smpt servers support
            """
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.usr, self.pss)
            message = """\
From: %s
To: %s
Subject: %s


%s
            """ % (self.usr, ", ".join(self.to), self.sub, self.body)


            server.sendmail(self.usr, self.to, message)
            self.mail_sent.emit()
            server.quit()
            self.exit(0)
        except Exception as e:
            print("AUTH::ERROR", e)
            self.exit(0)
