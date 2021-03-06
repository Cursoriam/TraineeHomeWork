from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema

from api_client.validation_serializers import ClientPostRequest
from api_client.validation_serializers import ClientPostResponse
from pitter import exceptions
from pitter.models import Client
from pitter.utils import check_token


class ClientViewToDelete(APIView):
    @classmethod
    @swagger_auto_schema(
        tags=['Client: delete'],
        request_body=ClientPostRequest,
        responses={
            200: ClientPostResponse,
            400: exceptions.ExceptionResponse,
        },
        operation_summary='Удаление пользователя',
        operation_description='Удаление пользователя в сервисе Pitter',
    )
    def delete(cls, request, login):
        """
        Запрос на удаление пользователя
        :param request:
        :param login:
        :return:
        """
        check_token(request)
        try:
            client = Client.objects.get(login=login)
        except Client.DoesNotExist:
            raise exceptions.InvalidUserError()

        client.delete()

        try:
            client = Client.objects.get(login=login)
        except Client.DoesNotExist:
            raise exceptions.InvalidUserError(message='Client deleted')
