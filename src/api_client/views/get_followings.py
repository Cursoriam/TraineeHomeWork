from typing import Dict
import json

from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from django.core.exceptions import EmptyResultSet
from rest_framework.response import Response

from api_client.validation_serializers import FollowerGetResponse
from pitter.models import Client
from pitter import exceptions
from pitter.decorators import response_dict_serializer


class GetFollowersView(APIView):
    @classmethod
    @response_dict_serializer(FollowerGetResponse)
    @swagger_auto_schema(
        tags=['Pitter: client'],
        responses={
            200: FollowerGetResponse,
            204: exceptions.ExceptionResponse,
            400: exceptions.ExceptionResponse,
        },
        operation_summary='Получение списка подписчиков',
        operation_description='Получения списка подписчиков '
                              'пользователя'
    )
    def get(cls, request, id) -> Dict[str, dict]:
        try:
            client = Client.objects.get(id=id)
        except Client.DoesNotExist:
            raise exceptions.InvalidUserError()

        followers = client.followers
        if followers.first() is None:
            raise exceptions.NoFollowersError

        return dict(followings=client.followings.all().values('following_id'))
