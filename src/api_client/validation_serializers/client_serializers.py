from rest_framework import serializers


class ClientPostRequest(serializers.Serializer):
    login = serializers.CharField()
    password = serializers.CharField()
    email_address=serializers.EmailField()
    enable_notifications=serializers.BooleanField()


class ClientPostResponse(serializers.Serializer):
    id = serializers.CharField(required=True, label='Идентификатор пользователя')

