from rest_framework import serializers


class PittPostResponse(serializers.Serializer):
    pitt_id = serializers.CharField(required=True, label='pitt id')
