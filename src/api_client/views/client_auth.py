from datetime import datetime
from datetime import timedelta
from typing import Dict

from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password

from api_client.validation_serializers import ClientLoginRequest
from api_client.validation_serializers import ClientLoginResponse
from pitter import exceptions
from pitter.decorators import request_post_serializer
from pitter.decorators import response_dict_serializer
from pitter.models import Client
from pitter.utils import create_token_payload
from pitter.utils import token_encode


class UserAuthenticate(APIView):
    @classmethod
    @request_post_serializer(ClientLoginRequest)
    @response_dict_serializer(ClientLoginResponse)
    @swagger_auto_schema(
        tags=['Client: authentication'],
        request_body=ClientLoginRequest,
        responses={
            200: ClientLoginResponse,
            400: exceptions.ExceptionResponse,
            422: exceptions.ExceptionResponse,
        },
        operation_summary='Аутентификация пользователя',
        operation_description='Аутентификация пользователя в сервисе Pitter',
    )
    def post(cls, request) -> Dict[str, str]:
        """
        Запрос на аутентификацию пользователя
        :param request:
        :return: Dict[str, str]
        """
        login = request.data['login']
        password = make_password(request.data['password'], 'zebra')
        try:
            client = Client.objects.get(login=login, password=password)
        except Client.DoesNotExist:
            raise exceptions.InvalidUserError()

        exp = datetime.utcnow() + timedelta(seconds=3600)

        payload = create_token_payload(client.id, client.login,
                                       client.password, exp)

        token = token_encode(payload)
        return dict(login=login, token=token,)
