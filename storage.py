import appdirs
import os
import hashlib


class CheckDirs():

    def __init__(self, email_id) -> None:
        conf_dir = appdirs.user_config_dir(appname='NexMail')
        self.check_or_create(conf_dir)
        self.check_or_create(conf_dir + "/accounts")
        self.check_or_create(conf_dir + "/config")

        account_dir = email_id.encode()
        hashed_dir = hashlib.sha256(account_dir).hexdigest()

        self.check_or_create(conf_dir + "/accounts/" + hashed_dir)
        self.check_or_create(conf_dir + "/accounts/" + hashed_dir + "/mails")

    def check_or_create(self, given_dir):
        if (not os.path.isdir(given_dir)):
            os.mkdir(given_dir)

