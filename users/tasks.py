from django.core.mail import send_mail
from goodreads.celery import app

@app.task
def send_email(subject, message, recepient_list):
    send_mail(
        subject,
        message,
        "muzaffarmurodogli@gmail.com",
        recepient_list
    )

