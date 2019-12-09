import json
import requests

from pitter import exceptions
from pitter import settings
from .validation import check_filepath


def speech_transcript(filepath):
    """
    Расшифровка речи из аудио сообщения
    :param filepath:
    :return:
    """
    check_filepath(filepath)
    filepath = {'filepath': filepath}
    try:
        text = requests.post(settings.SPEECH_TRANSCRIPT_URL,
                             data=filepath)
    except (ValueError, RuntimeError, TypeError, NameError,
            requests.exceptions.RequestException):
        raise exceptions.STTResponseError()

    if text.status_code == 500:
        raise exceptions.STTResponseError()
    text = json.loads(text.text)
    text = text['text']

    return text
