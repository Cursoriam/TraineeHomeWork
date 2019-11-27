import requests

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema


from pitter.decorators import request_post_serializer
from api_client.validation_serializers import TranscriptPostRequest


class SpeechTranscriptView(APIView):
    @classmethod
    @request_post_serializer(TranscriptPostRequest)
    @swagger_auto_schema(
        tags=['Speech to text'],
        request_body=TranscriptPostRequest,
        operation_summary='Транскрибирование речи в текст',
        operation_description='Транскрипция речи в текст '
                              'с помощью Google Speech-to-text',
    )
    def post(cls, request):
        text = requests.post('http://localhost:8118/voice', data={'filepath': request.data['filepath']})
        return Response(text, status=status.HTTP_200_OK)