from rest_framework.authentication import get_authorization_header
from rest_framework.views import APIView
from rest_framework.authentication import BaseAuthentication
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from drf_yasg.utils import swagger_auto_schema

from pitter.decorators import request_post_serializer
from api_client.validation_serializers import ClientLoginRequest
from pitter import exceptions
from pitter.models import Client


class UserAutorization(APIView, BaseAuthentication):
    @classmethod
    @request_post_serializer(ClientLoginRequest)
    @swagger_auto_schema(
        tags=['User authorization'],
        request_body=ClientLoginRequest,
        responses={
            200: ClientLoginRequest,
            401: exceptions.ExceptionResponse,
            404: exceptions.ExceptionResponse,
            415: exceptions.ExceptionResponse,
            500: exceptions.ExceptionResponse,
        },
        operation_summary='Авторизация пользователя',
        operation_description='Авторизация пользователя в сервисе Pitter'
                              ' с использованием токена',
    )
    def post(cls, request):
        auth = get_authorization_header(request).split()
        try:
            token = auth[0]
        except Exception:
            raise Exception('Bad credentials')
        login = request.data['login']
        password = make_password(request.data['password'], 'zebra')
        try:
            client = Client.objects.get(login=login, password=password)
        except Exception:
            raise Exception('Client does not exist')
        return Response({'login': login, 'token': token}, status=status.HTTP_200_OK)