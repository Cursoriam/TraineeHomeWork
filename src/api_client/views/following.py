from typing import Dict

from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema


from pitter.models import Following
from pitter.models import Client
from pitter.utils import check_token
from pitter import exceptions
from pitter.decorators import response_dict_serializer
from api_client.validation_serializers import FollowerPostResponse


class FollowerView(APIView):
    @classmethod
    @response_dict_serializer(FollowerPostResponse)
    @swagger_auto_schema(
        tags=['Client: follow'],
        responses={
            200: FollowerPostResponse,
            401: exceptions.ExceptionResponse,
            409: exceptions.ExceptionResponse,
        },
        operation_summary='Взаимодействие с подпиской',
        operation_description='Добавление подписки',
    )
    def post(cls, request, following_id) -> Dict[str, str]:
        """
        Запрос на добавление подписки
        :param request:
        :param following_id:
        :return:
        """
        client = check_token(request)

        try:
            following = Client.objects.get(id=following_id)
        except Client.DoesNotExist:
            raise exceptions.InvalidUserError(message='Following does not'
                                                      ' exists')

        if Following.objects.filter(follower_id=client.id,
                                    following_id=following_id).exists():
            raise exceptions.ValidationError(message='Following already '
                                                     'exists',
                                             status_code=409)

        following = Following.create_following(following_id, client.id)
        client.followings.add(following)

        return dict(follower_id=client.id, following_id=following_id)

    @classmethod
    @swagger_auto_schema(
        tags=['Client: follow'],
        responses={
            401: exceptions.ExceptionResponse,
            204: exceptions.ExceptionResponse,
        },
        operation_summary='Взаимодействие с подпиской',
        operation_description='Удаление подписки',
    )
    def delete(cls, request, following_id):
        """
        Запрос на удаление подписки
        :param request:
        :param following_id:
        :return:
        """
        client = check_token(request)
        try:
            following = Following.objects.get(following_id=following_id,
                                              follower_id=client.id,)
        except Following.DoesNotExist:
            raise exceptions.InvalidUserError(message='Following does not exists')

        following.delete()
        client.followings.filter(following_id=following_id,
                                 follower_id=client.id).delete()

        try:
            following = Following.objects.get(following_id=following_id,
                                              follower_id=client.id)
        except Following.DoesNotExist:
            raise exceptions.InvalidUserError(message='Following deleted', status_code=204)
