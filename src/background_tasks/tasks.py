import smtplib

from celery import Celery
from email.message import EmailMessage

from src.config import REDIS_PORT, REDIS_HOST, SMTP_USER, SMTP_PASSWORD

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465

celery = Celery('tasks', broker=f'redis://{REDIS_HOST}:{REDIS_PORT}')


def get_email_template_greeting(username: str, email_to: str):
    email = EmailMessage()
    email['Subject'] = 'Your Notebook '
    email['From'] = SMTP_USER
    email['To'] = email_to

    email.set_content(
        '<div>'
        f'<h1 style="color: red;">Здравствуйте, {username}, рады приветствовать в нашем приложении. АУЕ 😊</h1>'
        '<img src="https://upload.wikimedia.org/wikipedia/ru/thumb/9/94/%D0%93%D0%B8%D0%B3%D0%B0%D1%87%D0%B0%D0%B4.jpg/500px-%D0%93%D0%B8%D0%B3%D0%B0%D1%87%D0%B0%D0%B4.jpg" width="600">'
        '</div>',
        subtype='html'
    )
    return email


def get_email_template_task_notification(username: str, email_to: str, task_name: str):
    email = EmailMessage()
    email['Subject'] = 'Your Notebook '
    email['From'] = SMTP_USER
    email['To'] = email_to

    email.set_content(
        '<div>'
        f'<h1 style="color: red;">Здравствуйте, {username}, хотим напомнить что срок вашей задачи {task_name} истекает через 1 час</h1>'
        '</div>',
        subtype='html'
    )
    return email


@celery.task
def send_email_greetings(username: str, email_to: str):
    email = get_email_template_greeting(username, email_to)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(email)


@celery.task
def send_task_notification(username: str, email_to: str, task_name: str):
    email = get_email_template_task_notification(username, email_to, task_name)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(email)
