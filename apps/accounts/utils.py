# views.py or any other module
from django.core.mail import send_mail
from django.conf import settings

def send_test_email():
    subject = 'Test Email from Django with Mailjet SMTP'
    message = 'This is a test email sent using Mailjet SMTP with Django.'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = ['rabxtt@gmail.com']  # Replace with the recipient's email

    send_mail(
        subject,
        message,
        from_email,
        recipient_list,
        fail_silently=False,
    )
