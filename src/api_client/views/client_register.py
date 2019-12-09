from typing import Dict

from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password

from pitter import exceptions
from pitter.models import Client
from pitter.decorators import request_post_serializer
from pitter.decorators import response_dict_serializer
from api_client.validation_serializers import ClientPostRequest
from api_client.validation_serializers import ClientPostResponse


class ClientView(APIView):
    @classmethod
    @request_post_serializer(ClientPostRequest)
    @response_dict_serializer(ClientPostResponse)
    @swagger_auto_schema(
        tags=['Client: register'],
        request_body=ClientPostRequest,
        responses={
            200: ClientPostResponse,
            400: exceptions.ExceptionResponse,
            500: exceptions.ExceptionResponse,
            422: exceptions.ExceptionResponse,
        },
        operation_summary='Регистрация пользователя',
        operation_description='Регистрация пользователя в сервисе Pitter',
    )
    def post(cls, request) -> Dict[str, str]:
        """
        Запрос на регистрацию пользователя
        :param request:
        :return: Dict[str, str]
        """
        login: str = request.data['login']
        password: str = request.data['password']
        email_address: str = request.data['email_address']
        enable_notifications: bool = request.data['enable_notifications']

        if Client.objects.filter(login=login).exists():
            raise exceptions.InvalidUserError(message='User already exists',)
        result = Client.create_user(
            login=login,
            password=make_password(password, 'zebra'),
            email_address=email_address,
            enable_notifications=enable_notifications,
            )
        return result.to_dict()
