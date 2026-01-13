from django import forms
from django.core.mail import send_mail
from django.conf import settings
from users.models import CustomUser
from django.core.mail.message import EmailMessage

class UserCreateForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit)
        user.set_password(self.cleaned_data['password'])
        user.save()

        if user.email:
            try:
                # Ensure we have a valid from_email
                from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', None)
                if not from_email or from_email == 'noreply@yourdomain.com' or '@' not in from_email:
                    # Skip sending if email is not properly configured
                    import logging
                    logger = logging.getLogger(__name__)
                    logger.warning(f'Email not configured properly (DEFAULT_FROM_EMAIL={from_email}). Skipping welcome email to {user.email}')
                else:
                    email_message = EmailMessage(
                        subject='Welcome to Goodreads!',
                        body=f'Hello {user.first_name or user.username},\n\nWelcome to Goodreads! Your account has been successfully created.\n\nBest regards,\nThe Goodreads Team',
                        from_email=from_email,
                        to=[user.email],
                    )
                    # Send email - use fail_silently=False to see actual errors, but catch exceptions
                    email_message.send(fail_silently=False)
                    import logging
                    logger = logging.getLogger(__name__)
                    logger.info(f'Welcome email sent successfully to {user.email}')
            except Exception as e:
                # Log error but don't fail user registration
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f'Failed to send welcome email to {user.email}: {str(e)}', exc_info=True)
                # Don't raise the exception - allow user registration to succeed

        return user

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'profile_picture')

