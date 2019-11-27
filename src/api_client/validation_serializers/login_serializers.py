from rest_framework import serializers


class ClientLoginRequest(serializers.Serializer):
    login=serializers.CharField()
    password=serializers.CharField()