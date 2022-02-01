from PySide6.QtWidgets import (
    QHBoxLayout, QVBoxLayout, QPushButton,
    QLabel, QWidget, QScrollArea
)
from PySide6.QtGui     import QFont
from PySide6.QtCore    import Qt, QThread, Signal
from PySide6.QtWebEngineWidgets import QWebEngineView

from email.header      import decode_header, make_header 

import email


class MListCell(QWidget):

    def __init__(
            self, cell_text, cell_number, cell_mail_id, imap_inst, tab_layout
        ) -> None:
        super().__init__()

        self.cell_text = cell_text
        self.cell_number = cell_number
        self.cell_mail_id = cell_mail_id
        self.imap_inst = imap_inst
        self.tab_layout = tab_layout

        self.list_item_label = QLabel(self.cell_text)
        self.list_item_label.setFont(QFont("arial", 14))
        self.list_item_label.setStyleSheet("*{padding: 10px 10px 10px 10px;} *:hover {background: #888888;}")

        self.list_item_layout = QHBoxLayout()
        self.list_item_layout.addWidget(self.list_item_label)

        self.list_item = QVBoxLayout()
        self.setLayout(self.list_item_layout)
    
    def mousePressEvent(self, event):

        """ Creates a new tab for reading the mail and sets current
            tab to the new one.
        """
        if len(self.cell_text) > 30:
            self.cropped = self.cell_text[0:30]
        else:
            self.cropped = self.cell_text
        temp_tab = WebviewTab(self.cell_text, self.imap_inst, self.cell_mail_id) 
        self.tab_layout.addTab(temp_tab, self.cropped)
        self.tab_layout.setCurrentIndex(self.tab_layout.count()-1)


class MListTab(QWidget):

    def __init__(self, imap_inst, tab_layout) -> None:
        super().__init__()
        self.mail_list = []
        self.imap_inst = imap_inst
        self.tab_layout = tab_layout

        wid = QWidget()
        self.layout = QVBoxLayout(wid)
        self.layout.setAlignment(Qt.AlignTop)

        self.layout1 = QVBoxLayout()

        self.scroll = QScrollArea()
        self.scroll.setWidget(wid)

        self.scroll.setWidgetResizable(True)


        self.layout1.addWidget(self.scroll)
        self.setLayout(self.layout1)

        for i in range(50):
            self.mail_list.append(MListCell("", i, -1, self.imap_inst, self.tab_layout))
            self.layout.addWidget(self.mail_list[i])

    def clear_mail_list(self):
        for i in range(50):
            self.mail_list[i].cell_text = ""
            self.mail_list[i].cell_mail_id = -1
            self.mail_list[i].list_item_label.setText("")
            
    def create_new_cell(self, subject_str, temp_num, index):
        self.mail_list[temp_num].list_item_label.setText(subject_str)
        self.mail_list[temp_num].cell_text = subject_str
        self.mail_list[temp_num].cell_mail_id = index
        print(index, "LLLLL")

    def fill_mail_list(self):
        pass


class WebviewTab(QWidget):
    def __init__(self, subject, imap_inst, mail_id) -> None:
        super().__init__()
        self.subject = subject
        self.imap_inst = imap_inst
        self.mail_id = mail_id

        self.layout = QVBoxLayout()
        self.top_bar = QHBoxLayout()
        
        self.title_label = QLabel(self.subject)
        self.title_label.setFont(QFont("arial", 14))
        self.top_bar.addWidget(self.title_label)

        self.layout.addLayout(self.top_bar)

        self.view = QWebEngineView()
        self.layout.addWidget(self.view, 1)

        self.imap_inst.select("inbox")
        print("COMID", self.mail_id)
        _, idata = self.imap_inst.fetch(str(self.mail_id), "(RFC822)")
        _, b = idata[0] 
        ac_email = email.message_from_bytes(b)
        body = ""
        if ac_email.is_multipart():
            for part in ac_email.walk():
                ctype = part.get_content_type()
                cdispo = str(part.get('Content-Disposition'))

                if ctype == 'text/plain' and 'attachment' not in cdispo:
                    body = part.get_payload(decode=True)  # decode
                if ctype == 'text/html':
                    body = part.get_payload(decode=True)  # decode
        else:
            body =ac_email.get_payload(decode=True)

        self.body_str = str(body)
        self.body_str = str(make_header(decode_header(self.body_str)))
        self.body_str = self.body_str.replace("\\n", "")
        self.body_str = self.body_str.replace("\\r", "")

        self.view.setHtml(self.body_str)

        self.setLayout(self.layout)

    def del_func(self):
        del self.layout


class MLoadWorker(QThread):

    ierror = Signal()
    istart = Signal()
    ifinish = Signal()
    iemit_cell = Signal(str, int, str)

    def __init__(self, imap_inst, mail_list, page) -> None:
        super().__init__()
        self.imap = imap_inst
        self.page = page
        self.mail_list = mail_list
        self.break_var = False

    def run(self):
        self.istart.emit()
        try:
            temp_num = 0
            print(self.mail_list)
            for index in (
                        self.mail_list[
                            (self.page*50): ((self.page+1)*50)
                        ]
                    ):
                if (self.break_var): 
                    break
                print(index)
                _, idata = self.imap.fetch(str(index), "(RFC822)")
                _, b = idata[0]
                ac_email = email.message_from_bytes(b)
                subject_str = str(ac_email["subject"])
                subject_str = str(make_header(decode_header(subject_str)))
                self.iemit_cell.emit(subject_str, temp_num, index)
                print("COUT::", index)
                temp_num += 1
            self.ifinish.emit()
            self.exit(0)

        except Exception as e:
            print("AUTH::ERROR", e)
            self.ierror.emit()
            self.exit(0)
