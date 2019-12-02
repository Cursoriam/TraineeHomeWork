from typing import Dict

from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema

from pitter.utils import check_token
from pitter.utils import speech_transcript
from pitter import exceptions
from pitter.models import Pitt
from pitter.models import Client
from pitter.decorators import request_post_serializer
from pitter.decorators import response_dict_serializer
from api_client.validation_serializers import TranscriptPostRequest
from api_client.validation_serializers import PittPostResponse


class CreatePittView(APIView):
    @classmethod
    @request_post_serializer(TranscriptPostRequest)
    @response_dict_serializer(PittPostResponse)
    @swagger_auto_schema(
        tags=['Pitter: client'],
        request_body=TranscriptPostRequest,
        operation_summary='Создание pitt\'а',
        operation_description='Создание pitt\'а пользователем',
    )
    def post(cls, request, login) -> Dict[str, str]:
        check_token(request)
        try:
            client = Client.objects.get(login=login)
        except Client.DoesNotExist:
            raise exceptions.InvalidUserError()
        id = client.id
        filepath = request.data['filepath']

        text = speech_transcript(filepath)
        pitt = Pitt.create_pitt(id, filepath, text)
        client.pitts.add(pitt)

        return dict(pitt_id=pitt.id)
