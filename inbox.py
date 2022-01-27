from email.header      import decode_header, make_header
from PySide6.QtWidgets import QMainWindow, QHBoxLayout, QVBoxLayout, QLabel, QWidget, QLineEdit, QScrollArea, QTabWidget
from PySide6.QtGui     import QFont
from PySide6.QtCore    import QThread, Signal

#from PySide2.QtWebEngineWidgets import QWebEngineView
import email

class Inbox(QMainWindow):

    def __init__(self, imp):
        super(Inbox, self).__init__()
        self.imap_inst = imp

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

        self.previous = QLabel("<")
        self.previous.setFont(QFont(font, fontsize))
        mail_bar.addWidget(self.previous)

        self.next = QLabel(">")
        self.next.setFont(QFont(font, fontsize))
        mail_bar.addWidget(self.next)


        ### MENU BAR

        fontsize = 16

        self.inbox = QLabel("Inbox")
        self.inbox.setFont(QFont(font, fontsize))
        menu_bar.addWidget(self.inbox)
        self.inbox.setStyleSheet("background-color: yellow;")

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

        self.tab_layout = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()

        self.tab_layout.addTab(self.tab1,"Inbox")
        self.tab_layout.addTab(self.tab2,"Browser")

        widget = QWidget()
        self.layout = QVBoxLayout(widget)
        layout1 = QVBoxLayout()
        layout2 = QVBoxLayout()

        labe = QLabel("brower, WOkring>")

        scroll_area = QScrollArea()

        scroll_area.setWidget(widget)
        scroll_area.setWidgetResizable(True)

        #view = QWebEngineView()
        #view.setUrl(QUrl("https://www.google.com"))

        layout1.addWidget(scroll_area)
        layout2.addWidget(labe)
        #layout2.addWidget(view)

        self.tab1.setLayout(layout1)
        self.tab2.setLayout(layout2)
        area_box.addWidget(self.tab_layout)


        final_widget = QWidget() 
        final_widget.setLayout(main_window)
        self.setCentralWidget(final_widget)

        try:
            self.temp_var = self.mail_ret_thread()

        except Exception as e:
            print("ERROR::", e)


    def mail_ret_thread(self):
        self.ret_mail = inboxWorker(self.imap_inst)
        self.ret_mail.itask.connect(self.ret_successful)
        self.ret_mail.ierror.connect(self.return_error)
        self.ret_mail.iloaded_emails.connect(self.number_of_emails_loaded)
        self.ret_mail.iemail_subject.connect(self.add_label)
        self.ret_mail.start()

    def number_of_emails_loaded(self, val):
        print("INBOX::", val, "emails loaded")

    def ret_successful(self, val):
        print("INBOX::emails successfully ret")

    def return_error(self, val):
        print("INBOX::error while retrieving")

    def add_label(self, subject):
        print("SUBJECT::", subject)
        self.layout.addWidget(QLabel(subject))

        ### FINAL

class inboxWorker(QThread):

    ierror = Signal(int)
    itask = Signal(int)
    iloaded_emails = Signal(int)
    iemail_subject = Signal(str)

    def __init__(self, imap, num = 10) -> None:
        super().__init__()
        self.imap = imap
        self.num = num

    def run(self):
        try:
            _, self.temp_msg = self.imap.select("INBOX")
            self.total_messages = int(self.temp_msg[0])

            for index in range(self.total_messages, self.total_messages - self.num, -1):
                _, idata = self.imap.fetch(str(index), "(RFC822)")
                _, b = idata[0]
                ac_email = email.message_from_bytes(b)
                subject_str = str(ac_email["subject"])
                subject_str = str(make_header(decode_header(subject_str)))

                self.iemail_subject.emit(subject_str)
                self.iloaded_emails.emit(self.total_messages - index)
            self.itask.emit(7)

        except Exception as e:
            print("AUTH::ERROR", e)
            self.ierror.emit(1)

