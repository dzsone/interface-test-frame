"""
Mail class. Used to send mail to specified users. Multiple recipients can be specified with attachments.
"""
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from socket import gaierror, error
from comm.Log import logger


class Email:
    def __init__(self, server, sender, password, receiver, title, message=None, path=None):
        """initialization Email

        :param title: Email title, required.
        :param message: The body of the message, not required.
        :param path: Attachment path, which can be passed in list (multiple attachments) or str (single attachment), but not required.
        :param server: smtp server, required.
        :param sender: Sender, required.
        :param password: Sender password, required.
        :param receiver: Recipient, multiple recipients separated by ";", required.
        """
        self.title = title
        self.message = message
        self.files = path

        self.msg = MIMEMultipart('related')

        self.server = server
        self.sender = sender
        self.receiver = receiver
        self.password = password

    def _attach_file(self, att_file):
        """Add a single file to the list of attachments"""
        att = MIMEText(open('%s' % att_file, 'rb').read(), 'plain', 'utf-8')
        att["Content-Type"] = 'application/octet-stream'
        file_name = re.split(r'[\\|/]', att_file)
        att["Content-Disposition"] = 'attachment; filename="%s"' % file_name[-1]
        self.msg.attach(att)
        logger.info('attach file {}'.format(att_file))

    def send(self):
        self.msg['Subject'] = self.title
        self.msg['From'] = self.sender
        self.msg['To'] = self.receiver

        # Mail's body message
        if self.message:
            self.msg.attach(MIMEText(self.message))

        # Add attachments, support multiple attachments (incoming list), or single attachment (incoming str)
        if self.files:
            if isinstance(self.files, list):
                for f in self.files:
                    self._attach_file(f)
            elif isinstance(self.files, str):
                self._attach_file(self.files)

        # Connect to server and send
        try:
            smtp_server = smtplib.SMTP(self.server)  # connect sever
        except (gaierror and error) as e:
            logger.exception('Failed to send mail, unable to connect to SMTP server, check network and SMTP server. %s', e)
        else:
            try:
                smtp_server.login(self.sender, self.password)  # login
            except smtplib.SMTPAuthenticationError as e:
                logger.exception('Username password verification failed！%s', e)
            else:
                smtp_server.sendmail(self.sender, self.receiver.split(';'), self.msg.as_string())  # send mail
            finally:
                smtp_server.quit()  # 断开连接
                logger.info('Sending message "{0}" succeeded! To: {1}. If you do not receive the email, please check the bin,'
                            'At the same time check whether the recipient address is correct'.format(self.title, self.receiver))