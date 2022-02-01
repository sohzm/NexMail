from PySide6.QtWidgets import (
    QHBoxLayout, QVBoxLayout, QLabel, QWidget,
    QPlainTextEdit, QPushButton, QLineEdit
)
from PySide6.QtGui     import QFont

class MCreateTab(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.title = "Create New Mail"

        self.layout = QVBoxLayout()
        self.top_bar = QVBoxLayout()
        self.bottom_bar = QHBoxLayout()
        
#        self.title_label = QLabel(self.title)
#        self.title_label.setFont(QFont("arial", 12))

        ### TO
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

        #self.top_bar.addWidget(self.title_label)
        self.top_bar.addLayout(self.to_layout)
        self.top_bar.addLayout(self.subject_layout)

        self.input_field = QPlainTextEdit()
        self.input_field.setPlaceholderText("Type your email here.")
        self.input_field.setFont(QFont("arial", 12))

        self.send_button = QPushButton("SEND MAIL")
        self.bottom_bar.addWidget(self.send_button)

        self.layout.addLayout(self.top_bar)
        self.layout.addWidget(self.input_field)
        self.layout.addLayout(self.bottom_bar)
        self.setLayout(self.layout)
