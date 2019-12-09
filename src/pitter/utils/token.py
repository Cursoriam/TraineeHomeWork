import jwt

from django.conf import settings


def token_encode(payload):
    """
    Создание токена
    :param payload:
    :return:
    """
    token = jwt.encode(payload, open(settings.JWT_PRIVATE_KEY_PATH).read(),
                       'RS256',)
    return token.decode('utf-8')


def token_decode(token):
    """
    Дешифровка токена
    :param token:
    :return:
    """
    payload = jwt.decode(token, open(settings.JWT_PUBLIC_KEY_PATH).read(),
                         'RS256',)
    return payload
