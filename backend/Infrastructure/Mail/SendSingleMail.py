from config import send_email_task
from worker.Model import SendMailTaskBody


class SendSingleMail:
    """Class to send a single mail task to worker"""

    @staticmethod
    def send(
        subject: str,
        recipients: list[str],
        body: str,
        html: str | None = None
    ) -> None:
        """Function to send the mail"""

        send_email_task.apply_async(args=[
            SendMailTaskBody(
                subject=subject,
                recipients=recipients,
                body=body,
                html=html
            ).toDict()
        ])
