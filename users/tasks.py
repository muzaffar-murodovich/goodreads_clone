from django.core.mail import send_mail
from django.conf import settings
from goodreads.celery import app

@app.task
def send_email(subject, message, recepient_list):
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            recepient_list,
            fail_silently=False,
        )
    except Exception as e:
        # Log the error for debugging
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f'Failed to send email: {str(e)}')
        raise  # Re-raise to let Celery handle retries

