from datetime import datetime
from datetime import timedelta
from typing import Dict

from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView

from api_client.validation_serializers import ClientLoginRequest
from api_client.validation_serializers import ClientLoginResponse
from pitter import exceptions
from pitter.decorators import response_dict_serializer
from pitter.utils import create_token_payload
from pitter.utils import token_encode
from pitter.utils import check_token
from pitter.models import Client


class UserLogoutView(APIView):
    @classmethod
    @response_dict_serializer(ClientLoginResponse)
    @swagger_auto_schema(
        tags=['Client: logout'],
        responses={
            200: ClientLoginResponse,
            400: exceptions.ExceptionResponse,
            422: exceptions.ExceptionResponse,
        },
        operation_summary='Logout пользователя',
        operation_description='Logout пользователя в сервисе Pitter',
    )
    def post(cls, request) -> Dict[str, str]:
        """
        Запрос на logout пользователя
        :param request:
        :return:
        """
        client = check_token(request)

        exp = datetime.utcnow() + timedelta(seconds=0)

        payload = create_token_payload(client.id, client.login,
                                       client.password, exp)

        token = token_encode(payload)

        return dict(login=client.login, token=token)
