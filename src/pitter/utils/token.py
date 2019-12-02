import jwt

from django.conf import settings


def token_encode(payload):
    token = jwt.encode(payload, open(settings.JWT_PRIVATE_KEY_PATH).read(),
                       'RS256',)
    return token


def token_decode(token):
    payload = jwt.decode(token, open(settings.JWT_PUBLIC_KEY_PATH).read(),
                         'RS256',)
    return payload
