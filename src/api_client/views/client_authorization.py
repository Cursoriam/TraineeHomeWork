from rest_framework.views import APIView
from rest_framework.authentication import BaseAuthentication
from django.contrib.auth.hashers import make_password
from drf_yasg.utils import swagger_auto_schema

from pitter.decorators import request_post_serializer
from pitter.decorators import response_dict_serializer
from api_client.validation_serializers import ClientLoginRequest
from api_client.validation_serializers import ClientLoginResponse
from pitter import exceptions
from pitter.models import Client
from pitter.utils import check_token


class UserAutorization(APIView, BaseAuthentication):
    @classmethod
    @request_post_serializer(ClientLoginRequest)
    @response_dict_serializer(ClientLoginResponse)
    @swagger_auto_schema(
        tags=['User authorization'],
        request_body=ClientLoginRequest,
        responses={
            200: ClientLoginResponse,
            400: exceptions.ExceptionResponse,
            422: exceptions.ExceptionResponse,
        },
        operation_summary='Авторизация пользователя',
        operation_description='Авторизация пользователя в сервисе Pitter'
                              ' с использованием токена',
    )
    def post(cls, request):
        token = check_token(request)
        login = request.data['login']
        password = make_password(request.data['password'], 'zebra')
        try:
            client = Client.objects.get(login=login, password=password)
        except Client.DoesNotExist:
            raise exceptions.InvalidUserError()
        return dict(login=login, token=token)
