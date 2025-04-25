import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP

from worker.config import MailConfig, logger
from worker.Model import SendMailTaskBody


class SendMailHandler:

    @staticmethod
    def handle(data: SendMailTaskBody) -> None:
        """Send mail"""

        subject = data.subject
        recipients = data.recipients
        body = data.body
        html = data.html

        try:
            logger.info(f'Worker | SendMailHandler | Sending mail to {
                        recipients} with subject {subject}')

            msg = MIMEMultipart()
            msg['From'] = MailConfig.MAIL_DEFAULT_SENDER
            msg['To'] = recipients[0]
            msg['Subject'] = subject

            msg.attach(MIMEText(body, 'plain'))

            if html:
                msg.attach(MIMEText(html, 'html'))

            with SMTP(MailConfig.MAIL_SERVER, MailConfig.MAIL_PORT) as server:
                if MailConfig.MAIL_USE_TLS:
                    server.starttls()

                if os.getenv('FLASK_ENV') == 'production':

                    if MailConfig.MAIL_USERNAME and MailConfig.MAIL_PASSWORD:
                        server.login(
                            MailConfig.MAIL_USERNAME,
                            MailConfig.MAIL_PASSWORD)

                server.sendmail(
                    MailConfig.MAIL_DEFAULT_SENDER,
                    recipients[0],
                    msg.as_string())

            logger.info(f'Worker | SendMailHandler | Mail sent to {
                        recipients} with subject {subject}')

        except Exception as e:
            logger.error(f'Worker | SendMailHandler | {e}')
            raise e
