from datetime import datetime
import jwt


from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from django.contrib.auth.hashers import make_password

from api_client.validation_serializers import ClientLoginRequest
from pitter import exceptions
from pitter.decorators import request_post_serializer, response_dict_serializer
from pitter.models import Client
from pitter.settings import JWT_PRIVATE_KEY_PATH


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







        
        

