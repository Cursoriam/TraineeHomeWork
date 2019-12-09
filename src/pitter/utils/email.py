from django.core.mail import send_mail
from django.conf import settings


def email_notification(subject, message, recepient_list):
    """
    Уведомление пользователя сообщением
    :param subject:
    :param message:
    :param recepient_list:
    :return:
    """
    send_mail(subject, message, settings.EMAIL_HOST, recepient_list)
