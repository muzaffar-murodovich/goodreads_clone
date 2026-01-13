from django.core.mail import send_mail
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import CustomUser
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=CustomUser)
def send_welcome_email(sender, instance, created, **kwargs):
    """Send welcome email when a new user is created"""
    if created and instance.email:
        try:
            from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', None)
            if not from_email or '@' not in from_email:
                logger.warning(f'Cannot send welcome email: DEFAULT_FROM_EMAIL not configured properly')
                return
            
            send_mail(
                "Welcome to Goodreads Clone",
                f"Hi, {instance.first_name or instance.username}! Welcome to Goodreads Clone. Enjoy the books",
                from_email,
                [instance.email],
                fail_silently=False,
            )
            logger.info(f'Welcome email sent successfully to {instance.email}')
        except Exception as e:
            # Log error but don't break user creation
            logger.error(f'Failed to send welcome email to {instance.email}: {str(e)}', exc_info=True)