from rest_framework import serializers


class TranscriptPostRequest(serializers.Serializer):
    filepath = serializers.CharField(required=True,
                                     label='Путь к файлу с образцом речи',)
