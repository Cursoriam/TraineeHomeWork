from rest_framework import serializers


class ClientLoginRequest(serializers.Serializer):
    login = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

class ClientLoginResponse(serializers.Serializer):
    login = serializers.CharField(required=True)
    token = serializers.CharField(required=True)