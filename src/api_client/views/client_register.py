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
        tags=['Pitter: mobile'],
        request_body=ClientPostRequest,
        responses={
            200: ClientPostResponse,
            401: exceptions.ExceptionResponse,
            404: exceptions.ExceptionResponse,
            415: exceptions.ExceptionResponse,
            500: exceptions.ExceptionResponse,
        },
        operation_summary='Создание заявки',
        operation_description='Создание заявки в сервисе Pitter',
    )
    def post(cls, request) -> Dict[str, str]:
        """
        Создание заявки клиентом
        :param request:
        :return:
        """
        login: str = request.data['login']
        password: str = request.data['password']
        email_address: str = request.data['email_address']
        enable_notifications: bool = request.data['enable_notifications']
        result = Client.create_user(
            login=login,
            password=make_password(password, 'zebra'),
            email_address=email_address,
            enable_notifications=enable_notifications,
            )
        return result.to_dict()