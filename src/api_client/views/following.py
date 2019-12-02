from typing import Dict

from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema


from pitter.models import Following
from pitter.models import Client
from pitter.utils import email_notification
from pitter.utils import check_token
from pitter import exceptions
from pitter.decorators import response_dict_serializer
from api_client.validation_serializers import FollowerPostResponse


class FollowerView(APIView):
    @classmethod
    @response_dict_serializer(FollowerPostResponse)
    @swagger_auto_schema(
        tags=['Pitter: client'],
        responses={
            200: FollowerPostResponse,
            401: exceptions.ExceptionResponse,
            409: exceptions.ExceptionResponse,
        },
        operation_summary='Взаимодействие с подпиской',
        operation_description='Добавление подписки',
    )
    def post(cls, request, follower_id, following_id) -> Dict[str, str]:
        check_token(request)
        try:
            client = Client.objects.get(id=follower_id)
        except Client.DoesNotExist:
            raise exceptions.InvalidUserError()

        try:
            following = Client.objects.get(id=following_id)
        except Client.DoesNotExist:
            raise exceptions.InvalidUserError(message='Following does not'
                                                      ' exists')

        if Following.objects.filter(follower_id=follower_id,
                                    following_id=following_id).exists():
            raise exceptions.ValidationError(message='Following already '
                                                     'exists',
                                             status_code=409)

        following = Following.create_following(following_id, follower_id)
        client.followings.add(following)

        if client.enable_notifications:
            subject='New following!'
            message='You make new following'
            recepient_list=['recevier@gmail.com']
            email_notification(subject, message, recepient_list)

        return dict(follower_id=follower_id, following_id=following_id)

    @classmethod
    @swagger_auto_schema(
        tags=['Pitter: client'],
        responses={
            401: exceptions.ExceptionResponse,
            204: exceptions.ExceptionResponse,
        },
        operation_summary='Взаимодействие с подпиской',
        operation_description='Удаление подписки',
    )
    def delete(cls, request, follower_id, following_id):
        check_token(request)
        try:
            following = Following.objects.get(following_id=following_id,
                                              follower_id=follower_id,)
        except Following.DoesNotExist:
            raise exceptions.InvalidUserError(message='Following does not exists')

        following.delete()

        try:
            following = Following.objects.get(following_id=following_id)
        except Following.DoesNotExist:
            raise exceptions.InvalidUserError(message='Following deleted', status_code=204)
