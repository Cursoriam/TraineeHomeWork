from typing import Dict

from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView

from pitter import exceptions
from pitter.models import Client
from pitter.utils import check_token
from pitter.decorators import response_dict_serializer
from api_client.validation_serializers import SearchPostResponse


class ClientListView(APIView):
    @classmethod
    @response_dict_serializer(SearchPostResponse)
    @swagger_auto_schema(
        tags=['Client: list'],
        responses={
            200: SearchPostResponse,
            400: exceptions.ExceptionResponse,
            500: exceptions.ExceptionResponse,
            422: exceptions.ExceptionResponse,
        },
        operation_summary='Получение списка пользователей',
        operation_description='Получение списка пользователей в сервисе '
                              'Pitter',
    )
    def get(cls, request) -> Dict[str, list]:
        """
        Запрос на получение списка пользователей
        :param request:
        :return:
        """
        check_token(request)
        client_list = []
        for client in Client.objects.all():
            client_data = {'id': client.id,
                           'login': client.login,
                           }
            client_list.append(client_data)

        if not client_list:
            raise exceptions.NoFollowersError(message='No such users')

        client_list = sorted(client_list, key=lambda i: i['login'])

        return dict(result=client_list)
