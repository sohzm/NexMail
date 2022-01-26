import sys
from PySide6.QtWidgets import QApplication

from login import Login

app = QApplication(sys.argv)

window = Login()
window.show()
window.setFixedSize(window.size());

sys.exit(app.exec())
