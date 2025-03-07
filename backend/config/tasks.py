import os

from celery import Celery

from Infrastructure.Logger import logger
from worker.Model import SendMailTaskBody

celery = Celery(
    host=os.getenv('CELERY_BROKER_NAME'),
    broker=os.getenv('CELERY_BACKEND_URL'),
    backend=os.getenv('CELERY_RESULT_BACKEND'))


@celery.task(name="send_email_task")
def send_email_task(data: SendMailTaskBody):

    logger.info(
        f"Worker | send_email_task | Created | Sending email to {
            data['recipients']}: {
            data['subject']}")

    return data
