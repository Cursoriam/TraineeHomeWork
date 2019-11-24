from typing import Dict


from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse

from api_client.validation_serializers import ClientPostRequest
from api_client.validation_serializers import ClientPostResponse
from pitter import exceptions
from pitter.decorators import request_post_serializer, response_dict_serializer
from pitter.models import Client


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
            password=make_password(password),
            email_address=email_address,
            enable_notifications=enable_notifications,
            )

        return result.to_dict()


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

        
        

