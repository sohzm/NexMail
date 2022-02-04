from PySide6.QtWidgets import (
    QMainWindow, QHBoxLayout, QVBoxLayout, 
    QLabel, QWidget, QLineEdit, QScrollArea, 
    QTabWidget, QPushButton
)
from PySide6.QtGui     import QFont
from PySide6.QtCore    import Qt

from inbox_tools    import MListTab, MLoadWorker

import email
import copy

class Inbox(QMainWindow):

    def __init__(self, imp):
        super(Inbox, self).__init__()
        self.imap_inst = imp

        self.setWindowTitle("NexMail")

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
        self.search.setStyleSheet(
            "padding: 3px 3px 3px 10px solid black;"
        )
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

        self.showing = QLabel("")
        self.showing.setFont(QFont(font, fontsize))
        mail_bar.addWidget(self.showing)

        self.status = QLabel("1 - 50")
        self.status.setFont(QFont(font, fontsize))
        mail_bar.addWidget(self.status)

        self.previous = QPushButton("Previous")
        mail_bar.addWidget(self.previous)
        self.previous.mousePressEvent = self.prev_page

        self.next = QPushButton("Next")
        mail_bar.addWidget(self.next)
        self.next.mousePressEvent = self.next_page


        ### MENU BAR

        fontsize = 16

        self.create = QLabel("New Mail")
        self.create.setFont(QFont(font, fontsize))
        menu_bar.addWidget(self.create)
        #self.create.mousePressEvent = self.mail_editor

        self.inbox = QLabel("Inbox")
        self.inbox.setFont(QFont(font, fontsize))
        menu_bar.addWidget(self.inbox)
        self.inbox.setStyleSheet("background-color: #888888;")

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
        self.tab_layout.setTabsClosable(True)
        self.tab_layout.tabCloseRequested.connect(self.close_curr_tab)


        widget = QWidget()
        self.layout = QVBoxLayout(widget)
        self.layout.setAlignment(Qt.AlignTop)
        layout1 = QVBoxLayout()

        scroll_area = QScrollArea()

        scroll_area.setWidget(widget)
        scroll_area.setWidgetResizable(True)

        layout1.addWidget(scroll_area)

        area_box.addWidget(self.tab_layout)

        final_widget = QWidget() 
        final_widget.setLayout(main_window)
        self.setCentralWidget(final_widget)
        self.thread_is_running = False
        self.inbox_page = 0

        try:
            self.on_inbox_clicked()

        except Exception as e:
            print("ERROR::", e)

    def on_inbox_clicked(self, event = 0):
        self.temp_crt = MListTab(self.imap_inst, self.tab_layout)
        self.tab_layout.addTab(self.temp_crt, "Inbox")
        self.tab_layout.setCurrentIndex(self.tab_layout.count()-1)

        self.imap_inst.select("inbox")
        #_, data = self.imap_inst.search(None, "ALL")
        _, data = self.imap_inst.uid("search", None, "ALL")
        #print(data)

        temp_data = email.message_from_bytes(data[0])

        self.temp_list = str(temp_data).split()
        self.temp_list.reverse()

        self.inbox_mail = MLoadWorker(
            self.imap_inst, self.temp_list, 
            self.inbox_page
        )
        self.inbox_mail.iemit_cell.connect(self.temp_crt.create_new_cell)
        self.inbox_mail.istart.connect(self.started_thread)
        self.inbox_mail.ifinish.connect(self.thread_completed)
        self.inbox_mail.start()

    def next_page(self, event):
        if (self.inbox_mail.isRunning()):
            self.inbox_mail.break_var = True
            
        self.inbox_mail.wait()
        self.inbox_page += 1
        self.status.setText(
            str((self.inbox_page*50)+1) 
            + "-" 
            + str((self.inbox_page+1)*50)
        )
        self.temp_crt.clear_mail_list()
        self.inbox_mail = MLoadWorker(
            self.imap_inst, self.temp_list, self.inbox_page
        )
        self.inbox_mail.iemit_cell.connect(self.temp_crt.create_new_cell)
        self.inbox_mail.istart.connect(self.started_thread)
        self.inbox_mail.ifinish.connect(self.thread_completed)
        self.inbox_mail.start()

    def prev_page(self, event):
        if (self.inbox_page > 0): 
            if (self.inbox_mail.isRunning()):
                self.inbox_mail.break_var = True

            self.inbox_mail.wait()
            self.inbox_page -= 1
            self.status.setText(
                str((self.inbox_page*50)+1)
                + "-"
                + str((self.inbox_page+1)*50)
            )
            self.temp_crt.clear_mail_list()
            self.inbox_mail = MLoadWorker(
                self.imap_inst, self.temp_list, self.inbox_page
            )
            self.inbox_mail.iemit_cell.connect(self.temp_crt.create_new_cell)
            self.inbox_mail.istart.connect(self.started_thread)
            self.inbox_mail.ifinish.connect(self.thread_completed)
            self.inbox_mail.start()

    def started_thread(self):
        self.showing.setText("Loading... ")

    def thread_completed(self):
        self.showing.setText("Showing ")

#    def mail_editor(self, event):
#        self.temp_crt = MCreateTab()
#        self.tab_layout.addTab(self.temp_crt, "New Mail")
#        self.tab_layout.setCurrentIndex(self.tab_layout.count()-1)

    def close_curr_tab(self, x):
        if (x != 0):
            """
            has memory management issues, closing tab dosen't free 
            the memory it was holding (will improve later)
            """
            self.tab_layout.removeTab(x)

#    def return_error(self):
#        print("INBOX::error while retrieving", len(self.mail_array))
#
#    def create_mail(self, subject, body, sender, val):
#        if self.mail_array[val] != val:
#            self.layout.removeWidget(self.mail_array[val])
#            self.mail_array[val].deleteLater()
#            self.mail_array[val] = None
#
#        self.mail_array[val] = MListCell(subject, body, sender, val, self.tab_layout)
#        self.mail_array[val].setFixedHeight(60)
#        self.mail_array[val].setStyleSheet("*{padding: 10px 10px 10px 10px;} *:hover {background: #888888;}")
#        self.layout.addWidget(self.mail_array[val])
