from PySide2.QtWidgets import QMainWindow, QHBoxLayout, QVBoxLayout, QLabel, QWidget, QLineEdit, QScrollArea
from PySide2.QtGui import QPixmap, QImage, QPalette, QColor, Qt, QFont, QFontDatabase

class Color(QWidget):
    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)

class Inbox(QMainWindow):
    print("ENtered Inbox")

    def __init__(self):
        super(Inbox, self).__init__()

        self.setWindowTitle("Inbox")

        # Layouts

        main_window = QVBoxLayout()

        main_bar = QHBoxLayout()
        icon_box = QHBoxLayout()
        tool_bar = QVBoxLayout()
        user_bar = QHBoxLayout()
        mail_bar = QHBoxLayout()

        area_box = QHBoxLayout()
        menu_bar = QVBoxLayout()
        #mail_box = QWidget()
        
        tool_bar.addLayout(user_bar)
        tool_bar.addLayout(mail_bar)

        main_bar.addLayout(icon_box)
        main_bar.addLayout(tool_bar)

        area_box.addLayout(menu_bar)
        #area_box.addLayout(mail_box)

        main_window.addLayout(main_bar)
        main_window.addLayout(area_box, 1)

        ### ICON BOX

        self.addFont()
        icon = QLabel("NexMail")
        icon.setFont(QFont("Iosevka", 32))
        icon_box.addWidget(icon)

        ### USER BAR 

        fontsize = 12
        font = "arial"

        self.search = QLineEdit()
        self.search.setPlaceholderText("Search Mail")
        self.search.setStyleSheet("padding: 3px 3px 3px 10px solid black;")
        self.search.setFont(QFont(font, fontsize))
        self.search.setFixedWidth(480)
        user_bar.addWidget(self.search)

        self.space1 = QLabel()
        user_bar.addWidget(self.space1, 1)

        self.help = QLabel("Help")
        self.help.setFont(QFont(font, fontsize))
        user_bar.addWidget(self.help)

        self.settings = QLabel("Settings")
        self.settings.setFont(QFont(font, fontsize))
        user_bar.addWidget(self.settings)

        self.account = QLabel("Account")
        self.account.setFont(QFont(font, fontsize))
        user_bar.addWidget(self.account)
        

        ### MAIL BAR

        self.reload = QLabel("Reload")
        self.reload.setFont(QFont(font, fontsize))
        mail_bar.addWidget(self.reload)

        self.space2 = QLabel()
        mail_bar.addWidget(self.space2, 1)

        self.status = QLabel("Status")
        self.status.setFont(QFont(font, fontsize))
        mail_bar.addWidget(self.status)


        ### MENU BAR

        fontsize = 16

        self.inbox = QLabel("Inbox")
        self.inbox.setFont(QFont(font, fontsize))
        menu_bar.addWidget(self.inbox)

        self.important = QLabel("Important")
        self.important.setFont(QFont(font, fontsize))
        menu_bar.addWidget(self.important)

        self.sent = QLabel("Sent")
        self.sent.setFont(QFont(font, fontsize))
        menu_bar.addWidget(self.sent)

        self.draft = QLabel("Draft")
        self.draft.setFont(QFont(font, fontsize))
        menu_bar.addWidget(self.draft)

        self.chats = QLabel("Chats")
        self.chats.setFont(QFont(font, fontsize))
        menu_bar.addWidget(self.chats)

        ### MAIL BOX

        widget = QWidget()
        layout = QVBoxLayout(widget)

        scroll_area = QScrollArea()
        for index in range(1000):
            layout.addWidget(QLabel('Label %02d' % index))

        scroll_area.setWidget(widget)
        scroll_area.setWidgetResizable(True)
        area_box.addWidget(scroll_area)


        ### FINAL

        final_widget = QWidget() 
        final_widget.setLayout(main_window)
        self.setCentralWidget(final_widget)

    def addFont(self):
        font_db = QFontDatabase()
        font_id = font_db.addApplicationFont("fonts/iosevka-regular.ttf")
