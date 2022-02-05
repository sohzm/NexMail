from PySide6.QtWidgets import (
    QHBoxLayout, QVBoxLayout,  QScrollBar,
    QLabel, QWidget, QScrollArea, QFrame
)
from PySide6.QtGui     import QFont
from PySide6.QtCore    import Qt, QThread, Signal, QRect
from PySide6.QtWebEngineWidgets import QWebEngineView

from email.header      import decode_header, make_header 

import email

class MListCell(QWidget):

    def __init__(
            self, cell_text, cell_number, 
            cell_mail_id, imap_inst, tab_layout
        ) -> None:
        super().__init__()

        self.cell_text = cell_text
        self.cell_number = cell_number
        self.cell_mail_id = cell_mail_id
        self.imap_inst = imap_inst
        self.tab_layout = tab_layout

        self.row = QHBoxLayout()

        self.list_item_label = QLabel(self.cell_text)
        self.list_item_label.setFont(QFont("arial", 14))
        self.list_item_label.setStyleSheet(
            "*{padding: 10px 10px 10px 10px;} \
            *:hover {background: #3377ff;}"
        )

        self.list_item_layout = QHBoxLayout()
        self.from_label = QLabel()
        self.from_label.setFont(QFont("arial", 12))
        self.from_label.setFixedWidth(250)
        self.from_label.setStyleSheet(
            "*{color: #999999;} \
            *:hover {background: #3377ff;}"
        )

        self.row.addWidget(self.from_label)
        self.row.addWidget(self.list_item_label)

        self.list_item_layout.addLayout(self.row)
        self.list_item = QVBoxLayout()
        self.list_item.addLayout(self.list_item_layout)

        self.line = QFrame()
        self.line.setGeometry(QRect(1, 1, 1, 12))
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        
        self.list_item.addWidget(self.line)
        self.setLayout(self.list_item)
    
    def mousePressEvent(self, event):

        """ Creates a new tab for reading the mail and sets current
            tab to the new one.
        """
        if len(self.cell_text) > 30:
            self.cropped = self.cell_text[0:30]
        else:
            self.cropped = self.cell_text
        temp_tab = WebviewTab(
            self.cell_text, self.imap_inst, self.cell_mail_id
        )
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
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)


        self.layout1.addWidget(self.scroll)
        self.setLayout(self.layout1)

        for i in range(50):
            self.mail_list.append(
                MListCell( "", i, -1, self.imap_inst, self.tab_layout)
                )
            self.layout.addWidget(self.mail_list[i])

    def clear_mail_list(self):
        for i in range(50):
            self.mail_list[i].cell_text = ""
            self.mail_list[i].cell_mail_id = -1
            self.mail_list[i].list_item_label.setText("")
            
    def create_new_cell(self, subject_str, from_str, temp_num, index):

        from_list = from_str.split("<")
        self.mail_list[temp_num].list_item_label.setText(subject_str)
        self.mail_list[temp_num].from_label.setText(from_list[0])
        self.mail_list[temp_num].cell_text = subject_str
        self.mail_list[temp_num].cell_mail_id = index


class WebviewTab(QWidget):
    def __init__(self, subject, imap_inst, mail_id) -> None:
        super().__init__()
        self.subject = subject
        self.imap_inst = imap_inst
        self.mail_id = mail_id

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

        self.setLayout(self.layout)

        self.open_web = MLoadWebpage(
            self.subject, self.imap_inst, 
            self.mail_id
        )
        self.open_web.wemit_page.connect(self.set_webpage_content)
        self.open_web.start()

    def set_webpage_content(self, body_str):
        self.view.setHtml(body_str)

    def del_func(self):
        del self.layout

class MLoadWebpage(QThread):
    wemit_page = Signal(str)

    def __init__(self, subject, imap_inst, mail_id) -> None:
        super().__init__()

        self.subject = subject
        self.imap_inst = imap_inst
        self.mail_id = mail_id

    def run(self):
        try:
            self.imap_inst.select("inbox")
            _, idata = self.imap_inst.uid('fetch', self.mail_id, "(RFC822)")
            _, b = idata[0] 
            ac_email = email.message_from_bytes(b)
            body = ""
            if ac_email.is_multipart():
                for part in ac_email.walk():
                    ctype = part.get_content_type()
                    cdispo = str(part.get('Content-Disposition'))

                    if ctype == 'text/plain' and 'attachment' not in cdispo:
                        temp_type = "text"
                        body = part.get_payload(decode=True)  # decode
                    if ctype == 'text/html':
                        temp_type = "html"
                        body = part.get_payload(decode=True)  # decode
            else:
                body =ac_email.get_payload(decode=True)

            self.body_str = body.decode()
            self.wemit_page.emit(self.body_str)
        except Exception as e:
            print("ERROR::", e)


class MLoadWorker(QThread):

    ierror = Signal()
    istart = Signal()
    ifinish = Signal()
    iemit_cell = Signal(str, str, int, str)

    def __init__(self, imap_inst, mail_list, page) -> None:
        super().__init__()
        self.imap = imap_inst
        self.page = page
        self.mail_list = mail_list
        self.break_var = False

    def run(self):
        self.istart.emit()
        try:
            temp_mail_list = self.mail_list[
                (self.page*50): ((self.page+1)*50)
            ]
            my_string = ','.join(temp_mail_list)
            _, idata = self.imap.uid(
                'fetch', my_string, 
                '(BODY.PEEK[HEADER.FIELDS (SUBJECT FROM)])'
            )
            ldata = list(idata)
            ldata = [x for x in ldata if x != b')']
            index = 49
            for i in ldata:
                ac_email = email.message_from_bytes(i[1])
                subject_str = str(ac_email["subject"])
                subject_str = str(make_header(decode_header(subject_str)))
                from_str = str(ac_email["from"])
                from_str = str(make_header(decode_header(from_str)))
                self.iemit_cell.emit(
                    subject_str, from_str, 
                    index, str(temp_mail_list[index])
                )
                index -= 1
            self.ifinish.emit()
            self.exit(0)

        except Exception as e:
            print("AUTH::ERROR", e)
            self.ierror.emit()
            self.exit(0)
