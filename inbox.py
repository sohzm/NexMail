from PySide6.QtWidgets import (
    QMainWindow, QHBoxLayout, QVBoxLayout, 
    QLabel, QWidget, QLineEdit, QScrollArea, 
    QTabWidget, QPushButton
)
from PySide6.QtGui     import QFont, QPixmap
from PySide6.QtCore    import Qt

from inbox_tools    import MListTab, MLoadWorker
from create         import MCreateTab

import email

class Inbox(QMainWindow):

    def __init__(self, imp, usr, pss):
        super(Inbox, self).__init__()
        self.imap_inst = imp 
        self.username = usr
        self.password = pss

        self.setWindowTitle("NexMail")

        """
        LAYOUTS
        """

        main_window = QVBoxLayout()

        main_bar = QHBoxLayout()
        icon_box = QHBoxLayout()
        tool_bar = QVBoxLayout()
        user_bar = QHBoxLayout()
        mail_bar = QHBoxLayout()

        area_box = QHBoxLayout()
        menu_bar = QVBoxLayout()

        tool_bar.addLayout(user_bar)
        tool_bar.addLayout(mail_bar)

        main_bar.addLayout(icon_box)
        main_bar.addLayout(tool_bar)

        area_box.addLayout(menu_bar)

        main_window.addLayout(main_bar)
        main_window.addLayout(area_box, 1)


        """
        ICON BOX
        """

        icon = QLabel("NexMail")
        icon.setFont(QFont("Iosevka", 22))
        icon.setFixedWidth(170)
        icon.setStyleSheet("padding: 18px solid black;")
        icon_box.addWidget(icon)


        """
        USER BAR
        """

        fontsize = 12
        font = "arial"

        # search bar
        self.search = QLineEdit()
        self.search.setPlaceholderText("Search Mail")
        self.search.setStyleSheet(
            "*{padding: 3px 3px 3px 10px solid black;}"
        )
        self.search.setFont(QFont(font, fontsize))
        self.search.setFixedWidth(480)
        user_bar.addWidget(self.search)

        # spacer
        self.space1 = QLabel()
        user_bar.addWidget(self.space1, 1)

        # help
        self.help = QLabel("Help")
        self.help.setFont(QFont(font, fontsize))
        user_bar.addWidget(self.help)
        self.help.setPixmap(QPixmap('icons/help-circle.png'))
        self.help.setStyleSheet("padding: 5px 5px 5px 5px solid black;")


        # settings
        self.settings = QLabel("Settings")
        self.settings.setFont(QFont(font, fontsize))
        user_bar.addWidget(self.settings)
        self.settings.setPixmap(QPixmap('icons/cog.png'))
        self.settings.setStyleSheet("padding: 5px 5px 5px 5px solid black;")

        # account
        self.account = QLabel("Account")
        self.account.setFont(QFont(font, fontsize))
        user_bar.addWidget(self.account)
        self.account.setPixmap(QPixmap('icons/account.png'))
        self.account.setStyleSheet( "padding: 5px 5px 5px 5px solid black;")
        

        """
        MAIL BAR
        """

        # reload 
        self.reload_layout = QHBoxLayout()

        self.reload_icon = QLabel("Reload")
        
        self.reload_icon.setPixmap(QPixmap('icons/reload.png'))
        #self.reload = QLabel("Reload")
        #self.reload.setFont(QFont(font, fontsize))
        self.reload_layout.addWidget(self.reload_icon)
        #self.reload_layout.addWidget(self.reload)
        mail_bar.addLayout(self.reload_layout)

        # spacer
        self.space2 = QLabel()
        mail_bar.addWidget(self.space2, 1)

        # showing
        self.showing = QLabel("")
        self.showing.setFont(QFont(font, fontsize))
        mail_bar.addWidget(self.showing)

        # status
        self.status = QLabel("1 - 50")
        self.status.setFont(QFont(font, fontsize))
        mail_bar.addWidget(self.status)

        # previous
        self.previous = QPushButton("Previous")
        mail_bar.addWidget(self.previous)
        self.previous.mousePressEvent = self.prev_page
        self.previous.setStyleSheet( "padding: 5px 10px;")

        # next
        self.next = QPushButton("Next")
        mail_bar.addWidget(self.next)
        self.next.mousePressEvent = self.next_page
        self.next.setStyleSheet( "padding: 5px 10px;")


        """
        MENU BAR
        """

        fontsize = 13
        height = 50


        # create mail
        self.create = QLabel("New Mail")
        self.create.setFont(QFont(font, fontsize))
        self.create.setFixedHeight(height)
        self.create.mousePressEvent = self.mail_editor
        self.create_lyt = QHBoxLayout()
        self.create_icon = QLabel("Reload")
        self.create_icon.setStyleSheet( "padding: 10px 10px 10px 20px;")
        self.create_icon.setPixmap(QPixmap('icons/pencil-plus.png'))
        self.create_lyt.addWidget(self.create_icon)
        self.create_lyt.addWidget(self.create)
        self.create_lyt.setAlignment(Qt.AlignLeft)
        menu_bar.addLayout(self.create_lyt)

        # inbox
        self.inbox = QLabel("Inbox")
        self.inbox.setFont(QFont(font, fontsize))
        self.inbox.setFixedHeight(height)
        self.inbox_lyt = QHBoxLayout()
        self.inbox_icon = QLabel("Reload")
        self.inbox_icon.setStyleSheet( "padding: 10px 10px 10px 20px;")
        self.inbox_icon.setPixmap(QPixmap('icons/inbox-outline.png'))
        self.inbox_lyt.addWidget(self.inbox_icon)
        self.inbox_lyt.addWidget(self.inbox)
        self.inbox_lyt.setAlignment(Qt.AlignLeft)
        menu_bar.addLayout(self.inbox_lyt)

        # important mails
        self.important = QLabel("Important")
        self.important.setFont(QFont(font, fontsize))
        self.important.setFixedHeight(height)
        self.important_lyt = QHBoxLayout()
        self.important_icon = QLabel("Reload")
        self.important_icon.setStyleSheet( "padding: 10px 10px 10px 20px;")
        self.important_icon.setPixmap(QPixmap('icons/star-outline.png'))
        self.important_lyt.addWidget(self.important_icon)
        self.important_lyt.addWidget(self.important)
        self.important_lyt.setAlignment(Qt.AlignLeft)
        menu_bar.addLayout(self.important_lyt)

        # sent mails
        self.sent = QLabel("Sent")
        self.sent.setFont(QFont(font, fontsize))
        self.sent.setFixedHeight(height)
        self.sent_lyt = QHBoxLayout()
        self.sent_icon = QLabel("Reload")
        self.sent_icon.setStyleSheet( "padding: 10px 10px 10px 20px;")
        self.sent_icon.setPixmap(QPixmap('icons/email-fast-outline.png'))
        self.sent_lyt.addWidget(self.sent_icon)
        self.sent_lyt.addWidget(self.sent)
        self.sent_lyt.setAlignment(Qt.AlignLeft)
        menu_bar.addLayout(self.sent_lyt)

        # drafts
        self.draft = QLabel("Draft")
        self.draft.setFont(QFont(font, fontsize))
        self.draft.setFixedHeight(height)
        self.draft_lyt = QHBoxLayout()
        self.draft_icon = QLabel("Reload")
        self.draft_icon.setStyleSheet( "padding: 10px 10px 10px 20px;")
        self.draft_icon.setPixmap(QPixmap('icons/book-edit-outline.png'))
        self.draft_lyt.addWidget(self.draft_icon)
        self.draft_lyt.addWidget(self.draft)
        self.draft_lyt.setAlignment(Qt.AlignLeft)
        menu_bar.addLayout(self.draft_lyt)

        # chats
        self.chats = QLabel("Chats")
        self.chats.setFont(QFont(font, fontsize))
        self.chats.setFixedHeight(height)
        self.chats_lyt = QHBoxLayout()
        self.chats_icon = QLabel("Reload")
        self.chats_icon.setStyleSheet( "padding: 10px 10px 10px 20px;")
        self.chats_icon.setPixmap(QPixmap('icons/message-outline.png'))
        self.chats_lyt.addWidget(self.chats_icon)
        self.chats_lyt.addWidget(self.chats)
        self.chats_lyt.setAlignment(Qt.AlignLeft)
        menu_bar.addLayout(self.chats_lyt)

        self.space3 = QLabel()
        self.space3.setFixedWidth(170)
        menu_bar.addWidget(self.space3, 1)

        """
        MAIL BOX
        """

        # tab layout
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
        _, data = self.imap_inst.uid("search", None, "ALL")

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

    def mail_editor(self, event):
        self.mail_create = MCreateTab(self.username, self.password)
        self.tab_layout.addTab(self.mail_create, "New Mail")
        self.tab_layout.setCurrentIndex(self.tab_layout.count()-1)

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
