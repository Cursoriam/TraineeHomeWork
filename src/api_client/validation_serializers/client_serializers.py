from rest_framework import serializers


class ClientPostRequest(serializers.Serializer):
    file=serializers.FileField(required=True, use_url=False)

class ClientPostResponse(serializers.Serializer):
    result=serializers.CharField(required=True)
