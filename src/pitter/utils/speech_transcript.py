import requests

from .validation import check_filepath
from pitter import settings
from pitter import exceptions


def speech_transcript(filepath):
    check_filepath(filepath)
    try:
        text = requests.post(settings.SPEECH_TRANSCRIPT_URL,
                             data=filepath)
    except (ValueError, RuntimeError, TypeError, NameError,
            requests.exceptions.RequestException):
        raise exceptions.STTResponseError()

    return text
