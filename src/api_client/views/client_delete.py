from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema

from api_client.validation_serializers import ClientPostRequest
from api_client.validation_serializers import ClientPostResponse
from pitter import exceptions
from pitter.models import Client


class ClientViewToDelete(APIView):
    @swagger_auto_schema(
        tags=['Pitter: mobile'],
        request_body=ClientPostRequest,
        responses={
            200: ClientPostResponse,
            400: exceptions.ExceptionResponse,
        },
        operation_summary='Удаление пользователя',
        operation_description='Удаление пользователя в сервисе Pitter',
    )
    def delete(cls, request, login):
        try:
            client = Client.objects.get(login=login)
        except Client.DoesNotExist:
            raise exceptions.InvalidUserError()

        client.delete()

        try:
            client = Client.objects.get(login=login)
        except Client.DoesNotExist:
            raise exceptions.InvalidUserError(message='Client deleted')
