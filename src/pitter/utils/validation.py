import jwt

from rest_framework.authentication import get_authorization_header

from pitter import exceptions
from pitter.models import Client
from .token import token_decode


def check_filepath(filepath):
    """
    Проверка пути к файлу
    :param filepath:
    :return:
    """
    try:
        f = open(filepath)
        f.close()
    except FileNotFoundError:
        raise exceptions.FilePathError()

    return filepath


def check_token(request):
    """
    Проверка токена
    :param request:
    :return:
    """

    auth = get_authorization_header(request).split()
    if not auth:
        raise exceptions.TokenError()

    if len(auth) > 1:
        msg = 'Invalid token header'
        raise exceptions.TokenError()

    try:
        token = auth[0]
    except (UnicodeError, IndexError):
        msg = 'Invalid token header. Token ' \
              'string should not contain invalid characters.'
        raise exceptions.TokenError(msg)

    return auth_token(token)


def auth_token(token):
    """
    Аутентификация токена
    :param token:
    :return:
    """
    try:
        payload = token_decode(token)
    except jwt.ExpiredSignature or jwt.DecodeError or jwt.InvalidTokenError:
        raise exceptions.TokenError('Token is invalid', status_code=403)
    id = payload['id']
    login = payload['login']
    password = payload['password']
    try:
        client = Client.objects.get(
            id=id,
            login=login,
            password=password,
        )
    except Client.DoesNotExist:
        raise exceptions.TokenError('Token is invalid', status_code=500)

    return client
