from typing import Dict

from pitter.models import Client
from pitter import exceptions

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
    data = []
    for following in client.followings.all():
        following_id = following.following_id
        following_user = Client.objects.get(id=following_id)
        following_pitts = following_user.pitts.first()
        if following_pitts:
            for pitt in following_user.pitts.all():
                pitt_data = {'user_id': pitt.user_id,
                             'filepath': pitt.audio_file_path,
                             'speech_transcription':
                                 pitt.speech_transcription}
                data.append(pitt_data)

    if not data:
        raise exceptions.NoFollowersError(message='No feed')

    return data
