import sys
from PySide2.QtWidgets import QApplication

from login import Login

app = QApplication(sys.argv)

window = Login()
window.show()
window.setFixedSize(window.size());

app.exec_()
