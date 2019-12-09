from rest_framework import serializers


class FollowerPostRequest(serializers.Serializer):
    follower_login = serializers.CharField(required=True, max_length=50,
                                       label='Логин пользователя')
    following_login = serializers.CharField(required=True, max_length=50,
                                           label='Логин подписчика')


class FollowerPostResponse(serializers.Serializer):
    follower_id = serializers.CharField(required=True, label='Логин подписчика')
    following_id = serializers.CharField(required=True, label='Логин подписки')

class FollowerGetResponse(serializers.Serializer):
    followings = serializers.DictField(required=True, label='Список подписок')