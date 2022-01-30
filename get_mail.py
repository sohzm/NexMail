from email.header      import decode_header, make_header 
from PySide6.QtCore    import QThread, Signal

import email

class MLoadWorker(QThread):

    ierror = Signal()
    istart = Signal()
    ifinish = Signal()
    iexport_email = Signal(str, str, str, int)

    def __init__(self, imap, page, num = 50) -> None:
        super().__init__()
        self.imap = imap
        self.num = num
        self.page = page
        self.break_var = False

    def run(self):
        self.istart.emit()
        try:
            _, self.temp_msg = self.imap.select("INBOX")
            self.total_messages = int(self.temp_msg[0])
            self.total_messages -= self.page*50

            temp_num = 0
            for index in range(self.total_messages, self.total_messages - self.num, -1):
                if (self.break_var): break
                _, idata = self.imap.fetch(str(index), "(RFC822)")
                _, b = idata[0]
                ac_email = email.message_from_bytes(b)
                body = ""
                if ac_email.is_multipart():
                    for part in ac_email.walk():
                        ctype = part.get_content_type()
                        cdispo = str(part.get('Content-Disposition'))

                        # skip any text/plain (txt) attachments
                        if ctype == 'text/plain' and 'attachment' not in cdispo:
                            body = part.get_payload(decode=True)  # decode
                        if ctype == 'text/html':
                            body = part.get_payload(decode=True)  # decode
                # not multipart - i.e. plain text, no attachments, keeping fingers crossed
                else:
                    body =ac_email.get_payload(decode=True)
                subject_str = str(ac_email["subject"])
                subject_str = str(make_header(decode_header(subject_str)))

                sender_str = str(ac_email["From"])
                sender_str = str(make_header(decode_header(subject_str)))

                body_str = str(body)
                body_str = body_str.replace("\\n", "")
                body_str = body_str.replace("\\r", "")
                #body_str = str(make_header(decode_header(body_str)))
                self.iexport_email.emit(subject_str, body_str, sender_str, temp_num)
                temp_num += 1
                print("COUT::", index)
            self.ifinish.emit()
            self.exit(0)

        except Exception as e:
            print("AUTH::ERROR", e)
            self.ierror.emit()
            self.exit(0)
