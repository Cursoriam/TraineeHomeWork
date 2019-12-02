from django.core.mail import send_mail
from django.conf import settings


def email_notification(subject, message, recepient_list):
    send_mail(subject, message, settings.EMAIL_HOST, recepient_list)