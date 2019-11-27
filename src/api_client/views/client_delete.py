from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from django.http import HttpResponse

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