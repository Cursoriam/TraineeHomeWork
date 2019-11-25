from typing import Dict
from calendar import timegm
from datetime import datetime
import jwt


from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_jwt.utils import jwt_payload_handler
from rest_framework_jwt.utils import jwt_encode_handler
from rest_framework_jwt.settings import api_settings
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import get_authorization_header
from rest_framework.authentication import BaseAuthentication
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse

from api_client.validation_serializers import ClientPostRequest
from api_client.validation_serializers import ClientPostResponse
from api_client.validation_serializers import ClientLoginRequest
from pitter import exceptions
from pitter.decorators import request_post_serializer, response_dict_serializer
from pitter.models import Client
from pitter.settings import JWT_PRIVATE_KEY_PATH


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


class UserAuthenticate(APIView):
    @classmethod
    @request_post_serializer(ClientLoginRequest)
    @swagger_auto_schema(
        tags=['User authentication'],
        request_body=ClientLoginRequest,
        responses={
            200: ClientLoginRequest,
            401: exceptions.ExceptionResponse,
            404: exceptions.ExceptionResponse,
            415: exceptions.ExceptionResponse,
            500: exceptions.ExceptionResponse,
        },
        operation_summary='Аутентификация пользователя',
        operation_description='Аутентификация пользователя в сервисе Pitter',
    )
    def post(cls, request):
        login = request.data['login']
        password = make_password(request.data['password'], 'zebra')
        try:
            client = Client.objects.get(login=login, password=password)
        except Exception:
            raise Exception('Client does not exist')

        payload = {
            'id': client.id,
            'login': client.login,
            'password': client.password,
            'email_address': client.email_address,
            'enable_notifications': client.enable_notifications,
            'exp': datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA,
        }
        token=jwt.encode(payload, open(JWT_PRIVATE_KEY_PATH).read(), 'RS256')
        return Response({'login': login, 'token': token}, status=status.HTTP_200_OK)


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
        return Response({'login':login, 'token': token}, status=status.HTTP_200_OK)


class ClientViewToDelete(APIView):
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
        operation_summary='Удаление пользователя',
        operation_description='Удаление пользователя в сервисе Pitter',
    )
    def delete(cls, request, id):
        try:
            client = Client.objects.get(id=id)
        except exceptions.ExceptionResponse:
            return HttpResponse(204)

        client.delete()

        return HttpResponse(204)

        
        

