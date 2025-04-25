from dataclasses import asdict, dataclass


@dataclass
class SendMailTaskBody:

    subject: str
    recipients: list[str]
    body: str
    html: str | None

    def toDict(self):
        return asdict(self)

    @staticmethod
    def fromDict(data: dict):
        return SendMailTaskBody(
            subject=data['subject'],
            recipients=data['recipients'],
            body=data['body'],
            html=data.get('html')
        )
