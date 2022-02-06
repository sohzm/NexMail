import sys

from PySide6.QtWidgets import QApplication

from login import Login

app = QApplication(sys.argv)

theme = "dark"

if theme == "dark":
    with open('styles/material-dark.qss', 'r') as f:
        style = f.read()
        app.setStyleSheet(style)

window = Login(theme)
window.show()
window.setFixedSize(window.size());

sys.exit(app.exec())
