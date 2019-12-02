from typing import Dict

from pitter import exceptions
from pitter.models import Client
from pitter.models import Pitt


def create_token_payload(id: str, login: str,
                         password: str, exp) -> Dict[str, str]:
    payload = {
        'id': id,
        'login': login,
        'password': password,
        'exp': exp,
    }

    return payload


def create_feed(client: Client):
    feed = {}
    for following in client.followings.all().values('following_id'):
        try:
            tmp = Client.objects.get(id=following).pitts
            pitts = tmp.all().values('speech_transcription')
        except None:
            raise exceptions.NoFollowersError('User does not have pitts')
        feed[following] = {following: pitts}

        return feed



