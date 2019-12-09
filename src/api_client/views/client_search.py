from typing import Dict

from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView

from pitter import exceptions
from pitter.models import Client
from pitter.utils import check_token
from pitter.decorators import request_post_serializer
from pitter.decorators import response_dict_serializer
from api_client.validation_serializers import SearchPostRequest
from api_client.validation_serializers import SearchPostResponse


class SearchView(APIView):
    @classmethod
    @request_post_serializer(SearchPostRequest)
    @response_dict_serializer(SearchPostResponse)
    @swagger_auto_schema(
        tags=['Client: search'],
        request_body=SearchPostRequest,
        responses={
            200: SearchPostRequest,
            400: exceptions.ExceptionResponse,
            500: exceptions.ExceptionResponse,
            422: exceptions.ExceptionResponse,
        },
        operation_summary='Поиск пользователя',
        operation_description='Поиск пользователя в сервисе Pitter',
    )
    def post(cls, request) -> Dict[str, list]:
        check_token(request)
        search_string = request.data['search_string']
        result = []
        for client in Client.objects.all():
            if search_string in client.login:
                client_data = {'id': client.id,
                               'login': client.login,
                               }
                result.append(client_data)
        if not result:
            raise exceptions.NoFollowersError(message='No such users')

        result = sorted(result, key=lambda i: i['login'])

        return dict(result=result)
