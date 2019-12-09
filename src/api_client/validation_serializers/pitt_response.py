from rest_framework import serializers


class PittPostResponse(serializers.Serializer):
    pitt_id = serializers.CharField(required=True, label='pitt id')
    filepath = serializers.CharField(required=True, label='pitt filepath')
    text = serializers.CharField(required=True, label='pitt text')
