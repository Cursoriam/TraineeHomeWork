import requests
import json

from .validation import check_filepath
from pitter import settings
from pitter import exceptions


def speech_transcript(filepath):
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
