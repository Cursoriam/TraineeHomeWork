import base64
import io
import os

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
from rest_framework.views import APIView
from rest_framework.response import Response

from src.api_client.validation_serializers import TicketPostRequest
from src.api_client.validation_serializers import TicketPostResponse
from src.pitter import exceptions
from src.pitter.decorators import request_post_serializer, response_dict_serializer

class ClientView(APIView):
    def encode_audio_(audio):
        audio_content=audio.read()
        return base64.b64encode(audio_content)

    def post(self, request):
        # Instantiates a client
        client = speech.SpeechClient()

        # The name of the audio file to transcribe
        file_name = os.path.join(
            os.path.dirname(__file__),
            'resources',
            'audio.wav')

        # Loads the audio into memory
        with io.open(file_name, 'rb') as audio_file:
            content = audio_file.read()
            audio = types.RecognitionAudio(content=content)

        config = types.RecognitionConfig(
            encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=8000,
            language_code='en-US')

        # Detects speech in the audio file
        response = client.recognize(config, audio)
        transcripted=" "
        for result in response.results:
            transcripted=transcripted+result.alternatives[0].transcript

        return Response({"{}".format(transcripted)})

